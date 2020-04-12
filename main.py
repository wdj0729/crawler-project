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
f = open("sharehouse.csv","w",encoding="UTF-8")
# 헤더 추가하기
f.write("제목,브랜드,방,가격")
f.write("\n")

html = driver.page_source
soup = BeautifulSoup(html,'html.parser')

#검색한 쉐어하우스 전체 개수
span_max_cnt = soup.select('span.number')[0].text
max_cnt = int(span_max_cnt)
print("서울시 쉐어하우스 전체 개수: ",max_cnt)

#검색한 쉐어하우스 리스트 정보
for i in range(1,max_cnt):
    title = driver.find_element_by_xpath("""//*[@id="root"]/div[3]/div[2]/div[1]/div[2]/div/a["""+ str(i) +"""]/div/div[2]/span[1]""")
    title_data = title.text.strip()
    brand = driver.find_element_by_xpath("""//*[@id="root"]/div[3]/div[2]/div[1]/div[2]/div/a["""+ str(i) +"""]/div/div[2]/span[2]""")
    brand_data = brand.text.strip()
    room = driver.find_elements_by_xpath("""//*[@id="root"]/div[3]/div[2]/div[1]/div[2]/div/a["""+ str(i) +"""]/div/div[2]/div[1]/span""")
    room_data = room[0].text.strip()
    price = driver.find_elements_by_xpath("""//*[@id="root"]/div[3]/div[2]/div[1]/div[2]/div/a["""+ str(i) +"""]/div/div[2]/div[2]/span""")
    price_data = price[0].text.strip()

    # replace 함수를 활용하여 ,를 제거
    title_data = title_data.replace(",","")
    brand_data = brand_data.replace(",","")
    room_data = room_data.replace(",","")
    price_data = price_data.replace(",","")

    # console 출력
    # print("제목",title_data)
    # print("브랜드",brand_data)
    # print("방",room_data)
    # print("가격",price_data)
    print(i)

    # 파일에 내용을 입력
    f.write(title_data + "," + brand_data + "," + room_data + "," + price_data + "\n")

# 작업이 끝난 파일 닫음
f.close()

# 브라우저 종료
driver.close()