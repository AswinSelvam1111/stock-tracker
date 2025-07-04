import os
import time
import sqlite3
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC

def openSite(driver, site: str):
    driver.get(f"{site}")
    print(f"{site} successfully booted.")

def getDriver(site: str):
    options = Options()
    options.add_argument("--headless")

    service = Service(executable_path="util/chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=options)
    openSite(driver, site)
    return driver


def searchLink(driver, xpath):
    link = driver.find_element(By.XPATH, xpath)
    driver.execute_script("arguments[0].scrollIntoView();", link)
    driver.execute_script("arguments[0].click();", link)
    print("Entering Yahoo Finance...") 

def stopLoading(driver):
    time.sleep(4)
    actions = ActionChains(driver)
    actions.send_keys(Keys.ESCAPE).perform()

def scrapeData(stockname, xpath):

    driver = getDriver("https://google.com")

    # Search the stockname in chrome
    input_element = driver.find_element(By.CLASS_NAME, "gLFyf")
    input_element.send_keys(f"{stockname} stock site:finance.yahoo.com" + Keys.ENTER)

    #Give leeway for the user to solve the CAPTCHA
    timeout = 0
    while driver.current_url:
        time.sleep(2)
        if f"{stockname}+stock" in driver.current_url:
            print("CAPTCHA Completed.")
            break
        elif timeout == 15:
            print("No Address detected!")
            driver.quit()
        else:
            timeout += 1
    

    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys(Keys.ESCAPE)  # Close search bar if still active

    # Find Yahoo Finance link
    searchLink(driver, xpath)
    stopLoading(driver)

    #getting info from stock webpage
    price = driver.find_element(By.XPATH, "/html/body/div[2]/main/section/section/section/article/section[1]/div[2]/div[1]/section/div/section/div[1]/div[1]/span").text
    diff = driver.find_element(By.XPATH, "/html/body/div[2]/main/section/section/section/article/section[1]/div[2]/div[1]/section/div/section/div[1]/div[2]/span").text
    perc = driver.find_element(By.XPATH, "/html/body/div[2]/main/section/section/section/article/section[1]/div[2]/div[1]/section/div/section/div[1]/div[3]/span").text

    driver.quit()
    return [price, diff, perc]

stockname = "GOOG"
xpath = "//h3[contains(text(), 'GOOG')]"

print(scrapeData(stockname, xpath))