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
f.write("매물명,지역,면적,보증금,월세,인실,만실,평균보증금,평균임대료,고정관리비,공과금(1/N),방개수,화장실개수,전용면적,"
"쇼파,와이파이,에어컨,세탁기,건조대,청소기,전자레인지,냉장고,다리미,정수기,토스터기,전기포트")
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

    sleep(0.1)

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
    # 평균보증금
    try:
        deposit_info = driver2.find_element_by_xpath("""//*[@id="root"]/div/div[3]/div[1]/div/div[4]/div[3]/div[1]/div[2]/div[1]/h1""")
        deposit_data = deposit_info.text.strip()
        deposit_data = deposit_data.replace(",","")
    except NoSuchElementException:
        deposit_info = driver2.find_element_by_xpath("""//*[@id="root"]/div/div[3]/div[1]/div/div[4]/div[4]/div[1]/div[2]/div[1]/h1""")
        deposit_data = deposit_info.text.strip()
        deposit_data = deposit_data.replace(",","")
    # 평균임대료
    try:
        month_info = driver2.find_element_by_xpath("""//*[@id="root"]/div/div[3]/div[1]/div/div[4]/div[3]/div[1]/div[2]/div[2]/h1""")
        month_data = month_info.text.strip()
        month_data = month_data.replace(",","")
    except NoSuchElementException:
        month_info = driver2.find_element_by_xpath("""//*[@id="root"]/div/div[3]/div[1]/div/div[4]/div[4]/div[1]/div[2]/div[2]/h1""")
        month_data = month_info.text.strip()
        month_data = month_data.replace(",","")
    # 고정관리비/공과금
    try:
        manage_info = driver2.find_element_by_xpath("""//*[@id="root"]/div/div[3]/div[1]/div/div[4]/div[3]/div[2]/div[1]/div[2]""")
        manage_data = manage_info.text.strip()
        manage_data = manage_data.replace(",","")
        # 공과금
        if(manage_data.find("공과금") >= 0):
            dues_data = "O"
        else:
            dues_data = "X"
        # 고정 관리비
        if(manage_data.find("만") >=0 ):
            loc = manage_data.find("만")
            manage_data = manage_data[0:loc+1]
        else:
            manage_data = ""
    except NoSuchElementException:
        manage_info = driver2.find_element_by_xpath("""//*[@id="root"]/div/div[3]/div[1]/div/div[4]/div[4]/div[2]/div[1]/div[2]""")
        manage_data = manage_info.text.strip()
        manage_data = manage_data.replace(",","")
        # 공과금
        if(manage_data.find("공과금") >= 0):
            dues_data = "O"
        else:
            dues_data = "X"
        # 고정 관리비
        if(manage_data.find("만") >=0 ):
            loc = manage_data.find("만")
            manage_data = manage_data[0:loc+1]
        else:
            manage_data = ""
    # 방 개수
    try:
        room_info = driver2.find_element_by_xpath("""//*[@id="root"]/div/div[3]/div[1]/div/div[4]/div[3]/div[2]/div[2]/div[2]""")
        room_data = room_info.text.strip()
        room_data = room_data.replace(",","").replace("<br/>","")
        max_len = len(room_data)
        loc = room_data.find("|")
        # 방 개수
        myroom_data = room_data[0:loc]
        # 화장실 개수
        washroom_data = room_data[loc+1:max_len].replace("화장실","").replace(" ","")
    except NoSuchElementException:
        room_info = driver2.find_element_by_xpath("""//*[@id="root"]/div/div[3]/div[1]/div/div[4]/div[4]/div[2]/div[2]/div[2]""")
        room_data = room_info.text.strip()
        room_data = room_data.replace(",","").replace("<br/>","")
        max_len = len(room_data)
        loc = room_data.find("|")
        # 방 개수
        myroom_data = room_data[0:loc]
        # 화장실 개수
        washroom_data = room_data[loc+1:max_len].replace("화장실","").replace(" ","")
    # 전용면적
    try:
        size_info = driver2.find_element_by_xpath("""//*[@id="root"]/div/div[3]/div[1]/div/div[4]/div[3]/div[2]/div[5]/div[2]""")
        size_data = size_info.text.strip()
        size_data = size_data.replace(",","")
        if(size_data.find("공용")>=0 or size_data.find("주방")>=0):
            size_data=""
    except NoSuchElementException:
        size_info = driver2.find_element_by_xpath("""//*[@id="root"]/div/div[3]/div[1]/div/div[4]/div[4]/div[2]/div[5]/div[2]""")
        size_data = size_info.text.strip()
        size_data = size_data.replace(",","")
        if(size_data.find("공용")>=0 or size_data.find("주방")>=0):
            size_data=""
    # 제공시설
    try:
        facility_info = driver2.find_element_by_xpath("""//*[@id="root"]/div/div[3]/div[1]/div/div[4]/div[3]""")
        facility_data = facility_info.text.strip()
        # 쇼파, 와이파이, 에어컨, 세탁기, 건조대
        if(facility_data.find("쇼파")>=0):
            f_data1 = "O"
        else:
            f_data1 = "X"
        if(facility_data.find("공유기")>=0):
            f_data2 = "O"
        else:
            f_data2 = "X"
        if(facility_data.find("에어컨")>=0):
            f_data3 = "O"
        else:
            f_data3 = "X"
        if(facility_data.find("세탁기")>=0):
            f_data4 = "O"
        else:
            f_data4 = "X"
        if(facility_data.find("건조대")>=0):
            f_data5 = "O"
        else:
            f_data5 = "X"
        # 청소기,전자레인지,냉장고,다리미,정수기
        if(facility_data.find("청소기")>=0):
            f_data6 = "O"
        else:
            f_data6 = "X"
        if(facility_data.find("레인지")>=0):
            f_data7 = "O"
        else:
            f_data7 = "X"
        if(facility_data.find("냉장고")>=0):
            f_data8 = "O"
        else:
            f_data8 = "X"
        if(facility_data.find("다리미")>=0):
            f_data9 = "O"
        else:
            f_data9 = "X"
        if(facility_data.find("정수기")>=0):
            f_data10 = "O"
        else:
            f_data10 = "X"
         # 토스터기,전기포트
        if(facility_data.find("토스터")>=0):
            f_data11 = "O"
        else:
            f_data11 = "X"
        if(facility_data.find("전기")>=0):
            f_data12 = "O"
        else:
            f_data12 = "X"
    except NoSuchElementException:
        facility_info = driver2.find_element_by_xpath("""//*[@id="root"]/div/div[3]/div[1]/div/div[4]/div[4]""")
        facility_data = facility_info.text.strip()
        # 쇼파, 와이파이, 에어컨, 세탁기, 건조대
        if(facility_data.find("쇼파")>=0):
            f_data1 = "O"
        else:
            f_data1 = "X"
        if(facility_data.find("공유기")>=0):
            f_data2 = "O"
        else:
            f_data2 = "X"
        if(facility_data.find("에어컨")>=0):
            f_data3 = "O"
        else:
            f_data3 = "X"
        if(facility_data.find("세탁기")>=0):
            f_data4 = "O"
        else:
            f_data4 = "X"
        if(facility_data.find("건조대")>=0):
            f_data5 = "O"
        else:
            f_data5 = "X"
        # 청소기,전자레인지,냉장고,다리미,정수기
        if(facility_data.find("청소기")>=0):
            f_data6 = "O"
        else:
            f_data6 = "X"
        if(facility_data.find("레인지")>=0):
            f_data7 = "O"
        else:
            f_data7 = "X"
        if(facility_data.find("냉장고")>=0):
            f_data8 = "O"
        else:
            f_data8 = "X"
        if(facility_data.find("다리미")>=0):
            f_data9 = "O"
        else:
            f_data9 = "X"
        if(facility_data.find("정수기")>=0):
            f_data10 = "O"
        else:
            f_data10 = "X"
         # 토스터기,전기포트
        if(facility_data.find("토스터")>=0):
            f_data11 = "O"
        else:
            f_data11 = "X"
        if(facility_data.find("전기")>=0):
            f_data12 = "O"
        else:
            f_data12 = "X"

    # 각 방
    try:
        driver2.find_element_by_xpath("""//*[@id="root"]/div/div[3]/div[1]/div/div[4]/div[5]/div[4]/h1/span[1]""").click()
    except:
        print("Cannot click 전체방 보기")
    j=1
    for item in range(j,10):
        try:
            dt_room_info = driver2.find_element_by_xpath("""//*[@id="root"]/div/div[3]/div[1]/div/div[4]/div[5]/div[4]/div[1]/table/tbody[""" +  str(j) + """]""")
            dt_room_data = dt_room_info.text.strip()
            # 면적
            if(dt_room_data.find("㎡") >= 0):
                dt_loc1 = dt_room_data.find("㎡")
                dt_data1 = dt_room_data[dt_loc1-4:dt_loc1]
            else:
                dt_data1=""
            # 보증금
            try:
                dt_data3_info = driver2.find_element_by_xpath("""//*[@id="root"]/div/div[3]/div[1]/div/div[4]/div[5]/div[4]/div[1]/table/tbody[""" +  str(j) + """]/tr[1]/td[2]""")
                dt_data2 = dt_data2_info.text.strip()
            except:
                dt_data2=""
            # 월세
            try:
                dt_data3_info = driver2.find_element_by_xpath("""//*[@id="root"]/div/div[3]/div[1]/div/div[4]/div[5]/div[4]/div[1]/table/tbody[""" +  str(j) + """]/tr[1]/td[3]""")
                dt_data3 = dt_data3_info.text.strip()
            except:
                dt_data3=""
            # 인실
            if(dt_room_data.find("인실") >= 0):
                dt_loc1 = dt_room_data.find("인실")
                dt_data4 = dt_room_data[dt_loc1-1:dt_loc1+1]
            else:
                dt_data4=""
            # 만실
            if(dt_room_data.find("공실") >= 0):
                dt_data5 = "X"
            elif(dt_room_data.find("입주") >=0):
                dt_data5 = "O"
            else:
                dt_data5=""

             # 파일에 내용을 입력 면적,보증금,월세,인실,만실
            f.write(house_name_data + "," + loc_data + "," +
            dt_data1 + "," + dt_data2 + "," + dt_data3 + "," + dt_data4 + "," + dt_data5 + "," + 
            deposit_data + "," + month_data + "," +
            manage_data + "," + dues_data + "," +
            myroom_data + "," + washroom_data + "," + 
            size_data + "," + 
            f_data1 + "," + f_data2 + "," + f_data3 + "," + f_data4 + "," + f_data5 + "," + 
            f_data6 + "," + f_data7 + "," + f_data8 + "," + f_data9 + ","+ f_data10 + "," + 
            f_data11 + "," + f_data12 + "\n")

            j += 1
        except:
            break

    i += 1

# 작업이 끝난 파일 닫음
f.close()

# 브라우저 종료
driver2.close()
driver.close()
