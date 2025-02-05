import pandas as pd

movie_titles = pd.read_csv('movie_titles.csv', delimiter=',', names=['movie_id', 'release_year', 'movie_title'], encoding='latin1', on_bad_lines='skip')
movie_titles.to_csv('movie_titles_with_headers.csv', index=False)
movie_titles_with_headers = pd.read_csv('movie_titles_with_headers.csv')
print(movie_titles_with_headers.head())

