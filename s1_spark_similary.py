# E:\mongodb\bin$ mongod --bind_ip_all --dbpath e:\mongo_json
# master@ cd ~ ; cd hadoop-2.10.0/sbin ; ./stop-dfs.sh ; ./start-dfs.sh
# master@ cd ~ ; cd spark-2.4.5-bin-hadoop2.7/sbin ; ./stop-all.sh ; ./start-all.sh
# hadoop fs -put ~/Desktop/spark101/movies/rating11 spark101/movies
# ui@ pyspark --master spark://master:7077 --executor-memory 8G

from pyspark import SparkContext
import time
from math import sqrt

def remove_duplicates(userRatings):
    ratings = userRatings[1]
    (movie1, rating1) = ratings[0]
    (movie2, rating2) = ratings[1]
    return movie1 < movie2

def make_movie_pairs(userRatings):
    ratings = userRatings[1]
    (movie1, rating1) = ratings[0]
    (movie2, rating2) = ratings[1]
    return ((movie1, movie2), (rating1, rating2))

def compute_score(ratingPairs):
    numPairs = 0
    sum_xx = sum_yy = sum_xy = 0
    for ratingX, ratingY in ratingPairs:
        sum_xx += ratingX * ratingX
        sum_yy += ratingY * ratingY
        sum_xy += ratingX * ratingY
        numPairs += 1

    numerator = sum_xy
    denominator = sqrt(sum_xx) * sqrt(sum_yy)

    score = 0
    if (denominator):
        score = (numerator / (float(denominator)))

    return (score, numPairs)

# if __name__ == "__main__":

    # sc = SparkContext()
    # data = sc.textFile("hdfs://master/user/spark/spark101/movies/usernum55")
    #                                                                   user          movie       rating
    # user_movie_ratings = data.map(lambda l: l.split()).map(lambda l: (int(l[0]), (int(l[1]), float(l[2]))))   

    data = sc.textFile("hdfs://master/user/spark/spark101/movies/rating50")
    
    user_movie_ratings = data.map(lambda l: l.split()).map(lambda l: (int(l[2]), (int(l[0]), float(l[1]))))

    self_joined_ratings = user_movie_ratings.join(user_movie_ratings)

    distinct_self_joined_ratings = self_joined_ratings.filter(remove_duplicates)

    movie_pairs = distinct_self_joined_ratings.map(make_movie_pairs)

    movie_pair_ratings = movie_pairs.groupByKey()

    movie_pair_with_scores = movie_pair_ratings.mapValues(compute_score)

    # movies_similarity_result = movie_pair_with_scores.collect()   #action

##################存成json文字#############################      
scores = movie_pair_with_scores.map(lambda p: (int(p[0][0]),int(p[0][1]),float(p[1][0]),int(p[1][1]))) 
schema = "in int, out int, sim float, con int"
df2 = spark.createDataFrame(scores,schema)
#df2.printSchema()
#df2.show(20) 

!cd /home/spark/Desktop/spark101/movies/ ;touch data7 
import pandas
df3 = df2.toPandas() 
df3.to_json('~/Desktop/spark101/movies/data40n',orient = "records")

##################insert to mongo############################
import json
from pymongo import MongoClient

myclient = MongoClient("mongodb://10.120.26.13:27017/")
db = myclient["MOVIE"]
Collection = db["data35"]

with open('/home/spark/Desktop/spark101/movies/data40n') as file:
    file_data = json.load(file)

if isinstance(file_data, list):
    Collection.insert_many(file_data)
else:
    Collection.insert_one(file_data)
