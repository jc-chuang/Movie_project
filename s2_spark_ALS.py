from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.ml.feature import VectorAssembler,VectorIndexer,OneHotEncoder,StringIndexer
from pyspark.ml.recommendation import ALS 
from pyspark.ml.evaluation import RegressionEvaluator

if __name__ == "__main__":

    spark = SparkSession \
        .builder \
        .getOrCreate()

    final_data = spark.read.csv("file:///home/spark/Desktop/spark101/movies_similarity/data/movies/new180",sep='\t',inferSchema=True, header=True)
    train_data, test_data = final_data.randomSplit([0.8,0.2])
    
    # Model training
    # Transform the test data using the model to get predictions
    # Evalute model performance with test set
    train_data, test_data = final_data.randomSplit([0.8,0.2])
    als = ALS(maxIter=5,userCol="userId",itemCol="movieId",ratingCol="rating" , coldStartStrategy="drop")
    model = als.fit(train_data)    
    predicted_test_data = model.transform(test_data)    
    evaluator = RegressionEvaluator(predictionCol="prediction", labelCol="rating", metricName="rmse")

    print("rmse: {}".format(evaluator.evaluate(predicted_test_data)))

from pyspark.ml.recommendation import ALS, ALSModel
# model.save("file:///home/spark/Desktop/spark101/movies_similarity/data/movies/2836")
model2 = ALSModel.load("file:///home/spark/Desktop/spark101/movies_similarity/data/movies/2836")

input_movieId = '3569'

movie_uers = model.recommendForAllItems(3)
user_row = movie_uers.where('movieId=%s' % (input_movieId)).collect()

user1 = str(((user_row[0].recommendations)[0]).userId)
user2 = str(((user_row[0].recommendations)[1]).userId)
user3 = str(((user_row[0].recommendations)[2]).userId)
near_user_list = [user1, user2, user3]

user_movies = model.recommendForAllUsers(3)
movie_set = set()

for u in near_user_list:
    movie_row = user_movies.where('userId=%s' % (u)).collect()
    movie1 = ((movie_row[0].recommendations)[0]).movieId
    movie2 = ((movie_row[0].recommendations)[1]).movieId
    movie3 = ((movie_row[0].recommendations)[2]).movieId
    movie_set.add(movie1)
    movie_set.add(movie2)
    movie_set.add(movie3)
print(movie_set)
