import requests
from bs4 import BeautifulSoup
import time
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options

def get_review (filename) :
    fname = './ss08/imdbreviews_{}.tsv'.format(filename)
    date1 = time.strftime('%m%d',time.localtime())
    with open('./ss08/{}.csv'.format(filename), 'r', encoding='utf-8') as e:
        m_list = e.readlines()
        m_list2 = m_list.copy()
    for movie_id in m_list:
        movie_id = movie_id.replace('\n','')
        print(movie_id)

        first_url = "https://www.imdb.com/title/{}/reviews?ref_=tt_urv".format(movie_id)
        chrome_options = Options()
        # chrome_options.add_argument('--headless')
        # chrome_options.add_argument("start-maximized")
        # chrome_options.add_argument("enable-automation")
        # chrome_options.add_argument("--headless")
        # chrome_options.add_argument("--no-sandbox")
        # chrome_options.add_argument("--disable-infobars")
        # chrome_options.add_argument("--disable-dev-shm-usage")
        # chrome_options.add_argument("--disable-browser-side-navigation")
        # chrome_options.add_argument("--disable-gpu")
        # chrome_options.add_argument('--dns-prefetch-disable')

        browser = Chrome(chrome_options=chrome_options, executable_path='./chromedriver')

        browser.get(first_url)
        first_soup = BeautifulSoup(browser.page_source, "html.parser")
        first_list = first_soup.select('div[class="lister-item-content"]')

        for first in first_list:

            first_title = first.select('a[class="title"]')[0].text.strip()
            first_user = first.select('span[class="display-name-link"]')[0].text
            first_date = first.select('span[class="review-date"]')[0].text
            try:
                first_rating = first.select('span[class="rating-other-user-rating"] span')[0].text
            except:
                first_rating = ''
            try:
                first_helpful = first.select('div[class="actions text-muted"]')[0].text.strip() \
                    .replace('Was this review helpful?  Sign in to vote.', '') \
                    .replace('\n', '').replace('Permalink', '').strip()
            except:
                first_helpful = ''

            try:
                first_content = first.select('div[class="text show-more__control"]')[0].text.replace("\t", '')
            except:
                first_content = first.select('div[class="text show-more__control clickable"]')[0].text.replace("\t", '')

            movie_list = [movie_id,first_user,first_date,first_rating,first_title, first_helpful,first_content]
            with open(fname, 'a', encoding='utf-8') as f:
                for o in movie_list:
                    o = o.replace("\n","")
                    f.write(o+'\t')
                f.write('\n')

        try:
            browser.find_element_by_id('load-more-trigger').click()
            reviews_num = int(first_soup.select('div[class="header"] span')[0].text
                              .replace(" Reviews", '').replace(',', ''))
            data_key = first_soup.select('div[class="load-more-data"]')[0]['data-key']
            browser.close()
        except:
            data_key = ''
            reviews_num = 0
            print("1 page done or no Reviews!")
            m_list2.pop(0)
            with open('./ss08/{}_{}.txt'.format(filename,date1), 'w', encoding='utf-8') as e:
                for s in m_list2:
                    e.write(s)
            browser.quit()
            pass

        s = 0
        while s < reviews_num // 25:
            review_url = 'https://www.imdb.com/title/{}/reviews/_ajax?ref_=undefined&paginationKey={}'.format(movie_id,data_key)
            review_res = requests.post(review_url)
            review_soup = BeautifulSoup(review_res.text, 'html.parser')
            reviews_list = review_soup.select('div[class="lister-item-content"]')

            for reviews in reviews_list:
                review_title = reviews.select('a[class="title"]')[0].text.strip()
                review_user = reviews.select('span[class="display-name-link"]')[0].text
                review_date = reviews.select('span[class="review-date"]')[0].text

                try:
                    review_rating = reviews.select('span[class="rating-other-user-rating"] span')[0].text
                except:
                    review_rating = ''

                try:
                    review_helpful = reviews.select('div[class="actions text-muted"]')[0].text.strip() \
                                                    .replace('Was this review helpful?  Sign in to vote.', '') \
                                                    .replace('\n', '').replace('Permalink', '').strip()
                except:
                    review_helpful = ''
                try:
                    review_content = reviews.select('div[class="text show-more__control"]')[0].text.replace("\t",'')
                except:
                    review_content = reviews.select('div[class="text show-more__control clickable"]')[0].text.replace("\t",'')

                movie_list2 = [movie_id, review_user, review_date, review_rating, review_title,
                               review_helpful,review_content]
                with open(fname, 'a', encoding='utf-8') as f:
                    for p in movie_list2:
                        p = p.replace("\n", "").replace("\t", "")
                        f.write(p + '\t')
                    f.write('\n')

            try:
                data_key = review_soup.select('div[class="load-more-data"]')[0]['data-key']
                s += 1
            except IndexError as e:
                print("well done! no more!")
                m_list2.pop(0)
                with open('./ss08/{}_{}.txt'.format(filename,date1), 'w', encoding='utf-8') as e:
                    for s in m_list2:
                        e.write(s)
                break

if __name__ == '__main__':
    start = time.time()
    get_review('p4_f1')
    end = time.time()
    print("總共用時{}秒".format((end - start)))