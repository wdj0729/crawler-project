from time import sleep
import timeit
import pickle
from traceback import print_exc

from sharekim_util import *
from sharekim_crawler import Crawler
from dbManager import *

if __name__ == '__main__':
    house_list = []
    try:
        if os.path.isfile("house_list.pickle"):
            with open('house_list.pickle', 'rb')as f:
                house_list = pickle.load(f)
        else:
            crawler = Crawler()
            house_list = crawler.run()
            with open('house_list.pickle', 'wb') as f:
                pickle.dump(house_list, f, pickle.HIGHEST_PROTOCOL)
        db = DbManger(house_list)
        db.run()
    except Exception as e:
        print(e)
        print_exc()
        



