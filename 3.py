from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from time import *
import pickle
from selenium.common.exceptions import *
import csv

start = time()
path = "./chromedriver.exe"

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

# test.csv파일을 쓰기모드(w)로 열기
f = open("test.csv","w",encoding="UTF-8")
# 헤더 추가하기
f.write("매물명,지역,보증금,월임대료,고정관리비/광열비,방개수,화장실개수")
f.write("\n")

html = driver.page_source
soup = BeautifulSoup(html,'html.parser')

house_list_warp_elem = driver.find_element_by_xpath("""//*[@id="root"]/div/div[3]/div[4]/div[2]/div[3]""")
house_lists_elem = house_list_warp_elem.find_elements_by_tag_name("a")

detail_link_list = []

for house in house_lists_elem:
    detail_link_list.append(house.get_property("href"))
    
# 중복 제거
detail_link_list = list(set(detail_link_list))

# content 담은 리스트 
data_list = []

#인덱스
i=1

driver2 = webdriver.Chrome(path)
driver2.maximize_window()

for item in detail_link_list:
    detail_start=time()
    print("주소:",item)
    print("인덱스:",i)

    # 컴앤스테이 상세페이지
    driver2.get(item)

    WebDriverWait(driver2, 5).until(
        EC.presence_of_element_located((By.ID, "root"))
    )
    # 매물명
    try:
        house_name = driver2.find_element_by_xpath("""//*[@id="root"]/div/div[3]/div[2]/div/h1""")
        house_name_data = house_name.text.strip()
    except NoSuchElementException:
        pass
    # 지역
    try:
        loc_info = driver2.find_element_by_xpath("""//*[@id="root"]/div/div[3]/div[1]/div/div[4]/div[3]/div[1]/div[1]/div[2]/h1""")
        loc_data = loc_info.text.strip()
    except NoSuchElementException:
        loc_info = driver2.find_element_by_xpath("""//*[@id="root"]/div/div[3]/div[1]/div/div[4]/div[4]/div[1]/div[1]/div[2]/h1""")
        loc_data = loc_info.text.strip()
    except NoSuchElementException:
        loc_info = driver2.find_element_by_xpath("""//*[@id="root"]/div/div[3]/div[1]/div/div[4]/div[5]/div[1]/div[1]/div[2]/h1""")
        loc_data = loc_info.text.strip()
    # 보증금
    try:
        deposit_info = driver2.find_element_by_xpath("""//*[@id="root"]/div/div[3]/div[1]/div/div[4]/div[3]/div[1]/div[2]/div[1]/h1""")
        deposit_data = deposit_info.text.strip()
        deposit_data = deposit_data.replace(",","")
    except NoSuchElementException:
        deposit_info = driver2.find_element_by_xpath("""//*[@id="root"]/div/div[3]/div[1]/div/div[4]/div[4]/div[1]/div[2]/div[1]/h1""")
        deposit_data = deposit_info.text.strip()
        deposit_data = deposit_data.replace(",","")
    except NoSuchElementException:
        deposit_info = driver2.find_element_by_xpath("""//*[@id="root"]/div/div[3]/div[1]/div/div[4]/div[5]/div[1]/div[2]/div[1]/h1""")
        deposit_data = deposit_info.text.strip()
        deposit_data = deposit_data.replace(",","")
    # 월임대료
    try:
        month_info = driver2.find_element_by_xpath("""//*[@id="root"]/div/div[3]/div[1]/div/div[4]/div[3]/div[1]/div[2]/div[2]/h1""")
        month_data = month_info.text.strip()
        month_data = month_data.replace(",","")
    except NoSuchElementException:
        month_info = driver2.find_element_by_xpath("""//*[@id="root"]/div/div[3]/div[1]/div/div[4]/div[4]/div[1]/div[2]/div[2]/h1""")
        month_data = month_info.text.strip()
        month_data = month_data.replace(",","")
    except NoSuchElementException:
        month_info = driver2.find_element_by_xpath("""//*[@id="root"]/div/div[3]/div[1]/div/div[4]/div[5]/div[1]/div[2]/div[2]/h1""")
        month_data = month_info.text.strip()
    # 고정관리비
    try:
        manage_info = driver2.find_element_by_xpath("""//*[@id="root"]/div/div[3]/div[1]/div/div[4]/div[3]/div[2]/div[1]/div[2]""")
        manage_data = manage_info.text.strip()
        manage_data = manage_data.replace(",","")
    except NoSuchElementException:
        manage_info = driver2.find_element_by_xpath("""//*[@id="root"]/div/div[3]/div[1]/div/div[4]/div[4]/div[2]/div[1]/div[2]""")
        manage_data = manage_info.text.strip()
        manage_data = manage_data.replace(",","")
    except NoSuchElementException:
        manage_info = driver2.find_element_by_xpath("""//*[@id="root"]/div/div[3]/div[1]/div/div[4]/div[5]/div[2]/div[1]/div[2]""")
        manage_data = manage_info.text.strip()
        manage_data = manage_data.replace(",","")
    # 방 개수
    try:
        room_info = driver2.find_element_by_xpath("""//*[@id="root"]/div/div[3]/div[1]/div/div[4]/div[3]/div[2]/div[2]/div[2]""")
        room_data = room_info.text.strip()
        room_data = room_data.replace(",","").replace("<br/>","")
        max_len = len(room_data)
        loc = room_data.find("|")
        myroom_data = room_data[0:loc]
        washroom_data = room_data[loc+1:max_len]
    except NoSuchElementException:
        room_info = driver2.find_element_by_xpath("""//*[@id="root"]/div/div[3]/div[1]/div/div[4]/div[4]/div[2]/div[2]/div[2]""")
        room_data = room_info.text.strip()
        room_data = room_data.replace(",","").replace("<br/>","")
        max_len = len(room_data)
        loc = room_data.find("|")
        myroom_data = room_data[0:loc]
        washroom_data = room_data[loc+1:max_len]
    except NoSuchElementException:
        room_info = driver2.find_element_by_xpath("""//*[@id="root"]/div/div[3]/div[1]/div/div[4]/div[5]/div[2]/div[2]/div[2]""")
        room_data = room_info.text.strip()
        room_data = room_data.replace(",","").replace("<br/>","")
        max_len = len(room_data)
        loc = room_data.find("|")
        myroom_data = room_data[0:loc]
        washroom_data = room_data[max_len-1:max_len]

    i += 1

    # 파일에 내용을 입력
    f.write(house_name_data + "," + loc_data + "," + deposit_data + "," + month_data + "," +
    manage_data + "," + myroom_data + "," + washroom_data + "\n")

# 작업이 끝난 파일 닫음
f.close()

# 브라우저 종료
driver2.close()
driver.close()
