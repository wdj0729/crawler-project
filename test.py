from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from time import *
from selenium.common.exceptions import *
import csv

start = time()
path = "./chromedriver.exe"

driver = webdriver.Chrome(path)
driver.maximize_window()

driver.implicitly_wait(3)

# 셰어킴 홈페이지
driver.get("https://sharekim.com/detail/1109")

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

product_info = driver.find_element_by_xpath("""//*[@id="blur-wrap"]/div[3]/div[1]/div[2]/div/div[1]/div[2]/div/div[2]""")
product_info_data = product_info.text.strip()
max_len = len(product_info_data)
if(product_info_data.find(":") > 0):
    loc = product_info_data.find(":")
    product_info_data = product_info_data[loc+2:max_len]

print(product_info_data)

driver.close()