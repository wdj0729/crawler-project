from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from time import *
import pickle
from selenium.common.exceptions import *

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

# content 담은 리스트 
data_list = []
listing_time=time()-start
print(listing_time)

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

    # 하우스 상세정보
    try: 
        detail_info = driver2.find_element_by_class_name("_Detail_info-detail__2OFZf")
        detail_info_data = detail_info.text.strip()
        detail_info_more = driver2.find_element_by_class_name("_Detail_info-detail-more__2n2DX")
        detail_info_more_data = detail_info_more.text.strip()
    except NoSuchElementException:
        pass
    # 방 정보
    try: 
        detail_room_info = driver2.find_element_by_class_name("_Detail_room_infomation__1fFZk")
        detail_room_info_data1 = detail_room_info.text.strip()
    except NoSuchElementException:
        pass
    # 하우스 소개
    try:
        detail_house_loc = driver2.find_element_by_class_name("_Detail_house-location__3yOQ6")
        detail_house_loc_data = detail_house_loc.text.strip()
    except NoSuchElementException:
        pass
    # 운영자 소개
    try:
        detail_master_info = driver2.find_element_by_class_name("_Detail_master-info__ftLT-")
        detail_master_info_data = detail_master_info.text.strip()
    except NoSuchElementException:
        pass

     # 딕셔너리에 데이터(리스트 형태)로 저장
    dic = {"하우스 상세정보1": detail_info_data, "하우스 상세정보2": detail_info_more_data,
            "방 정보1": detail_room_info_data1, "하우스 소개": detail_house_loc_data, "운영자 소개": detail_master_info_data}
    print("딕셔너리 :", dic)

    # 리스트에 딕셔너리 저장
    data_list.append(dic)

    i += 1

    print(time()-detail_start)

# 브라우저 종료
driver2.close()
driver.close()

# 파일 쓰기
with open("comeandstay_detail.pickle","wb") as fw:
    pickle.dump(data_list, fw)
