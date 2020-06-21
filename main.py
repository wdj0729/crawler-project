import pickle

from dbManager import *
from sharekim_crawler import Crawler
from sharekim_util import *

if __name__ == '__main__':
    import time
    time_str = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    try:
        if os.path.isfile("house_list_"+time_str+".pickle"):
            with open('house_list.pickle', 'rb')as f:
                house_list = pickle.load(f)
        else:
            crawler = Crawler()
            house_list = crawler.run()
            with open('house_list_'+time_str+'.pickle', 'wb') as f:
                pickle.dump(house_list, f, pickle.HIGHEST_PROTOCOL)
        db = DbManger(house_list)
        db.run()
    except Exception as e:
        print(e)
        print_exc()




