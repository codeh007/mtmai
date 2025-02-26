import pytest_asyncio

from mtmai import loader
from mtmai.core.config import settings
from mtmai.hatchet import Hatchet


@pytest_asyncio.fixture(scope="session")
async def mtmapp():
    """Session-wide mtmapp fixture"""
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
