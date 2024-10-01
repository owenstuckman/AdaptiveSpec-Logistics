# run_spider.py
import subprocess
import os
import pandas as pd

if __name__ == "__main__":
    # Specify the relative path to the script you want to run
    script_path = os.path.abspath('Scrapy-YellowPages-cloneStart/Scrapy-YellowPages-master/yellowp/spiders/ylp.py')
    
    # Run the script as a separate process

    professionString = "Plumbers"
    locationString = "Colombus"
    stateCode = "OH"

    # need to input for the parameters
    subprocess.run(["python", script_path, professionString, locationString, stateCode]) 

    print("done with subprocess")

    df = pd.read_csv("Scrapy-YellowPages-cloneStart/Main/output.csv")


    # Ensure has basic column data i am looking for 
    filtered_df = df.dropna(subset=['Name', 'Phone', 'Website', 'Locality'])

    filtered_df = df[df['Locality'].str.contains(locationString, case=False, na=False)]

    # filters to optimize selection
    filtered_df = df[df['TonsOfInfo'].str.contains("Business", case=False, na=False)]

    filtered_df = df[df['TonsOfInfo'].str.contains("Accredited", case=False, na=False)]

    


    # create csv file 
    filtered_df.to_csv('Scrapy-YellowPages-cloneStart/Main/filtered_data.csv', index=False)

    # remove outpud from web scrape
    os.remove("Scrapy-YellowPages-cloneStart/Main/output.csv")

