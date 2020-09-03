import pandas as pd
from dateutil.parser import parse
import datetime

#rating加上天數、user&movie改流水號
df = pd.read_csv('./rating200.csv',encoding='ISO-8859-1') 
df = pd.DataFrame(data=df,columns=['date1','day2','user','name1','ranting'])
print(df)
user_set = set()
movie_set = set()
user_dict = {}
movie_dict = {}

for i in range(2026525):   #2026525
    try:
        df.iloc[i, 1] = str((datetime.datetime.now() - parse(df.iloc[i, 0])).days) #文字轉天數
        user_set.add(df.iloc[i,2])   #移除重複user
        movie_set.add(df.iloc[i, 3]) #移除重複movie
        if i % 100 == 0:
            print(i)
    except:
        pass

for u,num in enumerate(list(user_set)):
    user_dict[num] = u+1

for o,num1 in enumerate(list(movie_set)):
    movie_dict[num1] = o+1

df2 = pd.DataFrame(list(user_dict.items()),columns=['user','usernum'])
res = pd.merge(df,df2, on='user')
df3 = pd.DataFrame(list(movie_dict.items()),columns=['name1','movienum'])
res2 = pd.merge(res,df3, on='name1')
# res = res.drop(columns=['user','name1'])
res2.to_csv('usernum99.tsv',sep='\t',encoding='ISO-8859-1',index=False)
