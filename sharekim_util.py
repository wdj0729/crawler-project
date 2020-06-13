import os
from time import *
from selenium import webdriver


def get_driver(visible=True) -> webdriver:
    path = os.getcwd() + "/chromedriver.exe"
    options = webdriver.ChromeOptions()
    # 크롬 옵션 설정
    options.add_argument("--window-size=1920x1080")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-extentions")

    if visible is False:
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(path, chrome_options=options)
    # driver = webdriver.Chrome(path)

    driver.maximize_window()
    driver.implicitly_wait(3)

    return driver

def get_house_list_urls(driver: webdriver) -> list:
    house_list_str = """document.body.getElementsByClassName("house-list-wrap")[0].scrollTop = document.body.getElementsByClassName("house-list-wrap")[0].scrollHeight"""

    while True:
        wrap_elem = driver.find_element_by_xpath("""//*[@id="root"]/div[3]/div[2]/div[1]/div[2]""")
        initial_wrap_height = wrap_elem.size['height']
        driver.execute_script(house_list_str)
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

    detail_link_list = [house.get_property("href") for house in house_lists_elem]
    return list(set(detail_link_list))


def list_divider(l: list, n: int) -> iter:
    for i in range(0, len(l), n):
        yield l[i: i+n]


def timer(func):
    def wrapper(self, *args, **kwargs):
        start_time = time()
        result = func(self, *args, **kwargs)
        end_time = time()
        print("{} 함수 실행시간은 {time:.2f}초".format(func.__name__, time=end_time - start_time))
        return result
    return wrapper

