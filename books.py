import scrapy


class BooksSpider(scrapy.Spider):
    name = "books"

    def start_requests(self):
        urls = [
            'http://books.toscrape.com/'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        for q in response.css("article.product_pod"):
            image_url= q.css("div.image_container img::attr(src)").get()
            book_title = q.css("h3 a::attr(title)").get()
            price= q.css("p.price_color::text").get()
            yield {
                'image_url': image_url,
                'book_title':book_title,
                'price':price,
            }
        
        next_page= response.css("li.next a::attr(href)").get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(url=next_page,callback=self.parse)
