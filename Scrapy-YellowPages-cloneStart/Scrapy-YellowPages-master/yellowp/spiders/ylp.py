# -*- coding: utf-8 -*-
import scrapy
from scrapy.crawler import CrawlerProcess

class YlpSpider(scrapy.Spider):
    name = "ylp"
    allowed_domains = ["yellowpages.com"]
    start_urls = ['http://www.yellowpages.com/search?search_terms=Electicians&geo_location_terms=Blacksburg%2C+VA']
    
    def parse(self, response):
        # Select each company listing based on the class "info"
        companies = response.xpath('//div[@class="info"]')
        
		# /html/body/div[1]/div[2]/div[1]/div[1]/div[4]/div[2]/div[3]/div/div/div[2]/div[1]/h2/a/span
        for company in companies:
            # Extract the company name
            name = company.xpath('.//div[@class="info-section info-primary"]/h2/a/span/text()').getall()
            
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



if __name__ == "__main__":
    process = CrawlerProcess(settings={
        'FEED_FORMAT': 'csv',  # Change format if needed
        'FEED_URI': '../../../output.csv',  # Change to your desired output path
    })

    # Add your spider to the process
    process.crawl(YlpSpider)
    process.start()  # The script will block here until the crawling is finished
    
