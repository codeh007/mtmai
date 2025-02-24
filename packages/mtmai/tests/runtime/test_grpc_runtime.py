import os

import pytest
from dotenv import load_dotenv

envFileAbsPath = os.path.abspath("../gomtm/env/mtmai.env")
load_dotenv(envFileAbsPath)


@pytest.mark.asyncio
async def test_grpc_runtime():
    print("test_abc")
