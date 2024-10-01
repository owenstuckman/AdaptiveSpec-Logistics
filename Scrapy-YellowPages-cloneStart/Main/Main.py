import subprocess
import os
import pandas as pd
import customtkinter as ctk
from tkinter import messagebox

# Specify the relative path to the script you want to run
script_path = os.path.abspath('Scrapy-YellowPages-cloneStart/Scrapy-YellowPages-master/yellowp/spiders/ylp.py')

# Function to filter the DataFrame
def filterTable(df):
    # Ensure has basic column data
    filtered_df = df.dropna(subset=['Name', 'Phone', 'Website', 'Locality'])

    # Filters to optimize selection
    #filtered_df = filtered_df[filtered_df['Locality'].str.contains(locationString, case=False, na=False)]
    filtered_df = filtered_df[filtered_df['TonsOfInfo'].str.contains("Business", case=False, na=False)]
    filtered_df = filtered_df[filtered_df['TonsOfInfo'].str.contains("Accredited", case=False, na=False)]

    return filtered_df

# Function to run the subprocess
def runSubprocess():
    global professionString, locationString, stateCode
    
    # Get input values from entries
    professionString = profession_entry.get()
    locationString = location_entry.get()
    stateCode = state_code_entry.get()

    # Run subprocess to scrape
    subprocess.run(["python", script_path, professionString, locationString, stateCode]) 
    print("done with subprocess")

    # Read data generated
    df = pd.read_csv("Scrapy-YellowPages-cloneStart/Main/output.csv")

    # Filter data
    filtered_df = filterTable(df)

    # Create csv file results
    filtered_df.to_csv('Scrapy-YellowPages-cloneStart/Main/filtered_data.csv', index=False)

    # Remove output from web scrape
    os.remove("Scrapy-YellowPages-cloneStart/Main/output.csv")

    messagebox.showinfo("Success", "Data scraped and filtered successfully!")

# Initialize the customtkinter application
ctk.set_appearance_mode("dark")  # Options: "dark", "light", "system"
ctk.set_default_color_theme("blue")  # Change the theme color

app = ctk.CTk()
app.title("Yellow Pages Scraper")
app.geometry("400x300")

# Profession input
profession_label = ctk.CTkLabel(app, text="Profession:")
profession_label.pack(pady=(20, 5))

profession_entry = ctk.CTkEntry(app, placeholder_text="Enter profession (e.g., Plumbers)")
profession_entry.pack(pady=(0, 10))

# Location input
location_label = ctk.CTkLabel(app, text="Location:")
location_label.pack(pady=(10, 5))

location_entry = ctk.CTkEntry(app, placeholder_text="Enter location (e.g., Columbus)")
location_entry.pack(pady=(0, 10))

# State Code input
state_code_label = ctk.CTkLabel(app, text="State Code:")
state_code_label.pack(pady=(10, 5))

state_code_entry = ctk.CTkEntry(app, placeholder_text="Enter state code (e.g., OH)")
state_code_entry.pack(pady=(0, 10))

# Run button
run_button = ctk.CTkButton(app, text="Run Scraper", command=runSubprocess)
run_button.pack(pady=(20, 10))

# Start the main loop
app.mainloop()
