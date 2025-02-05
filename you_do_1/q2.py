import duckdb
import os
import glob

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



# ortak filmleri olan kullanıcı çiftleri belirlenip benzer kullanıcıların puanlarına göre tahmini film puanları hesaplanır.

q2 = """
    with puanlar as materialized (
        select 
            column1 as kullanici_id, 
            column0 as film_id, 
            column3 as puan
        from (
            select * from rating_1
            union all
            select * from rating_2
            union all
            select * from rating_3
            union all
            select * from rating_4
        )
    ),
    aktif_kullanicilar as materialized (
        select distinct kullanici_id from puanlar 
        using sample 1000
    ),
    ciftler as materialized (
        select 
            a.kullanici_id as user1, 
            b.kullanici_id as user2, 
            count(*) as ortak_filmler
        from puanlar a
        join puanlar b 
            on a.film_id = b.film_id 
            and a.kullanici_id != b.kullanici_id
            and a.kullanici_id in (select kullanici_id from aktif_kullanicilar)
            and b.kullanici_id in (select kullanici_id from aktif_kullanicilar)
        group by user1, user2
        having ortak_filmler > 10  
    ),
    avg_film as materialized (
        select 
            kp.film_id, 
            mt.title as film_adi, 
            sum(kp.puan) as toplam_puan, 
            count(kp.puan) as puan_sayisi
        from puanlar kp
        join ciftler kc on kp.kullanici_id = kc.user2
        join movie_titles mt on kp.film_id = mt.movie_id
        and kp.film_id not in (
            select film_id from puanlar where kullanici_id = kc.user1
        )
        group by kp.film_id, mt.title
    )
    select 
        film_id, 
        film_adi, 
        toplam_puan / puan_sayisi as tahmini_puan
    from avg_film
    order by tahmini_puan desc
    limit 10;

"""


result = conn.execute(q2).fetchdf()
print(result)

conn.close()
