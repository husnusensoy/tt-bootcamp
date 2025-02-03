import duckdb
from jinja2 import Template

# 📍 Dosya yolları
ratings_file_pattern = '/Users/2na/Documents/binge/rating_*.txt'
movies_file = '/Users/2na/Documents/binge/movie_titles.csv'

# DuckDB bağlantısı
con = duckdb.connect()

# 📥 1. Adım: Ratings ve Movie Titles verilerini yükle
con.execute(f"""
    CREATE OR REPLACE TABLE ratings AS
    SELECT * FROM read_csv_auto('{ratings_file_pattern}', 
        HEADER=False, 
        DELIM=',', 
        COLUMNS={{'movie_id': 'VARCHAR', 'user_id': 'VARCHAR', 'rating_date': 'DATE', 'rating': 'INTEGER'}}
    );

    CREATE OR REPLACE TABLE movies AS
    SELECT * FROM read_csv('{movies_file}', 
        HEADER=True, 
        DELIM=',', 
        COLUMNS={{'movie_id': 'VARCHAR', 'movie_year': 'INTEGER', 'movie_name': 'VARCHAR'}}, 
        AUTO_DETECT=FALSE,
        IGNORE_ERRORS=TRUE
    );
""")

# 🎯 İlk satırdaki user_id'yi belirleme
target_user_id = 822109

# 🗒️ 2. Adım: Jinja2 ile SQL sorgusu
sql_template = Template("""
WITH GlobalStats AS (
    SELECT 
        AVG(rating) AS global_avg_rating
    FROM ratings
),

WatchedMovies AS (
    SELECT 
        r.movie_id,
        COALESCE(m.movie_name, 'Unknown Movie') AS movie_name,
        AVG(r.rating) AS avg_rating,
        COUNT(*) AS watch_count
    FROM ratings r
    LEFT JOIN movies m ON CAST(r.movie_id AS VARCHAR) = CAST(m.movie_id AS VARCHAR)
    WHERE r.user_id = '{{ target_user }}'
    GROUP BY r.movie_id, m.movie_name
),

SimilarUsers AS (
    SELECT
        r2.user_id AS similar_user,
        COUNT(*) AS common_movies
    FROM ratings r1
    JOIN ratings r2 ON r1.movie_id = r2.movie_id AND r1.user_id != r2.user_id
    WHERE r1.user_id = '{{ target_user }}'
    GROUP BY r2.user_id
    ORDER BY common_movies DESC
    LIMIT 10
),

CandidateMovies AS (
    SELECT
        r.movie_id,
        COALESCE(m.movie_name, 'Unknown Movie') AS movie_name,
        AVG(r.rating) AS avg_rating,
        COUNT(*) AS watch_count
    FROM ratings r
    JOIN SimilarUsers su ON r.user_id = su.similar_user
    LEFT JOIN movies m ON CAST(r.movie_id AS VARCHAR) = CAST(m.movie_id AS VARCHAR)
    WHERE r.movie_id NOT IN (SELECT movie_id FROM WatchedMovies)
    GROUP BY r.movie_id, m.movie_name
),

BayesianRecommendations AS (
    SELECT
        c.movie_id,
        c.movie_name,
        c.avg_rating,
        c.watch_count,
        (c.watch_count / (c.watch_count + 5.0)) * c.avg_rating + 
        (5.0 / (c.watch_count + 5.0)) * g.global_avg_rating AS bayesian_score
    FROM CandidateMovies c
    CROSS JOIN GlobalStats g
)

SELECT
    b.movie_name AS recommended_movie,
    ROUND(b.bayesian_score, 2) AS recommended_bayesian_score,
    b.watch_count AS recommended_watch_count,
    ROUND(b.avg_rating, 2) AS avg_rating
FROM BayesianRecommendations b
ORDER BY recommended_bayesian_score DESC NULLS LAST
LIMIT 30;
""")

# 🗂️ 3. Adım: SQL Sorgusunu çalıştır
rendered_sql = sql_template.render(target_user=target_user_id)
result = con.execute(rendered_sql).fetchdf()

# 📊 4. Adım: Sonuçları göster
print(f"\n🎯 Öneriler, User ID: {target_user_id} için yapılmıştır.\n")

print("\n📢 Önerilen Filmler:")
recommended_movies = result[['recommended_movie', 'recommended_bayesian_score', 'recommended_watch_count', 'avg_rating']].dropna()
for index, row in recommended_movies.iterrows():
    print(f"Film: {row['recommended_movie']}, Bayesian Puanı: {row['recommended_bayesian_score']}, İzlenme Sayısı: {int(row['recommended_watch_count'])}, Ortalama Puan: {row['avg_rating']}")
