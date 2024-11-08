import requests
from bs4 import BeautifulSoup
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to fetch mod description by URL
def fetch_mod_description(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        soup = BeautifulSoup(response.text, 'html.parser')
        description_div = soup.find('div', {'class': 'workshopItemDescription', 'id': 'highlightContent'})

        if description_div:
            logging.info(f"Successfully fetched description for {url}")
            return description_div.get_text(separator="\n", strip=True)
        else:
            logging.warning(f"Description not found in page for {url}")
            return "Description not found."
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to retrieve mod description for {url}: {e}")
        return "Failed to retrieve mod description."

# Main function to read URLs, fetch descriptions, and generate HTML pages
def generate_mod_html(file_path):
    try:
        # Read mod URLs from the text file
        with open(file_path, 'r') as f:
            mod_urls = [line.strip() for line in f.readlines() if line.strip()]
        logging.info(f"Read {len(mod_urls)} mod URLs from {file_path}")

        # Create an output folder for the HTML files
        os.makedirs('mod_descriptions', exist_ok=True)

        # Create an index HTML page to link all mod descriptions
        with open('mod_descriptions/index.html', 'w', encoding='utf-8') as index_file:
            index_file.write("<html><head><title>Project Zomboid Mod Descriptions</title></head><body>")
            index_file.write("<h1>Project Zomboid Mods</h1><ul>")

            # Process each mod URL
            for i, url in enumerate(mod_urls, 1):
                logging.info(f"Processing mod {i}: {url}")
                description = fetch_mod_description(url)

                # Create a unique HTML file for each mod
                mod_file_path = f'mod_descriptions/mod_{i}.html'
                try:
                    with open(mod_file_path, 'w', encoding='utf-8') as mod_file:
                        mod_file.write("<html><head><title>Mod Description</title></head><body>")
                        mod_file.write(f"<h2><a href='{url}' target='_blank'>Mod {i}</a></h2>")
                        mod_file.write(f"<p>{description}</p>")
                        mod_file.write("</body></html>")
                    logging.info(f"Successfully created HTML file for mod {i}")
                except Exception as e:
                    logging.error(f"Failed to write HTML file for mod {i}: {e}")

                # Add a link to this mod's description in the index file
                index_file.write(f"<li><a href='mod_{i}.html'>Mod {i}</a></li>")

            index_file.write("</ul></body></html>")
        logging.info("HTML files successfully generated in the 'mod_descriptions' folder.")
    except Exception as e:
        logging.error(f"An error occurred while generating mod HTML files: {e}")

# Path to the text file containing mod URLs
file_path = "C:/Users/ciara/Downloads/project_zomboid_mod_urls.txt"
generate_mod_html(file_path)
