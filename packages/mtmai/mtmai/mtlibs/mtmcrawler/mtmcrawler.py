"""
爬虫主要的功能
"""

from pydantic import BaseModel, Field

from mtmai.core.logging import get_logger

logger = get_logger()


async def _fetch_page_html(url: str):
    """
    爬取指定页面
    """
    import httpx

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            response.raise_for_status()
            return response.text
        except httpx.HTTPError as e:
            logger.error(f"HTTP error occurred: {e}")
            return None
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            return None


class MTCrawlerPageParams(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    site_id: str
    url: str
    current_depth: int = Field(default=0, ge=0, le=6)


# async def crawl_page(db: Session, params: MTCrawlerPageParams):
#     """
#     爬取一个页面并建立页面索引
#     """
#     logger.info(f"crawl_page: {params.url}")
#     html = await _fetch_page_html(params.url)
#     if html is None:
#         return None
#     logger.info(f"crawl_page: {len(html)}")

#     page_item = MTCrawlPage(
#         site_id=params.site_id,
#         url=params.url,
#         depth=params.current_depth,
#         title="",
#         description="",
#         keywords="",
#         author="fake_author",
#         copyright="fake_copyright",
#     )
#     db.add(page_item)
#     db.commit()
#     return page_item


class MTMCrawlerSiteParams(BaseModel):
    site_id: str
    entry_urls: list[str]
    # 最大爬取数量
    fetched_limit_count: int = Field(default=1000, ge=0)
    # 深度限制
    depth_limit: int = Field(default=3, ge=0, le=6)


class MTMCrawlerSiteContext(BaseModel):
    """单个爬虫运行上下文"""

    site_id: str

    # 已爬取页面数量
    fetched_count: int


# async def crawl_site(db: Session, params: MTMCrawlerSiteParams):
#     """
#     爬取一个站点并建立页面索引
#     """
#     logger.info(f"crawl_site: {params.entry_urls}")
#     context = MTMCrawlerSiteContext(site_id=params.site_id, fetched_count=0)

#     # 爬取入口页面
#     for url in params.entry_urls:
#         html = await crawl_page(
#             db, MTCrawlerPageParams(site_id=params.site_id, url=url, current_depth=0)
#         )
#         if html is None:
#             continue
