import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BestMoviesSpider(CrawlSpider):
    name = 'best_movies'
    allowed_domains = ['imdb.com']
    start_urls = ['https://www.imdb.com/search/title/?groups=top_250&sort=user_rating']

    rules = (
        Rule(LinkExtractor(restrict_xpaths=("//h3[@class='lister-item-header']/a")), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_xpaths=("(//a[@class='lister-page-next next-page'])[2]")), callback="parse_item", follow=True)
    )

    def parse_item(self, response):
        title = response.xpath("//div[@class='title_wrapper']/h1/text()").get()
        year = response.xpath("//span[@id='titleYear']/a/text()").get()
        duration = response.xpath("normalize-space(//div[@class='title_wrapper']/div/time/text())").get()
        genre1 = response.xpath("normalize-space(//div[@class='title_wrapper']/div/a[1]/text())").get()
        genre2 = response.xpath("normalize-space(//div[@class='title_wrapper']/div/a[2]/text())").get()
        genre3 = response.xpath("normalize-space(//div[@class='title_wrapper']/div/a[3]/text())").get()
        release = response.xpath("normalize-space(//div[@class='title_wrapper']/div/a[last()]/text())").get()
        genre = ""
        if genre1:
            genre = genre + genre1
            
        if genre2 != release:
            genre = genre + ", " + genre2
        
        if genre3 != release:
            genre = genre + ", " + genre3

        
        rating = response.xpath("//span[@itemprop='ratingValue']/text()").get()
        url = response.url

        yield {
            'rating': rating,
            'title': title,
            'year': year,
            'duration': duration,
            'genre': genre,
            "release": release,
            'url': url
        }         