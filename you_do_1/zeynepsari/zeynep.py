"""
!pip install scipy
!pip install scikit-learn
!pip install duckdb --upgrade
"""

# Import dependencies
from pathlib import Path

import duckdb
import pandas as pd
from scipy import stats
from sklearn.feature_extraction.text import CountVectorizer


def load_ratings(rating_paths):
    if isinstance(rating_paths, str):
        rating_paths = [rating_paths]

    queries = []
    for path in rating_paths:
        full_path = str(Path(path).resolve())

        query = f"""
        SELECT
            CAST(column0 AS INTEGER) AS movie_id,
            CAST(column1 AS INTEGER) AS user_id,
            CAST(column2 AS VARCHAR) AS date,
            CAST(column3 AS INTEGER) AS rating
        FROM read_csv_auto('{full_path}', delim=',', header=False)
        """
        queries.append(query)

    full_query = " UNION ALL ".join(queries)
    return duckdb.query(full_query).to_df()


# Converts file paths to absolute and builds a SQL query for movie data
def load_movies(movies_path):
    if isinstance(movies_path, str):
        movies_path = [movies_path]

    full_paths = [str(Path(path).resolve()) for path in movies_path]

    query = f"""
    SELECT
        TRY_CAST(column0 AS INTEGER) AS movie_id,
        TRY_CAST(column1 AS INTEGER) AS movie_year,
        column2 AS movie_name
    FROM read_csv_auto('{full_paths[0]}', delim=',', header=False, quote='"', escape='"', ignore_errors=True)
    WHERE movie_id IS NOT NULL
        AND movie_year IS NOT NULL 
        AND movie_name IS NOT NULL
    """

    return query


def compute_weighted_ratings(ratings):
    rating_distribution = (
        ratings.groupby("movie_id")["rating"]
        .value.counts(normalize=True)
        .unstack(fill_value=0)
    )
    rating_distribution["weighted_rating"] = (
        rating_distribution * rating_distribution.columns
    ).sum(axis=1)

    return rating_distribution.reset_index()


def merge_data(ratings, movies, rating_distribution):
    query = """
    SELECT
        r.movie_id,
        r.user_id,
        CAST(r.date AS DATE) AS date,
        r.rating,
        m.movie_year,
        rd.weighted_rating,
        EXTRACT(QUARTER FROM r.date) AS quarter
    FROM ratings AS r
    LEFT JOIN movies AS m ON r.movie_id = m.movie_id
    LEFT JOIN (
        SELECT movie_id, weighted_rating 
        FROM rating_distribution
    ) AS rd ON r.movie_id = rd.movie_id
    """

    merged_ratings = duckdb.query(query).df()
    return merged_ratings


def is_normal_distributed(serie):
    result = stats.anderson(serie, "norm")
    return result.statistic < result.critical_values[2]


def get_correlation(serie1, serie2):
    normality = is_normal_distributed(serie1) and is_normal_distributed(serie2)
    test = "pearson" if normality else "spearman"
    return serie1.corr(serie2, method=test)


def get_cold_start_recommendations(movies, rating_distribution, size=10):
    sorted_movies = rating_distribution.sort_values(
        by="weighted_rating", ascending=False
    )
    cold_start_movie_ids = sorted_movies.index[:size]
    return movies[movies["movie_id"].isin(cold_start_movie_ids)].reset_index(drop=True)


def get_liked_movie_names(ratings, movies, user_id):
    user_ratings = ratings[ratings["user_id"] == user_id]
    max_rating = user_ratings["rating"].max()
    liked_movies = user_ratings[user_ratings["rating"] == max_rating][
        "movie_id"
    ].tolist()
    liked_movie_names = movies[movies["movie_id"].isin(liked_movies)][
        "movie_name"
    ].tolist()
    return liked_movie_names, user_ratings["movie_id"].tolist()


def get_bow_df(names):
    if not names:
        return pd.DataFrame()

    vectorizer = CountVectorizer(stop_words="english", token_pattern=r"\b\w {2,} \ b")
    bow = vectorizer.fit_transform(pd.Series(names))

    return pd.DataFrame(bow.toarray(), columns=vectorizer.get_feature_names_out())


def get_top_words(ratings, movies, user_id, size=10):
    liked_movie_names, _ = get_liked_movie_names(ratings, movies, user_id)

    if not liked_movie_names:
        return pd.Series(dtype="object")

    word_frequencies = get_bow_df(liked_movie_names).sum(axis=0)
    word_frequencies.index = word_frequencies.index.str.lower()

    words_to_remove = ["season", "episode", "edition"]
    word_frequencies = word_frequencies[~word_frequencies.index.isin(words_to_remove)]
    word_frequencies = word_frequencies[
        ~word_frequencies.index.str.contains(r"^\d+$", na=False)
    ]

    return word_frequencies.sort_values(ascending=False).head(size)


def get_user_recommendations(ratings, movies, rating_distribution, user_id, size):
    rated_movie_ids = get_liked_movie_names(ratings, movies, user_id)

    unrated_movies = movies[~movies["movie_id"].isin(rated_movie_ids)].copy()

    top_words = get_top_words(ratings, movies, user_id, size).index

    unrated_movies["has_match"] = unrated_movies["movie_name"].apply(
        lambda x: any(word in x.lower() for word in top_words)
    )

    matching_movies = unrated_movies[unrated_movies["has_match"]]

    matching_movies_with_ratings = matching_movies.merge(
        rating_distribution[["weighted_rating"]],
        left_on="movie_id",
        right_index=True,
        how="left",
    )

    return (
        matching_movies_with_ratings.sort_values(by="weighted_rating", ascending=False)
        .head(size)
        .drop("weighted_rating", axis=1)
    )


movies_path = "/Users/zeynepsari/Projects/binge/movie_titles.csv"
rating_paths = [
    "/Users/zeynepsari/Projects/binge/rating_1.txt",
    "/Users/zeynepsari/Projects/binge/rating_2.txt",
    "/Users/zeynepsari/Projects/binge/rating_3.txt",
    "/Users/zeynepsari/Projects/binge/rating_4.txt",
]

movies = pd.read_csv(movies_path, encoding="ISO-8859-1", on_bad_lines="skip")
ratings_list = [
    pd.read_csv(path, encoding="ISO-8859-1", on_bad_lines="skip")
    for path in rating_paths
]


ratings = pd.concat(ratings_list, ignore_index=True)


print(movies.head())
print(ratings.head())


def get_cold_start_recommendations_2(movies, rating_distribution, size=15):
    sorted_movies = rating_distribution.sort_values(
        by="weighted_rating", ascending=False
    )
    cold_start_movie_ids = sorted_movies.index[:size]
    return movies[movies["movie_id"].isin(cold_start_movie_ids)].reset_index(drop=True)


def compute_weighted_ratings_2(ratings):
    rating_distribution = (
        ratings.groupby("movie_id")["rating"]
        .value_counts(normalize=True)
        .unstack(fill_value=0)
    )
    rating_distribution["weighted_rating"] = (
        rating_distribution * rating_distribution.columns
    ).sum(axis=1)
    return rating_distribution.reset_index()


rating_distribution = compute_weighted_ratings(ratings)
cold_start_recommendations = get_cold_start_recommendations(
    movies, rating_distribution, size=15
)
user_recommendations = get_user_recommendations(
    ratings, movies, rating_distribution, 4230, size=15
)


print(cold_start_recommendations, "\n")
print(user_recommendations)


rating_paths = [
    "/Users/zeynepsari/Projects/binge/rating_1.txt",
    "/Users/zeynepsari/Projects/binge/rating_2.txt",
    "/Users/zeynepsari/Projects/binge/rating_3.txt",
    "/Users/zeynepsari/Projects/binge/rating_4.txt",
]
movies_path = "/Users/zeynepsari/Projects/binge/movie_titles.csv"

# !ls /Users/zeynepsari/Projects/binge/
