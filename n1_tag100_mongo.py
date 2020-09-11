import nltk
import math
from nltk.stem import WordNetLemmatizer
import string
from nltk.corpus import stopwords
from collections import Counter
import time

dirpath = './reviews_summary_ALL_txt'    ###資料夾###
# f_list = os.listdir(dirpath)
f_list = ['tt1201607','tt0111161']
wordnet_lemmatizer = WordNetLemmatizer()
stopwords = set(stopwords.words('english'))
#額外自訂義停用字
stopwords = stopwords.union({
    'movie', 'film','time','ha','wa','dont','much','thing','many','watch','thats'})

#前處理
def my_tokenizer(s):
    s = s.lower() # downcase                           #建立{符號:None}字典
    remove_punctuation_map = dict((ord(char), None) for char in string.punctuation) #string.punctuation=標點符號
    no_punctuation = s.translate(remove_punctuation_map) #以字典移除標點符號
    tokens = nltk.tokenize.word_tokenize(no_punctuation) # nltk斷字
    tokens = [t for t in tokens if len(t) > 2] # 大於兩個字才要
    tokens = [wordnet_lemmatizer.lemmatize(t) for t in tokens] # 還原詞性
    tokens = [t for t in tokens if t not in stopwords] # 移除停用字
    tokens = [t for t in tokens if not any(c.isdigit() for c in t)] # 移除包含數字的字
    return tokens

def tf(word, count):
    return count[word] / sum(count.values())

def n_containing(word, count_list):
    return sum(1 for count in count_list if word in count)

def idf(word, count_list):
    return math.log(len(count_list) / (1 / n_containing(word, count_list)))

'''
主程式
'''
start = time.time()
for m_id in f_list:
    jn_list =[]
    tokens = []
    error_count = 0
    try:
        m_id = m_id.replace('.txt','')
        # titles = [line.rstrip() for line in open('./reviews_summary_ALL_txt/{}.txt'.format(m_id),encoding='utf-8')]
        with open('./reviews_summary_ALL_txt/{}.txt'.format(m_id), encoding='ISO-8859-1') as e:
            titles = e.readlines()

                                   ##############################資料夾#################################
        print(len(titles))
        # print(titles)
        for title in titles:
            try:
                title = title.encode('ascii', 'ignore').decode('utf-8') #將unicode字符串編碼為ascii並忽略錯誤
                tokens = my_tokenizer(title)                 #指定標準輸出編碼為utf-8
            except Exception as e:
                print(e)
                print(title)
                error_count += 1

        print('前處理後的字數:', len(tokens))
        print('error_count:',error_count)

        w_list = nltk.pos_tag(tokens) #標註詞性

        for w in w_list:  #只取名詞、形容詞
            if 'JJ' in w[1] :
                jn_list.append(w[0])
            if 'NNP' in w[1] :
                jn_list.append(w[0])

        count1 = Counter(jn_list)
        print('專有名詞+形容詞數量:',len(count1))
        
        dict_tf = {}
        dict_idf = {}
        set_tf = set()
        set_idf = set()
        
        scores_tf = {word: tf(word, count1) for word in count1}
        sorted_words_tf = sorted(scores_tf.items(), key=lambda x: x[1], reverse=True)
        scores_idf = {word: idf(word, count1) for word in count1}
        sorted_words_idf = sorted(scores_idf.items(), key=lambda x: x[1], reverse=True)

        for g in sorted_words_tf:
            dict_tf[g[0]]= '%.10f' % g[1]
        for h in sorted_words_idf:
            dict_idf[h[0]]= '%.10f' % h[1]

        for a in list(dict_tf.keys())[:500]:
            set_tf.add(a)
        for b in list(dict_idf.keys())[:500]:
            set_idf.add(b)

        cross_all = list(set_tf & set_idf)
        print('前500交集數量:', len(cross_all))

        dict_all ={}
        for r in cross_all:
            dict_all[r] = float(dict_tf[r]) * float(dict_idf[r])
        sorted_tuplelist = sorted(dict_all.items(), key=lambda x: x[1], reverse=True)

        #取tfidf高的
        sub_tag = sorted_tuplelist[:100]      ######################改這裡##########################
        sub_tag_dict = {}
        for y in sub_tag:
            sub_tag_dict[y[0]] = '%.10f' % y[1]

        ttid_dict = {}
        ttid_dict['_id'] = m_id
        ttid_dict[m_id] = sub_tag_dict
        print('TFIDF_TOP:', ttid_dict)

        # # 把json存進mongo
        # client = MongoClient('localhost', 27017)
        # db = client.movie_tag
        # new_posts = [ttid_dict]
        # posts = db.sum_100JJ               ######################和這裡##########################
        # result = posts.insert_many(new_posts)
        # print("Bulk Inserts Result is :", result.inserted_ids)
        # # result = db.test0827.insert_one({'732':((732, 1155), (1.0, 1))})
    except Exception as h:
        print(m_id, "--", h)

end = time.time()
print("總共用時{}秒".format((end - start)))
