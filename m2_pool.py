import time
from m_imdb_review import get_review
from multiprocessing.dummy import Pool as Theadpool

if __name__ == '__main__':
    start = time.time()

    f_list = ['f1','f2','f3']
    p = Theadpool(3)
    for i in f_list:
        p.apply_async(get_review, args=(i, ))
    p.close()
    p.join()

    end = time.time()
    print("總共用時{}秒".format((end - start)))





