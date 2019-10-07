import os
import hashlib
import pandas as pd

currnt_path = os.path.dirname(__file__)
books = pd.read_csv(os.path.join(currnt_path, 'books.csv')).iloc[:3000]
books.to_csv(os.path.join(currnt_path, "books_cut.csv"),
             index=False)

# print(books)
ranting=pd.read_csv(os.path.join(currnt_path, 'ratings.csv'))
merged = ranting.merge(books, on='book_id')
# print(merged)

clean = merged.dropna()
cut = clean.groupby('user_id').filter(lambda x: x['user_id'].count() <= 80)

print(cut)

clean.to_csv(os.path.join(currnt_path, "merged.csv"),
             index=False, columns=['user_id', 'book_id', 'rating'])
