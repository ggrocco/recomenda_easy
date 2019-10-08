import os
import numpy as np
import pandas as pd
from surprise import dump

class RecomendaEasy:
  @staticmethod
  def recomenda(books, user_id):
    _, svd = RecomendaEasy.load_dump()
    books = pd.DataFrame(books)
    books['est'] = books['book_id'].apply(lambda x: svd.predict(user_id, x).est)
    books = books.sort_values('est', ascending=False)
    return books.head(30)

  @staticmethod
  def load_dump():
    predictions_path = os.path.join(os.path.dirname(__file__), '../modelo/algo_svd')
    return dump.load(predictions_path)
