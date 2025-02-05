import polars as pl
import numpy as np

df_titles = pl.scan_csv(
    "data/binge/movie_titles.csv", encoding="utf8", ignore_errors=True, has_header=False,
    new_columns=["movie_id", "movie_year", "movie_name"],
    truncate_ragged_lines=True
).with_columns(pl.col("movie_id").cast(pl.Int64))

ratings_files = [
    "data/binge/rating_1.txt",
    "data/binge/rating_2.txt",
    "data/binge/rating_3.txt",
    "data/binge/rating_4.txt"
]

df_ratings = pl.concat([
    pl.scan_csv(f, new_columns=["movie_id", "user_id", "date", "rating"]) for f in ratings_files
]).with_columns(pl.col("movie_id").cast(pl.Int64))

df_ratings = df_ratings.collect()

user_ids = {id: idx for idx, id in enumerate(df_ratings["user_id"].unique())}
movie_ids = {id: idx for idx, id in enumerate(df_ratings["movie_id"].unique())}

num_users = len(user_ids)
num_movies = len(movie_ids)

#matris
r = np.zeros((num_users, num_movies))
for row in df_ratings.iter_rows():
    user_idx = user_ids[row[1]]
    movie_idx = movie_ids[row[0]]
    r[user_idx, movie_idx] = row[3]

# ALS Fonksiyonu
def als_train(r, k=10, lamba=0.1, iterations=10):
    num_users, num_movies = r.shape
    p = np.random.rand(num_users, k)
    q = np.random.rand(num_movies, k)

    for _ in range(iterations):
        for u in range(num_users):
            r_u = r[u, :]
            q_tq = q.T @ q + lamba * np.eye(k)
            p[u, :] = np.linalg.solve(q_tq, q.T @ r_u)

        for i in range(num_movies):
            r_i = r[:, i]
            p_tp = p.T @ p + lamba * np.eye(k)
            q[i, :] = np.linalg.solve(p_tp, p.T @ r_i)

    return p, q

p, q = als_train(r)

def recommend_movies(user_id, num_recommendations=10):
    if user_id not in user_ids:
        print("Kullanıcı bulunamadı")
    
    user_idx = user_ids[user_id]
    scores = p[user_idx] @ q.T
    movie_indices = np.argsort(scores)[::-1][:num_recommendations]
    
    recommended_movies = [list(movie_ids.keys())[i] for i in movie_indices]
    
    return df_titles.filter(pl.col("movie_id").is_in(recommended_movies)).collect()

print(recommend_movies(1))
