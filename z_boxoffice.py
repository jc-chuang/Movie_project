import requests
from bs4 import BeautifulSoup
res = requests.get('https://www.boxofficemojo.com/title/tt8110330/') #無預算
# https://www.boxofficemojo.com/title/tt8110330/credits/  #有預算
soup = BeautifulSoup(res.text, "html.parser")
budget_lis = soup.select('div[class="a-section a-spacing-none"] span')

for i,bu in enumerate(budget_lis):
    if bu.text == 'Budget':
        index_num = i+1
        print(budget_lis[index_num].text)
