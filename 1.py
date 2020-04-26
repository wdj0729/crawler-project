from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from time import *
from selenium.common.exceptions import *
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

# test.csv파일을 쓰기모드(w)로 열기
f = open("test.csv","w",encoding="UTF-8")
# 헤더 추가하기
f.write("업체명,지점명,성별전용,보증금,월세,인실")
f.write("\n")

html = driver.page_source
soup = BeautifulSoup(html,'html.parser')

house_list_warp_elem = driver.find_element_by_xpath("""//*[@id="root"]/div[3]/div[2]/div[1]/div[2]""")
house_lists_elem = house_list_warp_elem.find_elements_by_tag_name("a")

detail_link_list = []

for house in house_lists_elem:
    detail_link_list.append(house.get_property("href"))

#인덱스
i=1

#검색한 쉐어하우스 리스트 정보
for item in detail_link_list:
    try: 
        title = driver.find_element_by_xpath("""//*[@id="root"]/div[3]/div[2]/div[1]/div[2]/div/a["""+ str(i) +"""]/div/div[2]/span[1]""")
        title_data = title.text.strip()
    except NoSuchElementException:
        pass
    try:
        brand = driver.find_element_by_xpath("""//*[@id="root"]/div[3]/div[2]/div[1]/div[2]/div/a["""+ str(i) +"""]/div/div[2]/span[2]""")
        brand_data = brand.text.strip()
        if(brand_data.find("점") >= 0):
            fitem = brand_data.find("점")
            brand_data = brand_data[0:fitem+1]
        else:
            pass
    except NoSuchElementException:
        pass
    try:
        room = driver.find_elements_by_xpath("""//*[@id="root"]/div[3]/div[2]/div[1]/div[2]/div/a["""+ str(i) +"""]/div/div[2]/div[1]/span""")
        room_data = room[0].text.strip()
        if(room_data.find("여성") >= 0):
            room_data="여성전용"
        elif(room_data.find("남성") >= 0):
            room_data="남성전용"
        elif(room_data.find("무관") >= 0):
            room_data = "성별무관"
        else:
            pass
    except NoSuchElementException:
        pass
    try:
        price = driver.find_elements_by_xpath("""//*[@id="root"]/div[3]/div[2]/div[1]/div[2]/div/a["""+ str(i) +"""]/div/div[2]/div[2]/span""")
        price_data = price[0].text.strip()
        #보증금
        fitem = price_data.find("/")
        deposit_data = price_data[0:fitem-1]
        #월세
        sitem = price_data.find("(")
        month_data = price_data[fitem+2:sitem-1]
        #인실
        people_data = price_data[sitem+1:sitem+4]
    except NoSuchElementException:
        pass

    # replace 함수를 활용하여 ,를 제거
    title_data = title_data.replace(",","")
    brand_data = brand_data.replace(",","")
    room_data = room_data.replace(",","")
    price_data = price_data.replace(",","")
    deposit_data = deposit_data.replace(",","")
    month_data = month_data.replace(",","")
    people_data = people_data.replace(",","")

    print(i)

    # 파일에 내용을 입력
    f.write(title_data + "," + brand_data + "," + room_data + "," + deposit_data +"만원" + "," + month_data + "," + people_data + "\n")

    i+=1

# 작업이 끝난 파일 닫음
f.close()

# 브라우저 종료
driver.close() 