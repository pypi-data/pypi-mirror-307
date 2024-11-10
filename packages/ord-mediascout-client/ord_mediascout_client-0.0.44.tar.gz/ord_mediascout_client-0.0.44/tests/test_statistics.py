from ord_mediascout_client import (
    CreateInvoicelessStatisticsRequest,
    GetInvoicelessPeriodsRequest,
    InvoicelessStatisticsByPlatforms,
)

# Setup test data
_erid = 'Kra23f3QL'
_platformUrl = 'http://www.testplatform.ru'
_platformName = 'Test Platform 1'
_platformType = 'Site'
_platformOwnedByAgency = False
_type='CPM'
_impsPlan = 10000
_impsFact = 100
_startDatePlan = '2023-06-01'
_startDateFact = '2023-06-01'
_endDatePlan = '2023-06-20'
_endDateFact = '2023-06-20'
_amount = 50000
_price = 5


def test_create_statistics(client):
    request_data = CreateInvoicelessStatisticsRequest(
        statistics=[
            InvoicelessStatisticsByPlatforms(
                erid=_erid,
                platformUrl=_platformUrl,
                platformName=_platformName,
                platformType=_platformType,
                platformOwnedByAgency=_platformOwnedByAgency,
                type=_type,
                impsPlan=_impsPlan,
                impsFact=_impsFact,
                startDatePlan=_startDatePlan,
                startDateFact=_startDateFact,
                endDatePlan=_endDatePlan,
                endDateFact=_endDateFact,
                amount=_amount,
                price=_price,
            )
        ]
    )

    response_data = client.create_statistics(request_data)

    assert response_data is None


def test_get_statistics(client):
    request_data = GetInvoicelessPeriodsRequest(dateStart='2023-01-01', dateEnd='2023-06-21', status='Creating')

    response_data = client.get_statistics(request_data)

    for statistic in response_data:
        assert statistic.id is not None
