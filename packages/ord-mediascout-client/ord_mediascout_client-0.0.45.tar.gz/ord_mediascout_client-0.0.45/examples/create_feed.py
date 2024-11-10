import os

from dotenv import load_dotenv

from ord_mediascout_client import (
    CreateDelayedFeedElementsBulkRequest,
    CreateFeedElementsRequest,
    FeedElementTextDataItem,
    CreateFeedElement,
    CreateDelayedFeedElement,
    GetFeedElementsBulkInfo,
    GetFeedElementsWebApiDto,
    ORDMediascoutClient,
    ORDMediascoutConfig,
)

load_dotenv()

if os.getenv('LOGGING') == 'debug':
    import logging

    logger = logging.getLogger('ord_mediascout_client')
    logger.setLevel(logging.DEBUG)
    logging.basicConfig(level=logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler = logging.FileHandler('ord_mediascout_client.log')
    handler.setFormatter(formatter)
    logger.addHandler(handler)


api = ORDMediascoutClient(ORDMediascoutConfig())


#  Создаем несколько элементов в новом фиде
create_feed_elements__request_dto = CreateFeedElementsRequest(
    feedName='example',
    feedNativeCustomerId='example_id',
    feedElements=[
        CreateFeedElement(
            nativeCustomerId='7',
            description='haha7',
            advertiserUrls=['https://site.ru'],
            textData=[FeedElementTextDataItem(textData='haha')],
        ),
        CreateFeedElement(
            description='haha8',
            nativeCustomerId='8',
            advertiserUrls=['https://site.ru'],
            textData=[FeedElementTextDataItem(textData='haha')],
        ),
        CreateFeedElement(
            description='haha9',
            nativeCustomerId='9',
            advertiserUrls=['https://site.ru'],
            textData=[FeedElementTextDataItem(textData='haha')],
        ),
    ],
)
create_feed_elements__response_dto = api.create_feed_elements(create_feed_elements__request_dto)
print(create_feed_elements__response_dto)


# Создаем несколько элементов в ранее созданном фиде
append_feed_elements__request_dto = CreateFeedElementsRequest(
    feedId='FDZpYSRVLhQEG0p-x53GW2BA',
    feedElements=[
        CreateFeedElement(
            nativeCustomerId='17',
            description='haha17',
            advertiserUrls=['https://site.ru'],
            textData=[FeedElementTextDataItem(textData='haha')],
        ),
        CreateFeedElement(
            description='haha18',
            nativeCustomerId='18',
            advertiserUrls=['https://site.ru'],
            textData=[FeedElementTextDataItem(textData='haha')],
        ),
        CreateFeedElement(
            description='haha19',
            nativeCustomerId='19',
            advertiserUrls=['https://site.ru'],
            textData=[FeedElementTextDataItem(textData='haha')],
        ),
    ],
)
append_feed_elements__response_dto = api.create_feed_elements(append_feed_elements__request_dto)
print(append_feed_elements__response_dto)

#  Получаем список элементов фида по ID элементов
dto = GetFeedElementsWebApiDto(ids=['11375804f', '11375803f', '11375804f', '11375803f'])
result_dto = api.get_feed_elements(dto)


# Создаем пачку элементов в ранее созданном фиде (НЕ РАБОТАЕТ)
create_feed_elements_bulk__request_dto = CreateDelayedFeedElementsBulkRequest(
    feedElements=[
        CreateDelayedFeedElement(
            feedId='FDwwmDToQk_ES1GGezF9iH1g',
            nativeCustomerId='7',
            description='haha7',
            advertiserUrls=['https://site.ru'],
            textData=[FeedElementTextDataItem(textData='haha')],
        ),
        CreateDelayedFeedElement(
            feedId='FDwwmDToQk_ES1GGezF9iH1g',
            description='haha8',
            nativeCustomerId='8',
            advertiserUrls=['https://site.ru'],
            textData=[FeedElementTextDataItem(textData='haha')],
        ),
        CreateDelayedFeedElement(
            feedId='FDwwmDToQk_ES1GGezF9iH1g',
            description='haha9',
            nativeCustomerId='9',
            advertiserUrls=['https://site.ru'],
            textData=[FeedElementTextDataItem(textData='haha')],
        ),
    ]
)
create_feed_elements_bulk__response_dto = api.create_feed_elements_bulk(create_feed_elements_bulk__request_dto)
print(create_feed_elements_bulk__response_dto)

#  Получаем информацию о пачке с id = 'EB_LT_17n4h0-Bec4pKyhOFw'
dto = GetFeedElementsBulkInfo(id='EB_LT_17n4h0-Bec4pKyhOFw')
result_dto = api.get_feed_elements_bulk_info(dto)
print(result_dto)
