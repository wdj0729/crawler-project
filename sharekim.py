from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from time import *
import pickle
from selenium.common.exceptions import *

start = time()
path = "./chromedriver.exe"

driver = webdriver.Chrome(path)
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

# content 담은 리스트 
data_list = []
listing_time=time()-start
print(listing_time)

#인덱스
i=1

#검색한 쉐어하우스 리스트 정보
for item in detail_link_list:
    detail_start=time()
    print("인덱스:",i)

    #업체명
    try: 
        content = driver.find_element_by_xpath("""//*[@id="root"]/div[3]/div[2]/div[1]/div[2]/div[1]/a["""+ str(i) +"""]""")
        content_data = content.text.strip()
    except NoSuchElementException:
        content = driver.find_element_by_xpath("""//*[@id="root"]/div[3]/div[2]/div[1]/div[2]/div[3]/a["""+ str(i) +"""]""")
        content_data = content.text.strip()

    # 딕셔너리
    dic = {"content": content_data}
    print("dic:", dic)

    # 리스트에 딕셔너리 저장
    data_list.append(dic)
    
    i += 1

    print(time()-detail_start)

# 브라우저 종료
driver.close()

# 파일 쓰기
with open("sharekim.pickle","wb") as fw:
    pickle.dump(data_list, fw)