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

#SQL Cursor
cur = con.cursor()

cur.execute("SELECT id, name, url FROM cats")

rows = cur.fetchall()

def scrape_db(url):
    driver = webdriver.Chrome()
    driver.get(url)

    facts = driver.find_elements_by_class_name("pet-facts__content")
    for each in facts:
        try:
            sel_breed = each.find_element_by_xpath('.//div//div[1]//*[@class="h4__heading h4--light h4--compact"]').text
            sel_color = each.find_element_by_xpath('.//div//div[2]//*[@class="h4__heading h4--light h4--compact"]').text
            sel_age = each.find_element_by_xpath('.//div//div[3]//*[@class="h4__heading h4--light h4--compact"]').text
            sel_sex = each.find_element_by_xpath('.//div[2]//div[1]//*[@class="h4__heading h4--light h4--compact"]').text
            sel_pet_id = each.find_element_by_xpath('.//div[2]//div[2]//*[@class="h4__heading h4--light h4--compact"]').text
            sel_hair = each.find_element_by_xpath('.//div[2]//div[3]//*[@class="h4__heading h4--light h4--compact f-letter-caps"]').text

            cur.execute("UPDATE cats SET breed = (%s) WHERE url = (%s)", (sel_breed,url,))
            cur.execute("UPDATE cats SET color = (%s) WHERE url = (%s)", (sel_color,url,))
            cur.execute("UPDATE cats SET age = (%s) WHERE url = (%s)", (sel_age,url,))
            cur.execute("UPDATE cats SET sex = (%s) WHERE url = (%s)", (sel_sex,url,))
            cur.execute("UPDATE cats SET pet_id = (%s) WHERE url = (%s)", (sel_pet_id,url,))
            cur.execute("UPDATE cats SET hair = (%s) WHERE url = (%s)", (sel_hair,url,))
            
        except:
            continue

    con.commit() 


for r in rows:
    # print("id: {} name: {} url: {}".format(r[0], r[1], r[2]))
    print("scraping ID:", r[0])
    scrape_db(r[2])

# close cursor
cur.close()

# close connection
con.close()

