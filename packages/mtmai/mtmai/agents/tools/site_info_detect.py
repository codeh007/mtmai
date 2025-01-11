import httpx
from bs4 import BeautifulSoup
from pydantic import BaseModel


class SiteDetectInfo(BaseModel):
    title: str | None = None
    description: str | None = None


async def site_info_detect(url: str):
    """获取远程站点基本信息"""
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)

    soup = BeautifulSoup(resp.text, "html.parser")
    title = soup.title.string if soup.title else None
    meta_description = soup.find("meta", attrs={"name": "description"})
    description = meta_description["content"] if meta_description else None
    if description:
        description = description[:100]
    return SiteDetectInfo(title=title, description=description)
