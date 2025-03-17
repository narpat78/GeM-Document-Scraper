# dependencies
import time
import os
from actions import enter_captcha
from actions import select_category
from actions import select_date_range
from actions import enter_captcha_and_download
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# initializing the Chrome webdriver instance
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--kiosk")

driver = webdriver.Chrome(options=chrome_options)
# driver.maximize_window()

# GeM view contracts URL
driver.get('https://gem.gov.in/view_contracts')

# selecting the category and the date range
select_category(driver=driver, category='Note Sorting Machines')
select_date_range(driver=driver, from_date='01-02-2025', to_date='05-02-2025')
# entering captcha and loading the documents
enter_captcha(driver=driver, captcha_code='captcha_code1', img_id='captchaimg1')

# keep scrolling to load all the documents
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    try:
        WebDriverWait(driver, 5).until(EC.invisibility_of_element((By.ID, "load_more")))
        print("All documents are loaded. Stopping scroll.")
        break 
    except:
        print("Scrolling down... More documents loading.")

# number of documents available 
documents = driver.find_elements(By.CLASS_NAME, "border.block")
print(f"Number of loaded documents: {len(documents)}")

# downloading the documents
for doc in documents:
    document_link = doc.find_element(By.TAG_NAME, "a")
    driver.execute_script("arguments[0].click();", document_link)
    time.sleep(2)
    enter_captcha_and_download(driver=driver, captcha_code="captcha_code")
    
print(f"🎉 Script finished! Total documents downloaded: {len(documents)}")

# waiting and quitting the webdriver instance
time.sleep(5)
driver.quit()