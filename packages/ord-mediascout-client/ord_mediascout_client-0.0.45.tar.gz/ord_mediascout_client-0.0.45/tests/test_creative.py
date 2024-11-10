import pytest

from conftest import _setup_test_data

from ord_mediascout_client import (
    CreateCreativeRequest,
    GetCreativeGroupsRequest,
    CreativeGroupResponse,
    CreatedCreativeResponse,
    CreativeForm,
    CreativeStatus,
    DeleteRestoreCreativeWebApiDto,
    EditCreativeRequest,
    GetCreativesWebApiDto,
    GetCreativeStatusWebApiDto,
)


@pytest.fixture(scope="module")
def create_mediadata_creative(client, creative_data):
    data = creative_data()
    data['textData'] = []
    data['form'] = CreativeForm.Banner
    request_data = CreateCreativeRequest(**data)

    response_data = client.create_creative(request_data)
    return response_data


@pytest.fixture(scope="module")
def create_textdata_creative(client, creative_data):
    data = creative_data()
    data['mediaData'] = []
    data['form'] = CreativeForm.Text
    request_data = CreateCreativeRequest(**data)

    response_data = client.create_creative(request_data)
    return response_data


def test__create_mediadata_creative(create_mediadata_creative):
    assert create_mediadata_creative is not None
    assert isinstance(create_mediadata_creative, CreatedCreativeResponse)


def test__create_textdata_creative(create_textdata_creative):
    assert create_textdata_creative is not None
    assert isinstance(create_textdata_creative, CreatedCreativeResponse)


def test__get_creative_status(client, create_mediadata_creative):
    request_data = GetCreativeStatusWebApiDto(creativeId=create_mediadata_creative.id)

    response_data = client.get_creative_status(request_data)

    assert response_data is not None
    assert response_data.erid == create_mediadata_creative.erid


def test__get_creatives(client):
    request_data = GetCreativesWebApiDto(status=CreativeStatus.Registering)

    response_data = client.get_creatives(request_data)

    assert len(response_data) > 0
    for creative in response_data:
        assert creative.id is not None
        assert creative.status == CreativeStatus.Registering


def test__get_one_creative(client):
    request_data = GetCreativesWebApiDto(ids=_setup_test_data['creative']['ids'])

    response_data = client.get_creatives(request_data)

    assert len(response_data) == len(_setup_test_data['creative']['ids'])
    for creative in response_data:
        assert creative.id is not None
        assert creative.id in _setup_test_data['creative']['ids']


def test__edit_creative(client, create_mediadata_creative):
    request_data = EditCreativeRequest(
        id=create_mediadata_creative.id,
        creativeGroupId=create_mediadata_creative.creativeGroupId,
        advertiserUrls=['https://clisite1-edit.ru/', 'https://clisite2-edit.ru/'],
        overwriteExistingCreativeMedia=False,
    )
    filtered_data = request_data.dict(exclude_none=True)
    for field in request_data.__fields__:
        if field not in filtered_data:
            delattr(request_data, field)

    response_data = client.edit_creative(request_data)

    assert response_data is not None
    assert response_data.id == create_mediadata_creative.id


def test__edit_creative_group(client, create_mediadata_creative):
    # Получить креатив для извлечения параметров для запроса на редактирование
    request_creative = GetCreativesWebApiDto(ids=[create_mediadata_creative.id])
    creative = client.get_creatives(request_creative)[0]

    request_creative_group = CreativeGroupResponse(
        creativeGroupId=creative.creativeGroupId,
        creativeGroupName=creative.creativeGroupName,
        finalContractId=creative.finalContractId,
        isSelfPromotion=creative.isSelfPromotion,
        type=creative.type,
        form=creative.form,
        isSocial=creative.isSocial,
        isNative=creative.isNative,
        description="Edited description",
    )

    response_data = client.edit_creative_group(request_creative_group)

    assert response_data is not None
    assert response_data.creativeGroupId == creative.creativeGroupId


def test__get_creative_groups(client, creative_data):
    data = creative_data()
    request_data = GetCreativeGroupsRequest(
        finalContractId=data['finalContractId'],
        initialContractId=data['initialContractId'],
    )

    response_data = client.get_creative_groups(request_data)

    assert response_data is not None
    for creative_group in response_data:
        assert isinstance(creative_group.creativeGroupId, str)


def test__delete_and_restore_creative(client, create_mediadata_creative):
    request_data = DeleteRestoreCreativeWebApiDto(erid=create_mediadata_creative.erid)
    client.delete_creative(request_data)
    client.restore_creative(request_data)


def test__delete_creative(client, create_mediadata_creative):
    request_data = DeleteRestoreCreativeWebApiDto(erid=create_mediadata_creative.erid)
    client.delete_creative(request_data)
