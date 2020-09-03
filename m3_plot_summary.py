import requests
from bs4 import BeautifulSoup
import time
import random
from multiprocessing.dummy import Pool as Theadpool

def summary_synopsis(fname):
    with open('./ss08/{}.csv'.format(fname), 'r', encoding='utf-8') as e:
        m_list = e.readlines()
    date1 = time.strftime('%m%d',time.localtime())
    c = 0

    for m_id in m_list:
        m_id = m_id.replace('\n','')
        print(m_id)
        sum_url = 'https://www.imdb.com/title/{}/plotsummary?ref_=ttpl_ql_2'.format(m_id)
        res = requests.post(sum_url)
        soup = BeautifulSoup(res.text, 'html.parser')
        summary_synopsis_list = soup.select('li[class="ipl-zebra-list__item"]')

        for s in summary_synopsis_list:
            s = s.text.replace('\n','',1).split('\n')[0].replace('\t','')
            if "It looks like we don't have a" not in s:
                summary = m_id + '\t' + s
                with open('./ss08/summary_{}.tsv'.format(fname), 'a', encoding='utf-8') as f:
                    f.write(summary)
                    f.write('\n')

        c += 1
        with open('./ss08/{}_{}.txt'.format(fname,date1), 'w', encoding='utf-8') as f:
            for m in m_list[c:]:
                m = m.replace('\n', '')
                f.write(m)
                f.write('\n')
        time.sleep(random.randint(10, 30))

if __name__ == '__main__':
    #多執行緒
    start = time.time()

    f_list = ['f1','f2','f3']
    p = Theadpool(3)
    for i in f_list:
        p.apply_async(summary_synopsis, args=(i, ))
    p.close()
    p.join()

    end = time.time()
    print("總共用時{}秒".format((end - start)))