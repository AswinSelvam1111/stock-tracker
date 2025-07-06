import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def getDriver(site: str):
    options = uc.ChromeOptions()
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36")
    options.add_argument("--disable-blink-features=AutomationControlled")

    driver = uc.Chrome(options=options)
    driver.get(site)
    print(f"{site} successfully booted.")
    return driver

def scrapeData(symbol):

    url = f"https://sg.finance.yahoo.com/quote/{symbol}/"
    driver = getDriver(url)
    wait = WebDriverWait(driver, 20)

    try:
        priceElem = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.yf-ipw1h0.base[data-testid="qsp-price"]')))
        diffElem = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.yf-ipw1h0.base[data-testid="qsp-price-change"]')))
        percElem = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.yf-ipw1h0.base[data-testid="qsp-price-change-percent"]')))

        price = priceElem.text
        diff = diffElem.text
        perc = percElem.text

    except Exception as e:
        print("Failed to extract price info:", e)
        price, diff, perc = None, None, None
    finally:
        driver.quit()

    return price, diff, perc