import requests
import time
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from fake_useragent import UserAgent
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NewsScraper:

    def __init__(self, config):
        self.config = config
        self.ua = UserAgent()

    def get_page(self, url):
        try:
            headers = {'User-Agent': self.ua.random}
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'lxml')
        except requests.RequestException as e:
            logger.error(f"Ошибка при загрузке {url}: {e}")
            return None

    def scrape_bbc(self, soup, base_url):
        articles = []

        for article in soup.find_all('article', limit=self.config['MAX_ARTICLES']):
            try:
                title_elem = article.find('h3') or article.find('h2')
                title = title_elem.get_text(strip=True) if title_elem else "Нет заголовка"

                link_elem = article.find('a')
                link = urljoin(base_url, link_elem.get('href')) if link_elem else ""

                summary_elem = article.find('p')
                summary = summary_elem.get_text(strip=True) if summary_elem else ""

                if title and link:
                    articles.append({
                        'title': title,
                        'link': link,
                        'summary': summary[:200],
                        'source': 'BBC News'
                    })

            except Exception as e:
                logger.error(f"Ошибка парсинга статьи: {e}")
                continue

        return articles

    def scrape_cnn(self, soup, base_url):
        articles = []

        containers = soup.select('.container__item') or soup.find_all('div', class_='card')

        for container in containers[:self.config['MAX_ARTICLES']]:
            try:
                title_elem = (container.find('h3', class_='container__headline') or
                              container.find('h1') or container.find('h2'))
                title = title_elem.get_text(strip=True) if title_elem else "Нет заголовка"

                link_elem = container.find('a')
                link = urljoin(base_url, link_elem.get('href')) if link_elem else ""

                summary_elem = container.find('p', class_='container__description')
                summary = summary_elem.get_text(strip=True) if summary_elem else ""

                if title and link:
                    articles.append({
                        'title': title,
                        'link': link,
                        'summary': summary[:200],
                        'source': 'CNN'
                    })

            except Exception as e:
                logger.error(f"Ошибка парсинга статьи CNN: {e}")
                continue

        return articles

    def scrape_generic(self, soup, config):
        articles = []

        articles_elements = soup.select(config['article_selector'])

        for article in articles_elements[:self.config['MAX_ARTICLES']]:
            try:
                title_elem = article.select_one(config['title_selector'])
                link_elem = article.select_one(config['link_selector'])

                title = title_elem.get_text(strip=True) if title_elem else "Нет заголовка"
                link = urljoin(config['url'], link_elem.get('href')) if link_elem else ""

                summary = ""
                if config.get('summary_selector'):
                    summary_elem = article.select_one(config['summary_selector'])
                    summary = summary_elem.get_text(strip=True) if summary_elem else ""

                if title and link:
                    articles.append({
                        'title': title,
                        'link': link,
                        'summary': summary[:200],
                        'source': config['name']
                    })

            except Exception as e:
                logger.error(f"Ошибка парсинга: {e}")
                continue

        return articles

    def scrape_all(self):
        all_news = []

        for source in self.config['NEWS_SOURCES']:
            logger.info(f"Скраппинг {source['name']}...")

            soup = self.get_page(source['url'])
            if not soup:
                continue

            if source['name'] == 'BBC News':
                articles = self.scrape_bbc(soup, source['url'])
            elif source['name'] == 'CNN':
                articles = self.scrape_cnn(soup, source['url'])
            else:
                articles = self.scrape_generic(soup, source)

            all_news.extend(articles)
            logger.info(f"Найдено {len(articles)} статей на {source['name']}")

            time.sleep(self.config['REQUEST_DELAY'])

        return all_news
