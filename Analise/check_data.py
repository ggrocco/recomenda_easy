import plotly.graph_objs as go
from plotly.offline import init_notebook_mode, plot, iplot
import os
import pandas as pd

currnt_path = os.path.dirname(__file__)
path = os.path.join(currnt_path, 'reviews.json')

df = pd.read_json(path, orient='records')
df = pd.DataFrame(df, columns=['USER_ID', 'ISBN', 'NOTA'])

notas = df.groupby('ISBN')['NOTA'].count().reset_index(
).sort_values('NOTA', ascending=False)[:10]
print(notas)

# Analise das notas.
data = df['NOTA'].value_counts().sort_index(ascending=False)
trace = go.Bar(x=data.index,
               text=['{:.1f} %'.format(val) for val in (
                   data.values / df.shape[0] * 100)],
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
                                end=100,
                                size=5))
# Create layout
layout = go.Layout(title='Distribuição dos livros',
                   xaxis=dict(title='Quantidade de avaliações'),
                   yaxis=dict(title='Numero de livros'),
                   bargap=0.2)

# Create plot
fig = go.Figure(data=[trace], layout=layout)
fig.show()

# Number of ratings per user
data = df.groupby('USER_ID')['NOTA'].count().clip(upper=50)

# Create trace
trace = go.Histogram(x=data.values,
                     name='Ratings',
                     xbins=dict(start=2,
                                end=100,
                                size=2))
# Create layout
layout = go.Layout(title='Distribution Of Number of Ratings Per User (Clipped at 50)',
                   xaxis=dict(title='Ratings Per User'),
                   yaxis=dict(title='Count'),
                   bargap=0.2)

# Create plot
fig = go.Figure(data=[trace], layout=layout)
fig.show()

