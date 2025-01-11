import httpx
from bs4 import BeautifulSoup


async def get_readable_text(url: str) -> str:
    """获取 AI 可读文本"""
    try:
        response = httpx.get(url)
        response.raise_for_status()  # Raises a HTTPError if the status is 4xx, 5xx

        # Parse the webpage with BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")

        # Define the tags to be removed
        tags = [
            "a",
            "img",
            "script",
            "style",
            "svg",
            "iframe",
            "canvas",
            "video",
            "audio",
            "map",
            "noscript",
        ]

        # Remove each defined tag
        for tag in tags:
            for item in soup.find_all(tag):
                item.decompose()

        # Extract text from the parsed HTML
        text = soup.get_text()

        # Remove extra whitespace
        text = " ".join(text.split())
        # completion = self.anthropic.completions.create(
        #     model="claude-2",
        #     max_tokens_to_sample=1000000,
        #     prompt=f"{HUMAN_PROMPT} Please provide a exhaustive and concise summary of the following (formatted nicely in markdown): {text} {AI_PROMPT}",
        #     stream=False,
        # )
        # return completion.completion
        return text
    except httpx.HTTPError as e:
        return f"A HTTP error occurred: {str(e)}"
    except httpx.RequestException as e:
        return f"A request exception occurred: {str(e)}"
    except Exception as e:
        return f"An error occurred: {str(e)}"

    except Exception as e:
        raise e
