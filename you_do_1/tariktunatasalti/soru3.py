import duckdb
import pandas as pd
from jinja2 import Template

ratings_file_pattern = "/Users/2na/Documents/binge/rating_*.txt"
movies_file = "/Users/2na/Documents/binge/movie_titles.csv"

con = duckdb.connect()

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

movies_df = con.execute("""
    SELECT m.movie_id, m.movie_name
    FROM movies m
    JOIN (
        SELECT movie_id, COUNT(*) AS watch_count 
        FROM ratings 
        GROUP BY movie_id
    ) r 
    ON m.movie_id = r.movie_id
    WHERE r.watch_count >= 30
    ORDER BY m.movie_id
    LIMIT 6
""").fetchdf()

movie_pairs = [(movies_df.iloc[i]['movie_id'], movies_df.iloc[i+1]['movie_id']) for i in range(0, 6, 2)]

sql_template = Template("""
WITH GlobalMovieStats AS (
    SELECT 
        movie_id, 
        COUNT(*) AS watch_count,
        AVG(rating) AS avg_rating
    FROM ratings
    GROUP BY movie_id
),

GlobalStats AS (
    SELECT 
        AVG(avg_rating) AS global_avg_rating,
        AVG(watch_count) AS avg_watch_count
    FROM GlobalMovieStats
),

MovieRatings AS (
    SELECT 
        r.movie_id, 
        r.rating, 
        COUNT(*) AS rating_count,
        gms.watch_count
    FROM ratings r
    JOIN GlobalMovieStats gms ON r.movie_id = gms.movie_id
    WHERE r.movie_id IN ('{{ movie_a }}', '{{ movie_b }}')
    GROUP BY r.movie_id, r.rating, gms.watch_count
),

TotalRatings AS (
    SELECT 
        movie_id, 
        SUM(rating_count) AS total_count
    FROM MovieRatings
    GROUP BY movie_id
),

BayesianNormalized AS (
    SELECT 
        m.movie_id,
        m.rating,
        (m.rating_count + (g.global_avg_rating * (m.watch_count / g.avg_watch_count))) / 
        (t.total_count + (m.watch_count / g.avg_watch_count)) AS normalized_prob
    FROM MovieRatings m
    JOIN TotalRatings t ON m.movie_id = t.movie_id
    CROSS JOIN GlobalStats g
),

KL_Calculation AS (
    SELECT 
        b1.movie_id AS movie_a,
        b2.movie_id AS movie_b,
        SUM(b1.normalized_prob * LOG(b1.normalized_prob / NULLIF(b2.normalized_prob, 0))) AS kl_a_b,
        SUM(b2.normalized_prob * LOG(b2.normalized_prob / NULLIF(b1.normalized_prob, 0))) AS kl_b_a
    FROM BayesianNormalized b1
    JOIN BayesianNormalized b2 ON b1.rating = b2.rating
    WHERE b1.movie_id = '{{ movie_a }}' AND b2.movie_id = '{{ movie_b }}'
    GROUP BY b1.movie_id, b2.movie_id
)

SELECT 
    kl.movie_a,
    m1.movie_name AS movie_a_name,
    kl.movie_b,
    m2.movie_name AS movie_b_name,
    kl.kl_a_b AS kl_divergence_a_b,
    kl.kl_b_a AS kl_divergence_b_a
FROM KL_Calculation kl
JOIN movies m1 ON kl.movie_a = m1.movie_id
JOIN movies m2 ON kl.movie_b = m2.movie_id;
""")

for movie_a, movie_b in movie_pairs:
    rendered_sql = sql_template.render(movie_a=movie_a, movie_b=movie_b)
    result = con.execute(rendered_sql).fetchdf()

    movie_a_name = result['movie_a_name'][0]
    movie_b_name = result['movie_b_name'][0]
    kl_a_b = result['kl_divergence_a_b'][0]
    kl_b_a = result['kl_divergence_b_a'][0]

    print(f"\nFilm Çifti: {movie_a_name} ({movie_a}) vs {movie_b_name} ({movie_b})")

    if kl_a_b < 0.05 and kl_b_a < 0.05:
        print("Filmler çok benzer, biri kaldırılabilir.")
    elif kl_a_b < 0.2 and kl_b_a < 0.2:
        print("Filmler biraz farklı, ama benzer bir kitleye hitap edebilir.")
    else:
        print("Filmler oldukça farklı, ikisi de sistemde kalmalı.")
