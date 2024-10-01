import scrapy
from scrapy.crawler import CrawlerProcess
import sys

# Web scraper itself

# This specifically searches the yellow pages

# Made by Owen Stuckman on 9/30 for startup sprint 

# pulled most from a sample online

class YlpSpider(scrapy.Spider):
    name = "ylp"
    allowed_domains = ["yellowpages.com"]
    start_urls = [f'http://www.yellowpages.com/search?search_terms={sys.argv[1]}&geo_location_terms={sys.argv[2]}%2C+{sys.argv[3]}']
   
    
	# original testing url: http://www.yellowpages.com/search?search_terms=Electicians&geo_location_terms=Blacksburg%2C+VA

    def parse(self, response):
        # Select each company listing based on the class "info"
        companies = response.xpath('//div[@class="info"]')

        for company in companies:

            name = company.xpath('.//div[@class="info-section info-primary"]/h2/a/span/text()').getall()
            extraInfo = company.xpath('.//div["street-address]"]/text()').getall()
            locality = company.xpath('.//div[@class="locality"]/text()').getall()
            categories = company.xpath('.//div[@class="ratings"]/text()').getall()
            links = company.xpath('.//div[@class="links"]/text()').getall()
            badges = company.xpath('.//div[@class="badges"]/text()').getall()
            amenities = company.xpath('.//div[@class="amenities"]/text()').getall()
            categories = company.xpath('.//div[@class="categories"]/text()').getall()
            phone = company.xpath('.//div[@class="phones phone primary"]/text()').extract_first()
            website = company.xpath('.//div[@class="links"]/a/@href').extract_first()
            
            # Yield a dictionary containing the extracted data
            yield {
                'Name': name,
                'Phone': phone,
                'Website': website,
                'TonsOfInfo': extraInfo,
                'Locality' : locality,
                'Categories' : categories,
                'Links' : links,
                'Badges' : badges,
                'Amenities': amenities
                
            }



if __name__ == "__main__":
    process = CrawlerProcess(settings={
        'FEED_FORMAT': 'csv',  # Change format if needed
        'FEED_URI': 'Scrapy-YellowPages-cloneStart/Main/output.csv',  # Change to your desired output path
    })

# Scrapy-YellowPages-cloneStart/Scrapy-YellowPages-master/yellowp/spiders/ylp.py
    # Add your spider to the process
    process.crawl(YlpSpider)
    process.start()  # The script will block here until the crawling is finished
    print("output should be complete")
    print(f'http://www.yellowpages.com/search?search_terms={sys.argv[1]}&geo_location_terms={sys.argv[2]}%2C+{sys.argv[3]}')
