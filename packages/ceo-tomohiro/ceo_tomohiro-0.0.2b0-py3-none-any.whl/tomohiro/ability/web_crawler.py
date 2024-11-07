from duckduckgo_search import DDGS


def search_internet(keywords: str) -> str:
    """
        What does this function do: Searches the internet and returns the results.

        When to use this function: Use this function when you don't clearly know about something.

        Args:
            keywords (str): A string representing the search query.

        Returns:
            list: A list of search results as text.
    """
    with DDGS() as search:
        return str(search.text(keywords, region='wt-wt', safesearch='off', backend='api', max_results=20))
