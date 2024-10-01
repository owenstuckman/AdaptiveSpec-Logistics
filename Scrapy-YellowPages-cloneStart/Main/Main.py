import subprocess
import os
import pandas as pd
import customtkinter as ctk
from tkinter import messagebox, Frame, Listbox, Scrollbar


import os
from supabase import create_client, Client

url = ("https://ojfujjzsmsiizopneboj.supabase.co")
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9qZnVqanpzbXNpaXpvcG5lYm9qIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mjc3NTY5MDYsImV4cCI6MjA0MzMzMjkwNn0.w0yVyUnEEZJAB7W9-cAU6Gv2-Yym_Dm6aggr1KrYbbY"
supabase: Client = create_client(url, key)



# Specify the relative path to the script you want to run
script_path = os.path.abspath('Scrapy-YellowPages-cloneStart/Scrapy-YellowPages-master/yellowp/spiders/ylp.py')

# Initialize global variables
professionString = ""
locationString = ""
stateCode = ""
filtered_df = pd.DataFrame()

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
    global professionString, locationString, stateCode, filtered_df
    
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

    # Display the company names in blocks
    displayCompanyNames(filtered_df)

# Function to display company names in blocks
def displayCompanyNames(df):
    # Clear the previous widgets if any
    for widget in app.winfo_children():
        widget.destroy()

    # Create a scrollable frame for company listings
    scrollable_frame = ctk.CTkFrame(app)
    scrollable_frame.pack(pady=10, padx=10, fill='both', expand=True)

    canvas = ctk.CTkCanvas(scrollable_frame)
    scrollbar = Scrollbar(scrollable_frame, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    # Create a frame to hold the company name blocks
    company_frame = ctk.CTkFrame(canvas)
    canvas.create_window((0, 0), window=company_frame, anchor='nw')

    # Populate the frame with company name blocks
    for index, row in df.iterrows():
        company_button = ctk.CTkButton(company_frame, text=row['Name'], command=lambda r=row: showCompanyDetails(r))
        company_button.pack(pady=5, padx=5, fill='x')

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Update scroll region
    company_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

# Function to show company details
def showCompanyDetails(row):
    # Clear the previous widgets
    for widget in app.winfo_children():
        widget.destroy()

    # Display company details
    details_frame = ctk.CTkFrame(app)
    details_frame.pack(pady=10, padx=10, fill='both', expand=True)

    # Show relevant company information
    name_label = ctk.CTkLabel(details_frame, text=f"Company Name: {row['Name']}")
    name_label.pack(pady=(10, 5))

    phone_label = ctk.CTkLabel(details_frame, text=f"Phone: {row['Phone']}")
    phone_label.pack(pady=(5, 5))

    website_label = ctk.CTkLabel(details_frame, text=f"Website: {row['Website']}")
    website_label.pack(pady=(5, 5))

    locality_label = ctk.CTkLabel(details_frame, text=f"Locality: {row['Locality']}")
    locality_label.pack(pady=(5, 5))

    # Select button to save data and restart
    select_button = ctk.CTkButton(details_frame, text="Select", command=lambda: selectCompany(row))
    select_button.pack(pady=(10, 5))

    # Back button to return to the listing
    back_button = ctk.CTkButton(details_frame, text="Back", command=lambda: displayCompanyNames(filtered_df))
    back_button.pack(pady=(5, 5))

# Function to select a company
def selectCompany(row):
    global selected_company
    selected_company = row['Name']
    print(f"Selected Company: {selected_company}")  
    messagebox.showinfo("Selection", f"You selected: {selected_company}")
    response = (
    supabase.table("DataStore")
    .insert({"name": f"{selected_company}"})
    .execute()
    )

    app.destroy()  # Close the application

# Initialize the customtkinter application
ctk.set_appearance_mode("dark")  # Options: "dark", "light", "system"
ctk.set_default_color_theme("blue")  # Change the theme color

app = ctk.CTk()
app.title("Yellow Pages Scraper")
app.geometry("400x600")

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
