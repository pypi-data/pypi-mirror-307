from unittest.mock import patch

import pytest
import requests

from ord_mediascout_client.client import TemporaryAPIError


def test__temporary_error_raised_when_connection_error_occurs(client):
    with patch('requests.Session.send') as mock_request:
        mock_request.side_effect = requests.exceptions.ConnectionError

        with pytest.raises(TemporaryAPIError):
            client.ping()
