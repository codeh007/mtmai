from typing import List

from pydantic import BaseModel


class ChapterOutline(BaseModel):
    title: str
    description: str


class BookOutline(BaseModel):
    chapters: List[ChapterOutline]


class Chapter(BaseModel):
    title: str
    content: str


class WriteOutlineRequest(BaseModel):
    """参数: 生成文章大纲"""

    topic: str
    goal: str


class WriteSingleChapterRequest(BaseModel):
    """参数: 生成文章一个章节"""

    goal: str
    topic: str
    chapter_title: str
    chapter_description: str
    book_outlines: list[ChapterOutline]


class GenBookState(BaseModel):
    title: str | None = (
        "The Current State of AI in September 2024: Trends Across Industries and What's Next"
    )
    book: list[Chapter] | None = []
    book_outline: list[ChapterOutline] | None = []
    topic: str | None = (
        "Exploring the latest trends in AI across different industries as of September 2024"
    )
    goal: str | None = """
        The goal of this book is to provide a comprehensive overview of the current state of artificial intelligence in September 2024.
        It will delve into the latest trends impacting various industries, analyze significant advancements,
        and discuss potential future developments. The book aims to inform readers about cutting-edge AI technologies
        and prepare them for upcoming innovations in the field.
    """


# class BlogState(BaseModel):
#     description: str = Field(description="博客功能定位介绍")
#     seo_keywords: str = Field(description="SEO关键词列表")
#     day_published_count: int = Field(description="已完成的日更数量")
#     day_publish_count_hint: int = Field(description="建议日更数量")


# class BlogDescription(BaseModel):
#     """博客网站描述"""

#     description: str
