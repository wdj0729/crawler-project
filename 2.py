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

# test.csv파일을 쓰기모드(w)로 열기
f = open("test.csv","w",encoding="UTF-8")
# 헤더 추가하기
f.write("매물명,건물형태,방,화장실,층,전체면적,난방방식,"
"승강기,주차,반려동물,흡연,조리도구,식기류,전자레인지,전기포트,에어컨,정수기,"
"세탁기,식탁,청소기,신발장,냉장고,와이파이,커피포트,수납함,청소서비스,의자,"
"분리수거함,가스레인지,토스터,TV,소파,다리미,커튼,소독,전신거울,"
"빨래건조대,옷장,테라스,밥솥,스탠드,건조기,도로명주소")
f.write("\n")

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

# content 담은 리스트
data_list = []
listing_time=time()-start
print(listing_time)
# 인덱스
i = 1

driver2 = webdriver.Chrome(path)
driver2.maximize_window()

for item in detail_link_list:
    detail_start=time()
    print("주소:", item)
    print("인덱스:", i)

    # 셰어킴 상세페이지
    driver2.get(item)

    WebDriverWait(driver2, 5).until(
        EC.presence_of_element_located((By.ID, "root"))
    )

    # 매물명
    try:
        product_info = driver2.find_element_by_xpath("""//*[@id="blur-wrap"]/div[3]/div[1]/div[2]/div/div[1]/div[2]/div/div[2]""")
        product_info_data = product_info.text.strip()
        max_len = len(product_info_data)
        loc = product_info_data.find(":")
        product_info_data = product_info_data[loc+2:max_len]
    except NoSuchElementException:
        pass
    # 하우스 정보
    '''
    try:
        house_info = driver2.find_element_by_xpath("""//*[@id="blur-wrap"]/div[3]/div[1]/div[1]/section[2]/div[2]""")
        house_info_data = house_info.text.strip()
    except NoSuchElementException:
        pass
    '''
    # 상세 정보
    try:
        detail_info = driver2.find_element_by_xpath("""//*[@id="blur-wrap"]/div[3]/div[1]/div[1]/div[2]/section""")
        detail_info_data = detail_info.text.strip()
        # 건물형태
        if(detail_info_data.find("빌라") >= 0):
            dt_data1 = "빌라"
        elif(detail_info_data.find("아파트") >= 0):
            dt_data1 = "아파트"
        elif(detail_info_data.find("단독주택") >= 0):
            dt_data1 = "단독주택"
        elif(detail_info_data.find("기타") >= 0):
            dt_data1 = "기타"
        else:
            dt_data1 = ""
        # 방
        if(detail_info_data.find("방") >= 0):
            loc = detail_info_data.find("방")
            dt_data2 = detail_info_data[loc+2:loc+4].strip('\n')
            if(dt_data2.find("개")==-1):
                dt_data2 += "개"
        else:
            dt_data2 = ""
        # 화장실
        if(detail_info_data.find("화장실") >= 0):
            loc = detail_info_data.find("화장실")
            dt_data3 = detail_info_data[loc+4:loc+6].strip('\n')
            if(dt_data3.find("개")==-1):
                dt_data3 += "개"
        else:
            dt_data3 = ""
        # 층
        if(detail_info_data.find("층") >= 0):
            loc = detail_info_data.find("층")
            dt_data4 = detail_info_data[loc+5:loc+8].strip('/')
        else:
            dt_data4 = ""
        # 면적
        if(detail_info_data.find("평") >= 0):
            loc = detail_info_data.find("평")
            dt_data5 = detail_info_data[loc-2:loc+1].strip('(')
        else :
            dt_data5 = ""
        # 난방방식
        if(detail_info_data.find("방식") >= 0):
            loc = detail_info_data.find("방식")
            dt_data6 = detail_info_data[loc+3:loc+7].strip('\n')
        else:
            dt_data6 = ""
        # 승강기
        if(detail_info_data.find("승강기") >= 0):
            loc = detail_info_data.find("승강기")
            dt_data7 = detail_info_data[loc+4:loc+6].strip('\n')
            if(dt_data7.find("알") >= 0 ):
                dt_data7="알수없음"
        else:
            dt_data7 = ""
        # 주차
        if(detail_info_data.find("주차") >= 0):
            loc = detail_info_data.find("주차")
            dt_data8 = detail_info_data[loc+3:loc+6].strip('\n')
            if(dt_data8.find("반") >= 0):
                dt_data8=""
            elif(dt_data8.find("알") >= 0 ):
                dt_data8="알수없음"
        else:
            dt_data8 = ""
        # 반려동물
        if(detail_info_data.find("동물") >= 0):
            loc = detail_info_data.find("동물")
            dt_data9 = detail_info_data[loc+3:loc+6].strip('\n')
            if(dt_data9.find("흡") >= 0):
                dt_data9=""
        else:
            dt_data9 = ""
        # 흡연
        if(detail_info_data.find("흡연") >= 0):
            loc = detail_info_data.find("흡연")
            dt_data10 = detail_info_data[loc+3:loc+6].strip('\n')
            if(dt_data10.find("협") >= 0):
                dt_data10="별도협의"
        else:
            dt_data10 = ""
    except NoSuchElementException:
        pass
    # 공간 정보
    try:
        option_info = driver2.find_element_by_xpath("""//*[@id="blur-wrap"]/div[3]/div[1]/div[1]/section[4]/div[2]""")
        option_info_data = option_info.text.strip()
        # 조리도구, 식기류, 전자레인지, 전기포트, 에어컨
        if(option_info_data.find("조리도구") >= 0):
            op_data1="O"
        else:
            op_data1="X"
        if(option_info_data.find("식기") >= 0):
            op_data2= "O"
        else:
            op_data2="X"
        if(option_info_data.find("전자레인지") >= 0):
            op_data3= "O"
        else:
            op_data3="X"
        if(option_info_data.find("전기포트") >= 0):
            op_data4= "O"
        else:
            op_data4="X"
        if(option_info_data.find("에어컨") >= 0):
            op_data5= "O"
        else:
            op_data5="X"
        # 정수기, 세탁기, 식탁, 청소기, 신발장
        if(option_info_data.find("정수기") >= 0):
            op_data6="O"
        else:
            op_data6="X"
        if(option_info_data.find("세탁기") >= 0):
            op_data7= "O"
        else:
            op_data7="X"
        if(option_info_data.find("식탁") >= 0):
            op_data8= "O"
        else:
            op_data8="X"
        if(option_info_data.find("청소기") >= 0):
            op_data9= "O"
        else:
            op_data9="X"
        if(option_info_data.find("신발장") >= 0):
            op_data10= "O"
        else:
            op_data10="X"
        # 냉장고, 와이파이, 커피포트, 수납합, 청소서비스
        if(option_info_data.find("냉장고") >= 0):
            op_data11="O"
        else:
            op_data11="X"
        if(option_info_data.find("와이파이") >= 0):
            op_data12= "O"
        else:
            op_data12="X"
        if(option_info_data.find("커피포트") >= 0):
            op_data13= "O"
        else:
            op_data13="X"
        if(option_info_data.find("수납함") >= 0):
            op_data14= "O"
        else:
            op_data14="X"
        if(option_info_data.find("청소서비스") >= 0):
            op_data15= "O"
        else:
            op_data15="X"
        # 의자,분리수거함, 가스레인지, 토스터, TV
        if(option_info_data.find("의자") >= 0):
            op_data16="O"
        else:
            op_data16="X"
        if(option_info_data.find("분리수거함") >= 0):
            op_data17= "O"
        else:
            op_data17="X"
        if(option_info_data.find("가스레인지") >= 0):
            op_data18= "O"
        else:
            op_data18="X"
        if(option_info_data.find("토스터") >= 0):
            op_data19= "O"
        else:
            op_data19="X"
        if(option_info_data.find("TV") >= 0):
            op_data20= "O"
        else:
            op_data20="X"
        # 소파, 다리미, 커튼, 소독, 전신거울
        if(option_info_data.find("소파") >= 0):
            op_data21="O"
        else:
            op_data21="X"
        if(option_info_data.find("다리미") >= 0):
            op_data22= "O"
        else:
            op_data22="X"
        if(option_info_data.find("커튼") >= 0):
            op_data23= "O"
        else:
            op_data23="X"
        if(option_info_data.find("소독") >= 0):
            op_data24= "O"
        else:
            op_data24="X"
        if(option_info_data.find("전신거울") >= 0):
            op_data25= "O"
        else:
            op_data25="X"
        # 빨래건조대, 옷장, 테라스, 밥솥, 스탠드
        if(option_info_data.find("빨래건조대") >= 0):
            op_data26="O"
        else:
            op_data26="X"
        if(option_info_data.find("옷장") >= 0):
            op_data27= "O"
        else:
            op_data27="X"
        if(option_info_data.find("테라스") >= 0):
            op_data28= "O"
        else:
            op_data28="X"
        if(option_info_data.find("밥솥") >= 0):
            op_data29= "O"
        else:
            op_data29="X"
        if(option_info_data.find("스탠드") >= 0):
            op_data30= "O"
        else:
            op_data30="X"
        # 건조기
        if(option_info_data.find("건조기") >= 0):
            op_data31= "O"
        else:
            op_data31="X"
    except NoSuchElementException:
        pass
    # 입주 상담
    '''
    try:
        price = driver2.find_element_by_xpath("""//*[@id="blur-wrap"]/div[3]/div[2]/div[1]/section[1]""")
        price_data = price.text.strip()
    except NoSuchElementException:
        pass
    '''
    # 입지 정보
    try:
        address = driver2.find_element_by_xpath("""//*[@id="blur-wrap"]/div[3]/div[2]/div[1]/section[2]/p""")
        address_data = address.text.strip()
    except NoSuchElementException:
        pass

    print(time()-detail_start)

    # 파일에 내용을 입력
    f.write(product_info_data + "," + dt_data1 + "," + dt_data2 + "," + 
    dt_data3 + "," + dt_data4 + "," + dt_data5 + "," + dt_data6 + "," + dt_data7 + "," +
    dt_data8 + "," + dt_data9 + "," + dt_data10 + "," + op_data1 + "," + op_data2 + "," + 
    op_data3 + "," + op_data4 + "," + op_data5 + "," + op_data6 + "," + op_data7 + "," +
    op_data8 + "," + op_data9 + "," + op_data10 + ","+ op_data11 + "," + op_data12 + "," + 
    op_data13 + "," + op_data14 + "," + op_data15 + "," + op_data16 + "," + op_data17 + "," +
    op_data18 + "," + op_data19 + "," + op_data20 + "," + op_data21 + "," + op_data22 + "," + 
    op_data23 + "," + op_data24 + "," + op_data25 + "," + op_data26 + "," + op_data27 + "," +
    op_data28 + "," + op_data29 + "," + op_data30 + "," + op_data31 + "," + address_data + "\n")

    i += 1

# 작업이 끝난 파일 닫음
f.close()

# 브라우저 종료
driver2.close()
driver.close()
