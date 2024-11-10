from unittest.mock import patch

import pytest
from pydantic import ValidationError

from ord_mediascout_client.client import BadResponseError, TemporaryResponseError, UnexpectedResponseError


def test__requests__200_ok(client, create_platform_data):
    platform = create_platform_data()

    with patch('requests.Session.send') as mock_post:
        mock_post.return_value.status_code = 201
        mock_post.return_value.text = '{"id": "string"}'

        response = client.create_platform(platform)

    assert response.id == 'string'


def test__requests__400_bad_request(client, create_platform_data):
    platform = create_platform_data()

    with patch('requests.Session.send') as mock_post:
        mock_post.return_value.status_code = 400
        mock_post.return_value.text = '''{
          "errorType": "errorType_string",
          "errorItems": [
            {
              "propertyName": "string",
              "errorMessage": "string",
              "attemptedValue": "string",
              "customState": "string",
              "severity": "Error",
              "errorCode": "string",
              "formattedMessagePlaceholderValues": {
                "additionalProp1": "string",
                "additionalProp2": "string",
                "additionalProp3": "string"
              }
            }
          ]
        }'''

        with pytest.raises(BadResponseError) as exc_info:
            client.create_platform(platform)

        e = exc_info.value
        assert e.error.errorType == 'errorType_string'
        assert len(e.error.errorItems) == 1
        assert e.error.errorItems[0].propertyName == 'string'


def test__requests__400_problem_detail(client, create_platform_data):
    platform = create_platform_data()

    with patch('requests.Session.send') as mock_post:
        mock_post.return_value.status_code = 400
        mock_post.return_value.text = '''{
                "type": "https://lk.mediascout.ru/ru/400/",
                "title": "Ошибка валидации данных запроса.",
                "status": 400,
                "detail": "Форма распространения креатива/контейнера [Иное] не поддерживается, начиная с ЕРИР v.5",
                "traceId": "052cd6ff4f605a15c086c2cd65b3ae46"
            }'''

        with pytest.raises(BadResponseError) as exc_info:
            client.create_platform(platform)

        e = exc_info.value
        assert e.response.status_code == 400
        assert isinstance(e.__cause__, ValidationError)
        assert len(e.error.errorItems) == 1
        assert e.error.errorType == 'https://lk.mediascout.ru/ru/400/'
        assert e.error.errorItems[0].propertyName is None
        assert (
            e.error.errorItems[0].errorMessage
            == 'Форма распространения креатива/контейнера [Иное] не поддерживается, начиная с ЕРИР v.5'
        )


def test__requests__400_unexpected_response(client, create_platform_data):
    platform = create_platform_data()

    with patch('requests.Session.send') as mock_post:
        mock_post.return_value.status_code = 400
        mock_post.return_value.text = '''{
          "errorType": "errorType_string",
        }'''

        with pytest.raises(UnexpectedResponseError) as exc_info:
            client.create_platform(platform)

        e = exc_info.value
        assert e.response.status_code == 400
        assert isinstance(e.__cause__, ValidationError)


def test__requests__500_internal_error(client, create_platform_data):
    platform = create_platform_data()

    with patch('requests.Session.send') as mock_post:
        mock_post.return_value.status_code = 500
        mock_post.return_value.text = '''bla-bla-bla'''

        with pytest.raises(TemporaryResponseError) as exc_info:
            client.create_platform(platform)

        e = exc_info.value
        assert e.response.status_code == 500
        assert e.response.text == mock_post.return_value.text


def test__requests__502_bad_gateway(client, create_platform_data):
    platform = create_platform_data()

    with patch('requests.Session.send') as mock_post:
        mock_post.return_value.status_code = 502
        mock_post.return_value.text = '''bla-bla-2'''

        with pytest.raises(TemporaryResponseError) as exc_info:
            client.create_platform(platform)

        e = exc_info.value
        assert e.response.status_code == 502
        assert e.response.text == mock_post.return_value.text
