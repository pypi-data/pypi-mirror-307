import random

from ord_mediascout_client import (
    CreateInvoiceRequest,
    GetInvoicesParameters,
    InvoiceInitialContractItem,
    InvoicePartyRole,
    InvoiceStatisticsByPlatformsItem,
    InvoiceStatus,
    PlatformType,
)


# НЕ работает в режиме "get or create", только "create" с новым номером, потому number генерится
def test__create_invoice(client):
    request_data = CreateInvoiceRequest(
        number='INV-{}'.format(random.randrange(11111111, 99999999)),
        date='2023-03-20',
        contractorRole=InvoicePartyRole.Rr,
        clientRole=InvoicePartyRole.Ra,
        amount=20000.00,
        startDate='2023-03-23',
        endDate='2023-03-23',
        finalContractId='CTiwhIpoQ_F0OEPpKj8vWKGg',
        initialContractsData=[InvoiceInitialContractItem(initialContractId='CTKLAzsvgYREmK0unGXLsCTg', amount=1000.00)],
        statisticsByPlatforms=[
            InvoiceStatisticsByPlatformsItem(
                initialContractId='CTKLAzsvgYREmK0unGXLsCTg',
                erid='Pb3XmBtzsxtPgHUnh4hEFkxvF9Ay6CSGDzFnCHt',
                platformUrl='http://www.testplatform.ru',
                platformName='Test Platform 1',
                platformType=PlatformType.Site,
                platformOwnedByAgency=False,
                impsPlan=10000,
                impsFact=10,
                startDatePlan='2023-04-03',
                startDateFact='2023-04-03',
                endDatePlan='2023-04-03',
                endDateFact='2023-04-03',
                amount=1000.00,
                price=0.5,
                #                vatIncluded=True,
            )
        ],
    )

    response_data = client.create_invoice(request_data)

    assert response_data.id is not None


def test__get_invoices(client):
    request_data = GetInvoicesParameters(status=InvoiceStatus.Active)

    response_data = client.get_invoices(request_data)

    assert len(response_data) > 0
    for invoice in response_data:
        print(f'{invoice.id=}: {invoice.status}')
        assert invoice.id is not None
        assert invoice.status == InvoiceStatus.Active


def test__get_invoices__by_id(client):
    invoice_ids = ['INjBnsHydXB0-gmGlG-HtNmQ', 'INHPHd4um3W0CABa5MYiCtEg']
    request_data = GetInvoicesParameters(ids=invoice_ids)

    response_data = client.get_invoices(request_data)

    assert len(response_data) == 2
    for invoice in response_data:
        assert invoice.id in invoice_ids
