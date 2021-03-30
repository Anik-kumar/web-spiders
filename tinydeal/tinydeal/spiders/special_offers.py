import scrapy


class SpecialOffersSpider(scrapy.Spider):
    name = 'special_offers'
    allowed_domains = ['www.cigabuy.com']
    start_urls = ['https://www.cigabuy.com/specials.html']

    def parse(self, response):
        for product in response.xpath("//ul[@class='productlisting-ul']/div[@class='p_box_wrapper']/div"): 
            discount_price = product.xpath(".//div[@class='p_box_price cf']/span[@class='productSpecialPrice fl']/text()").get()
            if discount_price: 
                original_price = product.xpath(".//div[@class='p_box_price cf']/span[@class='normalprice fl']/text()").get()
            else:
                original_price = product.xpath(".//div[@class='p_box_price cf']/text()").get()

            yield {
                "title": product.xpath(".//a[@class='p_box_title']/text()").get(),
                "url": response.urljoin(product.xpath(".//a[@class='p_box_title']/@href").get()),
                "discounted_price": discount_price,
                "original_price": original_price
            }
        
        next_page = response.xpath("//a[@class='nextPage']/@href").get()

        if next_page: 
            yield scrapy.Request(url=next_page, callback=self.parse)

            