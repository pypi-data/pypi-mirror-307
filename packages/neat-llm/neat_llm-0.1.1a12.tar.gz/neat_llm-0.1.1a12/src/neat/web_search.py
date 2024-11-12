# %%
import re
from typing import Any, Dict, List, Optional
from urllib.parse import urlparse

import httpx
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS

from neat import neat

ddgs = DDGS()
region = "wt-wt"
safesearch = "moderate"


@neat.tool()
def search(query: str, max_results: int = 5) -> str:
    """
    Perform a web search using DuckDuckGo and format the results for LLM consumption.

    Args:
        query (str): The search query.
        max_results (int): Maximum number of results to return. Defaults to 5.

    Returns:
        str: A formatted string containing search results.
    """
    results = ddgs.text(
        keywords=query,
        region=region,
        safesearch=safesearch,
        max_results=max_results,
    )
    return _format_web_results(list(results))


def _format_web_results(results: List[Dict[str, str]]) -> str:
    """Format web search results for LLM consumption."""
    formatted_results = []
    for i, result in enumerate(results, 1):
        formatted_result = f"{i}. Title: {result['title']}\n   URL: {result['href']}\n   Summary: {result['body']}\n"
        formatted_results.append(formatted_result)
    return "\n".join(formatted_results)


search(query="What is the capital of France?")
if __name__ == "__main__":
    print(search(query="What is the capital of France?"))

# def image_search(query: str, max_results: int = 5) -> str:
#         """
#         Perform an image search using DuckDuckGo and format the results for LLM consumption.

#         Args:
#             query (str): The search query.
#             max_results (int): Maximum number of results to return. Defaults to 5.

#         Returns:
#             str: A formatted string containing image search results.
#         """
#         results = ddgs.images(
#             keywords=query,
#         region=region,
#         safesearch=safesearch,
#             max_results=max_results,
#         )
#         return _format_image_results(list(results))

# def _format_image_results(results: List[Dict[str, Any]]) -> str:
#         """Format image search results for LLM consumption."""
#         formatted_results = []
#         for i, result in enumerate(results, 1):
#             formatted_result = f"{i}. Title: {result['title']}\n   URL: {result['image']}\n   Source: {result['url']}\n"
#             formatted_results.append(formatted_result)
#         return "\n".join(formatted_results)

# def news_search(query: str, max_results: int = 5, timelimit: Optional[str] = "w") -> str:
#         """
#         Perform a news search using DuckDuckGo and format the results for LLM consumption.

#         Args:
#             query (str): The search query.
#             max_results (int): Maximum number of results to return. Defaults to 5.
#             timelimit (Optional[str]): Time limit for news articles. 'd' for day, 'w' for week, 'm' for month. Defaults to 'w'.

#         Returns:
#             str: A formatted string containing news search results.
#         """
#     results = ddgs.news(
#             keywords=query,
#         region=region,
#         safesearch=safesearch,
#             timelimit=timelimit,
#             max_results=max_results,
#         )
#     return _format_news_results(list(results))

# def _format_news_results(results: List[Dict[str, str]]) -> str:
#         """Format news search results for LLM consumption."""
#         formatted_results = []
#         for i, result in enumerate(results, 1):
#             formatted_result = f"{i}. Title: {result['title']}\n   Date: {result['date']}\n   URL: {result['url']}\n   Excerpt: {result['body']}\n"
#             formatted_results.append(formatted_result)
#         return "\n".join(formatted_results)

# def translate(text: str, to_lang: str = "en") -> str:
#     """
#     Translate text using DuckDuckGo's translation service.

#     Args:
#         text (str): The text to translate.
#         to_lang (str): The target language code. Defaults to 'en' for English.

#     Returns:
#         str: The translated text with original and detected language information.
#     """
#     result = ddgs.translate(keywords=text, to=to_lang)
#     if result:
#         return _format_translation_result(result[0])
#     return "Translation failed."

# def _format_translation_result(result: Dict[str, str]) -> str:
#     """Format translation result for LLM consumption."""
#     return f"Original ({result['detected_language']}): {result['original']}\nTranslated ({result['to']}): {result['translated']}"

# def get_suggestions(query: str) -> str:
#     """
#     Get search suggestions for a given query and format them for LLM consumption.

#     Args:
#         query (str): The query to get suggestions for.

#     Returns:
#         str: A formatted string containing search suggestions.
#     """
#     results = ddgs.suggestions(keywords=query, region=region)
#     return _format_suggestions(results)

# def _format_suggestions(results: List[Dict[str, str]]) -> str:
#     """Format search suggestions for LLM consumption."""
#     suggestions = [result["phrase"] for result in results]
#     return f"Suggestions for '{results[0]['phrase']}':\n" + "\n".join(
#         f"- {suggestion}" for suggestion in suggestions[1:]
#     )

# def find_answers(query: str) -> str:
#     """
#     Find instant answers for a given query and format them for LLM consumption.

#     Args:
#         query (str): The query to find answers for.

#     Returns:
#         str: A formatted string containing instant answers.
#     """
#     results = ddgs.answers(keywords=query)
#     return _format_answers(results)

# def _format_answers(results: List[Dict[str, Optional[str]]]) -> str:
#     """Format instant answers for LLM consumption."""
#     if not results:
#         return "No instant answers found."

#     formatted_answers = []
#     for i, answer in enumerate(results, 1):
#         formatted_answer = f"{i}. Topic: {answer['topic'] or 'N/A'}\n   Text: {answer['text']}\n   URL: {answer['url'] or 'N/A'}\n"
#         formatted_answers.append(formatted_answer)
#     return "\n".join(formatted_answers)

# def location_search(query: str, place: str, max_results: int = 5) -> str:
#     """
#     Perform a location-based search using DuckDuckGo Maps and format the results for LLM consumption.

#     Args:
#         query (str): The search query.
#         place (str): The location to search in.
#         max_results (int): Maximum number of results to return. Defaults to 5.

#     Returns:
#         str: A formatted string containing location search results.
#     """
#     results = ddgs.maps(keywords=query, place=place, max_results=max_results)
#     return _format_location_results(list(results))

# def _format_location_results(results: List[Dict[str, Union[str, float, None]]]) -> str:
#     """Format location search results for LLM consumption."""
#     if not results:
#         return f"No results found for the location search."

#     formatted_results = []
#     for i, result in enumerate(results, 1):
#         formatted_result = (
#             f"{i}. Name: {result['title']}\n"
#             f"   Address: {result['address']}\n"
#             f"   Coordinates: ({result['latitude']}, {result['longitude']})\n"
#             f"   Phone: {result['phone'] or 'N/A'}\n"
#             f"   Category: {result['category'] or 'N/A'}\n"
#         )
#         formatted_results.append(formatted_result)
#     return "\n".join(formatted_results)

# def summarize_web_content(url: str, max_length: int = 500) -> str:
#     """
#     Fetch and summarize web content from a given URL.

#     Args:
#         url (str): The URL of the web page to summarize.
#         max_length (int): Maximum length of the summary. Defaults to 500 characters.

#     Returns:
#         str: A summary of the web content.
#     """
#     # Note: This is a placeholder implementation. In a real-world scenario,
#     # you would need to implement web scraping and text summarization.
#     # This could involve using libraries like 'requests' for fetching content
#     # and implementing or using a summarization algorithm.
#     return f"Summary of content from {url} (max {max_length} characters)"

# def format_for_llm(data: Any) -> str:
#     """
#     Format any data type into a string representation suitable for LLM consumption.

#     Args:
#         data (Any): The data to format.

#     Returns:
#         str: A formatted string representation of the data.
#     """
#     if isinstance(data, (str, int, float, bool)):
#         return str(data)
#     elif isinstance(data, (list, tuple)):
#         return "\n".join(f"- {format_for_llm(item)}" for item in data)
#     elif isinstance(data, dict):
#         return "\n".join(
#             f"{key}: {format_for_llm(value)}" for key, value in data.items()
#         )
#     else:
#         return json.dumps(data, default=str, indent=2)


class ArticleFetcher:
    def __init__(self, timeout: int = 10, headers: Optional[Dict[str, str]] = None):
        """
        Initialize the ArticleFetcher.

        Args:
            timeout (int): Request timeout in seconds. Defaults to 10.
            headers (Optional[Dict[str, str]]): Custom headers for requests. Defaults to None.
        """
        self.timeout = timeout
        self.headers = headers or {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

    @neat.tool()
    async def fetch_article(self, url: str) -> str:
        """
        Fetch and parse an article from the given URL.

        Args:
            url (str): The URL of the article to fetch.

        Returns:
            Dict[str, Any]: A dictionary containing the parsed article data.
        """
        try:
            async with httpx.AsyncClient(headers=self.headers) as client:
                response = await client.get(url)
                response.raise_for_status()

                soup = BeautifulSoup(response.text, "html.parser")

                return self.format_for_llm(
                    {
                        "url": url,
                        "title": self._extract_title(soup),
                        "content": self._extract_content(soup),
                        "summary": self._generate_summary(self._extract_content(soup)),
                        "domain": self._extract_domain(url),
                    }
                )
        except httpx.HTTPStatusError as e:
            return {"error": f"HTTP error occurred: {e}"}
        except httpx.RequestError as e:
            return {"error": f"An error occurred while requesting {url}: {e}"}
        except Exception as e:
            return {"error": f"An unexpected error occurred: {e}"}

    def _extract_title(self, soup: BeautifulSoup) -> str:
        """Extract the title of the article."""
        title = soup.find("h1")
        return title.text.strip() if title else "No title found"

    def _extract_content(self, soup: BeautifulSoup) -> str:
        """Extract the main content of the article."""
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()

        # Find the main content (this is a simplified approach and may need adjustment for different sites)
        main_content = (
            soup.find("article")
            or soup.find("main")
            or soup.find("div", class_="content")
        )

        if main_content:
            paragraphs = main_content.find_all("p")
            content = " ".join(p.text for p in paragraphs)
        else:
            content = soup.get_text()

        return self._clean_text(content)

    def _clean_text(self, text: str) -> str:
        """Clean the extracted text."""
        # Remove extra whitespace
        text = re.sub(r"\s+", " ", text).strip()
        # Remove special characters
        text = re.sub(r"[^\w\s.,!?-]", "", text)
        return text

    def _generate_summary(self, content: str, max_length: int = 200) -> str:
        """Generate a simple summary of the content."""
        # This is a very basic summary generation. For better results, consider using
        # more advanced NLP techniques or a dedicated summarization library.
        sentences = content.split(".")
        summary = ""
        # for sentence in sentences:
        #     if len(summary) + len(sentence) > max_length:
        #         break
        #     summary += sentence + "."
        return summary.strip()

    def _extract_domain(self, url: str) -> str:
        """Extract the domain from the URL."""
        parsed_uri = urlparse(url)
        return "{uri.netloc}".format(uri=parsed_uri)

    def format_for_llm(self, article_data: Dict[str, Any]) -> str:
        """
        Format the article data for LLM consumption.

        Args:
            article_data (Dict[str, Any]): The article data to format.

        Returns:
            str: A formatted string representation of the article data.
        """
        if "error" in article_data:
            return f"Error fetching article: {article_data['error']}"

        formatted_data = f"Title: {article_data['title']}\n"
        formatted_data += f"URL: {article_data['url']}\n"
        formatted_data += f"Domain: {article_data['domain']}\n"
        formatted_data += f"Summary: {article_data['summary']}\n\n"
        formatted_data += (
            f"Content: {article_data['content']}..."  # Truncate content for brevity
        )

        return formatted_data
