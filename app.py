import time

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException


driver = webdriver.Chrome()
driver.get("https://www.qa.com/apprenticeships/apprenticeship-jobs/?postcode=E17%205RG&distance=30&startat=0&howmany=12")

def wait_xpath(driver, xpath_item):
    WebDriverWait(driver, 300).until(EC.presence_of_element_located((By.XPATH, xpath_item)))

def wait_class(driver, class_item):
    WebDriverWait(driver, 300).until(EC.presence_of_element_located((By.CLASS_NAME, class_item)))



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

list_of_links = []
for link in soup.find_all('a', href=True):
    lead_link = link.get('href')
    if lead_link.startswith("https://qaapprenticeships"):
        list_of_links.append(lead_link)

for link in list_of_links:
    print(list_of_links)

time.sleep(3000)
