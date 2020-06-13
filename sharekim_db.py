import pickle, csv
import sys
import pymysql
import string
from time import *

from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
        sleep(0.5)
        if initial_wrap_height == after_exec_wrap_height:
            break
        else:
            continue

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
try:
    detail_link_list.remove("https://sharekim.com/detail/4706")
except ValueError:
    pass

# 크롤링 걸리는 시간
listing_time = time() - start
print(listing_time)
print(len(detail_link_list))
# 지점 인덱스
house_id = 1

driver2 = webdriver.Chrome(path)
driver2.maximize_window()

driver3 = webdriver.Chrome(path)
driver3.maximize_window()

driver3.get("http://www.juso.go.kr/support/AddressMainSearch.do?searchType=TOTAL")

# 지점 리스트
house_list = []

for item in detail_link_list:
    detail_start = time()
    print("지점 링크주소:", item)
    print("지점 인덱스:", house_id)

    # div 에러 방지 인덱스
    j = 3

    # 셰어킴 상세페이지
    driver2.get(item)

    WebDriverWait(driver2, 5).until(
        EC.presence_of_element_located((By.ID, "root"))
    )

    # 매물명
    try:
        house_info = driver2.find_element_by_xpath(
            """//*[@id="blur-wrap"]/div[3]/div[1]/div[2]/div/div[1]/div[2]/div/div[2]""")
        house_info_data = house_info.text.strip()
        max_len = len(house_info_data)
        loc = house_info_data.find(":")
        house_name = house_info_data[loc + 2:max_len].replace(",", "").replace("\n", "")
    except NoSuchElementException:
        pass
    # 상세 정보
    try:
        detail_info = driver2.find_element_by_xpath("""//*[@id="blur-wrap"]/div[3]/div[1]/div[1]/div[2]/section""")
        detail_info_data = detail_info.text.strip()
        # 건물형태
        if detail_info_data.find("빌라") >= 0:
            house_type = "villa"
        elif detail_info_data.find("아파트") >= 0:
            house_type = "apt"
        elif detail_info_data.find("단독주택") >= 0:
            house_type = "house"
        elif detail_info_data.find("원룸") >= 0:
            house_type = "oneroom"
        elif detail_info_data.find("오피스텔") >= 0:
            house_type = "office"
        elif detail_info_data.find("기타") >= 0:
            house_type = "etc"
        else:
            house_type = None
        # 방
        if detail_info_data.find("방") >= 0:
            loc = detail_info_data.find("방")
            total_room_info = driver2.find_element_by_xpath(
                """//*[@id="blur-wrap"]/div[3]/div[2]/div[1]/section[1]/h5[2]""")
            total_room = total_room_info.text.strip()
            loc1 = total_room.find("(")
            loc2 = total_room.find(")")
            total_room = int(total_room[loc1:loc2].replace("(", "").replace(")", "").replace(" ", ""))
            room_cnt = total_room
        else:
            room_cnt = None
        # 화장실
        if detail_info_data.find("화장실") >= 0:
            loc = detail_info_data.find("화장실")
            washroom_cnt = int(detail_info_data[loc + 3:loc + 5].replace("\n", "").replace(" ", ""))
        else:
            washroom_cnt = None
        # 층
        if detail_info_data.find("총층") >= 0:
            loc = detail_info_data.find("총층")
            now_floor = detail_info_data[loc + 2:loc + 5].replace("\n", "").replace(" ", "")
            if now_floor.find("지하") >= 0:
                now_floor = None
            else:
                now_floor = int(now_floor.replace("층", "").replace(" ", ""))
        else:
            now_floor = None
        # 총층
        if detail_info_data.find("층/총층") >= 0:
            loc = detail_info_data.find("층/총층")
            total_floor = detail_info_data[loc + 7:loc + 10].replace("\n", "").replace("/", "")
            total_floor = int(total_floor.replace("층", ""))
        else:
            total_floor = None
        # 전체면적
        if detail_info_data.find("㎡") >= 0:
            loc1 = detail_info_data.find("적")
            loc2 = detail_info_data.find("㎡")
            house_area = float(detail_info_data[loc1 + 1:loc2].replace("\n", "").replace(" ", ""))
        else:
            house_area = None
    except NoSuchElementException:
        pass
    # 입지 정보
    try:
        # 도로명주소
        address = driver2.find_element_by_xpath("""//*[@id="blur-wrap"]/div[3]/div[2]/div[1]/section[2]/p""")
        road_address = address.text.strip()

        driver3.find_element_by_xpath("""//*[@id="keyword"]""").clear()

        driver3.find_element_by_xpath("""//*[@id="keyword"]""").send_keys(road_address)
        sleep(0.1)
        driver3.find_element_by_xpath("""//*[@id="searchButton"]""").click()

        district = None
        building = None
        building_data = None

        building_info = driver3.find_element_by_xpath("""//*[@id="list1"]/div[2]/span[2]""")
        building_data = building_info.text.strip()

        # 구로구일 경우
        if building_data.find("구로구") >= 0:
            district = "구로구"
            building = "구로동"
        # 구 찾으면
        elif building_data.find("구") >= 0:
            loc1 = building_data.find("구")
            district = building_data[loc1 - 3:loc1 + 1].replace("시", "").replace("별", "").replace(" ", "")
            # 동
            if building_data.find("동") >= 0:
                building = building_data[loc1 + 2:loc1 + 6].strip()
                building = "".join([i for i in building if not i.isdigit()])
                # 필동가 -> 필동
                if building == "필동가":
                    building = "필동"
            else:
                building = None
        # 구 못 찾을 경우
        else :
            district = None
            building = None

    except NoSuchElementException:
        loc1 = road_address.find("구")
        district = road_address[loc1-3:loc1 +1].replace("시", "").replace("별", "").replace(" ", "")
        loc2 = road_address.find("동")
        building = building_data[loc2-3:loc2 +1].strip()
        building = "".join([i for i in building if not i.isdigit()])
        pass
    
    # 경기도, 인천시 제외
    if road_address.find("경기") >=0:
        pass
    elif road_address.find("인천") >=0:
        pass
    # 서울시
    else:
        # SQL문 및 Placeholer data
        insert_into_house_SQL = """insert into sharehouse.houses 
        (house_name, area, house_type, room_cnt,washroom_cnt, now_floor, total_floor, road_address, district, building)
            values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""

        insert_into_room_SQL = """
        insert into sharehouse.rooms (room_name, gender, bed_cnt, area, house_id) 
        values (%s, %s, %s, %s, (select id from houses where house_name = %s));
        """

        insert_into_bed_SQL = """
        insert into sharehouse.beds (is_full, deposit, monthly_rent, room_id) 
        values (%s, %s, %s, (select id from rooms where house_id=(select id from houses where house_name=%s) and room_name=%s));
        """

        house_sql_data = [house_name, house_area, house_type, room_cnt, washroom_cnt, now_floor, total_floor, road_address,
                        district, building]

        # db커넥터 연결
        try:
            shareHouse_db = pymysql.connect(user='root', passwd='1234', host='localhost', db='sharehouse', charset='utf8')
            cursor = shareHouse_db.cursor(pymysql.cursors.DictCursor)

            cursor.execute(insert_into_house_SQL, house_sql_data)
            shareHouse_db.commit()
            print("successful house_data insertion")
            print(house_sql_data)
            print("-----------------------------")
        except Exception as e:
            _, _, tb = sys.exc_info()
            print('error line No = {}'.format(tb.tb_lineno))
            print(e)
            print(house_sql_data)
        finally:
            shareHouse_db.close()

        # 입주 상담 성별전용,면적,보증금,월세,인실,만실
        for i in range(0, total_room):

            try:
                unit_room = driver2.find_element_by_xpath(
                    """//*[@id="blur-wrap"]/div[3]/div[2]/div[1]/section[1]/div[""" + str(j) + """]""")
                unit_room_data = unit_room.text.strip()
                room_for = 1

                is_full = "F"
                # 성별전용
                if unit_room_data.find("여성") >= 0:
                    gender = "F"
                elif unit_room_data.find("남성") >= 0:
                    gender = "M"
                elif unit_room_data.find("무관") >= 0:
                    gender = "N"
                else:
                    gender = None
                # 면적
                if unit_room_data.find("㎡") >= 0:
                    unit_loc1 = unit_room_data.find("(")
                    unit_loc2 = unit_room_data.find("㎡")
                    room_area = unit_room_data[unit_loc1 + 1:unit_loc2].replace("\n,", "")
                    if room_area.find(")") >= 0:
                        unit_loc3 = room_area.find(")")
                        room_area = room_area[unit_loc3 + 1:unit_loc2].replace("\n", "").replace("(", "")
                    room_area = float(room_area.replace(" ", ""))
                else:
                    room_area = None

                # 인실
                unit_loc3 = unit_room_data.find("실")
                room_for = int(unit_room_data[unit_loc3 - 2:unit_loc3 - 1].replace("\n", "").replace(" ", ""))
                # 침대 개수
                bed_cnt = room_for
                # 만실
                if unit_room_data.find("즉시입주") >= 0:
                    is_full = "F"
                else:
                    is_full = "T"

                # 방 이름
                room_section_elem = driver2.find_element_by_xpath(
                    """//*[@id="blur-wrap"]/div[3]/div[2]/div[1]/section[1]""")
                unit_select_items_elem = room_section_elem.find_elements_by_class_name("UnitSelctItem")

                room_name = unit_select_items_elem[i].find_elements_by_tag_name("span")[0].text
                room_sql_data = [room_name, gender, bed_cnt, room_area, house_name]

                bed_label_elems = unit_select_items_elem[i].find_elements_by_tag_name("label")

            except Exception as e:
                _, _, tb = sys.exc_info()
                print('error line No = {}'.format(tb.tb_lineno))
                print(e)

            try:
                shareHouse_db = pymysql.connect(user='root', passwd='1234', host='localhost', db='sharehouse',
                                                charset='utf8')
                cursor = shareHouse_db.cursor(pymysql.cursors.DictCursor)
                cursor.execute(insert_into_room_SQL, room_sql_data)
                shareHouse_db.commit()
                print("successful room_data insertion")
                print(room_sql_data)
                print("-----------------------------")
            except Exception as e:
                _, _, tb = sys.exc_info()
                print('error line No = {}'.format(tb.tb_lineno))
                print(e)
                print(room_sql_data)
            finally:
                shareHouse_db.close()

            # 각 침대 만실, 보증금, 월세
            for bed in bed_label_elems:

                try:
                    badge_span_elem = bed.find_elements_by_tag_name('span')[1]
                    print(badge_span_elem.text)
                    # div 예외처리
                    if badge_span_elem.text == "상세설명" :
                        badge_span_elem = bed.find_elements_by_tag_name('span')[4]
                        # 만실
                        if badge_span_elem.text == "만실":
                            is_full = True
                        else:
                            is_full = False

                        rentFee_elem = bed.find_elements_by_tag_name('span')[6]
                        print(rentFee_elem.text)
                        rentFee = str(rentFee_elem.text)[:str(rentFee_elem.text).find('만원')].split('/')
                        # 보증금
                        deposit = rentFee[0].strip()
                        # 월세
                        monthly_rent = rentFee[1].strip()
                        bed_sql_data = [is_full, deposit, monthly_rent, house_name, room_name]
                    else :
                        # 만실
                        if badge_span_elem.text == "만실":
                            is_full = True
                        else:
                            is_full = False
                        
                        rentFee_elem = bed.find_elements_by_tag_name('span')[3]
                        print(rentFee_elem.text)
                        rentFee = str(rentFee_elem.text)[:str(rentFee_elem.text).find('만원')].split('/')
                        # 보증금
                        deposit = rentFee[0].strip()
                        # 월세
                        monthly_rent = rentFee[1].strip()
                        bed_sql_data = [is_full, deposit, monthly_rent, house_name, room_name]
                except Exception as e:
                    _, _, tb = sys.exc_info()
                    print('error line No = {}'.format(tb.tb_lineno))
                    print(bed_sql_data)
                    print(e)

                try:
                    shareHouse_db = pymysql.connect(user='root', passwd='1234', host='localhost', db='sharehouse',
                                                    charset='utf8')
                    cursor = shareHouse_db.cursor(pymysql.cursors.DictCursor)
                    cursor.execute(insert_into_bed_SQL, bed_sql_data)
                    shareHouse_db.commit()
                    print("successful bed_data insertion")
                    print(bed_sql_data)
                    print("-----------------------------")
                except Exception as e:
                    print(bed_sql_data)
                    print(e)
                finally:
                    shareHouse_db.close()

            j += 1

        house_id += 1

# 브라우저 종료
driver3.close()
driver2.close()
driver.close()