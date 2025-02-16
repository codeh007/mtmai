import pytest
from dotenv import load_dotenv
from mtmai.hatchet import Hatchet

load_dotenv()


def hatchet_client_fixture():
    @pytest.fixture
    def hatchet():
        return Hatchet(debug=True)

    return hatchet
