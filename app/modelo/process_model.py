from surprise import accuracy
import os
import pandas as pd
from app import mongo
from datetime import datetime
from dotenv import load_dotenv
from surprise import dump, Reader, Dataset, SVD
from surprise.model_selection import train_test_split

class ProcessModel:
  @staticmethod
  def build_model():
    ratings = mongo.db.ratings.find({})
    df = pd.DataFrame(list(ratings))
    reader = Reader(rating_scale=(1, 5))
    data = Dataset.load_from_df(df[['user_id', 'book_id', 'rating']], reader)
    predictions, algo = ProcessModel.predicting(data)
    ProcessModel.save(predictions, algo)

  @staticmethod
  def predicting(data):
    algo = SVD(n_epochs=5)
    print('Inicio processo predição', str(datetime.now()))
    trainset, testset = train_test_split(data, test_size=0.25)
    predictions = algo.fit(trainset).test(testset)
    print('RMSE:', accuracy.rmse(predictions))
    print('Termino processo predição', str(datetime.now()))
    return (predictions, algo)

  @staticmethod
  def save(predictions, algo):
    dump.dump(f'./app/modelo/dump_svd', predictions, algo)
    print('Saved')
