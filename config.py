HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

NEWS_SOURCES = [
    {
        'name': 'BBC News',
        'url': 'https://www.bbc.com/news',
        'article_selector': 'article',
        'title_selector': 'h3',
        'link_selector': 'a',
        'summary_selector': 'p'
    },
    {
        'name': 'CNN',
        'url': 'https://edition.cnn.com',
        'article_selector': '.container__item',
        'title_selector': '.container__headline',
        'link_selector': 'a',
        'summary_selector': '.container__description'
    }
]

REQUEST_DELAY = 1
MAX_ARTICLES = 20