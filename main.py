import psycopg2
from models import get_conn_cur

import time

import os
from dotenv import load_dotenv

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException




def wait_xpath(driver, xpath_item):
    WebDriverWait(driver, 300).until(EC.presence_of_element_located((By.XPATH, xpath_item)))

def wait_class(driver, class_item):
    WebDriverWait(driver, 300).until(EC.presence_of_element_located((By.CLASS_NAME, class_item)))




load_dotenv('.env')
driver = webdriver.Chrome()
driver.get(os.getenv('TARGET_URL'))
i = 1
while True:
    try:
        print("I is: ", i)
        load_more_xp = f"/html/body/div[2]/div/main/div/div[3]/div[2]/div[3]/button"
        load_more = driver.find_element(By.XPATH, load_more_xp)

        ActionChains(driver).scroll_to_element(load_more).perform() # Scrolling to the load more button
        wait_xpath(driver, load_more_xp) # Giving time for it to load

        try:
            ac_btn_xpath = "/html/body/div[1]/div[1]/div[5]/div[1]/a"
            ac_btn = driver.find_element(By.XPATH, ac_btn_xpath)
            ac_btn.click()
        except NoSuchElementException:
            print("No such AC")
            continue

        # time.sleep(3)
        load_more.click()
        time.sleep(3)
        i += 1

    except NoSuchElementException:
        break


url_rn = driver.current_url
rsp = requests.get(url_rn)
html_content = rsp.text

soup = BeautifulSoup(html_content, "html.parser")


insert_values = []
for link in soup.find_all('a', href=True):
    lead = link.get('href')
    if lead.startswith(os.getenv('TARGET_PREFIX')):
        postcode = "12345"
        comp_name = "Company Placeholder"
        insert_values.append((str(lead), str(postcode), str(comp_name)))



# adding to DB
conn, cur = get_conn_cur()

insert_script = """
    INSERT INTO jobs (link, postcode, comp_name)
    VALUES (%s, %s, %s)
    ON CONFLICT (link) DO NOTHING;
"""

print("All Values: ", insert_values)

cur.executemany(insert_script, insert_values)

conn.commit()
cur.close()

conn.close()