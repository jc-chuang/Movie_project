import time
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

############畫折線圖(最佳分群)
start = time.time()
res2=pd.read_csv('./5587_classic_DAY.csv')
res2 = res2.drop(columns=['name'])
res2 = res2.fillna(0)
# print(res2.shape)
silhouette_avg = []
for i in range(2,31):
    kmeans_fit = KMeans(n_clusters = i,max_iter=10).fit(res2)
    silhouette_avg.append(silhouette_score(res2, kmeans_fit.labels_))
plt.plot(range(2,31), silhouette_avg)
plt.show()
end = time.time()
print("折線圖共用時{}分".format((end - start)/60))

############ KMeans分群
# start = time.time()
# km = KMeans(n_clusters=20,max_iter=20)
# m_df = pd.read_csv('./tag10_2/movie_tag_res2.csv',index_col=['name1'])
# m_df = m_df.fillna(0)
# km.fit(m_df)
# clusters = km.labels_.tolist()
# m_df["cluster"] = clusters
# m_df.to_csv('./tag10_2/km.csv', encoding='utf-8', index=False)
# end = time.time()
# print("分群總共用時{}分".format((end - start)/60))
# # print(m_df)

