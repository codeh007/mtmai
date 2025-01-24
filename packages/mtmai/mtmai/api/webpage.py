import logging

from fastapi import APIRouter

from mtmai.deps import SiteDep
from mtmai.models.webpage import PageMetaAuthor, PageMetaResponse

router = APIRouter()

logger = logging.getLogger()


@router.get("/page_meta", response_model=PageMetaResponse)
async def page_meta(
    *,
    site: SiteDep,
):
    logger.info("current site: %s", site)
    return PageMetaResponse(
        title="test_page_meta",
        description="test_page_meta",
        keywords=["test_page_meta"],
        authors=[PageMetaAuthor(name="test_page_meta", url="test_page_meta")],
        creator="test_page_meta",
        manifest="test_page_meta",
    )
