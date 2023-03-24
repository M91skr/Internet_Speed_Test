"""---------------------------------------- Internet Speed Test ----------------------------------------
In this code, In this code, a speed test program and notification, non-fulfillment of sla by the internet provider,
is written on Twitter.
"""

# ---------------------------------------- Add Required Library ----------------------------------------

import os
import time

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# ----------------------------------------------------- Parameters -----------------------------------------------------

chrome_driver_path = "CHROME_DRIVER_PATH"
TEST_URL = "https://www.speedtest.net/"
PROMISED_DOWN = 1500
PROMISED_UP = 100
TWITTER_EMAIL = os.getenv("username")
TWITTER_PASSWORD = os.getenv("password")
TWITTER_MOBILE = os.getenv("mobile")
TWITTER_URL = "https://twitter.com/i/flow/login"

# ---------------------------------------------------- Speed Test ----------------------------------------------------

driver_service = Service(executable_path=chrome_driver_path)
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(service=driver_service, options=chrome_options)
down = 0
up = 0


def get_internet_speed():
    driver.get(TEST_URL)
    approve = driver.find_element(By.ID, "onetrust-accept-btn-handler")
    approve.click()
    start = driver.find_element(By.CLASS_NAME, "start-text")
    start.click()
    time.sleep(100)
    download = driver.find_element(By.XPATH, '//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/'
                                             'div[3]/div/div/div[2]/div[1]/div[1]/div/div[2]/span').text
    print(f"download: {download}")
    upload = driver.find_element(By.XPATH, '//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[3]'
                                           '/div/div/div[2]/div[1]/div[2]/div/div[2]/span').text
    print(f"upload: {upload}")
    if float(download) < PROMISED_DOWN or float(upload) < PROMISED_UP:
        tweet_at_provider(download, upload)
    else:
        driver.quit()


# ---------------------------------------------------- Tweeting ----------------------------------------------------


def tweet_at_provider(download, upload):
    driver.get(TWITTER_URL)
    time.sleep(5)
    name = driver.find_element(By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]'
                                         '/div/div/div/div[5]/label/div/div[2]/div/input')
    name.send_keys(TWITTER_EMAIL)
    time.sleep(2)
    name.send_keys(Keys.ENTER)
    try:
        time.sleep(5)
        password = driver.find_element(By.XPATH,
                                       '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]'
                                       '/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input')
        password.send_keys(TWITTER_PASSWORD)
        time.sleep(3)
        password.send_keys(Keys.ENTER)
    except NoSuchElementException:
        time.sleep(5)
        mobile = driver.find_element(By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/'
                                               'div[2]/div[1]/div/div[2]/label/div/div[2]/div/input')
        mobile.send_keys(TWITTER_MOBILE)
        time.sleep(3)
        mobile.send_keys(Keys.ENTER)
        time.sleep(5)
        password = driver.find_element(By.XPATH,
                                       '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]'
                                       '/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input')
        password.send_keys(TWITTER_PASSWORD)
        time.sleep(3)
        password.send_keys(Keys.ENTER)
    finally:
        time.sleep(10)
        cookies = driver.find_element(By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div[2]/div[1]/div/span/span')
        cookies.click()
        time.sleep(5)
        text = driver.find_element(By.CSS_SELECTOR, '#react-root > div > div > div.css-1dbjc4n.r-18u37iz.r-13qz1uu.'
                                                    'r-417010 > main > div > div > div > div.css-1dbjc4n.r-14lw9ot.r-'
                                                    'jxzhtn.r-1ljd8xs.r-13l2t4g.r-1phboty.r-1jgb5lz.r-11wrixw.r-61z16t.'
                                                    'r-1ye8kvj.r-13qz1uu.r-184en5c > div > div.css-1dbjc4n.r-14lw9ot.r-'
                                                    '184en5c > div > div.css-1dbjc4n.r-14lw9ot.r-oyd9sg > div:nth-child'
                                                    '(1) > div > div > div > div.css-1dbjc4n.r-1iusvr4.r-16y2uox.r-177'
                                                    '7fci.r-1h8ys4a.r-1bylmt5.r-13tjlyg.r-7qyjyx.r-1ftll1t > div.css-'
                                                    '1dbjc4n.r-184en5c > div > div > div > div > div > div.css-1dbjc4n.'
                                                    'r-16y2uox.r-bnwqim.r-13qz1uu.r-1g40b8q > div > div > div > div > '
                                                    'label > div.css-1dbjc4n.r-16y2uox.r-1wbh5a2 > div > div > div > '
                                                    'div > div > div.DraftEditor-editorContainer > div')

        twitte = f"Hey Internet Provider, why is my internet speed {download} down and {upload} up, when I pay for {PROMISED_DOWN} down and {PROMISED_UP} up?"
        text.send_keys(twitte)
        time.sleep(3)
        post = driver.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/'
                                             'div[2]/div[1]/div/div/div/div[2]/div[3]/div/div/div[2]/div[3]')
        post.click()

        driver.quit()


get_internet_speed()
