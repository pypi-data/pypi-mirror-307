import logging
from enum import Enum
from typing import Any, Optional, Type, cast

import requests
from pydantic.error_wrappers import ValidationError
from pydantic.main import BaseModel
from pydantic.tools import parse_raw_as
from requests.auth import HTTPBasicAuth

from .config import ORDMediascoutConfig
from .feed_models import (
    CreateContainerWebApiDto,
    CreateFeedElementsBulkWebApiDto,
    CreateFeedElementsWebApiDto,
    EditFeedElementWebApiDto,
    GetContainerWebApiDto,
    GetFeedElementsBulkInfo,
    GetFeedElementsWebApiDto,
    ResponseContainerWebApiDto,
    ResponseCreateFeedElementsBulkWebApiDto,
    ResponseEditFeedElementWebApiDto,
    ResponseFeedElementsWebApiDto,
    ResponseGetContainerWebApiDto,
    ResponseGetFeedElementsBulkInfo,
    ResponseGetFeedElementsWebApiDto,
)
from .models import (
    BadRequestResponse,
    ClearInvoiceDataWebApiDto,
    ClientResponse,
    CreateClientRequest,
    CreateCreativeRequest,
    CreatedCreativeResponse,
    CreateFinalContractRequest,
    CreateInitialContractRequest,
    CreateInvoicelessStatisticsRequest,
    CreateInvoiceRequest,
    CreateOuterContractRequest,
    CreatePlatformRequest,
    CreativeGroupResponse,
    CreativeResponse,
    CreativeStatus,
    DeleteContractWebApiDto,
    DeleteRestoreCreativeWebApiDto,
    EditCreativeRequest,
    EditFinalContractWebApiDto,
    EditInitialContractWebApiDto,
    EditInvoiceDataWebApiDto,
    EditInvoiceStatisticsWebApiDto,
    EditOuterContractWebApiDto,
    EditPlatformWebApiDto,
    EntityIdResponse,
    FinalContractResponse,
    GetClientRequest,
    GetCreativeGroupsRequest,
    GetCreativesParameters,
    GetCreativesWebApiDto,
    GetFinalContractsRequest,
    GetInitialContractRequest,
    GetInvoicelessPeriodsRequest,
    GetInvoicesWebApiDto,
    GetOuterContractsRequest,
    InitialContractResponse,
    InvoicelessStatisticsResponse,
    InvoiceResponse,
    InvoiceSummaryResponse,
    OuterContractResponse,
    PartialClearInvoiceInitialContractsRequest,
    PartialClearInvoiceWebApiDto,
    PlatformResponse,
    ProblemDetails,
    SupplementInvoiceWebApiDto,
    ValidationFailure,
)


class APIError(Exception):
    pass


class TemporaryAPIError(APIError):
    pass


class ResponseError(APIError):
    def __init__(self, response: requests.Response):
        super().__init__(
            f'Response error {response.status_code} for API {response.request.method} {response.request.url}'
        )
        self.response = response


class BadResponseError(APIError):
    def __init__(self, response: requests.Response, error: Optional[BadRequestResponse] = None):
        super().__init__(error and error.errorType or f'Bad response from API: {response.status_code}')
        self.response = response
        self.error = error


class TemporaryResponseError(TemporaryAPIError):
    def __init__(self, response: requests.Response):
        super().__init__(f'Temporary error: {response.status_code}')
        self.response = response


class UnexpectedResponseError(APIError):
    def __init__(self, response: requests.Response):
        super().__init__(f'Unexpected response with STATUS_CODE: {response.status_code}: {response.text}')
        self.response = response


class APIValidationError(APIError):
    def __init__(self, e: ValidationError):
        if callable(e.errors):
            error_list = e.errors()
            if error_list:
                error_message = error_list[0]
                loc = error_message.get('loc', [])
                msg = error_message.get('msg', 'Unknown message')
                error_details = f"ValidationError: '{loc[-1] if loc else 'Unknown field'} {msg}'"
            else:
                error_details = 'ValidationError: No error details available'
        else:
            error_details = 'ValidationError: Unable to retrieve error details'
        super().__init__(error_details)


class ORDMediascoutClient:
    def __init__(self, config: ORDMediascoutConfig):
        self.config = config
        self.auth = HTTPBasicAuth(self.config.username, self.config.password)
        self.headers = {'Content-Type': 'application/json-patch+json'}
        self.logger = logging.getLogger('ord_mediascout_client')
        self.sentry_logger = logging.getLogger('ord_mediascout_client.sentry')

    def _call(
        self,
        method: str,
        url: str,
        obj: Optional[BaseModel] = None,
        return_type: Optional[Type[Any]] = None,
        **kwargs: dict[str, Any],
    ) -> Any:
        try:
            request = requests.Request(
                method,
                f'{self.config.url}{url}',
                data=obj and obj.json(),
                auth=self.auth,
                headers=self.headers,
                **kwargs,
            )
            prepared_request = request.prepare()
        except Exception as e:
            self.logger.exception(f'Error while preparing request: {method} {url}')
            raise APIError from e

        try:
            with requests.Session() as session:
                response = session.send(prepared_request)

            self.logger.debug(
                f'API call: {method} {prepared_request.url}\n'
                f'Headers: {self.headers}\n'
                f'Body: {obj and obj.json(indent=4, ensure_ascii=False)}\n'
                f'Response: {response.status_code}\n'
                f'{response.text}'
            )
        except requests.ConnectionError as e:
            self.logger.exception(
                f'API call: {method} {prepared_request.url}\n'
                f'Headers: {self.headers}\n'
                f'Body: {obj and obj.json(indent=4, ensure_ascii=False)}\n'
                f'Exception: {e}\n'
            )
            raise TemporaryAPIError(f'Connection lost while requesting: {method} {url}') from e
        except requests.RequestException as e:
            self.logger.exception(
                f'API call: {method} {prepared_request.url}\n'
                f'Headers: {self.headers}\n'
                f'Body: {obj and obj.json(indent=4, ensure_ascii=False)}\n'
                f'Exception: {e}\n'
            )
            raise APIError from e

        match response.status_code:
            case 400 | 401:
                try:
                    bad_response = BadRequestResponse.parse_raw(response.text)
                except ValidationError as e:
                    try:
                        problem_details = ProblemDetails.parse_raw(response.text)
                    except ValidationError:
                        self.sentry_logger.exception(
                            f'API call: {method} {url}\n'
                            f'Headers: {self.headers}\n'
                            f'Body: {obj and obj.json(indent=4, ensure_ascii=False)}\n'
                            f'Exception: {e}\n'
                        )
                        raise UnexpectedResponseError(response) from e
                    else:
                        raise BadResponseError(
                            response,
                            BadRequestResponse(
                                errorType=problem_details.type,
                                traceId=problem_details.traceId,
                                errorItems=[ValidationFailure(errorMessage=problem_details.detail)],
                            ),
                        ) from e
                else:
                    raise BadResponseError(response, bad_response)
            case int() if 500 <= response.status_code < 600:
                raise TemporaryResponseError(response)
            case 200 | 201 | 204:
                if return_type is not None:
                    try:
                        return parse_raw_as(return_type, response.text or '{}')
                    except ValidationError as e:
                        raise APIValidationError(e) from e
            case _:
                self.sentry_logger.exception(
                    f'Unexpected response.status_code: {response.status_code}\n'
                    f'API call: {method} {url}\n'
                    f'Headers: {self.headers}\n'
                    f'Body: {obj and obj.json(indent=4, ensure_ascii=False)}\n'
                )
                raise UnexpectedResponseError(response)

    # Clients
    def create_client(self, client: CreateClientRequest) -> ClientResponse:
        client: ClientResponse = self._call('post', '/webapi/v3/clients', client, ClientResponse)
        return client

    def get_clients(self, parameters: GetClientRequest) -> list[ClientResponse]:
        params = self._prepare_params(parameters)
        clients: list[ClientResponse] = self._call(
            'get', '/webapi/v3/clients', None, list[ClientResponse], params=params
        )
        return clients

    # Contracts
    def create_initial_contract(self, contract: CreateInitialContractRequest) -> InitialContractResponse:
        contract: InitialContractResponse = self._call(
            'post', '/webapi/v3/contracts/initial', contract, InitialContractResponse
        )
        return contract

    def edit_initial_contract(self, contract: EditInitialContractWebApiDto) -> InitialContractResponse:
        contract: InitialContractResponse = self._call(
            'patch', '/webapi/v3/contracts/initial', contract, InitialContractResponse
        )
        return contract

    def get_initial_contracts(self, parameters: GetInitialContractRequest) -> list[InitialContractResponse]:
        params = self._prepare_params(parameters)
        contracts: list[InitialContractResponse] = self._call(
            'get', '/webapi/v3/contracts/initial', None, list[InitialContractResponse], params=params
        )
        return contracts

    def create_final_contract(self, contract: CreateFinalContractRequest) -> FinalContractResponse:
        contract: FinalContractResponse = self._call(
            'post', '/webapi/v3/contracts/final', contract, FinalContractResponse
        )
        return contract

    def edit_final_contract(self, contract: EditFinalContractWebApiDto) -> FinalContractResponse:
        contract: FinalContractResponse = self._call(
            'patch', '/webapi/v3/contracts/final', contract, FinalContractResponse
        )
        return contract

    def get_final_contracts(self, parameters: GetFinalContractsRequest) -> list[FinalContractResponse]:
        params = self._prepare_params(parameters)
        contracts: list[FinalContractResponse] = self._call(
            'get', '/webapi/v3/contracts/final', None, list[FinalContractResponse], params=params
        )
        return contracts

    def create_outer_contract(self, contract: CreateOuterContractRequest) -> OuterContractResponse:
        contract: OuterContractResponse = self._call(
            'post', '/webapi/v3/contracts/outer', contract, OuterContractResponse
        )
        return contract

    def edit_outer_contract(self, contract: EditOuterContractWebApiDto) -> OuterContractResponse:
        contract: OuterContractResponse = self._call(
            'patch', '/webapi/v3/contracts/outer', contract, OuterContractResponse
        )
        return contract

    def get_outer_contracts(self, parameters: GetOuterContractsRequest) -> list[OuterContractResponse]:
        params = self._prepare_params(parameters)
        contracts: list[OuterContractResponse] = self._call(
            'get', '/webapi/v3/contracts/outer', None, list[OuterContractResponse], params=params
        )
        return contracts

    # new
    def delete_contract(self, contract: DeleteContractWebApiDto) -> None:
        contract_kind = contract.contractKind.value if contract.contractKind else ''
        self._call('delete', f'/webapi/v3/contracts/{contract_kind}/{contract.contractId}', contract)

    # Creatives
    def create_creative(self, creative: CreateCreativeRequest) -> CreatedCreativeResponse:
        creative: CreatedCreativeResponse = self._call(
            'post', '/webapi/v3/creatives', creative, CreatedCreativeResponse
        )
        return creative

    def edit_creative(self, creative: EditCreativeRequest) -> CreativeResponse:
        updated_creative: CreativeResponse = self._call('patch', '/webapi/v3/creatives', creative, CreativeResponse)
        return updated_creative

    def get_creatives(self, parameters: GetCreativesParameters) -> list[CreativeResponse]:
        params = self._prepare_params(parameters)
        creatives: list[CreativeResponse] = self._call(
            'get', '/webapi/v3/creatives', None, list[CreativeResponse], params=params
        )
        return creatives

    # new
    def get_creative_status(self, parameters: GetCreativesWebApiDto) -> CreativeStatus:
        creative_status: CreativeStatus = self._call(
            'get', f'/webapi/v3/creatives/{parameters.id}/status', parameters, CreativeStatus
        )
        return creative_status

    # new
    def restore_creative(self, parameters: DeleteRestoreCreativeWebApiDto) -> None:
        self._call('put', f'/webapi/v3/creatives/restore/{parameters.erid or parameters.nativeCustomerId}', parameters)

    # new
    def delete_creative(self, parameters: DeleteRestoreCreativeWebApiDto) -> None:
        self._call('delete', f'/webapi/v3/creatives/{parameters.erid or parameters.nativeCustomerId}', parameters)

    # Creative Group
    def edit_creative_group(self, creative_group: CreativeGroupResponse) -> CreativeGroupResponse:
        updated_creative_group: CreativeGroupResponse = self._call(
            'patch', '/webapi/v3/creatives/group', creative_group, CreativeGroupResponse
        )
        return updated_creative_group

    def get_creative_groups(self, parameters: GetCreativeGroupsRequest) -> list[CreativeGroupResponse]:
        creative_groups: list[CreativeGroupResponse] = self._call(
            'get', '/webapi/v3/creatives/groups', parameters, list[CreativeGroupResponse]
        )
        return creative_groups

    # Feeds
    def create_container(self, container: CreateContainerWebApiDto) -> ResponseContainerWebApiDto:
        container: ResponseContainerWebApiDto = self._call(
            'post', '/webapi/v3/feeds/containers', container, ResponseContainerWebApiDto
        )
        return container

    def get_containers(self, parameters: GetContainerWebApiDto) -> list[ResponseGetContainerWebApiDto]:
        containers: list[ResponseGetContainerWebApiDto] = self._call(
            'get', '/webapi/v3/feeds/containers', parameters, list[ResponseGetContainerWebApiDto]
        )
        return containers

    def create_feed_elements(self, feed_elements: CreateFeedElementsWebApiDto) -> list[ResponseFeedElementsWebApiDto]:
        feed_elements: list[ResponseFeedElementsWebApiDto] = self._call(
            'post', '/webapi/v3/feeds/elements', feed_elements, list[ResponseFeedElementsWebApiDto]
        )
        return feed_elements

    def edit_feed_element(self, feed_element: EditFeedElementWebApiDto) -> ResponseEditFeedElementWebApiDto:
        feed_element: ResponseEditFeedElementWebApiDto = self._call(
            'patch', '/webapi/v3/feeds/elements', feed_element, ResponseEditFeedElementWebApiDto
        )
        return feed_element

    def get_feed_elements(self, parameters: GetFeedElementsWebApiDto) -> list[ResponseGetFeedElementsWebApiDto]:
        feed_elements: list[ResponseGetFeedElementsWebApiDto] = self._call(
            'get', '/webapi/v3/feeds/elements', parameters, list[ResponseGetFeedElementsWebApiDto]
        )
        return feed_elements

    def create_feed_elements_bulk(
        self, feed_elements_bulk: CreateFeedElementsBulkWebApiDto
    ) -> ResponseCreateFeedElementsBulkWebApiDto:
        feed_elements_bulk: ResponseCreateFeedElementsBulkWebApiDto = self._call(
            'post', '/webapi/v3/feeds/elements/bulk', feed_elements_bulk, ResponseCreateFeedElementsBulkWebApiDto
        )
        return feed_elements_bulk

    def get_feed_elements_bulk_info(
        self, feed_elements_bulk_info: GetFeedElementsBulkInfo
    ) -> ResponseGetFeedElementsBulkInfo:
        feed_elements_bulk_info: ResponseGetFeedElementsBulkInfo = self._call(
            'get', '/webapi/v3/feeds/elements/bulk', feed_elements_bulk_info, ResponseGetFeedElementsBulkInfo
        )
        return feed_elements_bulk_info

    # Invoices
    def create_invoice(self, invoice: CreateInvoiceRequest) -> EntityIdResponse:
        entity: EntityIdResponse = self._call('post', '/webapi/v3/invoices', invoice, EntityIdResponse)
        return entity

    def edit_invoice(self, invoice: EditInvoiceDataWebApiDto) -> InvoiceResponse:
        invoice: InvoiceResponse = self._call(
            'patch', f'/webapi/v3/invoices/{invoice.id}/edit', invoice, InvoiceResponse
        )
        return invoice

    def overwrite_invoice(self, invoice: EditInvoiceStatisticsWebApiDto) -> None:
        self._call('put', f'/webapi/v3/invoices/{invoice.id}/overwrite', invoice)

    def clear_invoice(self, invoice: ClearInvoiceDataWebApiDto) -> None:
        self._call('put', f'/webapi/v3/invoices/{invoice.id}/clear', invoice)

    def partial_clear_invoice(self, invoice: PartialClearInvoiceWebApiDto) -> None:
        self._call('put', f'/webapi/v3/invoices/{invoice.id}/partialclear', invoice)

    def supplement_invoice(self, invoice: SupplementInvoiceWebApiDto) -> EntityIdResponse:
        entity: EntityIdResponse = self._call(
            'patch', f'/webapi/v3/invoices/{invoice.id}/supplement', invoice, EntityIdResponse
        )
        return entity

    def get_invoices(self, parameters: GetInvoicesWebApiDto) -> list[InvoiceResponse]:
        params = self._prepare_params(parameters)
        invoices: list[InvoiceResponse] = self._call(
            'get', '/webapi/v3/invoices', None, list[InvoiceResponse], params=params
        )
        return invoices

    def get_invoice_summary(self, entity: EntityIdResponse) -> InvoiceSummaryResponse:
        invoice_summary: InvoiceSummaryResponse = self._call(
            'get', f'/webapi/v3/invoices/{entity.id}/summary', entity, InvoiceSummaryResponse
        )
        return invoice_summary

    def confirm_invoice(self, entity: EntityIdResponse) -> None:
        self._call('patch', f'/webapi/v3/invoices/{entity.id}/confirm', entity)

    def delete_invoice(self, entity: EntityIdResponse) -> None:
        self._call('delete', f'/webapi/v3/invoices/{entity.id}', entity)

    # new
    def delete_invoice_initial_contracts(
        self, invoice_id: int, initial_contracts: PartialClearInvoiceInitialContractsRequest
    ) -> None:
        self._call('delete', f'/webapi/v3/invoices/{invoice_id}/initial_contracts', initial_contracts)

    # WebApiPlatform
    def create_platform(self, platform: CreatePlatformRequest) -> EntityIdResponse:
        entity: EntityIdResponse = self._call('post', '/webapi/v3/platforms', platform, EntityIdResponse)
        return entity

    def edit_platform(self, platform: EditPlatformWebApiDto) -> PlatformResponse:
        updated_platform: PlatformResponse = self._call(
            'patch', f'/webapi/v3/platforms/{platform.id}', platform, PlatformResponse
        )
        return updated_platform

    # Statistics
    def create_statistics(self, statistics: CreateInvoicelessStatisticsRequest) -> None:
        statistics: None = self._call('post', '/webapi/v3/statistics', statistics, None)
        return statistics

    def get_statistics(self, parameters: GetInvoicelessPeriodsRequest) -> list[InvoicelessStatisticsResponse]:
        statistics: list[InvoicelessStatisticsResponse] = self._call(
            'get', '/webapi/v3/statistics', parameters, list[InvoicelessStatisticsResponse]
        )
        return statistics

    # PING
    def ping(self) -> bool:
        tmp_auth, self.auth = self.auth, None
        self._call('get', '/webapi/ping')
        self.auth = tmp_auth
        return True

    def ping_auth(self) -> bool:
        self._call('get', '/webapi/pingauth')
        return True

    def _prepare_params(self, parameters: BaseModel) -> dict[str, Any]:
        params: dict[str, Any] = cast(dict[str, Any], parameters.dict(exclude_none=True))
        for key, value in params.items():
            if isinstance(value, Enum):
                params[key] = value.value
        return params
