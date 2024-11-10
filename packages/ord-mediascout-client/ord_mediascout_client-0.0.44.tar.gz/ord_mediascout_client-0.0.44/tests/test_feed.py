import pytest

from ord_mediascout_client import (
    CreateFeedElementsWebApiDto,
    FeedElementTextDataItem,
    FeedElementWebApiDto,
    GetFeedElementsWebApiDto,
)


@pytest.mark.skip(reason='Not implemented')
def test_create_feed_elements(client, faker):
    request_dto = CreateFeedElementsWebApiDto(
        feedName='test_feed',
        feedNativeCustomerId='test_feed_id',
        feedElements=[
            FeedElementWebApiDto(
                nativeCustomerId=faker.uuid4(),
                description=faker.text(30),
                advertiserUrls=[faker.url()[:-1]],
                textData=[FeedElementTextDataItem(textData=faker.text())],
            )
        ],
    )

    response_dto = client.create_feed_elements(request_dto)

    assert len(response_dto) == 1
    assert response_dto[0].feedId is not None
    assert response_dto[0].feedName == request_dto.feedName
    assert response_dto[0].feedNativeCustomerId == request_dto.feedNativeCustomerId
    assert response_dto[0].status is not None
    assert response_dto[0].id is not None
    assert response_dto[0].nativeCustomerId == request_dto.feedElements[0].nativeCustomerId
    assert response_dto[0].description == request_dto.feedElements[0].description
    assert response_dto[0].advertiserUrls == request_dto.feedElements[0].advertiserUrls


@pytest.mark.skip(reason='Not implemented')
def test_request_absent_feed_element(client, faker):
    request_dto = GetFeedElementsWebApiDto(ids=['absent_feed_element_id'])

    response_dto = client.get_feed_elements(request_dto)

    assert len(response_dto) == 0


@pytest.mark.skip(reason='Not implemented')
def test_request_all_feed_element(client, faker):
    request_dto = GetFeedElementsWebApiDto()

    response_dto = client.get_feed_elements(request_dto)

    assert len(response_dto) != 0
