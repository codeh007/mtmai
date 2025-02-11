import logging
from typing import Annotated, AsyncGenerator

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from sqlmodel import Session
from sqlmodel.ext.asyncio.session import AsyncSession

from mtmai.core.config import HEADER_SITE_HOST, settings
from mtmai.crud.curd_site import get_site_domain
from mtmai.db.db import get_async_engine, get_checkpointer
from mtmai.db.db_manager import DatabaseManager
from mtmai.models.models import User
from mtmai.models.site import Site

logger = logging.getLogger(__name__)


# Global manager instances
# _db_manager: Optional[DatabaseManager] = None
# _websocket_manager: Optional[WebSocketManager] = None
# _team_manager: Optional[TeamManager] = None


reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token",
    auto_error=False,  # 没有 token header 时不触发异常
)


# def get_db() -> Generator[Session, None, None]:
#     with Session(engine) as session:
#         yield session


async def get_db() -> DatabaseManager:
    """Dependency provider for database manager"""
    if not _db_manager:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database manager not initialized",
        )
    return _db_manager


# async def get_websocket_manager() -> WebSocketManager:
#     """Dependency provider for connection manager"""
#     if not _websocket_manager:
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail="Connection manager not initialized",
#         )
#     return _websocket_manager


# async def get_team_manager() -> TeamManager:
#     """Dependency provider for team manager"""
#     if not _team_manager:
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail="Team manager not initialized",
#         )
#     return _team_manager


# Authentication dependency


async def get_current_user(
    # Add your authentication logic here
    # For example: token: str = Depends(oauth2_scheme)
) -> str:
    """
    Dependency for getting the current authenticated user.
    Replace with your actual authentication logic.
    """
    # Implement your user authentication here
    return "user_id"  # Replace with actual user identification


# Manager initialization and cleanup


async def init_managers(database_uri: str, config_dir: str, app_root: str) -> None:
    """Initialize all manager instances"""
    global _db_manager, _websocket_manager, _team_manager

    logger.info("Initializing managers...")

    try:
        # Initialize database manager
        _db_manager = DatabaseManager(engine_uri=database_uri, base_dir=app_root)
        _db_manager.initialize_database(auto_upgrade=settings.UPGRADE_DATABASE)

        # init default team config
        await _db_manager.import_teams_from_directory(
            config_dir, settings.DEFAULT_USER_ID, check_exists=True
        )

        # Initialize connection manager
        # _websocket_manager = WebSocketManager(db_manager=_db_manager)
        # logger.info("Connection manager initialized")

        # Initialize team manager
        _team_manager = TeamManager()
        logger.info("Team manager initialized")

    except Exception as e:
        logger.error(f"Failed to initialize managers: {str(e)}")
        await cleanup_managers()  # Cleanup any partially initialized managers
        raise


async def cleanup_managers() -> None:
    """Cleanup and shutdown all manager instances"""
    global _db_manager, _websocket_manager, _team_manager

    logger.info("Cleaning up managers...")

    # Cleanup connection manager first to ensure all active connections are closed
    if _websocket_manager:
        try:
            await _websocket_manager.cleanup()
        except Exception as e:
            logger.error(f"Error cleaning up connection manager: {str(e)}")
        finally:
            _websocket_manager = None

    # TeamManager doesn't need explicit cleanup since WebSocketManager handles it
    _team_manager = None

    # Cleanup database manager last
    if _db_manager:
        try:
            await _db_manager.close()
        except Exception as e:
            logger.error(f"Error cleaning up database manager: {str(e)}")
        finally:
            _db_manager = None

    logger.info("All managers cleaned up")


# Utility functions for dependency management


def get_manager_status() -> dict:
    """Get the initialization status of all managers"""
    return {
        "database_manager": _db_manager is not None,
        "websocket_manager": _websocket_manager is not None,
        "team_manager": _team_manager is not None,
    }


# Combined dependencies


async def get_managers():
    """Get all managers in one dependency"""
    return {
        "db": await get_db(),
        # "connection": await get_websocket_manager(),
        # "team": await get_team_manager(),
    }


# Error handling for manager operations


class ManagerOperationError(Exception):
    """Custom exception for manager operation errors"""

    def __init__(self, manager_name: str, operation: str, detail: str):
        self.manager_name = manager_name
        self.operation = operation
        self.detail = detail
        super().__init__(f"{manager_name} failed during {operation}: {detail}")


# Dependency for requiring specific managers


def require_managers(*manager_names: str):
    """Decorator to require specific managers for a route"""

    async def dependency():
        status = get_manager_status()
        missing = [name for name in manager_names if not status.get(f"{name}_manager")]
        if missing:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Required managers not available: {', '.join(missing)}",
            )
        return True

    return Depends(dependency)


async def get_asession() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSession(get_async_engine()) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]

AsyncSessionDep = Annotated[AsyncSession, Depends(get_asession)]


TokenDep = Annotated[str, Depends(reusable_oauth2)]


def get_host_from_request(request: Request):
    host = request.headers.get("Host")
    return host


HostDep = Annotated[str, Depends(get_host_from_request)]


# def get_current_user(session: SessionDep, token: TokenDep, request: Request) -> User:
#     token = token or request.cookies.get(settings.COOKIE_ACCESS_TOKEN)
#     try:
#         payload = jwt.decode(
#             token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
#         )
#         token_data = TokenPayload(**payload)
#     except (InvalidTokenError, ValidationError):
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Could not validate credentials",
#         )
#     user = session.get(User, token_data.sub)
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     if not user.is_active:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return user


CurrentUser = Annotated[User, Depends(get_current_user)]


def get_current_active_superuser(current_user: CurrentUser) -> User:
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=403, detail="The user doesn't have enough privileges"
        )
    return current_user


def get_optional_current_user(
    session: SessionDep, token: TokenDep, request: Request
) -> User | None:
    token = token or request.cookies.get(settings.COOKIE_ACCESS_TOKEN)
    if not token:
        return None
    try:
        return get_current_user(session, token, request)
    except HTTPException:
        return None


OptionalUserDep = Annotated[User | None, Depends(get_optional_current_user)]


CheckPointerDep = Annotated[AsyncPostgresSaver, Depends(get_checkpointer)]


async def get_site(session: AsyncSessionDep, request: Request) -> Site:
    """
    根据入站域名获取对应是site 对象
    """
    income_domain = request.headers.get(HEADER_SITE_HOST)
    if not income_domain:
        # 尝试从多个来源获取前端域名
        # 1. 检查反向代理头
        if "X-Forwarded-Host" in request.headers:
            income_domain = request.headers["X-Forwarded-Host"]
        # 2. 检查 Referer 头
        elif "Referer" in request.headers:
            from urllib.parse import urlparse

            referer = request.headers["Referer"]
            income_domain = urlparse(referer).netloc
        # 3. 检查 Origin 头
        elif "Origin" in request.headers:
            from urllib.parse import urlparse

            origin = request.headers["Origin"]
            income_domain = urlparse(origin).netloc
        # 4. 如果以上都失败，使用 Host 头作为后备
        else:
            income_domain = request.headers.get("Host")

    if income_domain:
        site = await get_site_domain(session, income_domain)
        return site
    else:
        raise HTTPException(status_code=400, detail="Unable to determine site domain")


SiteDep = Annotated[Site, Depends(get_site)]
SiteDep = Annotated[Site, Depends(get_site)]
SiteDep = Annotated[Site, Depends(get_site)]
