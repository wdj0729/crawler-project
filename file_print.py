import pickle

# sharekim.pickle의 index 0부터 3393까지, 전체 매물 개수는 3394개
try:
    with open("sharekim.pickle","rb") as fr:
            data = pickle.load(fr)
            print(data[0])
except EOFError:
    pass