# RezkaScraper

RezkaScraper — это библиотека на Python для асинхронного поиска контента (аниме, фильмов, сериалов и мультфильмов) на сайте Rezka.ag.

## Возможности:
- Поиск по названию: Выполняет поиск по ключевому слову и возвращает первое совпадение.
- Поиск по категориям: Поддержка категорий аниме, фильмы, сериалы, мультфильмы с пагинацией.

## Установка:
```
pip install rezka_scraper
```

## Пример использование:
```
import asyncio
from rezka_scraper import RezkaScraper

async def main():
    scraper = RezkaScraper()

    # Поиск по названию
    title, link = await scraper.search_rezka("Наруто")
    if title:
        print(f"Найдено: {title} - {link}")
    else:
        print("Ничего не найдено по запросу.")

    # Поиск аниме
    anime_results = await scraper.search_anime(page=1)
    print("Аниме на первой странице:")
    for title, link in anime_results:
        print(f"{title} - {link}")

    # Поиск фильмов
    movies_results = await scraper.search_movies(page=1)
    print("Фильмы на первой странице:")
    for title, link in movies_results:
        print(f"{title} - {link}")

asyncio.run(main())
```

## Примечания:
Для работы необходим стабильный интернет для выполнения запросов к сайту Rezka.ag.

Библиотека использует aiohttp для асинхронных HTTP-запросов и BeautifulSoup для парсинга HTML-контента.

## Как связаться со мной:
[![Telegram Badge](https://img.shields.io/badge/Contact-blue?style=flat&logo=telegram&logoColor=white)](https://t.me/OFFpolice) [![Telegram Badge](https://img.shields.io/badge/Channel-blue?style=flat&logo=telegram&logoColor=white)](https://t.me/OFFpolice2069) [![Twitter Badge](https://img.shields.io/twitter/follow/:OFFpolice2077)](https://x.com/OFFpolice2077) [![Instagram Badge](https://img.shields.io/badge/-Instagram-E4405F?style=flat&logo=instagram&logoColor=white)](https://www.instagram.com/offpolice2077)

## Лицензия:
Этот проект лицензируется по лицензии «MIT License» - более подробную информацию смотрите в файле [LICENSE](LICENSE).