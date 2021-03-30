import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BooksSpider(CrawlSpider):
    name = 'books'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com']

    rules = (
        Rule(LinkExtractor(restrict_xpaths=("//ol[@class='row']/li/article[@class='product_pod']")), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_xpaths=("//li[@class='next']/a")))
    )

    def parse_item(self, response):
        name = response.xpath(".//h3/a/@title").get()
        url = response.urljoin(response.xpath(".//h3/a/@href").get())
        price = response.xpath(".//div[@class='product_price']/p[@class='price_color']/text()").get()

        yield {
            'name': name,
            'price': price,
            'url': url
        }
        
