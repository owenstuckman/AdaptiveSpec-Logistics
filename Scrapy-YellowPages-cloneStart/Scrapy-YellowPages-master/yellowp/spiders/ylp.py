# -*- coding: utf-8 -*-
import scrapy

class YlpSpider(scrapy.Spider):
    name = "ylp"
    allowed_domains = ["yellowpages.com"]
    start_urls = ['http://www.yellowpages.com/search?search_terms=Electicians&geo_location_terms=Blacksburg%2C+VA']
    
    def parse(self, response):
        # Select each company listing based on the class "info"
        companies = response.xpath('//div[@class="info"]')
        
        for company in companies:
            # Extract the company name
            name = company.xpath('.//div[@class="n"]/a/div[@class="business-name"]/a/span/text()').extract_first()
            
            # Extract the company phone number
            phone = company.xpath('.//div[@class="phones phone primary"]/text()').extract_first()
            
            # Extract the company website link
            website = company.xpath('.//div[@class="links"]/a/@href').extract_first()
            
            # Yield a dictionary containing the extracted data
            yield {
                'Name': name,
                'Phone': phone,
                'Website': website
            }
