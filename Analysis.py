import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from time import sleep
from bs4 import BeautifulSoup
import csv
from selenium.common.exceptions import StaleElementReferenceException

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--kiosk-printing')
chrome_options.add_experimental_option("useAutomationExtension", False)
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_argument("--start-maximized")
# chrome_options.add_argument('--headless')

path_ = os.path.join(os.getcwd(), 'download')
prefs = {"download.default_directory": path_}
chrome_options.add_experimental_option("prefs", prefs)

driver = webdriver.Chrome(options=chrome_options)

url = "https://franchisesuppliernetwork.com/"
driver.get(url)
sleep(7)  # Wait for the page to load, adjust as needed
soup = BeautifulSoup(driver.page_source, 'html.parser')
header_links = []
header_items = soup.find_all('li', class_='menu-item')
for item in header_items:
    link = item.find('a')['href']
    header_links.append({"header_link": link})

print('header_links:-',header_links)
for link in header_links:
    try:
        # Get the link URL
        link_url = link['header_link']      
        sleep(10)
        driver.get(link_url)
        sleep(5)  

        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        
        # Count images and URLs
        image_count = len(soup.find_all('img'))
        href_urls = [a.get("href") for a in soup.find_all("a") if a.get("href")]
        href_count = len(href_urls)
        
        # Create CSV file for the current header link
        page_title =driver.title
        print(page_title)
        data_before_pipe = page_title.split('|')[0].strip()
        header_link_name = data_before_pipe.strip().replace("/", "-")  
        csv_filename = f"{header_link_name}_Info.csv"
        
        with open(csv_filename, "w", newline="") as csvfile:
            fieldnames = ["URL", "Image Count", "Href Count", "Href URLs"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            # Write header
            writer.writeheader()
            # Write data for the current header link
            writer.writerow({
                "URL": link_url,
                "Image Count": image_count,
                "Href Count": href_count,
                "Href URLs": "\n".join(href_urls)  # Convert the list to a string with newline separator
            })
        
        print(f"CSV file '{csv_filename}' created successfully")
    except StaleElementReferenceException:
        print("StaleElementReferenceException occurred. Retrying...")
        continue

# Close the browser
driver.quit()