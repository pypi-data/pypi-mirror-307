import pytest

from ord_mediascout_client import (
    ContractStatus,
    CreateFinalContractRequest,
    CreateInitialContractRequest,
    CreateOuterContractRequest,
    DeleteContractWebApiDto,
    DeleteContractKind,
    EditFinalContractWebApiDto,
    EditInitialContractWebApiDto,
    EditOuterContractWebApiDto,
    GetFinalContractsRequest,
    GetInitialContractRequest,
    GetOuterContractsRequest,
)


# Final Contract
@pytest.fixture(scope="module")
def create_final_contract(client, final_contract_data):
    data = final_contract_data()
    request_data = CreateFinalContractRequest(**data)

    response_data = client.create_final_contract(request_data)
    return response_data


def test__create_final_contract(client, create_final_contract):
    response_data = client.create_final_contract(create_final_contract)

    assert create_final_contract.number == response_data.number
    assert create_final_contract.date == response_data.date
    assert create_final_contract.amount == response_data.amount
    assert create_final_contract.type == response_data.type
    assert create_final_contract.subjectType == response_data.subjectType
    assert create_final_contract.clientId == response_data.clientId
    assert create_final_contract.id is not None
    assert create_final_contract.status == ContractStatus.Created or ContractStatus.Active


def test__get_final_contracts(client):
    request_data = GetFinalContractsRequest(status=ContractStatus.Active)

    response_data = client.get_final_contracts(request_data)

    for final_contract in response_data:
        assert final_contract.id is not None
        assert final_contract.status == ContractStatus.Active


def test__edit_final_contract(client, create_final_contract):
    data = create_final_contract.dict()
    data["number"] += "_edit_"
    data["amount"] += 1
    for key in ["id", "cid", "status", "contractorId", "contractorInn", "contractorName", "erirValidationError"]:
        data.pop(key, None)
    request_data = EditFinalContractWebApiDto(**data)

    response_data = client.edit_final_contract(create_final_contract.id, request_data)

    assert response_data.number == request_data.number
    assert response_data.amount == request_data.amount


# curl -X 'DELETE' 'https://demo.mediascout.ru/webapi/v3/contracts/FinalContract/CTiwhIpoQ_F0OEPpKj8vWKGg' -H 'accept: */*'
def test__delete_final_contract(client, create_final_contract):
    request_data = DeleteContractWebApiDto(
        contractId=create_final_contract.id,
        contractKind=DeleteContractKind.FinalContract
    )
    client.delete_contract(create_final_contract.id, request_data)


# Initial Contract
@pytest.fixture(scope="module")
def create_initial_contract(client, initial_contract_data):
    data = initial_contract_data()
    request_data = CreateInitialContractRequest(**data)

    response_data = client.create_initial_contract(request_data)
    return response_data


def test__create_initial_contract(client, create_initial_contract):
    response_data = client.create_initial_contract(create_initial_contract)

    assert create_initial_contract.number == response_data.number
    assert create_initial_contract.date == response_data.date
    assert create_initial_contract.amount == response_data.amount
    # assert create_initial_contract.isAgentActingForPublisher == response_data.isAgentActingForPublisher
    assert create_initial_contract.type == response_data.type
    assert create_initial_contract.subjectType == response_data.subjectType
    # assert create_initial_contract.actionType == response_data.actionType
    assert create_initial_contract.parentMainContractId == response_data.parentMainContractId
    assert create_initial_contract.contractorId == response_data.contractorId
    assert create_initial_contract.clientId == response_data.clientId
    assert create_initial_contract.finalContractId == response_data.finalContractId
    assert create_initial_contract.id is not None
    assert create_initial_contract.status == ContractStatus.Created or ContractStatus.Active


def test__get_initial_contracts(client):
    request_data = GetInitialContractRequest(status=ContractStatus.Active)

    response_data = client.get_initial_contracts(request_data)

    assert len(response_data) > 0
    for initial_contract in response_data:
        assert initial_contract.id is not None
        assert initial_contract.status == ContractStatus.Active


def test__edit_initial_contract(client, create_initial_contract):
    data = create_initial_contract.dict()
    data["number"] += "_edit_"
    data["amount"] += 1
    for key in [
        "id", "cid", "status", "contractorInn", "contractorName", "clientInn", "clientName", "erirValidationError"
    ]:
        data.pop(key, None)
    request_data = EditInitialContractWebApiDto(**data)

    response_data = client.edit_initial_contract(create_initial_contract.id, request_data)

    assert response_data.number == request_data.number
    assert response_data.amount == request_data.amount


def test__delete_initial_contract(client, create_initial_contract):
    request_data = DeleteContractWebApiDto(
        contractId=create_initial_contract.id,
        finalContractId=create_initial_contract.finalContractId,
        contractKind=DeleteContractKind.InitialContract
    )
    client.delete_contract(create_initial_contract.id, request_data)


# Outer Contract
@pytest.fixture(scope="module")
def create_outer_contract(client, outer_contract_data):
    data = outer_contract_data()
    request_data = CreateOuterContractRequest(**data)

    response_data = client.create_outer_contract(request_data)
    return response_data


def test__create_outer_contract(client, create_outer_contract):
    response_data = client.create_outer_contract(create_outer_contract)

    assert create_outer_contract.number == response_data.number
    assert create_outer_contract.date == response_data.date
    assert create_outer_contract.amount == response_data.amount
    # assert create_outer_contract.isAgentActingForPublisher == response_data.isAgentActingForPublisher
    assert create_outer_contract.type == response_data.type
    assert create_outer_contract.subjectType == response_data.subjectType
    # assert create_outer_contract.actionType == response_data.actionType
    # assert create_outer_contract.parentMainContractId == response_data.parentMainContractId
    assert create_outer_contract.contractorId == response_data.contractorId
    assert create_outer_contract.id is not None
    assert create_outer_contract.status == ContractStatus.Created or ContractStatus.Active


def test__get_outer_contracts(client):
    request_data = GetOuterContractsRequest(status=ContractStatus.Active)

    response_data = client.get_outer_contracts(request_data)

    assert len(response_data) > 0
    for outer_contract in response_data:
        assert outer_contract.id is not None
        assert outer_contract.status == ContractStatus.Active


def test__edit_outer_contract(client, create_outer_contract):
    data = create_outer_contract.dict()
    data["number"] += "_edit_"
    data["amount"] += 1
    for key in ["id", "cid", "status", "erirValidationError"]:
        data.pop(key, None)
    request_data = EditOuterContractWebApiDto(**data)

    response_data = client.edit_outer_contract(create_outer_contract.id, request_data)

    assert response_data.number == request_data.number
    assert response_data.amount == request_data.amount


def test__delete_outer_contract(client, create_outer_contract):
    request_data = DeleteContractWebApiDto(
        contractId=create_outer_contract.id,
        contractKind=DeleteContractKind.OuterContract
    )
    client.delete_contract(create_outer_contract.id, request_data)
