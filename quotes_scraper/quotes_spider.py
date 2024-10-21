import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = ["http://quotes.toscrape.com/"]
    
    def parse(self, response):
        for quote in response.css("div.quotes"):
            yield {
                "text": quote.css("span.text::text").get(),
                "author": quote.css("span small::text").get(),
                "tags": quote.css("div.tags a.tag::text").getall(),
            }

            # Отримуємо посилання на автора і викликаємо парсинг автора
            author_url = quote.css("span a::attr(href)").get()
            yield response.follow(author_url, self.parse_author)

        # Переходимо на наступну сторінку
        next_page = response.css("li.next a::attr(href)").get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
    
    def parse_author(self, response):
        # Парсимо дані про автора
        yield {
            "name": response.css("h3.author-title::text").get().strip(),
            "birthdate": response.css("span.author-born-date::text").get(),
            "bio": response.css("div.author-description::text").get().strip(),
        }
