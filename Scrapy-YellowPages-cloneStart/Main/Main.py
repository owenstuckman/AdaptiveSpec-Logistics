# run_spider.py
import subprocess
import os
import pandas as pd
import customtkinter as ctk
from tkinter import messagebox



# Specify the relative path to the script you want to run
script_path = os.path.abspath('Scrapy-YellowPages-cloneStart/Scrapy-YellowPages-master/yellowp/spiders/ylp.py')

# Run the script as a separate process

professionString = "Plumbers"
locationString = "Colombus"
stateCode = "OH"


def filterTable(df):
    # Ensure has basic column data i am looking for 
    filtered_df = df.dropna(subset=['Name', 'Phone', 'Website', 'Locality'])


    # filters to optimize selection
    filtered_df = df[df['Locality'].str.contains(locationString, case=False, na=False)]
    filtered_df = df[df['TonsOfInfo'].str.contains("Business", case=False, na=False)]
    filtered_df = df[df['TonsOfInfo'].str.contains("Accredited", case=False, na=False)]

    return filtered_df

def runSubprocess():
    # run subprocess - to scrap
    subprocess.run(["python", script_path, professionString, locationString, stateCode]) 
    print("done with subprocess")



if __name__ == "__main__":

    runSubprocess()

    # read data generated
    df = pd.read_csv("Scrapy-YellowPages-cloneStart/Main/output.csv")

    # filter data 
    filtered_df = filterTable(df)

    # create csv file results
    filtered_df.to_csv('Scrapy-YellowPages-cloneStart/Main/filtered_data.csv', index=False)

    # remove output from web scrape
    os.remove("Scrapy-YellowPages-cloneStart/Main/output.csv")

