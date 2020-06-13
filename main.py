from time import sleep
import timeit
import pickle
from traceback import print_exc

from sharekim_util import *
from sharekim_crawler import Crawler
from dbManager import *

if __name__ == '__main__':

    try:
        crawler = Crawler()
        house_list = crawler.run()
        db = DbManger(house_list)
        db.run()
    except Exception as e:
        print(e)
        print_exc()
        



