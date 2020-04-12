from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from time import *
import csv

path = "./chromedriver.exe"

driver = webdriver.Chrome(path)
driver.maximize_window()

driver.implicitly_wait(5)

# 셰어킴 홈페이지
driver.get("https://sharekim.com/search?location=37.60747912093436,126.9543820360534,9&category=[1]")

houselist_str = """document.body.getElementsByClassName("house-list-wrap")[0].scrollTop = document.body.getElementsByClassName("house-list-wrap")[0].scrollHeight"""

while True:
    wrap_elem = driver.find_element_by_xpath("""//*[@id="root"]/div[3]/div[2]/div[1]/div[2]""")
    initial_wrap_height = wrap_elem.size['height']

    driver.execute_script(houselist_str)

    sleep(0.5)

    after_exec_wrap_height = wrap_elem.size['height']

    if initial_wrap_height == after_exec_wrap_height:
        break

# sharehouse.csv파일을 쓰기모드(w)로 열기
# f = open("sharehouse.csv","w",encoding="UTF-8")
# 헤더 추가하기
# f.write("제목,브랜드,방,가격,인실")
# f.write("\n")

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

# 검색한 쉐어하우스 전체 개수
span_max_cnt = soup.select('span.number')[0].text
max_cnt = int(span_max_cnt)
print("서울시 쉐어하우스 전체 개수: ", max_cnt)

house_list_warp_elem = driver.find_element_by_xpath("""//*[@id="root"]/div[3]/div[2]/div[1]/div[2]/div""")
house_lists_elem = house_list_warp_elem.find_elements_by_tag_name("a")

detail_link_list = []

cnt=0

for house in house_lists_elem:
    detail_link_list.append(house.get_property("href"))
    cnt+=1

for item in detail_link_list:
    print(item)

print(cnt)

# 파일에 내용을 입력
# f.write(title_data + "," + brand_data + "," + room_data + "," + price_data + "," + month_data + "\n")

# 작업이 끝난 파일 닫음
# f.close()

# 브라우저 종료
driver.close()