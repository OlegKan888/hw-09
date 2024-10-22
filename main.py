import requests
from bs4 import BeautifulSoup
import json


# Функція для отримання цитат з кожної сторінки
def get_quotes(url):
    quotes = []
    authors = {}
    while url:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        # Отримуємо всі цитати
        for quote in soup.select(".quote"):
            text = quote.select_one(".text").get_text()
            author = quote.select_one(".author").get_text()
            tags = [tag.get_text() for tag in quote.select(".tag")]

            quotes.append({"text": text, "author": author, "tags": tags})

            # Отримуємо деталі автора, якщо їх ще немає в авторів
            if author not in authors:
                author_url = quote.select_one("a")["href"]
                author_info = get_author_details(
                    f"http://quotes.toscrape.com{author_url}"
                )
                authors[author] = author_info

        # Переходимо на наступну сторінку
        next_page = soup.select_one(".next a")
        url = f"http://quotes.toscrape.com{next_page['href']}" if next_page else None

    return quotes, authors


# Функція для отримання деталей автора
def get_author_details(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    author_details = {
        "name": soup.select_one(".author-title").get_text(),
        "birth_date": soup.select_one(".author-born-date").get_text(),
        "birth_place": soup.select_one(".author-born-location").get_text(),
        "description": soup.select_one(".author-description").get_text().strip(),
    }
    return author_details


# Запуск скрапінгу
quotes, authors = get_quotes("http://quotes.toscrape.com")

# Збереження даних у файли JSON
with open("quotes.json", "w") as f:
    json.dump(quotes, f, indent=4)

with open("authors.json", "w") as f:
    json.dump(authors, f, indent=4)

print("Дані збережені у файли quotes.json та authors.json")
