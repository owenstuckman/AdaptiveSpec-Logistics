# run_spider.py
import subprocess
import os
import pandas as pd

if __name__ == "__main__":
    # Specify the relative path to the script you want to run
    script_path = os.path.abspath('Scrapy-YellowPages-cloneStart/Scrapy-YellowPages-master/yellowp/spiders/ylp.py')
    
    # Run the script as a separate process
    subprocess.run(["python", script_path]) 

    print("done with subprocess")

    df = pd.read_csv("Scrapy-YellowPages-cloneStart/Main/output.csv")
    filtered_df = df.dropna(subset=['Name', 'Phone', 'Website'])
    filtered_df.to_csv('Scrapy-YellowPages-cloneStart/Main/filtered_data.csv', index=False)

    
    os.remove("Scrapy-YellowPages-cloneStart/Main/output.csv")

