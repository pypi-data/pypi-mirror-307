from unittest.mock import patch

import pytest
import requests

from ord_mediascout_client.client import TemporaryAPIError


def test_get_statistics(client):
    with patch('requests.Session.send') as mock_request:
        mock_request.side_effect = requests.exceptions.ConnectionError

        with pytest.raises(TemporaryAPIError):
            client.ping()
