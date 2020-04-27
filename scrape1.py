import requests
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import psycopg2
import time

# SQL Database
con = psycopg2.connect(
    host =  "localhost",
    database = "db_cats",
    user = "username",
    password = "password")

# url = "https://www.donedeal.ie/dogs?start=0"
# url_inner = "https://www.donedeal.ie/dogs-for-sale/cocker-spaniel-male/24404040?campaign=3"

# url = "https://www.adoptapet.com/pet-search?clan_id=2&geo_range=50&location=93611&page=1"
# url_alt_inner ="https://www.adoptapet.com/pet/24834470-clovis-california-cat"
# url_alt_inner2 ="https://www.adoptapet.com/pet/27979908-fresno-california-cat"


def scrape_page(url):
    driver = webdriver.Chrome()
    driver.get(url)

    # Wait for page to load
    try: 
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "searchResultsContainer")))
    except TimeoutException:
        print("Timed out")
    finally:
        print("Page Loaded")

    # SQL Cursor
    cur = con.cursor()

    # Wait for data container to load
    time.sleep(5)

    pet_card = driver.find_elements_by_class_name("search__result")

    for each in pet_card:
        name = each.find_element_by_xpath('.//div//div//*[@class="pet__name"]').text
        url = each.find_element_by_xpath('.//*[@class="pet__item__link"]').get_attribute("href")

        cur.execute("insert into cats (name, url) values (%s, %s)", (name, url,))

    # commit changes
    con.commit()

    # close cursor
    cur.close()

for i in range(1,11):
    url = "https://www.adoptapet.com/pet-search?clan_id=2&geo_range=50&location=93611&page={}".format(i)
    scrape_page(url)

# close connection
con.close()