# run_spider.py
import subprocess
import os

if __name__ == "__main__":
    # Specify the relative path to the script you want to run
    script_path = os.path.abspath('../yellowp/spiders/ylp.py')
    
    # Run the script as a separate process
    subprocess.run(["python", script_path])  # Adjust to "python3" if needed

    ouput_path = os.path.abspath("output.csv")
    os.remove(ouput_path)

