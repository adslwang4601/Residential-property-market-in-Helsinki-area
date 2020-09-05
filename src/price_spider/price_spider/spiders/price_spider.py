import scrapy

class QuotesSpider(scrapy.Spider):
    name = "price"

    start_urls = [
        f"https://asuntojen.hintatiedot.fi/haku/?c=Vantaa&cr=1&t=3&l=2&z={i}&search=1" for i in range(0, 40)
    ]

    def parse(self, response):       
        for url in start_urls:
            next_page = response.css('#next-prev-top').get() 
            if re.search(next_page, "seuraava sivu"): # if page contains next page, then yield request
                yield scrapy.Request(url, callback=self.parse_book)

    def parse(self, response):
        rows =  response.xpath('//*[@id="mainTable"]/tbody[3]')
        for row in rows.css('tr'):         
            yield {
                'district' : row.xpath('td[1]/text()').get(),
                'apartment_type' : row.xpath('td[2]/text()').get(),
                'property_type' : row.xpath('td[3]/text()').get(),
                'floor_area' : row.xpath('td[4]/text()').get(),
                'price' : row.xpath('td[5]/text()').get(),                
                'price_m2' : row.xpath('td[6]/text()').get(),
                'build_year' : row.xpath('td[7]/text()').get(),
                'floor' : row.xpath('td[8]/text()').get(),
                'elevator' : row.xpath('td[9]/text()').get(),
                'condition' : row.xpath('td[10]/text()').get(),
                'plot' : row.xpath('td[11]/text()').get(),
                'energy_class': row.xpath('td[12]/text()').get()
            }

            