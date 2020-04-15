import pickle

# sharekim.pickle의 index 0~n
try:
    with open("sharekim.pickle","rb") as fr:
            data = pickle.load(fr)
            print(data[0])
except EOFError:
    pass