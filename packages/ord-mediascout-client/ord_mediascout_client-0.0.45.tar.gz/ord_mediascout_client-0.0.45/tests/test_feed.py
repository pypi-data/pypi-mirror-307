import pytest

from tests.conftest import print_obj
from conftest import _setup_test_data

from ord_mediascout_client import (
    CreateFeedElementsRequest,
    CreateAdvertisingContainerRequest,
    CreateDelayedFeedElementsBulkRequest,
    EditFeedElementsRequest,
    EditDelayedFeedElementsBulkRequest,
    GetContainerWebApiDto,
    GetFeedElementsWebApiDto,
)


@pytest.fixture(scope="module")
def create_container(client, feed_elements_data, container_data):
    feed_data = feed_elements_data()
    data = container_data(
        feedNativeCustomerId=feed_data['feedNativeCustomerId'],
        nativeCustomerId=feed_data['feedElements'][0]['nativeCustomerId']
    )
    request_data = CreateAdvertisingContainerRequest(**data)

    response_data = client.create_container(request_data)
    return response_data


@pytest.fixture(scope="module")
def create_feed_element(client, feed_elements_data):
    data = feed_elements_data()
    request_data = CreateFeedElementsRequest(**data)

    response_data = client.create_feed_elements(request_data)
    return response_data, data


@pytest.fixture(scope="module")
def create_feed_elements_bulk(client, bulk_feed_elements_data):
    data = bulk_feed_elements_data()
    request_data = CreateDelayedFeedElementsBulkRequest(**data)

    response_data = client.create_feed_elements_bulk(request_data)
    return response_data


def test__create_feed_element(create_feed_element):
    created_element, request_data = create_feed_element

    assert len(created_element) == 1
    assert created_element[0].feedId is not None
    assert created_element[0].feedName == request_data['feedName']
    assert created_element[0].feedNativeCustomerId == request_data['feedNativeCustomerId']
    assert created_element[0].status is not None
    assert created_element[0].id is not None
    assert created_element[0].nativeCustomerId == request_data['feedElements'][0]['nativeCustomerId']
    assert created_element[0].description == request_data['feedElements'][0]['description']
    assert created_element[0].advertiserUrls == request_data['feedElements'][0]['advertiserUrls']


def test__create_container(create_container):
    created_container = create_container
    assert created_container is not None
    assert created_container.id is not None


def test__get_containers(client):
    request_data = GetContainerWebApiDto(status='Active')

    response_data = client.get_containers(request_data)

    for container in response_data:
        assert container is not None


def test__get_feed_elements(client):
    # Прописал вручную ids, так как сервис возвращает слишком много активных элементов
    request_data = GetFeedElementsWebApiDto(ids=_setup_test_data['feed']['elements'], status='Active')

    response_data = client.get_feed_elements(request_data)

    for feed_element in response_data:
        assert feed_element is not None


def test__edit_feed_element(client, create_feed_element, edit_feed_elements_data):
    created_element, request_data = create_feed_element
    edit_data = edit_feed_elements_data(feedElements=[
        {
            'id': created_element[0].id,
            'textData': [
                {
                    'id': created_element[0].textData[0].id,
                    'actionType': 'Edit',
                    'textData': 'Edited text data',
                },
            ],
        },
    ])
    request_data = EditFeedElementsRequest(**edit_data)

    response_data = client.edit_feed_element(request_data)

    for element in response_data:
        assert element is not None


def test__create_feed_elements_bulk(create_feed_elements_bulk):
    response_data = create_feed_elements_bulk

    assert response_data is not None
    assert response_data.id is not None


# Используется заранее созданный фид с элементами и не пустыми полями feedElementId и feedId.
# После создания фида методом client.create_feed_elements_bulk(), запрос методом
# client.get_feed_elements_bulk_info() возвращает элементы с еще пустыми feedElementId и feedId.
# По этому выполнить редактирование client.edit_feed_elements_bulk() сразу нельзя.
# Так же нужно дождаться изменения статуса элементов с "ReadyToDownload" и появления загруженных данных в feedElementMedias
def test__edit_feed_elements_bulk(client, bulk_edit_feed_elements_data):
    edit_data = bulk_edit_feed_elements_data()
    request_data = EditDelayedFeedElementsBulkRequest(**edit_data)

    response_data = client.edit_feed_elements_bulk(request_data)

    assert response_data.id is not None


@pytest.mark.skip(reason="Этот тест временно отключен")
def test__request_absent_feed_element(client, faker):
    request_dto = GetFeedElementsWebApiDto(ids=['absent_feed_element_id'])

    response_dto = client.get_feed_elements(request_dto)

    assert len(response_dto) == 0


@pytest.mark.skip(reason="Этот тест временно отключен")
def test__request_all_feed_element(client, faker):
    request_dto = GetFeedElementsWebApiDto()

    response_dto = client.get_feed_elements(request_dto)

    assert len(response_dto) != 0
