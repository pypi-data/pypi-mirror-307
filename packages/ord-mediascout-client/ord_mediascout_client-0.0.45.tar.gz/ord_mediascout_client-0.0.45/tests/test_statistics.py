from ord_mediascout_client import (
    CreateInvoicelessStatisticsRequest,
    GetInvoicelessPeriodsRequest,
)


def test_create_statistics(client, statistics_data):
    data = statistics_data()
    request_data = CreateInvoicelessStatisticsRequest(**data)

    response_data = client.create_statistics(request_data)

    assert response_data is None


def test_get_statistics(client):
    request_data = GetInvoicelessPeriodsRequest(dateStart='2023-01-01', dateEnd='2023-06-21', status='Creating')

    response_data = client.get_statistics(request_data)

    for statistic in response_data:
        assert statistic.id is not None
