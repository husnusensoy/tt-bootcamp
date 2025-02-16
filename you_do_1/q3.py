import duckdb
import os
import glob
import numpy as np
from scipy.stats import entropy


current_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(current_dir, "ratings_db.duckdb")
conn = duckdb.connect(db_path)


for file in glob.glob(os.path.join(current_dir, "rating_*.txt")):
    table_name = os.path.splitext(os.path.basename(file))[0] 
    conn.execute(f"""
        CREATE OR REPLACE TABLE {table_name} AS 
        SELECT * FROM read_csv_auto('{file}')
    """)


movie_titles_file = os.path.join(current_dir, "movie_titles.csv")
if os.path.exists(movie_titles_file):
    conn.execute("""
        CREATE OR REPLACE TABLE movie_titles AS 
        SELECT * FROM read_csv_auto(?, ALL_VARCHAR=TRUE, IGNORE_ERRORS=TRUE,
                                   columns={'movie_id': 'INTEGER', 'year': 'INTEGER', 'title': 'STRING'})
    """, [movie_titles_file])


# Rastgele seçilen iki film için en az 100 puan veren güvenli ve ortak kullanıcıların ortalama puanlarını karşılaştırarak KL Distance hesaplanır.


question_3 = """
with user_rating_counts as (
    select column1 as user_id, count(*) as rating_count
    from rating_1 group by column1
    union all
    select column1, count(*) from rating_2 group by column1
    union all
    select column1, count(*) from rating_3 group by column1
    union all
    select column1, count(*) from rating_4 group by column1
),
guvenli_ortak as (
    select user_id from user_rating_counts where rating_count > 100
),
movie_ratings as (
    select column0 as movie_id, column1 as user_id, column3 as rating from rating_1
    union all
    select column0, column1, column3 from rating_2
    union all
    select column0, column1, column3 from rating_3
    union all
    select column0, column1, column3 from rating_4
),
movies as (
    select movie_id from movie_ratings group by movie_id order by random() limit 2
),
film1_puanlari as (
    select mr.user_id, mr.rating as film1_rating
    from movie_ratings mr
    where mr.movie_id = (select movie_id from movies limit 1 offset 0)
    and mr.user_id in (select user_id from guvenli_ortak)
),
film2_puanlari as (
    select mr.user_id, mr.rating as film2_rating
    from movie_ratings mr
    where mr.movie_id = (select movie_id from movies limit 1 offset 1)
    and mr.user_id in (select user_id from guvenli_ortak)
),
ortak_kullanicilar as (
    select f1.user_id, f1.film1_rating, f2.film2_rating
    from film1_puanlari f1
    inner join film2_puanlari f2 on f1.user_id = f2.user_id
)
select 
    (select movie_id from movies limit 1 offset 0) as film1_id,
    (select movie_id from movies limit 1 offset 1) as film2_id,
    film1_rating, film2_rating
from ortak_kullanicilar;

"""

result = conn.execute(question_3).fetchdf()
conn.close()
film1_id = result['film1_id'][0]
film2_id = result['film2_id'][0]
film1_scores = result['film1_rating'].values
film2_scores = result['film2_rating'].values
hist_bins = np.arange(1, 7) 
film1_hist, _ = np.histogram(film1_scores, bins=hist_bins, density=True)
film2_hist, _ = np.histogram(film2_scores, bins=hist_bins, density=True)





film1_hist += 1e-10
film2_hist += 1e-10

kl_div = entropy(film1_hist, film2_hist)
print(f"Film 1 ID: {film1_id}")
print(f"Film 2 ID: {film2_id}")
print(f"KL Divergence: {kl_div}")


