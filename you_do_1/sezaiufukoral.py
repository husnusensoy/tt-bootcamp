from pathlib import Path
import duckdb
import pandas as pd
from scipy import stats
from sklearn.feature_extraction.text import CountVectorizer
from scipy.special import kl_div
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

conn = duckdb.connect("./database.db")

conn.execute("""
CREATE TABLE IF NOT EXISTS movies (
    movie_id INTEGER PRIMARY KEY,
    movie_year INTEGER,
    movie_name TEXT
)
""")

conn.execute("""
CREATE TABLE IF NOT EXISTS ratings (
    movie_id INTEGER,
    user_id INTEGER,
    date TEXT,
    rating INTEGER
)
""")

conn.execute("""
ALTER TABLE movies ADD COLUMN IF NOT EXISTS weighted_rating FLOAT
""")

def load_ratings_to_db(rating_paths):
    for path in rating_paths:
        full_path = str(Path(path).resolve())
        print(f"Loading file: {full_path}")
        query = f"""
        INSERT INTO ratings (movie_id, user_id, date, rating)
        SELECT DISTINCT
            CAST(column0 AS INTEGER) AS movie_id,
            CAST(column1 AS INTEGER) AS user_id,
            CAST(column2 AS VARCHAR) AS date,
            CAST(column3 AS INTEGER) AS rating
        FROM read_csv_auto('{full_path}', delim=',', header=False)
        """
        conn.execute(query)
    conn.commit()
    print("Ratings data loaded.")

def update_weighted_ratings_in_db():
    query = """
    WITH rating_counts AS (
        SELECT 
            movie_id,
            rating,
            COUNT(*) AS rating_count
        FROM ratings
        GROUP BY movie_id, rating
    ),
    total_ratings AS (
        SELECT 
            movie_id,
            SUM(rating_count) AS total_count
        FROM rating_counts
        GROUP BY movie_id
    )
    UPDATE movies
    SET weighted_rating = (
        SELECT 
            SUM(r.rating * r.rating_count) / ANY_VALUE(tr.total_count)
        FROM rating_counts r
        JOIN total_ratings tr ON r.movie_id = tr.movie_id
        WHERE r.movie_id = movies.movie_id
    )
    WHERE movie_id IN (SELECT DISTINCT movie_id FROM ratings)
    """
    
    conn.execute(query)
        
def load_movies_to_db(movies_path):
    existing_movies_count = conn.execute("SELECT COUNT(*) FROM movies").fetchone()[0]
    
    if existing_movies_count > 0:
        print("Movies data already loaded.")
        return
    
    full_path = str(Path(movies_path).resolve())
    
    query = f"""
    INSERT INTO movies (movie_id, movie_year, movie_name, weighted_rating)
    SELECT DISTINCT
        TRY_CAST(column0 AS INTEGER) AS movie_id,
        TRY_CAST(column1 AS INTEGER) AS movie_year,
        column2 AS movie_name,
        NULL AS weighted_rating
    FROM read_csv(
        '{full_path}', 
        delim=',', 
        header=false,
        quote='"',
        escape='"',
        null_padding=true,
        ignore_errors=true
    )
    WHERE column0 IS NOT NULL AND column1 IS NOT NULL AND column2 IS NOT NULL
    """

    conn.execute(query)
    update_weighted_ratings_in_db()
    print("Movies data loaded.")
    

def get_cold_start_recommendations_sql(size=10):
    query = f"""
    SELECT m.movie_id, m.movie_name, m.movie_year, m.weighted_rating
    FROM movies m
    ORDER BY m.weighted_rating DESC
    LIMIT {size}
    """
    result = conn.execute(query).fetch_df()
    return result

def get_liked_movie_names_sql(user_id):
    query = f"""
    WITH user_ratings AS (
        SELECT movie_id, rating
        FROM ratings
        WHERE user_id = {user_id}
    )
    SELECT m.movie_id, m.movie_name
    FROM user_ratings ur
    JOIN movies m ON ur.movie_id = m.movie_id
    WHERE ur.rating = (SELECT MAX(rating) FROM user_ratings)
    """
    
    result = conn.execute(query).fetch_df()
    return result

def get_bow_df(names):
    if names.empty:
        return pd.DataFrame()
    
    vectorizer = CountVectorizer(stop_words='english', token_pattern=r'\b\w{2,}\b')
    bow = vectorizer.fit_transform(pd.Series(names))
    return pd.DataFrame(bow.toarray(), columns=vectorizer.get_feature_names_out())

def get_top_words(user_id, size=10):
    liked_movie_names = get_liked_movie_names_sql(user_id)
    if liked_movie_names.empty:
        return pd.Series(dtype="object")

    word_frequencies = get_bow_df(liked_movie_names['movie_name']).sum(axis=0)
    
    word_frequencies.index = word_frequencies.index.str.lower()
    
    words_to_remove = ["season", "episode", "edition"]
    word_frequencies = word_frequencies[~word_frequencies.index.isin(words_to_remove)]
    word_frequencies = word_frequencies[~word_frequencies.index.str.contains(r'^\d+$', na=False)]
    
    return word_frequencies.sort_values(ascending=False).head(size)

def get_user_recommendations_sql(user_id, size=10):
    
    liked_movies = get_liked_movie_names_sql(user_id)
    if liked_movies.empty:
        return pd.DataFrame()

    top_words = get_top_words(user_id, size)

    like_conditions = " OR ".join([f"m.movie_name LIKE '%{word}%'" for word in top_words.index])
    
    query_unrated_movies = f"""
    WITH rated_movies AS (
        SELECT movie_id
        FROM ratings
        WHERE user_id = {user_id}
    )
    SELECT m.movie_id, m.movie_name, m.weighted_rating
    FROM movies m
    WHERE m.movie_id NOT IN (SELECT movie_id FROM rated_movies)
    AND ({like_conditions})
    ORDER BY m.weighted_rating DESC
    LIMIT {size}
    """
    
    result = conn.execute(query_unrated_movies).fetch_df()
    return result

def compare_two_movies(movie_id1: int, movie_id2: int):
    query = f"""
        SELECT m.movie_id, m.movie_name, m.movie_year, m.weighted_rating
        FROM movies m
        WHERE m.movie_id IN ({movie_id1}, {movie_id2})
    """
    
    movies_df = conn.execute(query).fetch_df()
    
    if movies_df.shape[0] < 2:
        print("Biri veya her iki film veritabanında bulunamadı.")
        return None

    movies_df.set_index("movie_id", inplace=True)
    movies_df = movies_df.loc[[movie_id1, movie_id2]]
    
    name_1 = movies_df.iloc[0, 0]
    name_2 = movies_df.iloc[1, 0]
    
    weighted_1 = movies_df.iloc[0, -1]
    weighted_2 = movies_df.iloc[1, -1]
    
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform([name_1, name_2])

    tfidf_array1 = tfidf_matrix[0].toarray()[0]
    tfidf_array2 = tfidf_matrix[1].toarray()[0]
    
    epsilon = 1e-10
    tfidf_array1 = np.maximum(tfidf_array1, epsilon)
    tfidf_array2 = np.maximum(tfidf_array2, epsilon)

    kl_divergence = kl_div(tfidf_array1, tfidf_array2).sum()

    print("\nWeighted Ratings:")
    print(f"{name_1}: {weighted_1}\n{name_2}: {weighted_2}")
    print(f"\n{name_1}-\n{name_2} divergence: {kl_divergence}")

rating_paths = ["./data/rating_1.txt", "./data/rating_2.txt", "./data/rating_3.txt", "./data/rating_4.txt"]
movies_path = './data/movie_titles.csv'

load_ratings_to_db(rating_paths)
load_movies_to_db(movies_path)

cold_start_recommendations = get_cold_start_recommendations_sql(size=10)
user_recommendations = get_user_recommendations_sql(user_id=4230, size=10)

print(f"\nCold Start:\n{cold_start_recommendations.get('movie_name', " ")}")
print(f"\nRecommendations Based on Likes:\n{user_recommendations.get('movie_name', " ")}")
compare_two_movies(1, 2)