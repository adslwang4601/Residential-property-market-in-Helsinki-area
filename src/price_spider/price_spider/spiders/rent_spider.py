import scrapy
import pandas as pd

class QuotesSpider(scrapy.Spider):
    name = "rent"
    df = pd.read_csv('../../../../data/Espoo_Vantaa.csv')
    df['postcode'] = df['postcode'].astype(str).str.pad(width=5, side='left', fillchar='0')
    
    # find rent where transaction prices are available
    postcode_list = df['postcode'].unique() 
    start_urls = [
       f"https://asuntojen.hintatiedot.fi/haku/vuokratiedot?c=&ps={postcode}&renderType=renderTypeTable" for postcode in \
        postcode_list
    ]

    def parse(self, response):
        rows =  response.xpath('//*[@id="mainTable"]/tbody[2]/tr')
        # /html/body/div/div[4]/table/tbody[2]/tr[1]/td/strong
        for row in rows[1:]:
            yield {
                'postcode': response.xpath(' /html/body/div/div[4]/table/tbody[2]/tr[1]/td/strong/text()').get(),
                'apartment_type' : row.xpath('td[1]/text()').get(),
                'ARA_rental' : row.xpath('td[2]/text()').get(),
                'nonsub_old' : row.xpath('td[3]/text()').get(),
                'nonsub_new' : row.xpath('td[4]/text()').get()
                
            }
            
            
#crapy crawl rent  -o ../../../../data/rent.jl
            