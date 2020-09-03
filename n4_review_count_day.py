import pandas as pd
from dateutil.parser import parse
import os
dirpath = './imdb_reviews_ALL_txt'    ###資料夾###
m_list = os.listdir(dirpath)

#轉換成可計算的日期格式
# df = pd.read_csv('./review_date_user.csv',encoding='ISO-8859-1',index_col='name1')
# df2 = pd.DataFrame(data=df,columns=['date1','date2'])
#
# for i in range(2794737):
#     try:
#         df2.iloc[i,1]=parse(df2.iloc[i,0])
#     except:
#         pass
# df2.to_csv('./review_timetra.csv', encoding='utf-8')
# print('時間轉換完畢')

df = pd.read_csv('./review_timetra.csv',encoding='utf-8',index_col='name1')
df2 = pd.DataFrame(data=df,columns=['date1','date2'])
print(df2)
for m_id in m_list:
    m_id = m_id.replace('.txt','')
    try:
        m_df = df2.loc[m_id,['date2']].sort_values(by=['date2'])
        print(m_df)
        m_first = m_df.values[0][0]
        m_last = m_df.values[-1][0]
        m_day = (m_last-m_first).days
        lines = m_id + ',' + str(m_day)
        with open('./movie_days2.csv', 'a', encoding='utf-8') as g:
            g.write(lines)
            g.write('\n')

    except TypeError as r:
        print(m_id,r)
        pass

    df2.to_csv('./review_tran.csv',encoding='utf-8')

df3 = df2.sort_values(['name1'], ascending=True) \
    .groupby(['name1'], sort=False).count() \
df3.to_csv('./df3.csv', encoding='utf-8')

