import duckdb
from jinja2 import Template

ratings_file_pattern = "/Users/2na/Documents/binge/rating_*.txt"
movies_file = "/Users/2na/Documents/binge/movie_titles.csv"

con = duckdb.connect()

# SQL komutunu çalıştır
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

target_user_id = 822109
bayesian_weight = 25.0 

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
    LEFT JOIN movies m ON r.movie_id = m.movie_id
    WHERE r.user_id = '{{ target_user }}'
    GROUP BY r.movie_id, m.movie_name
),

UserMovies AS (
    SELECT user_id, LIST(movie_id) AS movies_watched
    FROM ratings
    GROUP BY user_id
),

JaccardSimilarity AS (
    SELECT
        r2.user_id AS similar_user,
        COUNT(DISTINCT r1.movie_id) * 1.0 / NULLIF(COUNT(DISTINCT r1.movie_id) + COUNT(DISTINCT r2.movie_id) - COUNT(DISTINCT r1.movie_id), 0) AS jaccard_score
    FROM ratings r1
    JOIN ratings r2 ON r1.movie_id = r2.movie_id AND r1.user_id != r2.user_id
    WHERE r1.user_id = '{{ target_user }}'
    GROUP BY r2.user_id
    ORDER BY jaccard_score DESC
    LIMIT 50
),

CandidateMovies AS (
    SELECT
        r.movie_id,
        COALESCE(m.movie_name, 'Unknown Movie') AS movie_name,
        AVG(r.rating) AS avg_rating,
        COUNT(*) AS watch_count,
        SUM(js.jaccard_score) AS total_similarity_score
    FROM ratings r
    JOIN JaccardSimilarity js ON r.user_id = js.similar_user
    LEFT JOIN movies m ON r.movie_id = m.movie_id
    WHERE r.movie_id NOT IN (SELECT movie_id FROM WatchedMovies)
    GROUP BY r.movie_id, m.movie_name
),

BayesianRecommendations AS (
    SELECT 
        c.movie_id,
        c.movie_name,
        c.avg_rating,
        c.watch_count,
        c.total_similarity_score,
        (c.watch_count / (c.watch_count + {{ bayesian_weight }})) * c.avg_rating +
        ({{ bayesian_weight }} / (c.watch_count + {{ bayesian_weight }})) * g.global_avg_rating AS bayesian_score,
        (c.total_similarity_score * c.avg_rating) AS weighted_bayesian_score
    FROM CandidateMovies c
    CROSS JOIN GlobalStats g
)

SELECT
    b.movie_name AS recommended_movie,
    ROUND(b.weighted_bayesian_score, 2) AS recommended_weighted_score,
    ROUND(b.bayesian_score, 2) AS recommended_bayesian_score,
    b.watch_count AS recommended_watch_count,
    ROUND (b.avg_rating, 2) AS avg_rating
FROM BayesianRecommendations b
ORDER BY recommended_weighted_score DESC NULLS LAST
LIMIT 30;
""")

sql_query = sql_template.render(target_user=target_user_id, bayesian_weight=bayesian_weight)

result = con.execute(sql_query).fetchdf()

result.to_csv("soru2.csv", index=False)

import pandas as pd
pd.set_option('display.max_rows', None)  
pd.set_option('display.max_columns', None)
print(result)
