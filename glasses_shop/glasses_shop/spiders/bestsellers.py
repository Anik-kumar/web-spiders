import scrapy


class BestsellersSpider(scrapy.Spider):
    name = 'bestsellers'
    allowed_domains = ['www.glassesshop.com']
    start_urls = ['https://www.glassesshop.com/bestsellers']

    def parse(self, response):
        glasses = response.xpath("//div[@class='col-12 pb-5 mb-lg-3 col-lg-4 product-list-row text-center product-list-item']")
        for glass in glasses:
            url = glass.xpath(".//div[@class='product-img-outer']/a[1]/@href").get()
            img_url = glass.xpath(".//div[@class='product-img-outer']/a[1]/img[1]/@data-src").get()
            primary_color = glass.xpath(".//div[@class='p-title-block']/div[1]/div[1]/div/span[1]/@title").get()
            name = glass.xpath(".//div[@class='p-title-block']/div[@class='mt-3']/div/div[1]/div/a[1]/text()").get()
            name = name.strip() + " - " + primary_color
            price = glass.xpath(".//div[@class='p-title-block']/div[@class='mt-3']/div/div[2]/div/div[1]/span/text()").get()
            yield {
                'url': url,
                'img_url': img_url,
                'name': name,
                'price': price
            }

        next_page = glass.xpath("//a[@rel='next' and @class='page-link' and @aria-label]/@href").get()

        if next_page: 
            yield response.Request(url=next_page, callback=self.parse)


# //div[@class='col-12 pb-5 mb-lg-3 col-lg-4 product-list-row text-center product-list-item']/div[@class='product-img-outer']/a[1]/img[1]/@src

# //div[@id='product-lists']/div/div[@class='p-title']/a/text()
