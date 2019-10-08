import os
import hashlib
import pandas as pd
from datetime import datetime
from surprise import dump, Reader, Dataset, SVD, accuracy
from surprise.model_selection import train_test_split

currnt_path = os.path.dirname(__file__)
ratings = pd.read_csv(os.path.join(currnt_path, 'ratings_last_version.csv'))

min_book_ratings = 9
filter_books = ratings['book_id'].value_counts() > min_book_ratings
filter_books = filter_books[filter_books].index.tolist()

min_user_ratings = 80
filter_users = ratings['user_id'].value_counts() > min_user_ratings
filter_users = filter_users[filter_users].index.tolist()

df_new = ratings[(ratings['book_id'].isin(filter_books)) &
                 (ratings['user_id'].isin(filter_users))]

reader = Reader(rating_scale=(1, 5))
dataset = Dataset.load_from_df(ratings[['user_id', 'book_id', 'rating']], reader)

algo = SVD(n_epochs=5)
trainset, testset = train_test_split(dataset, test_size=0.25)
predictions = algo.fit(trainset).test(testset)
accuracy.rmse(predictions)

dump.dump('./algo_temp', None, algo)
_, algo1 = dump.load('./algo_temp')
print(algo1.predict(9938847, 664))
