from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from time import *
from selenium.common.exceptions import *
import csv
import pickle

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
soup = BeautifulSoup(html, 'html.parser')

# 상세 페이지 매물 링크 저장
house_list_warp_elem = driver.find_element_by_xpath("""//*[@id="root"]/div[3]/div[2]/div[1]/div[2]""")
house_lists_elem = house_list_warp_elem.find_elements_by_tag_name("a")

detail_link_list = []

for house in house_lists_elem:
    detail_link_list.append(house.get_property("href"))

# 중복 제거
detail_link_list = list(set(detail_link_list))
try:
    detail_link_list.remove("https://sharekim.com/detail/3540")
except ValueError:
    pass

# 크롤링 걸리는 시간
listing_time=time()-start
print(listing_time)
# 지점 인덱스
house_id = 1

driver2 = webdriver.Chrome(path)
driver2.maximize_window()

# 지점 리스트
house_list = []

for item in detail_link_list:
    detail_start=time()
    print("지점 링크주소:", item)
    print("지점 인덱스:", house_id)

    # div 에러 방지 인덱스
    j=3

    # 셰어킴 상세페이지
    driver2.get(item)

    WebDriverWait(driver2, 5).until(
        EC.presence_of_element_located((By.ID, "root"))
    )

    # 매물명
    try:
        house_info = driver2.find_element_by_xpath("""//*[@id="blur-wrap"]/div[3]/div[1]/div[2]/div/div[1]/div[2]/div/div[2]""")
        house_info_data = house_info.text.strip()
        max_len = len(house_info_data)
        loc = house_info_data.find(":")
        house_name = house_info_data[loc+2:max_len].replace(",","").replace("\n","")
    except NoSuchElementException:
        pass
    # 상세 정보
    try:
        detail_info = driver2.find_element_by_xpath("""//*[@id="blur-wrap"]/div[3]/div[1]/div[1]/div[2]/section""")
        detail_info_data = detail_info.text.strip()
        # 건물형태
        if(detail_info_data.find("빌라") >= 0):
            house_type = "villa"
        elif(detail_info_data.find("아파트") >= 0):
            house_type = "apt"
        elif(detail_info_data.find("단독주택") >= 0):
            house_type = "house"
        elif(detail_info_data.find("원룸") >= 0):
            house_type = "oneroom"
        elif(detail_info_data.find("오피스텔") >= 0):
            house_type = "office"
        elif(detail_info_data.find("기타") >= 0):
            house_type = "etc"
        else:
            house_type = "NULL"
        # 방
        if(detail_info_data.find("방") >= 0):
            loc = detail_info_data.find("방")
            total_room_info = driver2.find_element_by_xpath("""//*[@id="blur-wrap"]/div[3]/div[2]/div[1]/section[1]/h5[2]""")
            total_room = total_room_info.text.strip()
            loc1 = total_room.find("(")
            loc2 = total_room.find(")")
            total_room = int(total_room[loc1:loc2].replace("(","").replace(")","").replace(" ",""))
            room_cnt = total_room
        else:
            room_cnt = -1
        # 화장실
        if(detail_info_data.find("화장실") >= 0):
            loc = detail_info_data.find("화장실")
            washroom_cnt = int(detail_info_data[loc+3:loc+5].replace("\n","").replace(" ",""))
        else:
            washroom_cnt = -1
        # 층
        if(detail_info_data.find("총층") >= 0):
            loc = detail_info_data.find("총층")
            now_floor = detail_info_data[loc+2:loc+5].replace("\n","").replace(" ","")
            if(now_floor.find("지하")>=0):
                now_floor = int(-1)
            else:
                now_floor = int(now_floor.replace("층","").replace(" ",""))
        else:
            now_floor = -1
        # 총층
        if(detail_info_data.find("층/총층") >= 0):
            loc = detail_info_data.find("층/총층")
            total_floor = detail_info_data[loc+7:loc+10].replace("\n","").replace("/","")
            total_floor = int(total_floor.replace("층",""))
        else:
            total_floor = -1
        # 전체면적
        if(detail_info_data.find("㎡") >= 0):
            loc1 = detail_info_data.find("적")
            loc2 = detail_info_data.find("㎡")
            house_area = float(detail_info_data[loc1+1:loc2].replace("\n","").replace(" ",""))
        else :
            house_area = -1
    except NoSuchElementException:
        pass
    # 입지 정보
    try:
        # 도로명주소
        address = driver2.find_element_by_xpath("""//*[@id="blur-wrap"]/div[3]/div[2]/div[1]/section[2]/p""")
        road_address = address.text.strip()
    except NoSuchElementException:
        pass
    # 입주 상담 성별전용,면적,보증금,월세,인실,만실
    for item in range(0,total_room):
        try:
            unit_room = driver2.find_element_by_xpath("""//*[@id="blur-wrap"]/div[3]/div[2]/div[1]/section[1]/div[""" + str(j) + """]""")
            unit_room_data = unit_room.text.strip()
            room_for=-1
            is_full="F"
            # 성별전용
            if(unit_room_data.find("여성") >= 0):
                gender = "F"
            elif(unit_room_data.find("남성") >= 0):
                gender = "M"
            elif(unit_room_data.find("무관") >= 0):
                gender = "N"
            else:
                pass
            # 면적
            if(unit_room_data.find("㎡") >= 0):
                unit_loc1 = unit_room_data.find("(")
                unit_loc2 = unit_room_data.find("㎡")
                room_area = unit_room_data[unit_loc1+1:unit_loc2].replace("\n,","")
                if(room_area.find(")") >= 0):
                    unit_loc3 = room_area.find(")")
                    room_area = room_area[unit_loc3+1:unit_loc2].replace("\n","").replace("(","")
                room_area = float(room_area.replace(" ",""))
            else:
                room_area = -1
            # 보증금
            unit_loc = unit_room_data.find("/")
            deposit = unit_room_data[unit_loc-5:unit_loc-1].replace("\n","").replace("개","").replace("월","")
            deposit = deposit.replace(",","").replace(".","").replace(" ","")
            if(deposit == "0"):
                deposit = "0"
            else:
                deposit += "0000"
            deposit = int(deposit)
            #월세
            unit_loc2 = unit_room_data.find("만원")
            monthly_rent = unit_room_data[unit_loc+1:unit_loc2].replace(" ","").replace("\n","")
            monthly_rent = monthly_rent.replace(",","").replace(".","")
            if(monthly_rent == "0"):
                monthly_rent = "0"
            else:
                monthly_rent += "0000"
            monthly_rent = int(monthly_rent)
            # 인실
            unit_loc3 = unit_room_data.find("실")
            room_for = int(unit_room_data[unit_loc3-2:unit_loc3-1].replace("\n","").replace(" ",""))
            # 만실
            if(unit_room_data.find("만실") >= 0):
                is_full = "T"
            else:
                is_full = "F"  
        except:
            pass

        dic = [{'house_name': house_name, 'gender': gender, 'house_area': house_area, 'house_type': house_type,
        'room_cnt': room_cnt, 'washroom_cnt': washroom_cnt, 'now_floor': now_floor, 'total_floor': total_floor,
        'road_address': road_address, 
        'rooms':[{'room_area': room_area, 'room_for':room_for,
        'beds':[{'is_full': is_full, 'deposit': deposit, 'monthly_rent':monthly_rent}]}]}]

        print(dic)

        house_list.append(dic)

        print(time()-detail_start)

        j += 1

    house_id += 1

# 브라우저 종료
driver2.close()
driver.close()

# 파일 쓰기
with open("sharekim.pickle","wb") as fw:
    pickle.dump(house_list, fw)
