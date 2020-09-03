import requests
from bs4 import BeautifulSoup
import time
import random

date1 = time.strftime('%m%d',time.localtime())
with open('./movielist_plus.csv', 'r', encoding='utf-8') as e:
    m_list = e.readlines()
    m_list2 = m_list.copy()

for m_id in m_list:
    m_id=m_id.replace('\n','')
    url = 'https://www.imdb.com/title/{}/releaseinfo?ref_=tt_dt_dt#akas'.format(m_id)
    res = requests.post(url)
    soup = BeautifulSoup(res.text, 'html.parser')

    try:
        original_title = soup.select('table[class="ipl-zebra-list akas-table-test-only"] tr')[0].text\
            .replace('(original title)','').replace('\n','').lstrip()
    except:
        original_title = soup.select('h3[itemprop="name"] a')[0].text

    print(m_id,original_title)
    title_list = soup.select('table[class="ipl-zebra-list akas-table-test-only"] tr')

    taiwan_title = ''
    korea_title = ''
    japan_title = ''
    hongkong_list = []
    World_wide_list = []
    for i in title_list:
        a = i.text.replace('\n','\t')
        aka_list = [m_id,a]
        # if 'Taiwan' in a:
        #     taiwan_title = a.replace('Taiwan','').replace('\n','')
        # if 'South Korea' in a:
        #     korea_title = a.replace('South Kore','').replace('\n','')
        # if 'Japan' in a:
        #     japan_title = a.replace('Japan','').replace('\n','').replace('Japan (Japanese title)','')
        # if 'Hong Kong' in a:
        #     hongkong_list.append(a.replace('\n',''))
        # if 'World-wide' in a:
        #     World_wide_list.append(a.replace('\n', ''))
    # aka_list = [m_id,original_title,taiwan_title,korea_title,japan_title,str(hongkong_list),str(World_wide_list)]

        with open('./aka_all.tsv', 'a', encoding='utf-8') as f:
            for o in aka_list:
                f.write(o + '\t')
            f.write('\n')

    m_list2.pop(0)
    with open('./aka_{}.txt'.format(date1), 'w', encoding='utf-8') as e:
        for s in m_list2:
            e.write(s)
    time.sleep(random.randint(1, 3))

