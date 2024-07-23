from selenium import webdriver
import json
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

cookies_file_path = r'path/chrome.json'

driver = webdriver.Chrome()

driver.get("https://www.linkedin.com")

with open(cookies_file_path, 'r') as file:
    cookies = json.load(file)

def normalize_cookie(cookie):
    if 'sameSite' not in cookie or cookie['sameSite'] in ["no_restriction", "unspecified"]:
        cookie['sameSite'] = "None"
    if 'expirationDate' in cookie:
        cookie['expiry'] = int(cookie['expirationDate'])
        del cookie['expirationDate']
    if 'path' not in cookie:
        cookie['path'] = '/'
    if 'domain' not in cookie:
        cookie['domain'] = '.linkedin.com'
    return cookie

driver.get("https://www.linkedin.com")  
time.sleep(5) 

for cookie in cookies:
    cookie = normalize_cookie(cookie)
    try:
        driver.add_cookie(cookie)
        print(f"Added cookie: {cookie}")
    except Exception as e:
        print(f"Failed to add cookie: {cookie}. Error: {e}")

driver.get("https://www.linkedin.com/mynetwork/grow/")
time.sleep(10)  

last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

connect_buttons = driver.find_elements(By.XPATH, '//button[text()="Connect"]')

print(f"Number of connect buttons found: {len(connect_buttons)}")

if len(connect_buttons) > 0:
    for i in range(min(1000, len(connect_buttons))):
        try:
            button = connect_buttons[i]
            ActionChains(driver).move_to_element(button).click().perform()
            time.sleep(1)
            print(f"Sent connection request {i + 1}")
        except Exception as e:
            print(f"Error sending connection request {i + 1}: {e}")
else:
    print("No connect buttons found. Please check the page layout or selector.")

driver.quit()
