import os
import numpy as np
import pandas as pd
from surprise import dump

class RecomendaEasy:
  @staticmethod
  def recomenda(user_id):
    predictions, algo = RecomendaEasy.load_by('svd')
    new_set = RecomendaEasy.conteudo_novo(user_id, predictions)
    df = algo.test(new_set)
    df.sort_values(by='err')[:10]

  @staticmethod
  def conteudo_novo(user_id, predictions):
    dataset = RecomendaEasy.load_dataset(predictions)
    iids = dataset['iid'].unique()
    recomendados = dataset.loc[dataset['uid'] == user_id, 'iid']
    diff = np.setdiff1d(iids, recomendados, True)
    return [[user_id, iid, 4.] for iid in diff]

  @staticmethod
  def load_by(file):
    predictions_path = os.path.join(os.path.dirname(__file__), f'../modelo/{file}_20190925')
    return dump.load(predictions_path)

  @staticmethod
  def load_dataset(predictions):
    return pd.DataFrame(predictions, columns=['uid', 'iid', 'rui', 'est', 'details'])
