from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from time import *
import csv

path = "C:/Users/Jay/Downloads/chromedriver_win32/chromedriver.exe"

driver = webdriver.Chrome(path)
driver.maximize_window()

driver.implicitly_wait(5)

# 1호선 목록
stations_1 = ["광운대","석계","신이문","외대앞","회기",
"청량리","제기동","신설동","동묘앞","동대문",
"종로5가","종로3가","종각","시청","서울역",
"남영","용산","노량진","대방","신길",
"영등포","신도림","구로","구일","개봉",
"오류동","온수","역곡","소사","부천",
"부개","부평","백운","동암","간석",
"주안","도화","제물포","도원","동인천",
"인천","광명","가산디지털단지","독산","금천구청",
"석수","관악","안양","명학","금정",
"군포","당정","의왕","성균관대","화서",
"수원"]

# 2호선 목록
stations_2 = ["시청","을지로입구","을지로3가","을지로4가","동대문역사공원",
"신당","상왕십리","왕십리","한양대","뚝섬",
"성수","건대입구","구의","강변","잠실나루",
"잠실","신천","종합운동장","삼성","선릉",
"역삼","강남","교대","서초","방배",
"사당","낙성대","서울대입구","봉천","신림",
"신대방","구로디지털단지","대림","신도림","문래",
"영등포구청","당산","합정","홍대입구","신촌",
"이대","아현","충정로","용답","신답",
"용두","신설동","도림천","양천구청","신정네거리",
"까치산"]

# 3호선 목록
stations_3 = ["대화","주엽","정발산","마두","백석",
"대곡","화정","원당","삼송","지축",
"구파발","연신내","불광","녹번","홍제",
"무악재","독립문","경복궁","안국","종로3가",
"을지로3가","충무로","동대입구","약수","금호",
"옥수","압구정","신사","잠원","고속터미널",
"교대","남부터미널","양재","매봉","도곡",
"대치","학여울","대청","일원","수서",
"가락시장","경찰병원","오금"]

# 4호선 목록
stations_4 = ["창동","쌍문","수유","미아","미아삼거리",
"길음","성신여대입구","한성대입구","혜화","동대문",
"동대문역","동대문역사문화공원","충무로","명동","회현",
"서울역","숙대입구","삼각지","신용산","이촌",
"동작","이수","사당"]

# 5호선 목록
stations_5 = ["발산","화곡","까치산","신정","목동",
"오목교","양평","영등포구청","영등포시장",
"신길","여의도","여의나루","마포","공덕",
"애오개","충정로","서대문","광화문","종로3가",
"을지로4가","동대문역사문화공원","청구","신금호","행당",
"마장","답십리","장한평","군자","아차산",
"천호"]

# 서울 지하철 목록
# https://seoul.exploremetro.com/ko/pedia/

# 셰어킴 홈페이지
driver.get("https://sharekim.com/")
#해당 사이트의 제목이 셰어킴 인지 확인
assert "셰어킴" in driver.title
# 매물찾기 클릭
driver.find_element_by_xpath("""//*[@id="root"]/div[1]/nav/div/ul/li[3]/a""").click()
# 검색창 찾기
elem = driver.find_element_by_id("searchInput")
# 검색어 입력
elem.send_keys("서울역")
# 엔터키
elem.send_keys(Keys.ENTER)
# 쉐어하우스 클릭
driver.find_element_by_xpath("""//*[@id="root"]/div[2]/div/ul[1]/li[1]/button""").click()

#########################################################################################

# sharehouse.csv파일을 쓰기모드(w)로 열기
f = open("sharehouse.csv","w",encoding="UTF-8")
# 헤더 추가하기
f.write("제목,브랜드,방,가격,인실")
f.write("\n")

html = driver.page_source
soup = BeautifulSoup(html,'html.parser')

#검색한 쉐어하우스 전체 개수
span_max_cnt = soup.select('span.number')[0].text
max_cnt = int(span_max_cnt)
# print(max_cnt)

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
    month = driver.find_elements_by_xpath("""//*[@id="root"]/div[3]/div[2]/div[1]/div[2]/div/a["""+ str(i) +"""]/div/div[2]/div[2]/span/span""")
    month_data = month[0].text.strip()

    # replace 함수를 활용하여 ,를 제거
    title_data = title_data.replace(",","")
    brand_data = brand_data.replace(",","")
    room_data = room_data.replace(",","")
    price_data = price_data.replace(",","")
    month_data = month_data.replace(",","")

    # console 출력
    print("제목",title_data)
    print("브랜드",brand_data)
    print("방",room_data)
    print("가격",price_data)
    print("인실",month_data)
    print(i)

    # 파일에 내용을 입력
    f.write(title_data + "," + brand_data + "," + room_data + "," + price_data + "," + month_data + "\n")

# 작업이 끝난 파일 닫음
f.close()

# 브라우저 종료
driver.close()