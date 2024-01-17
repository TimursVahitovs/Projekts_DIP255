from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

service = Service()
option = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=option)

def rd_veikals(product):
    cookie = driver.find_element(By.ID, "CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll")
    cookie.click()
    find = driver.find_element(By.NAME, "search_string")
    find.click()
    find.send_keys(product)
    find.submit()
    time.sleep(2)
    try:
        price = driver.find_element(By.CLASS_NAME, "price")
    except:
        print("RD: product not found")
        price = 30000.14159265359 # izmantoju, kā, cerams, nēeksistējošo cenu, gadījumā, ja prece netiek atrasta
        return price
    price = float(price.text.replace(" €", ""))
    print("RD: ", price, " €")
    return price

def euronics(product):
    cookie = driver.find_element(By.ID, "cookie-accept-all-button")
    cookie.click()
    find = driver.find_element(By.ID, "searchKeyword")
    find.click()
    find.send_keys(product)
    find.submit()
    time.sleep(2)
    try:
        price = driver.find_element(By.CLASS_NAME, "price")
    except:
        print("Euronics: product not found")
        price = 30000.14159265359
        return price
    price = float(price.text.strip().replace("  €", "").replace(" ", ".").split('\n')[0])
    print("Euronics: ", price, " €")
    return price

def tet(product):
    find = driver.find_element(By.NAME, "query")
    find.click()
    find.send_keys(product)
    find.submit()
    time.sleep(1)
    try:
        sort = driver.find_element(By.CLASS_NAME, "i-grid-status__select-container")
    except:
        print("tet: product not found")
        price = 30000.14159265359
        return price
    sort.click()
    relevance = driver.find_element(By.XPATH, "//a[@rel='relevance' and text()='Atbilstība']")
    time.sleep(1)
    relevance.click()
    time.sleep(2)
    find = driver.find_element(By.CLASS_NAME, "i-product-item__link")
    find.click()
    price = driver.find_element(By.CLASS_NAME, "i-product-data__price-inner")
    price = float(price.text.strip().replace("€", "").replace(",", ".").replace(" ", ""))
    print("tet: ", price, " €")
    return price
def viens_a(product):
    find = driver.find_element(By.ID, "q")
    find.click()
    find.send_keys(product)
    find.submit()
    time.sleep(2)
    try:
        price = driver.find_element(By.XPATH, "//span[@itemprop='price']")
    except:
        print("1a: product not found")
        price = 30000.14159265359
        return price
    price = float(price.text.replace(".","").replace(",", "."))
    print("1a: ", price, " €")
    return price


def compare_prices(rd_price, euronics_price, tet_price, viens_a_price):
    min_price = min(rd_price, euronics_price, tet_price, viens_a_price)
    if min_price == 30000.14159265359:
        print("Your product was not found in any store")
        exit()
    if min_price == rd_price:
        print("RD Veikals has the lowest price:", min_price, " €")
    elif min_price == euronics_price:
        print("Euronics has the lowest price:", min_price, " €")
    elif min_price == tet_price:
        print("tet has the lowest price:", min_price, " €")
    elif min_price == viens_a_price:
        print("1a has the lowest price:", min_price, " €")

print("This script allows you to check where, out of the four most popular electronics stores in Latvia, your chosen product is cheaper.")
product = input("Enter product name: ")

url = "https://www.rdveikals.lv/home/lv/"
driver.get(url)
time.sleep(2)

rd_price = rd_veikals(product)

url = "https://www.euronics.lv/"
driver.get(url)
time.sleep(2)

euronics_price = euronics(product)

url = "https://www.tet.lv/veikals/"
driver.get(url)
time.sleep(2)

tet_price = tet(product)

url = "https://www.1a.lv/"
driver.get(url)
time.sleep(2)

viens_a_price = viens_a(product)

compare_prices(rd_price, euronics_price, tet_price, viens_a_price)

driver.quit()