import os
from pymongo import MongoClient
import pandas as pd
import time
from pandas.io.json import json_normalize
import pprint #tt9647768

# 1 ############取得電影id
# dirpath = './imdb_summary_ALL_txt'
# f_list = os.listdir(dirpath)
#
# client = MongoClient('localhost', 27017)
# db = client.movie_tag
# posts = db.sum_100JJ
# col_list = []
# f_list2 = []
# df2 = pd.DataFrame()
#
# #每2000部分別儲存成csv
# count = 1
# se_list = []
#
# for m_id in f_list:
#     m_id = m_id.replace('.txt','')
#     print(m_id,':',count)
#     f_list2.append(m_id)
#     result2 = posts.find_one({"_id":m_id})
#     m_dict = dict(result2)
#     aa = json_normalize(m_dict[m_id])
#     aa['name1'] = m_id
#     df2 = df2.append(aa,ignore_index=True)
#     if count % 2000 == 0:
#         df2 = df2.fillna(0)
#         df2.to_csv('./sum100JJ/movie_tag_{}.csv'.format(count), encoding='utf-8', index=False)
#         df2 = pd.DataFrame()
#     if count == len(f_list):
#         df2 = df2.fillna(0)
#         df2.to_csv('./sum100JJ/movie_tag_{}.csv'.format(count), encoding='utf-8', index=False)
#     count += 1
#     #movie_tag_21445.csv    sum100 movie_tag_21384.csv


# 2 #################2000電影檔合併
df_list=[]
for i in range(2,23,2):
    start = time.time()
    df_list.append(pd.read_csv('./sum100JJ/movie_tag_{}000.csv'.format(i)))
    end = time.time()
    print("開啟檔案{}-總共用時{}秒".format(i,(end - start)))

t_start = time.time()
res = pd.concat(df_list, ignore_index=True)
res.to_csv('./sum100JJ/movie_tag_res2.csv', encoding='utf-8', index=False)
print(res.shape)
t_end = time.time()
print("存檔總共用時{}分".format((t_end - t_start)/60))

# 3 ###############merge後儲存(基本分類+tag)
# m_df = pd.read_csv('./movie_classic_zero.csv')
# df2 = pd.read_csv('./sum100JJ/movie_tag_res2.csv')
# df2 = res2.fillna(0)
# # print(df2)
# res = pd.merge(m_df,df2, on='name1')
# res = res.fillna(0)
# res.to_csv('./sum100/movie_merge.csv',encoding='utf-8',index=False)
# print(res)
