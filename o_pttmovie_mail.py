import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime as dt
import smtplib
from email.mime.text import MIMEText
import re
import time

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'\
                        ' AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'}
x, y = {}, []

def content_get(title_list):
    '取得本次爬取範圍之字典={po文時間:連結} + po文時間list'
    article_url_list = []
    datetime_list =[]
    for title_soup in title_list:
        try:
            article_url = 'https://www.ptt.cc' + title_soup.select('a')[0]['href']  # 取得每篇文章網址
            article_res = requests.get(article_url, headers=headers)
            article_soup = BeautifulSoup(article_res.text, 'html.parser')
            article_info_list = article_soup.select('div[class="article-metaline"] span')  # 取標題段框框中的東西
            for n, info in enumerate(article_info_list):  # n = 索引、info = list中的元素
                if (n + 1) % 6 == 0 :
                    datetime1 = info.text
                    datetime1 = (dt.strptime(datetime1, "%a %b %d %H:%M:%S %Y"))
                    datetime_list.append(datetime1)
                    article_url_list.append(article_url)

        except IndexError:
            del title_soup

    for z in datetime_list:
        y.append(z)
    post_dict = dict(zip(datetime_list, article_url_list))
    x.update(post_dict)

def content_gettxt(post_dict,post_timesort,last_post_time):
    '使用content_get取得之字典，比對找出新文章，並各別存成文字檔'
    print('第二步~開始找新文章')
    global npost_dict,npost_time
    author = ''
    title = ''
    datetime1 = ''
    p = 0
    new_time_list = []
    new_title_list =[]

    def validateTitle(title):
        '替換標題中的非法字元(作為檔名)'
        rstr = r"[\/\\\:\*\?\"\<\>\|]"
        new_title = re.sub(rstr, "_", title)  # 替換為下劃線
        return new_title

    while post_timesort[p] > last_post_time:
        new_url = post_dict[post_timesort[p]]
        new_res = requests.get(new_url, headers=headers)
        new_soup = BeautifulSoup(new_res.text, 'html.parser')
        new_article_list = new_soup.select('div[class="article-metaline"] span')
        #取得作者、標題、發文時間
        for n, info in enumerate(new_article_list):
            if (n + 1) % 6 == 2:
                author = info.text
            if (n + 1) % 6 == 4:
                title = info.text
                new_title_list.append([author, title, new_url])
            if (n + 1) % 6 == 0 :
                datetime1 = info.text
                datetime1 = (dt.strptime(datetime1, "%a %b %d %H:%M:%S %Y"))
                new_time_list.append(datetime1)

        new_content = new_soup.select('#main-content')[0].text.split('--')[0]  # 取得文章本身內容
        push_info_list = new_soup.select('div[class="push"] span[class ="hl push-tag"]')
        down_info_list = new_soup.select('div[class="push"] span[class="f1 hl push-tag"]')
        # 計算推噓文數
        push_up = len(push_info_list)
        push_down = 0
        push_arrow = 0

        for down in down_info_list:
            if '噓' in down.text:
                push_down += 1
            if '→' in down.text:
                push_arrow += 1

        score = push_up - push_down
        num = push_up + push_down + push_arrow

        new_content += '\n---split---\n'
        new_content += '推: %s \n' % (push_up)
        new_content += '噓: %s \n' % (push_down)
        new_content += '→: %s \n' % (push_arrow)
        new_content += '分數: %s \n' % (score)
        new_content += '樓數: %s \n' % (num)
        new_content += '作者: %s \n' % (author)
        new_content += '標題: %s \n' % (title)
        new_content += '時間: %s \n' % (datetime1)

        try:
            title1 = validateTitle(title)

            with open('./movie6/%s.txt' % (title1), 'w', encoding='utf-8') as f:
                f.write(new_content)

        except IndexError as e:
            print(e)
        p += 1

    npost_dict = dict(zip(new_time_list, new_title_list))
    npost_time = new_time_list
    print(npost_dict)
    print(npost_time)

def send_mail_for_me(npost_dict,npost_time):
    '利用 Gmail 的服務寄發通知信'
    send_gmail_user = 'jcc6881@gmail.com'
    send_gmail_password = '2wsx8ik,'
    rece_gmail_user = 'jcc6881@gmail.com'

    msg = MIMEText('最新的po文時間: ' + str(npost_time[0])\
                   + '\n文章標題：' + npost_dict[npost_time[0]][1]\
                   + '\n文章作者：' + npost_dict[npost_time[0]][0]\
                   + '\n文章連結：' + npost_dict[npost_time[0]][2])

    msg['Subject'] = ('已儲存movie版'+ str(len(npost_time)) + '篇新文章')
    msg['From'] = send_gmail_user
    msg['To'] = rece_gmail_user

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(send_gmail_user, send_gmail_password)
    server.send_message(msg)
    server.quit()

def error_mail(t, e):
    '爬蟲失敗mail通知'
    send_gmail_user = 'jcc6881@gmail.com'
    send_gmail_password = '2wsx8ik,'
    rece_gmail_user = 'jcc6881@gmail.com'

    msg = MIMEText('[%s] 執行期間錯誤：%s' % (t, e))

    msg['Subject'] = ('movie版爬蟲GG惹'+ str(t) )
    msg['From'] = send_gmail_user
    msg['To'] = rece_gmail_user

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(send_gmail_user, send_gmail_password)
    server.send_message(msg)
    server.quit()

def ptt_movie():
    if not os.path.exists('movie6'):
        os.mkdir('movie6')
    url = 'https://www.ptt.cc/bbs/movie/index.html'
    for r in range(1,4): #爬最新的三頁
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        title_list = soup.select('div.title')
        content_get(title_list) #method1'取得本次爬取範圍之字典={po文時間:連結} + po文時間list
        print('開始爬第',r,'頁')
        url = 'https://www.ptt.cc' + soup.select('div [class="btn-group btn-group-paging"]')[0].select('a')[1]['href']

    y1 = sorted(y, reverse=True) #將method1'取得之時間list排序

    with open('last_post_time.txt', 'r', encoding='utf-8') as q:
        last_post_time1 = q.readline()
        last_post_time1 = dt.strptime(last_post_time1,"%Y-%m-%d %H:%M:%S")
        content_gettxt(x, y1,last_post_time1)

    with open('last_post_time.txt', 'w', encoding='utf-8') as u:
        u.write(str(y1[0]))

    send_mail_for_me(npost_dict, npost_time)

def main():
    SLEEPTIME = 1800
    try:
        while True:
            print('[%s] 開始執行' % dt.now())
            ptt_movie()  # 開始執行主流程
            print('[%s] 已儲存%s篇新文章' % (dt.now(),len(npost_time)))
            if len(npost_time) == 0:
                break
            else:
                time.sleep(SLEEPTIME)

    except Exception as e:
        print('[%s] 執行期間錯誤：%s' % (dt.now(), e))
        error_mail(dt.now(), e)

if __name__ == '__main__':
    main()

# 尚未研究:1. 例外處理優化 2. 昀燊的code 3.研究re.sub