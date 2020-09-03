import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
}
# url = 'https://www.metacritic.com/browse/movies/score/metascore/all/filtered?view=condensed&page=1'
# res = requests.get(url,headers=headers)
# print(res)
# soup = BeautifulSoup(res.text, 'html.parser')
# movie_list = soup.select('tr[class="expand_collapse"]')
# for i,movie in enumerate(movie_list):
#     title = movie.select('td[class="details"] a h3')[0].text
#     url = movie.select('a[class="title"]')[0]['href']
#     year = movie.select('td[class="details"] span')[1].text.split(', ')[1]
#     # print(year)
#     m_lis=[title,url,year]
#     with open('metacritic.tsv', 'a', encoding='utf-8') as f:
#         for o in m_lis:
#             o = o.replace("\n", "")
#             f.write(o + '\t')
#         f.write('\n')
#     title=title.text
#     url = soup.select('tr[class="expand_collapse"] td[class="details"] a')[i]['href']
#     print(title)
#     print(url)

url = 'https://www.metacritic.com/movie/shoplifters/user-reviews'
res = requests.get(url,headers=headers)
print(res)
soup = BeautifulSoup(res.text, 'html.parser')
review_list = soup.select('div[class="review pad_top1"]')
for review in review_list:
    rr = review.select('span[class="blurb blurb_expanded"]')
    if rr == []:
        rr = review.select('div[class="review_body"]')
    print(rr[0].text)
