import requests
from bs4 import BeautifulSoup
import time
import random

'''vote 10001 ↑ = 5,587 取得movieid_list'''
id_dict = {}
id_list = []
start = 1
for i in range(66):
    # url = 'https://www.imdb.com/search/title/?title_type=feature,documentary&release_date=2000-01-01,2020-06-30' \
    #       '&sort=user_rating,desc&count=250&num_votes=10001,10000000000&start={}'.format(start)
    url = 'https://www.imdb.com/search/title/?title_type=feature,documentary&release_date=2000-01-01,2020-06-30' \
          '&num_votes=301,1000&sort=user_rating,desc&count=250&start={}'.format(start)
    res = requests.post(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    title_list = soup.select('h3[class="lister-item-header"]')

    for n, title in enumerate(title_list):
        id2 = title.select('a')[0]['href'].replace('/title/', '').replace('/', '') + '\n'
        name = title.select('a')[0].text
        id_dict[id2] = name
        id_list.append(id2)
        with open('./vote300_8_list.csv', 'a', encoding='utf-8') as e:
            e.write(id2)
    time.sleep(random.randint(1, 3))
    start += 250

print('done',len(id_list))

'''TOP 250 '''
# url = 'https://www.imdb.com/chart/top/?ref_=nv_mv_250'
# url = 'https://www.imdb.com/search/title/?title_type=feature,documentary&release_date=2000-01-01,2020-06-30' \
#       '&sort=user_rating,desc&count=250&num_votes=10001,10000000000'
# url ='https://www.imdb.com/title/tt0111161/'
# res = requests.post(url)
# soup = BeautifulSoup(res.text, 'html.parser')
# summary = soup.select('div[class="summary_text"]')[0].text.replace('\n','').strip()
# print(summary)

# title_list = soup.select('table[class="chart full-width"] td[class="titleColumn"]')
# id_list = []
# for n, title in enumerate(title_list):
#     id_list.append(title.select('a')[0]['href'].replace('/title/','').replace('/',''))
#
# print(len(id_list))
# print(id_list)
#     title_url = title.select('a')[0]['href']
#     print('https://www.imdb.com' + title_url)
#
#     title = title.text.replace(' ','').split('\n')[1:-1]
#     print(title)
# print(id_list)

'''討論度前100'''
# url = 'https://www.imdb.com/chart/moviemeter/?ref_=nv_mv_mpm'
# res = requests.post(url)
# soup = BeautifulSoup(res.text, 'html.parser')
# title_list = soup.select('table[class="chart full-width"] td[class="titleColumn"]')
#
# for n, title in enumerate(title_list):
#     title_no = title.find('div').text.split('\n')[0]
#     title_name = title.select('a')[0].text + title.select('span')[0].text
#     title_url = 'https://www.imdb.com' + title.select('a')[0]['href']
#     print('熱議排名:',title_no)
#     print(title_name)
#     print(title_url)
# 
#     # '''進入電影內頁'''
#     res2 = requests.post(title_url)
#     soup2 = BeautifulSoup(res2.text, 'html.parser')
#
#     try:
#         movie_rating = soup2.select('div[class="ratingValue"] strong')[0]['title']
#     except:
#         movie_rating = '---'
#     print('觀眾評分:',movie_rating)
#
#     try:
#         movie_time = soup2.select('div[class="subtext"] time')[0].text.replace(' ', '').replace('\n', '')
#     except:
#         movie_time = '---'
#     print('片長:',movie_time)
#
#     movie_tag_list = soup2.select('div[class="subtext"] a')
#     for tag in range(len(movie_tag_list)-1):
#         movie_tag = movie_tag_list[tag]
#         print(movie_tag.text)
#     print()
#     print('===')

'''演員列表頁'''
# FullCast_url = 'https://www.imdb.com/title/tt1051906/fullcredits'
# res3 = requests.post(FullCast_url)
# soup3 = BeautifulSoup(res3.text, 'html.parser')
# Directed_by = soup3.select('table[class="simpleTable simpleCreditsTable"] a')
# # print(type(Directed_by))
# print(Directed_by)
