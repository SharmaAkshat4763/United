from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import os
import time

# ANSI escape code for colored text
RED_TEXT = "\033[91m"
GREEN_TEXT = "\033[92m"
RESET_TEXT = "\033[0m"

# Function to write data to a file
def write_to_file(data, filename):
    with open(filename, "a") as file:
        file.write(data + "\n")

# Function to fetch data for a single college ID
def fetch_data(college_id, driver, filename):
    start_time = time.time()  # Record start time for this ID fetch
    try:
        driver.get("http://pay.icampuserp.in/")  # Replace with the actual URL
        print(f"Fetching data for ID: {college_id}")

        # Locate the College ID input field and enter the ID
        college_id_field = WebDriverWait(driver, 0).until(
            EC.presence_of_element_located((By.ID, "ContentPlaceHolder1_txt_StudentId"))
        )
        college_id_field.clear()
        college_id_field.send_keys(str(college_id))
        college_id_field.send_keys(Keys.TAB)

        # Wait for the data to load
        # Reduce sleep time but make it dynamic based on response time
        time.sleep(1)  # Initial short sleep

        # Use WebDriverWait with specific conditions
        try:
            student_name = WebDriverWait(driver, 0).until(
                EC.presence_of_element_located((By.ID, "ContentPlaceHolder1_txt_Name"))
            ).get_attribute("value")
        except:
            student_name = "N/A"

        try:
            contact_number = WebDriverWait(driver, 0).until(
                EC.presence_of_element_located((By.ID, "ContentPlaceHolder1_hf_ContactNo"))
            ).get_attribute("value")
        except:
            contact_number = "N/A"

        try:
            dob = WebDriverWait(driver, 0).until(
                EC.presence_of_element_located((By.ID, "ContentPlaceHolder1_txt_DOB"))
            ).get_attribute("value")
        except:
            dob = "N/A"

        try:
            batch = WebDriverWait(driver, 0).until(
                EC.presence_of_element_located((By.ID, "ContentPlaceHolder1_txt_Batch"))
            ).get_attribute("value")
        except:
            batch = "N/A"

        try:
            course = WebDriverWait(driver, 0).until(
                EC.presence_of_element_located((By.ID, "ContentPlaceHolder1_txt_Course"))
            ).get_attribute("value")
        except:
            course = "N/A"

        try:
            dept = WebDriverWait(driver, 0).until(
                EC.presence_of_element_located((By.ID, "ContentPlaceHolder1_txt_Dept"))
            ).get_attribute("value")
        except:
            dept = "N/A"

        try:
            year = WebDriverWait(driver, 0).until(
                EC.presence_of_element_located((By.ID, "ContentPlaceHolder1_txt_Year"))
            ).get_attribute("value")
        except:
            year = "N/A"

        # Compile the data into a string
        data = f"ID: {college_id}, Name: {student_name}, Contact: {contact_number}, DOB: {dob}, Batch: {batch}, Course: {course}, Dept: {dept}, Year: {year}"

        # Write the data to the file
        write_to_file(data, filename)
        print(f"Data for ID {college_id} written to file")

    except Exception as e:
        print(f"Error fetching data for ID {college_id}: {e}")

    end_time = time.time()  # Record end time for this ID fetch
    return end_time - start_time  # Return the time taken for this ID fetch

# Main function to iterate through a range of college IDs
def main(start_id, end_id):
    # Set up Chrome options for headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Initialize the WebDriver with the headless options
    driver = webdriver.Chrome(options=chrome_options)

    filename = "student_data.txt"
    file_path = os.path.join(os.getcwd(), filename)

    # Ensure the file is created and empty before starting
    with open(file_path, "w") as file:
        file.write("")

    print(f"Writing data to {file_path}")

    total_time = 0.0
    time_per_id_estimate = 0.0
    num_completed_ids = 0

    try:
        for college_id in range(start_id, end_id + 1):
            time_taken = fetch_data(college_id, driver, file_path)
            total_time += time_taken
            num_completed_ids += 1

            # Update time per ID estimate
            if num_completed_ids == 1:
                time_per_id_estimate = time_taken
            else:
                time_per_id_estimate = (time_per_id_estimate * (num_completed_ids - 1) + time_taken) / num_completed_ids

            # Calculate estimated time remaining
            ids_remaining = end_id - start_id + 1 - num_completed_ids
            estimated_remaining_time = ids_remaining * time_per_id_estimate / 60  # Convert to minutes

            print(f"{GREEN_TEXT}Time taken for ID {college_id}: {time_taken:.2f} seconds{RESET_TEXT}")
            print(f"{RED_TEXT}Estimated remaining time: {estimated_remaining_time:.2f} minutes{RESET_TEXT}")

    finally:
        driver.quit()

    print(f"\nTotal time taken: {total_time:.2f} seconds")

# Set the range of college IDs to search
start_id = 21230713
end_id = 21230715

# Run the main function
main(start_id, end_id)
