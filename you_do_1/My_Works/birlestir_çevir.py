import pandas as pd


rating_files = ['rating_1.txt', 'rating_2.txt', 'rating_3.txt', 'rating_4.txt']
ratings_list = []

for file in rating_files:
    df = pd.read_csv(file, delimiter=',', names=['movie_id', 'user_id', 'date', 'rating'])
    ratings_list.append(df)


all_ratings = pd.concat(ratings_list)


all_ratings.to_csv('merged_ratings.csv', index=False)
