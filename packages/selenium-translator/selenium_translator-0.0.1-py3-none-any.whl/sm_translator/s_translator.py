import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os



def downloading(path):
    if len(os.listdir(path)) == 0:
        time.sleep(1)
        downloading(path)
    else:
        if '.crdownload' in os.listdir(path)[0] or '.temp' in os.listdir(path)[0] or '.tmp' in os.listdir(path)[0]:
            time.sleep(1)
            downloading(path)
        else:
            print(os.listdir(path)[0], 'file translated')




def file_translation(file_path, download_path):

    if not os.path.isfile(file_path):
        print('File not found at path')
        return

    url = 'https://translate.google.com/?sl=auto&tl=en&op=docs'

    download_path = download_path + r'\file'
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    chrome_options = Options()
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    prefs = {
        "download.default_directory": download_path,  # Set the custom download directory
        "download.prompt_for_download": False,  # Disable download prompt
        "directory_upgrade": True,  # Automatically set the new download directory
        "safebrowsing.enabled": True  # Enable safe browsing (required for some downloads)
    }
    chrome_options.add_argument("--window-size=1920,1080")  # Run in headless mode
    chrome_options.add_argument("--disable-gpu")  # Disable GPU for better performance (optional)
    chrome_options.add_argument("--no-sandbox")  # Add for environments like Linux (optional)
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(options=chrome_options)


    driver.get(url)

    try:
        cookie_btn = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[text()="Accept all"]')))
        ActionChains(driver).click(cookie_btn).perform()
    except Exception as e:
        pass

    drag_drop = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located(
            (By.XPATH, '//input[@type="file"]')))

    # Use send_keys to upload the file
    drag_drop.send_keys(file_path)
    translate = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located(
            (By.XPATH, '//span[@class="VfPpkd-vQzf8d" and text()="Translate"]')))
    ActionChains(driver).click(translate).perform()

    load = True
    print('translating...')
    while load:
        try:
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located(
                    (By.XPATH,
                     '//button[contains(@style,"--mdc-ripple-fg-translate-end: 18.635417938232422px, -9.5px; max-width: 292px;")]')))
        except Exception as e:
            load = False
        time.sleep(1)

    download_translation = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located(
            (By.XPATH, '//span[@class="VfPpkd-vQzf8d" and text()="Download translation"]')))
    ActionChains(driver).click(download_translation).perform()

    downloading(download_path)

















