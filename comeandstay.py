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

driver = webdriver.Chrome(path)
driver.maximize_window()

driver.implicitly_wait(3)

# 컴앤스테이 홈페이지
driver.get("https://www.thecomenstay.com/search")

# 서울특별시 행정구 25개
# https://m.blog.naver.com/PostView.nhn?blogId=kkjun1277&logNo=221452982269&proxyReferer=https:%2F%2Fwww.google.com%2F
driver.find_element_by_class_name('search-input').send_keys('서울특별시 강남구')
sleep(0.5)
driver.find_element_by_xpath("""//*[@id="root"]/div/div[3]/div[1]/form/label[1]/div[1]/button""").click()

# 무한 스크롤
houselist_str = """document.body.getElementsByClassName("_Search_result-body__1GPGY")[0].scrollTop = document.body.getElementsByClassName("_Search_result-body__1GPGY")[0].scrollHeight"""

while True:
    wrap_elem = driver.find_element_by_xpath("""//*[@id="root"]/div/div[3]/div[4]/div[2]/div[3]""")
    initial_wrap_height = wrap_elem.size['height']

    driver.execute_script(houselist_str)

    sleep(0.5)

    after_exec_wrap_height = wrap_elem.size['height']

    if initial_wrap_height == after_exec_wrap_height:
        break

html = driver.page_source
soup = BeautifulSoup(html,'html.parser')

house_list_warp_elem = driver.find_element_by_xpath("""//*[@id="root"]/div/div[3]/div[4]/div[2]/div[3]""")
house_lists_elem = house_list_warp_elem.find_elements_by_tag_name("a")

detail_link_list = []

cnt = 0

for house in house_lists_elem:
    detail_link_list.append(house.get_property("href"))
    cnt+=1

print("매물 개수:",cnt)
    
# 중복 제거
detail_link_list = list(set(detail_link_list))

