from unittest.mock import patch

import pytest
import pytest_asyncio
from mtmai import loader
from mtmai.core.config import settings
from mtmai.hatchet import Hatchet


@pytest.fixture(scope="session")
def mock_config():
    """模拟配置对象"""
    a = loader.CredentialsData(username="admin@example.com", password="Admin123!!")
    return a


@pytest_asyncio.fixture(scope="session")
async def mtmapp(mock_config):
    """Session-wide mtmapp fixture"""

    with patch(
        "mtmai.loader.ConfigLoader.load_credentials", autospec=True
    ) as mock_load:
        mock_load.return_value = mock_config
        config_loader = loader.ConfigLoader()

        loaded_config = config_loader.load_client_config(
            loader.ClientConfig(server_url=settings.GOMTM_URL)
        )
        assert loaded_config.credentials.username == "admin@example.com"
        app = Hatchet.from_config(loaded_config, debug=True)
        await app.boot()
        print("app boot 完成")
        yield app
        await app.shutdown()
