import pytest

from ord_mediascout_client import CreatePlatformRequest, EditPlatformWebApiDto


# НЕ работает в режиме "get or create", только "create" с новым url, потому url и название генерятся
@pytest.fixture(scope="module")
def create_platform(client, platform_data):
    data = platform_data()
    request_data = CreatePlatformRequest(**data)

    response_data = client.create_platform(request_data)
    return response_data, request_data


def test__create_platform(create_platform):
    created_platform, _ = create_platform

    assert created_platform is not None
    assert created_platform.id is not None


def test__edit_platform(client, create_platform):
    created_platform, platform_data = create_platform
    platform_data.name += "_edit_"
    request_data = EditPlatformWebApiDto(**platform_data.dict())

    response_data = client.edit_platform(created_platform.id, request_data)

    assert response_data is not None
    assert isinstance(response_data.id, str)
    assert request_data.name == response_data.name
