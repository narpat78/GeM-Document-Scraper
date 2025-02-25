from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import base64
import re
from PIL import Image
import pytesseract
import time


def select_category(driver, category):
    '''selecting the category from different categories available'''
    element = Select(driver.find_element(By.ID, 'buyer_category'))
    element.select_by_visible(category)
    print(f'Selected Category: {category}')

def select_date_range(driver, from_date, to_date):
    '''selecting the date range for document extraction'''
    from_date_element = driver.find_element(By.ID, 'from_date_contract_search1')
    to_date_element = driver.find_element(By.ID, 'to_date_contract_search1')
    
    driver.execute_script("arguments[0].removeAttribute('readonly')", from_date_element)
    driver.execute_script("arguments[0].removeAttribute('readonly')", to_date_element)
    
    from_date_element.clear()
    from_date_element.send_keys(from_date)
    to_date_element.clear()
    to_date_element.send_keys(to_date)

    print(f'Selected Date Range: {from_date} to {to_date}')

def extract_captcha(driver, img_id):
    '''extracting and saving the captcha image from base64 data'''
    try:
        captcha_img = driver.find_element(By.ID, img_id)
        img_src = captcha_img.get_attribute("src")
        match = re.search(r'base64,(.*)', img_src)
        if match:
            base64_string = match.group(1)
            image_data = base64.b64decode(base64_string)
            with open("captcha/captcha.jpg", "wb") as img_file:
                img_file.write(image_data)
        else:
            print("⚠️ Failed to read Captcha! Refreshing and Retrying.")

    except Exception as e:
        print(f"⚠️ Error in Extracting the Captcha: {e}")

def read_captcha():
    '''reading the captcha using Tesseract OCR'''
    try:
        image = Image.open("captcha/captcha.jpg")
        text = pytesseract.image_to_string(image)
        captcha = text.replace(" ", "").strip()
        return captcha

    except Exception as e:
        print(f"⚠️ Error reading Captcha: {e}")

def refresh_captcha(driver, img_id):
    '''refreshing the captcha'''
    try:
        print("🔄 Refreshing Captcha...")
        refresh_button = driver.find_element(By.XPATH, f"//a[contains(@onclick, 'loadCap1')]")
        refresh_button.click()
        time.sleep(2)  
        extract_captcha(driver, img_id)  

    except Exception as e:
        print(f"⚠️ Error refreshing Captcha: {e}")

def enter_captcha(driver, captcha_code, img_id):
    '''entering the captcha and submitting to load the documents'''
    while True:
        extract_captcha(driver, img_id)
        captcha = read_captcha()
        cap_input = driver.find_element(By.ID, captcha_code)
        cap_input.clear() 
        cap_input.send_keys(captcha)

        search_button = driver.find_element(By.ID, "searchlocation1")
        driver.execute_script("arguments[0].click();", search_button)
        time.sleep(1)  

        try:
            error = driver.find_element(By.ID, "pcaptcha_code1").text.strip()
            if error:
                refresh_captcha(driver, img_id)
            else:
                print("✅ Captcha accepted! Loading the Documents.")
                break 
        except Exception as e:
            print("⚠️ Error entering the Captcha: {e}")
            break 