from mtmai.core.config import settings
from mtmai.hatchet import Hatchet
from mtmai.services.gomtm_db_session_service import GomtmDatabaseSessionService


class MtmEngine:
    def get_session(self):
        if not hasattr(self, "_session_service"):
            self._session_service = GomtmDatabaseSessionService(
                db_url=settings.MTM_DATABASE_URL
            )
        return self._session_service


mtm_engine = MtmEngine()

mtmapp = Hatchet()
