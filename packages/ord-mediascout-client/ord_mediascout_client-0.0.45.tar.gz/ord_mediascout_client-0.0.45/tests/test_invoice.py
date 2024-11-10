import pytest
import random
import copy

from ord_mediascout_client import (
    ClearInvoiceDataWebApiDto,
    CreateInvoiceRequest,
    EditInvoiceDataWebApiDto,
    EditInvoiceStatisticsWebApiDto,
    EntityIdResponse,
    GetInvoicesWebApiDto,
    InvoiceStatus,
    PartialClearInvoiceWebApiDto,
    PartialClearInvoiceStatisticsItem,
    PartialClearInvoiceStatisticsRequest,
    PartialClearInvoiceInitialContractsRequest,
)


# НЕ работает в режиме "get or create", только "create" с новым номером, потому number генерится
@pytest.fixture(scope="module")
def create_invoice(client, invoice_data):
    data = invoice_data()
    request_data = CreateInvoiceRequest(**data)

    response_data = client.create_invoice(request_data)
    # Возвращать приходится и данные запроса, так как МС в при создании акта возвращает лишь ID
    # и дополнительные данные акта потом извлечь из МС не получится
    return response_data, request_data


def test__create_invoice(create_invoice):
    created_invoice, _ = create_invoice
    assert created_invoice is not None
    assert created_invoice.id is not None


def test__get_invoices(client):
    request_data = GetInvoicesWebApiDto(status=InvoiceStatus.Active)

    response_data = client.get_invoices(request_data)

    assert len(response_data) > 0
    for invoice in response_data:
        print(f'{invoice.id=}: {invoice.status}')
        assert invoice.id is not None
        assert invoice.status == InvoiceStatus.Active


def test__get_one_invoice(client, create_invoice):
    created_invoice, _ = create_invoice
    request_data = GetInvoicesWebApiDto(ids=[created_invoice.id])

    response_data = client.get_invoices(request_data)[0]

    assert response_data.id is not None


def test__get_invoice_summary(client, create_invoice):
    created_invoice, _ = create_invoice
    request_data = EntityIdResponse(id=created_invoice.id)

    response_data = client.get_invoice_summary(request_data)

    assert response_data is not None
    assert isinstance(response_data.id, str)


def test__edit_invoice(client, create_invoice):
    # Получить и подготовить данные акта для редактирования
    created_invoice, _invoice_data = create_invoice
    invoice_data = copy.deepcopy(_invoice_data)
    # Отредактировать данные
    invoice_data.number += '_edit_'
    del(invoice_data.initialContractsData)
    del(invoice_data.statisticsByPlatforms)

    request_data = EditInvoiceDataWebApiDto(**invoice_data.dict())

    response_data = client.edit_invoice(created_invoice.id, request_data)

    assert response_data is not None
    assert isinstance(response_data.id, str)


def test__overwrite_invoice(client, create_invoice):
    created_invoice, _invoice_data = create_invoice
    invoice_data = copy.deepcopy(_invoice_data)
    # Отредактировать данные
    invoice_data.initialContractsData[0].amount += random.randrange(10, 100)
    invoice_data.statisticsByPlatforms[0].amount += random.randrange(10, 100)

    request_data = EditInvoiceStatisticsWebApiDto(
        initialContractsData=invoice_data.initialContractsData,
        statisticsByPlatforms=invoice_data.statisticsByPlatforms,
    )

    client.overwrite_invoice(created_invoice.id, request_data)


def test__confirm_invoice(client, create_invoice):
    created_invoice, _ = create_invoice
    request_data = EntityIdResponse(id=created_invoice.id)

    client.clear_invoice(request_data)


def test__clear_invoice(client, create_invoice):
    created_invoice, _ = create_invoice
    request_data = ClearInvoiceDataWebApiDto(id=created_invoice.id)

    client.clear_invoice(request_data)


def test__partial_clear_invoice(client, create_invoice):
    created_invoice, invoice_data = create_invoice
    data = invoice_data.statisticsByPlatforms[0].dict()
    for key in ["amount", "impsFact", "impsPlan", "platformName", "platformOwnedByAgency", "platformType", "price"]:
        data.pop(key, None)
    request_data = PartialClearInvoiceWebApiDto(
        initialContracts=[initital_contract.initialContractId for initital_contract in invoice_data.initialContractsData],
        statisticsByPlatforms=[PartialClearInvoiceStatisticsItem(**data)],
    )

    client.partial_clear_invoice(created_invoice.id, request_data)


def test__delete_invoice_initial_contracts(client, create_invoice):
    created_invoice, invoice_data = create_invoice

    request_data = PartialClearInvoiceInitialContractsRequest(
        initialContracts=[
            initital_contract.initialContractId for initital_contract in invoice_data.initialContractsData
        ]
    )

    client.delete_invoice_initial_contracts(created_invoice.id, request_data)


def test__delete_invoice_statistics(client, create_invoice):
    created_invoice, invoice_data = create_invoice
    data = invoice_data.statisticsByPlatforms[0].dict()
    for key in ["amount", "impsFact", "impsPlan", "platformName", "platformOwnedByAgency", "platformType", "price"]:
        data.pop(key, None)
    request_data = PartialClearInvoiceStatisticsRequest(
        statistics=[PartialClearInvoiceStatisticsItem(**data)]
    )
    client.delete_invoice_statistics(created_invoice.id, request_data)


def test__delete_invoice(client, create_invoice):
    created_invoice, _ = create_invoice
    request_data = EntityIdResponse(id=created_invoice.id)
    client.delete_invoice(request_data)


