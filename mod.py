import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set the collection name variable for easier access
collection_name = "Tinkerbooms Never-Neverland"

# Path to the text file containing URLs
url_file_path = "C:/Users/ciara/Downloads/project_zomboid_mod_urls.txt"

# Chrome options without headless mode
chrome_options = Options()
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Initialize the Chrome driver service
chrome_service = Service("C:/Users/ciara/Downloads/chromedriver-win64/chromedriver.exe")
driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
wait = WebDriverWait(driver, 20)

# Open the Steam login page for manual login
login_url = "https://store.steampowered.com/login/"
driver.get(login_url)
print("Please log in to your Steam account manually and complete any 2FA if required. Press Enter here once you're logged in.")
input()  # Wait for manual login and 2FA

# Proceed with processing URLs once logged in
print("Starting to process mod URLs...")

# Read URLs from the text file
with open(url_file_path, "r") as file:
    urls = [line.strip() for line in file if line.strip()]

for url in urls:
    print(f"Processing URL: {url}")
    driver.get(url)

    try:
        print("Attempting to click 'Add to Collection' button...")
        add_to_collection_button = wait.until(
            EC.element_to_be_clickable((By.ID, "AddToCollectionBtn"))
        )
        driver.execute_script("arguments[0].onclick();", add_to_collection_button)
        print("'Add to Collection' button clicked. Waiting for popup...")

        popup = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "newmodal")))
        print("Popup opened successfully.")

    except Exception as e:
        print(f"Error clicking 'Add to Collection' for URL {url}: {e}")
        continue  # Move to the next URL if 'Add to Collection' fails

    try:
        print(f"Checking '{collection_name}' checkbox in popup...")
        collection_checkbox = wait.until(
            EC.element_to_be_clickable((By.XPATH, f"//input[@data-title=\"{collection_name}\"]"))
        )

        if not collection_checkbox.is_selected():
            driver.execute_script("arguments[0].click();", collection_checkbox)
            print("Checkbox was unchecked; now checked.")
        else:
            print("Checkbox already checked; skipping.")

    except Exception as e:
        print(f"Error checking or clicking checkbox for URL {url}: {e}")
        continue  # Move to the next URL if the checkbox fails

    try:
        print("Attempting to click 'OK' button in popup...")
        ok_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//div[@class='btn_green_steamui btn_medium']//span[contains(text(), 'OK')]"))
        )
        driver.execute_script("arguments[0].click();", ok_button)
        print("'OK' button clicked.")

    except Exception as e:
        print(f"Error clicking 'OK' button for URL {url}: {e}")
        continue  # Move to the next URL if 'OK' fails

print("Script completed.")
driver.quit()
