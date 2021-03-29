import scrapy


class NationalDept2Spider(scrapy.Spider):
    name = 'national_dept2'
    allowed_domains = ['worldpopulationreview.com']
    start_urls = ['http://worldpopulationreview.com/countries/countries-by-national-debt/']

    def parse(self, response):
        countries = response.xpath('//div[@class="jsx-2642336383 table-container"]/table/tbody/tr')

        for country in countries:
            name = country.xpath('.//td[1]/a/text()').get()
            dept = country.xpath('.//td[2]/text()').get()

            yield {
                "country_name": name,
                "country_dept": dept
            }