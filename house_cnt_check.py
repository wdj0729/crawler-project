from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from time import *
import pickle
from selenium.common.exceptions import *

path = "./chromedriver.exe"

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")
# 혹은 options.add_argument("--disable-gpu")

# UserAgent값을 바꿔줍시다!
options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")

driver = webdriver.Chrome(path,options=options)
driver.maximize_window()

driver.implicitly_wait(3)

# 셰어킴 홈페이지
driver.get("https://sharekim.com/search?location=37.60747912093436,126.9543820360534,9&category=[1]")

# 무한 스크롤
houselist_str = """document.body.getElementsByClassName("house-list-wrap")[0].scrollTop = document.body.getElementsByClassName("house-list-wrap")[0].scrollHeight"""

while True:
    wrap_elem = driver.find_element_by_xpath("""//*[@id="root"]/div[3]/div[2]/div[1]/div[2]""")
    initial_wrap_height = wrap_elem.size['height']

    driver.execute_script(houselist_str)

    sleep(0.5)

    after_exec_wrap_height = wrap_elem.size['height']

    if initial_wrap_height == after_exec_wrap_height:
        break

html = driver.page_source
soup = BeautifulSoup(html,'html.parser')

house_list_warp_elem = driver.find_element_by_xpath("""//*[@id="root"]/div[3]/div[2]/div[1]/div[2]""")
house_lists_elem = house_list_warp_elem.find_elements_by_tag_name("a")

detail_link_list = []

for house in house_lists_elem:
    detail_link_list.append(house.get_property("href"))

# 중복 제거
detail_link_list = list(set(detail_link_list))

house_cnt = 0

for i in detail_link_list:
    house_cnt+=1

print("전체 쉐어하우스 업체 개수:",house_cnt)

# 브라우저 종료
driver.close()
