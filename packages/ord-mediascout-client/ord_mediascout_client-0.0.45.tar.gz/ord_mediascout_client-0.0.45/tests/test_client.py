from ord_mediascout_client import (
    CounterpartyStatus,
    CreateClientRequest,
    GetClientRequest,
)


def test__create_client(client, client_data):
    data = client_data()
    request_data = CreateClientRequest(**data)

    response_data = client.create_client(request_data)

    assert request_data.name == response_data.name
    assert request_data.inn == response_data.inn
    # assert request_data.mobilePhone == response_data.mobilePhone
    # assert request_data.epayNumber == response_data.epayNumber
    # assert request_data.regNumber == response_data.regNumber
    # assert request_data.oksmNumber == response_data.oksmNumber
    # assert request_data.createMode == response_data.createMode
    assert request_data.legalForm == response_data.legalForm
    assert response_data.id is not None
    assert response_data.status == CounterpartyStatus.Active


def test__get_clients(client):
    request_data = GetClientRequest(status=CounterpartyStatus.Active)

    response_data = client.get_clients(request_data)

    assert len(response_data) > 0
    for participant in response_data:
        assert participant.id is not None
        assert participant.status == CounterpartyStatus.Active


def test__get_client__by_id(client):
    client_id = 'CLGk5Rgt3AHk6er6qXR1T4mA'
    request_data = GetClientRequest(id=client_id)

    response_data = client.get_clients(request_data)

    assert len(response_data) == 1
    for participant in response_data:
        assert participant.id == client_id


def test__get_client__by_inn(client):
    inn = '7740000076'
    request_data = GetClientRequest(inn=inn)

    response_data = client.get_clients(request_data)

    assert len(response_data) == 1
    for participant in response_data:
        assert participant.id is not None
        assert participant.inn == inn
