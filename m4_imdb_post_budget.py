import requests
from bs4 import BeautifulSoup

with open('./Certification_list.csv', 'r', encoding='utf-8') as e:
    m_list = e.readlines()

for m_id in m_list:
    m_id = m_id.replace('\n','')
    url = 'https://www.imdb.com/title/{}/?ref_=adv_li_tt'.format(m_id)
    res = requests.post(url)
    soup = BeautifulSoup(res.text, 'html.parser')

    #取得分級
    Certif_list = soup.select('div[class="subtext"]')
    for i in Certif_list:
        a = str(i.text).replace(' ','').replace('\n','').split('|')[0]
        with open('Certification.tsv', 'a', encoding='utf-8') as f:
                f.write(m_id + '\t' + a)
                f.write('\n')

    # # #取得票房
    # budget_list = soup.select('div[class="txt-block"]')
    # for i in budget_list:
    #     a = i.text
    #     if 'Cumulative Worldwide Gross:' in a:
    #         a = a.replace(' ', '').replace('\n', '').replace('Budget:', '').replace('(estimated)', '')
    #         with open('Budget.tsv', 'a', encoding='utf-8') as f:
    #             f.write(m_id + '\t' + a)
    #             f.write('\n')

#     #取得海報
#     try:
#         post_url = soup.select('div[class="poster"] img')[0]['src']
#         res_img = requests.get(post_url)
#         img_content = res_img.content  #取得圖片的文字檔(二進制)
#         print(post_url)
#         with open('./imdb_plus_post/' + m_id +'.jpg', 'wb') as f:
#             f.write(img_content)   #二進制要用wb寫入
#     except:
#         pass

    # #取得預算
    # budget_list = soup.select('div[class="txt-block"]')
    # for i in budget_list:
    #     a = i.text
    #     if 'Budget:' in a:
    #         a = a.replace(' ', '').replace('\n', '').replace('Budget:', '').replace('(estimated)', '')
    #         with open('Budget.tsv', 'a', encoding='utf-8') as f:
    #             f.write(m_id + '\t' + a)
    #             f.write('\n')

    #取得中文名
#     try:
#         rating = soup.select('span[itemprop="ratingValue"]')[0].text
#     except:
#         rating = ''
#     try:
#         vote = soup.select('span[class="small"]')[0].text
#     except:
#         vote = ''
#     try:
#         title = soup.select('div[class="title_wrapper"] h1')[0].text.split(' (20')[0]
#     except:
#         title = ''
#     try:
#         runtime = soup.select('div[class="txt-block"] time')[0].text
#     except:
#         runtime = ''
#     try:
#         originalTitle = soup.select('div[class="title_wrapper"] div[class="originalTitle"]')[0].text
#         originalTitle = originalTitle.replace(' (original title)','')
#     except:
#         originalTitle = ''

#     with open('1_other.tsv', 'a', encoding='utf-8') as g:
#         g.write(m_id +'\t'+rating+'\t'+vote+'\t'+title+'\t'+runtime+'\t'+originalTitle)
#         g.write('\n')
#     time.sleep(random.randint(1, 3))
