import os
import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set the URL To the Peg engine
url =  input("Press Enter the URL to the peg engine.")

# Defult peg engine url
# "file:///home/pandragon/Downloads/Telegram%20Desktop/Peg/Peg%20engine%20(2)/Online%20version%20%C2%BB%20PEG.js%20%E2%80%93%20Parser%20Generator%20for%20JavaScript.html"

# Get the current directory
current_directory = os.path.dirname(os.path.abspath(__file__))

# Set the parent folder path containing folders starting with "Mir"
parent_folder_path = current_directory

# Ask the user for their choice of browser
browser_choice = input("Enter 'F' for Firefox or 'C' for Chrome: ").strip().upper()

if browser_choice == "F":
    # Create a Firefox browser instance
    driver = webdriver.Firefox()
elif browser_choice == "C":
    # Create a Chrome browser instance
    driver = webdriver.Chrome()
else:
    print("Invalid choice. Exiting.")
    exit()

# Open the URL in the browser
driver.get(url)

# Initialize auto_mode and delay_time
auto_mode = False
delay_time = 3  # 3 second delay

# Create a log file for data collection
log_file = os.path.join(current_directory, "DataCollection.log")

# Function to log messages to the log file
def log_message(message):
    with open(log_file, "a") as log:
        log.write(message + "\n")
    print(message)

# Process folders starting with "Mir"
for folder_name in os.listdir(parent_folder_path):
    if folder_name.startswith("Mir") and os.path.isdir(os.path.join(parent_folder_path, folder_name)):
        log_message(f"\nProcessing folder: {folder_name}")
        folder_path = os.path.join(parent_folder_path, folder_name)
        json_data_file = os.path.join(current_directory, f"{folder_name}.json")
        issues_file = os.path.join(current_directory, "Issues.txt")

        # Create a folder for the output JSON and issues files
        output_folder = os.path.join(current_directory, f"{folder_name} JSON")
        os.makedirs(output_folder, exist_ok=True)

        # Create output JSON file and issues file paths within the output folder
        json_output_file = os.path.join(output_folder, f"{folder_name}.json")
        issues_output_file = os.path.join(output_folder, "Issues.txt")

        # Open the output JSON file for reading and writing
        try:
            with open(json_output_file, "r") as file:
                data = json.load(file)
        except (json.JSONDecodeError, FileNotFoundError):
            data = {"BOOKING": []}

        # Initialize counters
        total_files = 0
        trash_files = 0
        error_files = 0

        # Process the .MIR files in the current folder
        for mir_file in os.listdir(folder_path):
            if mir_file.endswith(".MIR"):
                total_files += 1
                mir_file_path = os.path.join(folder_path, mir_file)

                # Read the content of the .MIR file
                with open(mir_file_path, "r") as file:
                    mir_content = file.read()

                # Find the textarea element by its ID and paste the content
                textarea = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "input")))
                textarea.clear()
                textarea.send_keys(mir_content)

                # Wait for user input
                if not auto_mode:
                    user_input = input(f"Enter 'AUTO' to automatically process, 'SKIP' to skip this folder, or press Enter to verify {mir_file}: ")
                    if user_input.strip().upper() == "AUTO":
                        auto_mode = True
                    elif user_input.strip().upper() == "SKIP":
                        break
                    else:
                        input("Press Enter to continue...")

                # Wait for a brief delay
                time.sleep(delay_time)

                # Wait for the <pre> element with id "output" to be present
                pre_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "output")))

                # Get the JSON data from the <pre> element
                json_text = pre_element.text

                # Check if the JSON text contains "undefined"
                if "undefined" in json_text:
                    log_message(f"Found 'undefined' in JSON data for {mir_file}")
                    # Write the issue to the issues output file
                    with open(issues_output_file, "a") as file:
                        file.write(f"Filename: {mir_file}\nIssue: Found 'undefined' in JSON data\n\n")
                    continue

                # Parse the JSON data
                try:
                    new_data = json.loads(json_text)
                except json.JSONDecodeError:
                    error_files += 1
                    log_message(f"Error decoding JSON data in {mir_file}")

                    # Get the error message from the "parse-message" div
                    error_message = driver.find_element(By.CSS_SELECTOR, "div#parse-message.message.error").text

                    # Write the issue to the issues output file
                    with open(issues_output_file, "a") as file:
                        file.write(f"Filename: {mir_file}\nError Message: {error_message}\n\n")

                    continue

                # Check if "TOTRASH" key exists and its value
                if "TOTRASH" in new_data and new_data["TOTRASH"] is False:
                    # Check if "BOOKING" key exists
                    if "BOOKING" in new_data:
                        booking_data = new_data["BOOKING"]
                        data["BOOKING"].extend(booking_data)

                        # Write the updated data to the output file
                        with open(json_output_file, "w") as file:
                            json.dump(data, file, indent=2)

                        log_message(f"Booking data collected from {mir_file}")
                elif "TOTRASH" in new_data and new_data["TOTRASH"] is True:
                    trash_files += 1

                    # Extract error message from "ERRMSG" field
                    error_message = new_data.get("ERRMSG", "No error message")

                    # Print and log the error message
                    error_message_formatted = f"Error in {mir_file}: {error_message}"
                    log_message(error_message_formatted)
                    print(error_message_formatted)

                    # Write the issue to the issues output file
                    with open(issues_output_file, "a") as file:
                        file.write(f"Filename: {mir_file}\nError Message: {error_message}\n\n")

                # Clear the input textarea
                textarea.clear()

        # Write the summary to the issues output file
        if os.path.exists(issues_output_file):
            with open(issues_output_file, "a") as file:
                file.write(f"Summary for {folder_name}:\n")
                file.write(f"Total Files: {total_files}\n")
                file.write(f"Files with 'TOTRASH': true:     {trash_files}\n")
                file.write(f"Files with JSON decoding errors:  {error_files}\n\n")

# Close the browser
driver.quit()
