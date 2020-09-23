from pyspark.ml.recommendation import ALS, ALSModel

if __name__ == "__main__":

    spark = SparkSession \
        .builder \
        .getOrCreate()

model2 = ALSModel.load("file:///home/spark/Desktop/spark101/movies_similarity/data/movies/150W_2748")

movie_uers = model2.recommendForAllItems(3)
user_movies = model2.recommendForAllUsers(3)

input_movieId = '3569'
movie_set = set()
user_row = movie_uers.where('movieId=%s' % (input_movieId)).collect()
user1 = str(((user_row[0].recommendations)[0]).userId)
user2 = str(((user_row[0].recommendations)[1]).userId)
user3 = str(((user_row[0].recommendations)[2]).userId)
near_user_list = [user1, user2, user3]       

for u in near_user_list:
    movie_row = user_movies.where('userId=%s' % (u)).collect()
    movie1 = ((movie_row[0].recommendations)[0]).movieId
    movie2 = ((movie_row[0].recommendations)[1]).movieId
    movie3 = ((movie_row[0].recommendations)[2]).movieId
    movie_set.add(movie1)
    movie_set.add(movie2)
    movie_set.add(movie3)
print(movie_set)
