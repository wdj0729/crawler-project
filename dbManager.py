import sys
from traceback import print_exc
import pymysql
from sharekim_util import timer

date_format_str = "DATE_FORMAT(NOW(), '%Y-%m-01')"
insert_into_house_SQL = """insert into sharehouse.houses 
(house_name, area, house_type, room_cnt,washroom_cnt, now_floor, total_floor, road_address, district, building)
values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""

insert_into_room_SQL = "insert into sharehouse.rooms (room_name, gender, bed_cnt, area, house_id) values (%s, %s, %s, %s, (select id from houses where house_name = %s and DATE(h.created_at) >= " + date_format_str + "));"

insert_into_bed_SQL = "insert into sharehouse.beds (is_full, deposit, monthly_rent, room_id) values (%s, %s, %s, (select id from rooms where house_id=(select id from houses where house_name=%s and DATE(h.created_at) >= " + date_format_str + ") and room_name=%s));"


class DbManger:

    # 크롤한 dict들의 list를 입력받음
    def __init__(self, data: list):
        self.data = data
        self.db = pymysql.connect(user='root', passwd='1234', host='localhost', db='sharehouse', charset='utf8')
        self.cursor = self.db.cursor(pymysql.cursors.DictCursor)
        self.house_data = []
        self.room_data = []
        self.bed_data = []

    def insert(self):
        try:
            self.cursor.executemany(insert_into_house_SQL, self.house_data)
            self.cursor.executemany(insert_into_room_SQL, self.room_data)
            self.cursor.executemany(insert_into_bed_SQL, self.bed_data)
            self.db.commit()
        except Exception as e:
            _, _, tb = sys.exc_info()
            print('error line No = {}'.format(tb.tb_lineno))
            print(e)
            print_exc()
        finally:
            self.db.close()

    def parse_list(self):
        for house in self.data:
            house_tmp = [house["house_name"], house["house_area"], house["house_type"], house["room_cnt"],
                         house["washroom_cnt"],
                         house["now_floor"], house["total_floor"], house["road_address"], house["district"],
                         house["building"]]
            self.house_data.append(house_tmp)
            for room in house["room_dict_list"]:
                room_tmp = [room["room_name"], room["gender"], room["bed_cnt"], room["room_area"], house["house_name"]]
                self.room_data.append(room_tmp)
                for bed in room["bed_dict_list"]:
                    bed_tmp = [bed["is_full"], bed["deposit"], bed["monthly_rent"], house["house_name"],
                               room["room_name"]]
                    self.bed_data.append(bed_tmp)

    @timer
    def run(self):
        self.parse_list()
        self.insert()
