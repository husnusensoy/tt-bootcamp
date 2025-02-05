import duckdb
import os
import glob
import tempfile


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


# IMDB Ağırlıklı Puan

# WR = (v / (v + m) * R) + (m / (v + m) * C)

# WR -> Ağırlıklı puan 
# R  -> Filmin ortalama puanı
# v  -> Filme verilen toplam oy sayısı
# m  -> Minimum oy sayısı
# C  -> Tüm filmlerin ortalama puanı



q1 = """
    with movie_stats as (
        select 
            mt.movie_id, 
            mt.title as film_adi, 
            count(r.movie_id) as puan_sayisi, 
            avg(r.rating) as ortalama_puan
        from movie_titles mt
        join (
            select column0 as movie_id, column3 as rating from rating_1
            union all
            select column0 as movie_id, column3 as rating from rating_2
            union all
            select column0 as movie_id, column3 as rating from rating_3
            union all
            select column0 as movie_id, column3 as rating from rating_4
        ) r on mt.movie_id = r.movie_id
        group by mt.movie_id, mt.title
    ),
    sabitler as (
        select 
            avg(ortalama_puan) as c, 
            percentile_cont(0.90) within group (order by puan_sayisi) as m
        from movie_stats
    )
    select 
        fi.movie_id, 
        fi.film_adi, 
        fi.puan_sayisi, 
        fi.ortalama_puan,
        (fi.puan_sayisi / (fi.puan_sayisi + s.m) * fi.ortalama_puan) + 
        (s.m / (fi.puan_sayisi + s.m) * s.c) as agirlikli_puan
    from movie_stats fi, sabitler s
    where fi.puan_sayisi >= s.m
    order by agirlikli_puan desc
    limit 10;

"""

result = conn.execute(q1).fetchdf()
print(result)



