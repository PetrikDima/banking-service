import requests
from bs4 import BeautifulSoup, ResultSet, PageElement, Tag, NavigableString
from typing import List, Dict, Set


class FinanceNewsScraper:
    """Class for scraping financial news from a given website."""

    BASE_URL = "https://finance.yahoo.com"

    def __init__(self, base_url: str = None):
        self._base_url = base_url or self.BASE_URL
        self._headers = {
            'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                           'AppleWebKit/537.36 (KHTML, like Gecko) '
                           'Chrome/91.0.4472.124 Safari/537.36')
        }
        self._seen_links: Set[str] = set()
        self._finance_news: List[Dict[str, str]] = []

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(base_url='{self._base_url}')"

    def __len__(self) -> int:
        return len(self._finance_news)

    def _send_request(self) -> requests.Response:
        """Send request and return response."""
        response = requests.get(self._base_url, headers=self._headers)
        response.raise_for_status()
        return response

    @staticmethod
    def _parse_html(html: str) -> ResultSet[PageElement | Tag | NavigableString]:
        """Parse HTML and return list of article elements."""
        soup = BeautifulSoup(html, 'html.parser')
        return soup.find_all('a', href=True)

    @staticmethod
    def _is_relevant_news(title: str, link: str) -> bool:
        """Check if the news article is relevant to finance."""
        relevant_keywords = {'invest', 'stock', 'market', 'economy', 'inflation', 'finance'}
        return any(keyword in title.lower() for keyword in relevant_keywords) and ('news' in link or 'story' in link)

    def _get_unique_news(self, articles: ResultSet[PageElement | Tag | NavigableString]) -> None:
        """Extract unique financial news articles."""
        for article in articles:
            title = article.get_text(strip=True)
            link = article['href']
            if not link.startswith('http'):
                link = f'{self.BASE_URL}{link}'

            if self._is_relevant_news(title, link) and link not in self._seen_links:
                self._seen_links.add(link)
                self._finance_news.append({'title': title, 'url': link})

    def scrape_news(self) -> None:
        """Main method for scraping news."""
        try:
            response = self._send_request()
            articles = self._parse_html(response.text)
            self._get_unique_news(articles)
        except requests.RequestException as e:
            print(f"Error fetching news: {e}")

    def display_news(self) -> None:
        """Print scraped news articles."""
        if self._finance_news:
            for item in self._finance_news:
                print(f"Title: {item['title']}")
                print(f"URL: {item['url']}")
        else:
            print("No finance news found.")

    def __iter__(self):
        """Make the scraper iterable."""
        return iter(self._finance_news)

    def __getitem__(self, index: int) -> Dict[str, str]:
        """Allow indexing into the news list."""
        return self._finance_news[index]

    def clear(self) -> None:
        """Reset stored news and seen links."""
        self._finance_news.clear()
        self._seen_links.clear()


if __name__ == "__main__":
    scraper = FinanceNewsScraper()
    scraper.scrape_news()
    scraper.display_news()
    print(f"Total articles scraped: {len(scraper)}")
