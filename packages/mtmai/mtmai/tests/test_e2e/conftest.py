from unittest.mock import patch

import pytest
import pytest_asyncio
from mtmai import loader
from mtmai.core.config import settings
from mtmai.hatchet import Hatchet


@pytest.fixture(scope="session")
def mock_config():
    """模拟配置对象"""
    a = loader.CredentialsData(username="test", password="test")
    return a


@pytest_asyncio.fixture(scope="session")
async def mtmapp(mock_config):
    """Session-wide mtmapp fixture"""

    with patch("mtmai.loader.ClientConfig.load_credentials") as mock_load:
        mock_load.return_value = mock_config
        app = Hatchet.from_config(
            loader.ConfigLoader().load_client_config(
                loader.ClientConfig(
                    server_url=settings.GOMTM_URL,
                )
            ),
            debug=True,
        )
        await app.boot()
        print("app boot 完成")
        yield app
        # Cleanup after all tests
        await app.shutdown()
