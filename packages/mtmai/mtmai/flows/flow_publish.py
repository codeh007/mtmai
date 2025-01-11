from prefect import get_run_logger, task

from mtmai.models.book_gen import (
    GenBookState,
)


@task()
async def publish_article(
    site_id: str,
    state: GenBookState,
):
    """
    本地博客发布
    """

    logger = get_run_logger()
    logger.info("本地博客发布")
    book_content = ""
    for chapter in state.book:
        # Add the chapter title as an H1 heading
        book_content += f"# {chapter.title}\n\n"
        # Add the chapter content
        book_content += f"{chapter.content}\n\n"

    # The title of the book from self.state.title
    book_title = state.title

    logger.info("文章生成完成, 开始发布")
    filename = (
        f"./{book_title.replace(' ', '_').replace("'", '_').replace('"', '_')}.md"
    )

    logger.info("Book saved as %s", filename)
