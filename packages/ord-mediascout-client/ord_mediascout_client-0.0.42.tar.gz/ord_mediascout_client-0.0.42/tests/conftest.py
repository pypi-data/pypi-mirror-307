import logging
import random
import time

import pytest

from ord_mediascout_client import CreatePlatformRequest, ORDMediascoutClient, ORDMediascoutConfig, PlatformType

logging.getLogger('faker').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)


@pytest.fixture
def client():
    config = ORDMediascoutConfig()
    return ORDMediascoutClient(config)


@pytest.fixture(scope='session', autouse=True)
def faker_session_locale():
    return ['ru_RU']


@pytest.fixture(scope='session', autouse=True)
def faker_seed():
    return int(time.time())


@pytest.fixture
def create_platform_data():
    def _create_platform_data(**kwargs):
        rnd = random.randrange(111, 999)
        data = {
            'name': f'Test Platform {rnd}',
            'type': PlatformType.Site,
            'url': f'https://www.testplatform{rnd}.ru/',
            'isOwner': False,
        }
        data.update(kwargs)
        return CreatePlatformRequest(**data)

    return _create_platform_data
