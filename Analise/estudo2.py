import os
import pandas as pd
import numpy as np

# graficos
from plotly.offline import plot, iplot
import plotly.graph_objs as go


# Faz a conexão com o banco.
from pymongo import MongoClient
uri = 'mongodb://heroku_l5cst43x:p73b72vp244qf874m5aple0jf1@ds131312.mlab.com:31312/heroku_l5cst43x'
client = MongoClient(uri)
database = client.get_database()
db = client['heroku_l5cst43x']
ratings = db['ratings']

# currnt_path = os.path.dirname(__file__)
# reviews = pd.read_csv(os.path.join(currnt_path, 'ratings.csv'))
# books = pd.read_csv(os.path.join(currnt_path, 'books.csv'))

# Dimensão dos dataframes
# print("books:", books.shape)
# print("reviews:", reviews.shape)

# Merge
# merged = reviews.merge(books, on='book_id')
# print(merged.shape)
# print(merged.head)

# Separa somente as colunas importantes pra analise.
# df = merged[['user_id', 'book_id', 'rating']]
df=pd.DataFrame(list(ratings.find({})))
df.drop(columns="_id", inplace=True)
print('Dimensão:', df.shape)
print('Primeiros valores:', df.head())

# Exploração dos dados

# Distribuição das notas
data = df['rating'].value_counts().sort_index(ascending=False)
trace = go.Bar(x=data.index,
               text=['{:.1f} %'.format(val) for val in (
                   data.values / df.shape[0] * 100)],
               textposition='auto',
               textfont=dict(color='#000000'),
               y=data.values,
               )
layout = dict(title='Distribuição dos {} reviews'.format(df.shape[0]),
              xaxis=dict(title='Nota'),
              yaxis=dict(title='Total'))
fig = go.Figure(data=[trace], layout=layout)
fig.show()

# Numero de notas por livro
data = df.groupby('book_id')['rating'].count()
trace = go.Histogram(x=data.values,
                     name='Nots',
                     xbins=dict(start=0,
                                end=500,
                                size=100))
layout = go.Layout(title='Distribuição de notas por livro (Clipped at 100)',
                   xaxis=dict(title='Total de notas por livro'),
                   yaxis=dict(title='Total'),
                   bargap=0.2)
fig = go.Figure(data=[trace], layout=layout)
fig.show()


# Numero de notas por ususario
data = df.groupby('user_id')['rating'].count()
trace = go.Histogram(x=data.values,
                     name='Notas',
                     xbins=dict(start=0,
                                end=400,
                                size=10))
layout = go.Layout(title='Numero de notas por usuario',
                   xaxis=dict(title='Notas por usuario'),
                   yaxis=dict(title='Total'),
                   bargap=0.2)
fig = go.Figure(data=[trace], layout=layout)
fig.show()

print('Com mais rating:', df.groupby('book_id')['rating'].count().reset_index(
).sort_values('rating', ascending=False)[:10])
print('Com menos rating:', df.groupby('book_id')['rating'].count().reset_index(
).sort_values('rating', ascending=True)[:10])

from surprise.model_selection import cross_validate
from surprise import Reader, Dataset, NormalPredictor, KNNBasic, KNNWithMeans
from surprise import KNNWithZScore, KNNBaseline, SVD, BaselineOnly, SVDpp
from surprise import NMF, SlopeOne, CoClustering

reader = Reader(rating_scale=(1, 5))
data = Dataset.load_from_df(df[['user_id', 'book_id', 'rating']], reader)

benchmark = []
# Testa todos os algoritimos
for algoritimo in [SVD(), SVDpp(), SlopeOne(), NMF(), NormalPredictor(), KNNBaseline(), KNNBasic(), KNNWithMeans(), KNNWithZScore(), BaselineOnly(), CoClustering()]:
    print('Inicio algoritimo', algoritimo)
    # Cross validation
    resultados = cross_validate(algoritimo, data, measures=['RMSE'], cv=3, verbose=False)
    tmp = pd.DataFrame.from_dict(resultados).mean(axis=0)
    tmp = tmp.append(pd.Series([str(algoritimo).split(' ')[0].split('.')[-1]], index=['Algoritimo']))
    benchmark.append(tmp)

pd.DataFrame(benchmark).set_index('Algoritimo').sort_values('test_rmse')


print('Using ALS')
bsl_options = {'method': 'als', 'n_epochs': 5, 'reg_u': 12, 'reg_i': 5}
algo = BaselineOnly(bsl_options=bsl_options)
cross_validate(algo, data, measures=['RMSE'], cv=3, verbose=False)


from surprise.model_selection import train_test_split
from surprise import accuracy
trainset, testset = train_test_split(data, test_size=0.25)
algo = BaselineOnly(bsl_options=bsl_options)
predictions = algo.fit(trainset).test(testset)
accuracy.rmse(predictions)


trainset = algo.trainset

def get_Iu(uid):
    """ return the number of items rated by given user
    args:
      uid: the id of the user
    returns:
      the number of items rated by the user
    """
    try:
        return len(trainset.ur[trainset.to_inner_uid(uid)])
    except ValueError: # user was not part of the trainset
        return 0

def get_Ui(iid):
    """ return number of users that have rated given item
    args:
      iid: the raw id of the item
    returns:
      the number of users that have rated the item.
    """
    try:
        return len(trainset.ir[trainset.to_inner_iid(iid)])
    except ValueError:
        return 0

df = pd.DataFrame(predictions, columns=['uid', 'iid', 'rui', 'est', 'details'])
df['Iu'] = df.uid.apply(get_Iu)
df['Ui'] = df.iid.apply(get_Ui)
df['err'] = abs(df.est - df.rui)


df.head()

best_predictions = df.sort_values(by='err')[:10]
best_predictions

worst_predictions = df.sort_values(by='err')[-10:]
worst_predictions

df.loc[df['book_id'] == '055358264X']['rating'].describe()


import matplotlib.pyplot as plt
# %matplotlib notebook

df.loc[df['book_id'] == '055358264X']['rating'].hist()
plt.xlabel('rating')
plt.ylabel('Number of ratings')
plt.title('Number of ratings book ISBN 055358264X has received')
plt.show()
