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

def getInitialInput():
    # Get input from the user
    profession = profession_input.get()
    location = location_input.get()
    state_code = state_input.get()

    if not profession or not location or not state_code:
        messagebox.showerror("Error", "Please fill in all fields.")
        return

def filterTable(df):
    # Ensure has basic column data i am looking for 
    filtered_df = df.dropna(subset=['Name', 'Phone', 'Website', 'Locality'])


    # filters to optimize selection
    filtered_df = df[df['Locality'].str.contains(locationString, case=False, na=False)]
    filtered_df = df[df['TonsOfInfo'].str.contains("Business", case=False, na=False)]
    filtered_df = df[df['TonsOfInfo'].str.contains("Accredited", case=False, na=False)]
    filtered_df = df[df['Locality'].str.contains(locationString, case=False, na=False)]

    return filtered_df

def runSubprocess():
    # run subprocess - to scrap
    subprocess.run(["python", script_path, professionString, locationString, stateCode]) 
    print("done with subprocess")


# init window

# Initialize the main window
ctk.set_appearance_mode("System")  # Modes: "System" (default), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Change theme colors here

root = ctk.CTk()
root.title("YellowPages Scraper")
root.geometry("600x400")  # Set the size of the window

# Create and place the input fields
ctk.CTkLabel(root, text="Profession:").grid(row=0, column=0, padx=10, pady=5)
profession_input = ctk.CTkEntry(root)
profession_input.grid(row=0, column=1, padx=10, pady=5)

ctk.CTkLabel(root, text="Location:").grid(row=1, column=0, padx=10, pady=5)
location_input = ctk.CTkEntry(root)
location_input.grid(row=1, column=1, padx=10, pady=5)

ctk.CTkLabel(root, text="State Code:").grid(row=2, column=0, padx=10, pady=5)
state_input = ctk.CTkEntry(root)
state_input.grid(row=2, column=1, padx=10, pady=5)

# Button to run the spider
run_button = ctk.CTkButton(root, text="Run Scraper", command=runSubprocess())
run_button.grid(row=3, column=0, columnspan=2, pady=10)


if __name__ == "__main__":

    # read data generated
    df = pd.read_csv("Scrapy-YellowPages-cloneStart/Main/output.csv")

    # filter data 
    filtered_df = filterTable(df)

    # create csv file results
    filtered_df.to_csv('Scrapy-YellowPages-cloneStart/Main/filtered_data.csv', index=False)

    # remove output from web scrape
    os.remove("Scrapy-YellowPages-cloneStart/Main/output.csv")


# Table display

    # Create a table to display the CSV data
    columns = ('Name', 'Phone', 'Website', 'Locality')
    tree = ctk.CTkTabview(root, columns=columns, show='headings', height=10)
    tree.heading('Name', text='Name')
    tree.heading('Phone', text='Phone')
    tree.heading('Website', text='Website')
    tree.heading('Locality', text='Locality')

    # Place the table in the window
    tree.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    # Start the CustomTkinter event loop
    root.mainloop()