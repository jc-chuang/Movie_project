import requests,json
from bs4 import BeautifulSoup
# url='https://www.themoviedb.org/movie?language=zh-TW'
# req=requests.get(url=url,headers=headers)
# soup=BeautifulSoup(req.text,'html.parser')
# url_movie='https://www.themoviedb.org' + '/movie/516486?language=zh-TW'

headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0'}
with open('TMDB_ID.csv', 'r', encoding='utf-8') as e:
    m_list = e.readlines()
for i in m_list:
    ii = i.replace('\n','')
    url_movie='https://www.themoviedb.org' + '/movie/{}'.format(ii)+'?language=en-US'
    req_movie=requests.get(url=url_movie,headers=headers)
    soup_movie=BeautifulSoup(req_movie.text,'html.parser')
    you_need_year =soup_movie.select('span[class="tag release_date"]')
    you_need_genre = soup_movie.select('span[class="genres"]')
    for m,id in enumerate(you_need_year):
        year = you_need_year[m].text
        genre = you_need_genre[m].text.replace('\n','').replace(',\xa0','|')
        i_list = [ii,year,genre]
        with open('tmdb_genre_US.tsv', 'a', encoding='utf-8') as f:
            for p in i_list:
                p = p.replace("\n", "").replace("\t", "")
                f.write(p + '\t')
            f.write('\n')
