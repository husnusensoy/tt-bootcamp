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
bayesian_weight = 5.0 

sql_template = Template("""
WITH GlobalStats AS (
    SELECT
        AVG(rating) AS global_avg_rating
    FROM ratings
),

SummaryMovies AS ( 
    SELECT 
        r.movie_id,
        COALESCE(m.movie_name, 'Unknown Movie') AS movie_name,
        AVG (r.rating) AS avg_rating,
        COUNT (*) AS watch_count
    FROM ratings r
    LEFT JOIN movies m ON r.movie_id = m.movie_id
    GROUP BY r.movie_id, m.movie_name
),

BayesianRecommendations AS (
    SELECT
        s.movie_id,
        s.movie_name,
        s.avg_rating,
        s.watch_count,
        (s.watch_count / (s.watch_count + {{bayesian_weight}} )) * s.avg_rating +
        ({{bayesian_weight}} / (s.watch_count + {{bayesian_weight}})) * g.global_avg_rating AS bayesian_score
    FROM SummaryMovies s
    CROSS JOIN GlobalStats g
)

SELECT 
    b.movie_name AS recommended_movie,
    Round(b.bayesian_score,2) AS recommended_bayesian_score,
    b.watch_count AS recommended_watch_count,
    ROUND (b.avg_rating,2) AS avg_rating
FROM BayesianRecommendations b
ORDER BY recommended_bayesian_score DESC NULLS LAST
LIMIT 30;
""")


sql_query = sql_template.render(bayesian_weight=bayesian_weight)

result = con.execute(sql_query).fetchdf()

result.to_csv("soru1.csv", index=False)