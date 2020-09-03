import requests,json
from bs4 import BeautifulSoup
url='https://www.rottentomatoes.com/top/bestofrt/?year=2019'
headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0'}
req=requests.get(url=url,headers=headers)
soup=BeautifulSoup(req.text,'html.parser')

soup_list=str(soup.select('script')[1]).replace('</script>','>').split('>')
# print(soup_list)
data=json.loads(soup_list[1])
for data in data['itemListElement']:
    print(data['url'])

# 處理class
with open('tomato.csv', 'r', encoding='utf-8') as e:
    m_list = e.readlines()
# m_list =['border_2018','born_to_be_wild_2011']
for m_name in m_list:
    name1 = m_name.replace('\n','')
    url='https://www.rottentomatoes.com/m/{}'.format(name1)
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0'}
    req=requests.get(url=url,headers=headers)
    soup=BeautifulSoup(req.text,'html.parser')

    try:
        classic =soup.select('div.meta-value')[1].text.replace('\n','').split(',')
        classic1 =[clas.strip() for clas in classic]
        classic2 = str(classic1).replace('[','').replace(']','').replace(',','|').replace("'",'')
    except:
        try:
            classic = soup.select('div.meta-value')[0].text.replace('\n', '').split(',')
            classic1 = [clas.strip() for clas in classic]
            classic2 = str(classic1).replace('[', '').replace(']', '').replace(',', '|').replace("'", '')
        except:
            classic2 =''
    try:
        year = soup.select('span[class="h3 year heroImageNoMovie-year"]')[0].text
    except:
        year = ''
    g_list = [name1, year, classic2]
    print(g_list)
    with open('to_genre.tsv', 'a', encoding='utf-8') as f:
        for p in g_list:
            p = p.replace("\n", "").replace("\t", "")
            f.write(p + '\t')
        f.write('\n')