import sys
import os
from scrapy.crawler import CrawlerProcess

# Import spider
file_path = "C:/Users/ostuc/Documents/GitHub/YellowPageScrapeQuick/Scrapy-YellowPages-cloneStart/Scrapy-YellowPages-master/yellowp/spiders/ylp.py"


# Get the directory containing the file
directory_path = os.path.dirname(file_path)

# Add the directory to the Python path
sys.path.append(directory_path)

# Import the file as a module
import ylp


if __name__ == "__main__":
    process = CrawlerProcess()

    # Add your spider to the process
    process.crawl(ylp)
    process.start()  # The script will block here until the crawling is finished