from constants import *
import requests
import schedule
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


# Set up the Selenium WebDriver in headless mode
def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Enable headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")  # Optional, improve compatibility
    chrome_options.add_argument("--start-maximized")  # Ensure consistent layout
    chrome_options.add_argument("--window-size=1920,1080")  # Set the resolution
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-browser-side-navigation")

    # Set up ChromeDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver


# Determine the shoe color based on the URL
def get_shoe_color(url):
    if url == CLOUDTILT_BLACK_IVORY_URL:
        return "Black Ivory"
    elif url == CLOUDTILT_QUARTZ_PEARL_URL:
        return "Quartz Pearl"
    else:
        return "Unknown Color"


# Send a message to Telegram
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print("Message sent to Telegram.")
        else:
            print(f"Failed to send message: {response.text}")
    except Exception as e:
        print(f"Error sending message: {e}")


# Bot function to find input elements and check availability
def check_sizes_availability(url):
    driver = setup_driver()
    results = []
    try:
        shoe_color = get_shoe_color(url)
        driver.get(url)

        # Wait for the DOM to stabilize
        wait = WebDriverWait(driver, 10)
        xpath_query = "//*[starts-with(@id, 'template--17296576807050__main')]"
        input_elements = wait.until(
            EC.presence_of_all_elements_located((By.XPATH, xpath_query))
        )

        sizes_to_check = {"42.5": "Unknown", "43": "Unknown"}

        # Define class-to-status mapping
        class_status_mapping = {
            "soldout minimum-quantity-soldout": "Sold Out",
            " minimum-quantity-soldout": "Sold Out",
            " ": "In Stock",
        }

        if input_elements:
            for element in input_elements:
                # Get attributes
                element_id = element.get_attribute("id")
                element_classes = element.get_attribute("class")
                element_value = element.get_attribute("value")

                # Determine status using the mapping
                status = class_status_mapping.get(element_classes, "Unknown")
                if element_value in sizes_to_check:
                    sizes_to_check[element_value] = status

        # Add results to the output list
        results.append(f"Shoe Color: {shoe_color}")
        for size, status in sizes_to_check.items():
            if status == "In Stock":
                results.append(f"  Size {size}: {status} ({url})")
            else:
                results.append(f"  Size {size}: {status}")

    except Exception as e:
        results.append(f"An error occurred while scraping {url}: {e}")
    finally:
        driver.quit()

    return "\n".join(results)


# Scrape all URLs and send results to Telegram
def scrape_all():
    print("Starting scrape task...")
    urls = [
        CLOUDTILT_BLACK_IVORY_URL,
        CLOUDTILT_BLACK_IVORY_URL2,
        CLOUDTILT_QUARTZ_PEARL_URL,
    ]
    for url in urls:
        message = check_sizes_availability(url)
        send_telegram_message(message)
    print("Scrape task completed.")


# Schedule the bot to run 6 times in 24 hours
schedule.every().day.at("00:00").do(scrape_all)
schedule.every().day.at("04:00").do(scrape_all)
schedule.every().day.at("08:00").do(scrape_all)
schedule.every().day.at("12:00").do(scrape_all)
schedule.every().day.at("16:00").do(scrape_all)
schedule.every().day.at("20:00").do(scrape_all)


# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(1)
