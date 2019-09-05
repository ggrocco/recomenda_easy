import os
import pandas as pd
from pymongo import MongoClient
from dotenv import load_dotenv
from surprise import NormalPredictor
from surprise import Dataset
from surprise import Reader
from surprise.model_selection import cross_validate

# TODO: REMOVER
# https://towardsdatascience.com/building-and-testing-recommender-systems-with-surprise-step-by-step-d4ba702ef80b

# Carrega as variaves de ambinte.
load_dotenv()
uri = os.environ.get('MONGODB_URI')

# Faz a conexão com o banco.
client = MongoClient(uri)
database = client.get_database()
db = client['heroku_l5cst43x']
comments = db['comments']

# Monda o data frame.
df = pd.DataFrame(list(comments.find({'AVALIADOR_ID': {'$ne': 'ANONIMO'}}, {
                  '_id': 0, 'USER_ID': 1, 'ISBN': 1, 'NOTA': 1})))

# Analise das notas.
from plotly.offline import init_notebook_mode, plot, iplot
import plotly.graph_objs as go
data = df['NOTA'].value_counts().sort_index(ascending=False)
trace = go.Bar(x=data.index,
               text=['{:.1f} %'.format(val) for val in (data.values / df.shape[0] * 100)],
               textposition='auto',
               textfont=dict(color='#000000'),
               y=data.values)

# Create o plot
layout = dict(title='Distribuição das {} notas'.format(df.shape[0]),
              xaxis=dict(title='Nota'),
              yaxis=dict(title='Total'))
fig = go.Figure(data=[trace], layout=layout)
fig.show()


# Analise dos livros.
data = df.groupby('ISBN')['NOTA'].count()
trace = go.Histogram(x=data.values,
                     name='Notas',
                     xbins=dict(start=0,
                                end=12,
                                size=1))
# Create layout
layout = go.Layout(title='Distribuição dos livros',
                   xaxis=dict(title='Quantidade de avaliações'),
                   yaxis=dict(title='Numero de livros'),
                   bargap=0.2)

# Create plot
fig = go.Figure(data=[trace], layout=layout)
fig.show()


notas = df.groupby('ISBN')['NOTA'].count().reset_index(
).sort_values('NOTA', ascending=False)[:40]
print(notas)

# Number of ratings per user
data = df.groupby('USER_ID')['NOTA'].count().clip(upper=50)

# Create trace
trace = go.Histogram(x=data.values,
                     name='Ratings',
                     xbins=dict(start=0,
                                end=50,
                                size=1))
# Create layout
layout = go.Layout(title='Distribution Of Number of Ratings Per User (Clipped at 50)',
                   xaxis=dict(title='Ratings Per User'),
                   yaxis=dict(title='Count'),
                   bargap=0.2)

# Create plot
fig = go.Figure(data=[trace], layout=layout)
fig.show()

# Define o rating_scale.
reader = Reader(rating_scale=(1, 5))

# Monda o dataset sobre o data frame e scala.
data = Dataset.load_from_df(df[['USER_ID', 'ISBN', 'NOTA']], reader)
cv = cross_validate(NormalPredictor(), data, cv=2)
print(cv)
