from scraper import NewsScraper
from storage import DataStorage
from config import NEWS_SOURCES, REQUEST_DELAY, MAX_ARTICLES
import sys


def main():

    config = {
        'NEWS_SOURCES': NEWS_SOURCES,
        'REQUEST_DELAY': REQUEST_DELAY,
        'MAX_ARTICLES': MAX_ARTICLES
    }

    print("ЗАПУСК НОВОСТНОГО СКРАППЕРА")
    print(f" Источники: {len(NEWS_SOURCES)} сайтов")
    print(f" Максимум статей с источника: {MAX_ARTICLES}")
    print("-" * 50)

    scraper = NewsScraper(config)
    news_data = scraper.scrape_all()

    if not news_data:
        print("Не удалось получить новости")
        sys.exit(1)

    storage = DataStorage()

    print("\nСОХРАНЕНИЕ ДАННЫХ:")
    print("-" * 50)

    storage.save_json(news_data)
    storage.save_csv(news_data)
    storage.save_excel(news_data)

    storage.print_summary(news_data)

    print("\n Готово!")


if __name__ == "__main__":
    main()