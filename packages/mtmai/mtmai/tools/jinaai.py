import requests
from mtmai.core.config import settings
from smolagents import tool

headers = {"Authorization": "Bearer " + settings.JINA_API_KEY}


@tool
def scrape_page_with_jina_ai(url: str) -> str:
    """Scrapes content from a webpage using Jina AI's web scraping service.

    Args:
        url: The URL of the webpage to scrape. Must be a valid web address to extract content from.

    Returns:
        str: The scraped content in markdown format.
    """
    print(f"Scraping Jina AI..: {url}")
    # response = requests.get("https://r.jina.ai/" + url, headers=headers)
    response = requests.get("https://r.jina.ai/" + url)

    markdown_content = response.text

    return markdown_content


@tool
def search_facts_with_jina_ai(query: str) -> str:
    """Searches for facts and information using Jina AI's search service.

    Args:
        query: The search query string used to find relevant facts and information.

    Returns:
        str: The search results in markdown format containing relevant facts and information.
    """
    print(f"Searching Jina AI..: {query}")
    # response = requests.get("https://s.jina.ai/" + query, headers=headers)
    response = requests.get("https://s.jina.ai/" + query)
    markdown_content = response.text

    return markdown_content
