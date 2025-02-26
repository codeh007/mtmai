# import os

import pytest

# from dotenv import load_dotenv

# envFileAbsPath = os.path.abspath("../gomtm/env/mtmai.env")
# load_dotenv(envFileAbsPath)
# gomtm_host_addr = "http://localhost:8383"


@pytest.mark.asyncio
async def test_example(mtmapp) -> None:
    print("Worker started")
    assert mtmapp is not None
    print(f"Mtmapp instance: {mtmapp}")
