import polars as pl

df_titles = pl.scan_csv(
    "data/binge/movie_titles.csv",encoding="utf8",ignore_errors=True,has_header=False,  new_columns=["movie_id", "movie_year", "movie_name"],  
    truncate_ragged_lines=True  ).with_columns(pl.col("movie_id").cast(pl.Int64))  

ratings_files = [
    "data/binge/rating_1.txt",
    "data/binge/rating_2.txt",
    "data/binge/rating_3.txt",
    "data/binge/rating_4.txt"
]

df_ratings = pl.concat([
    pl.scan_csv(f, new_columns=["movie_id", "user_id", "date", "rating"]) for f in ratings_files
]).with_columns(pl.col("movie_id").cast(pl.Int64))  
#cold advice
top_movies = (
    df_ratings
    .group_by("movie_id")
    .agg(pl.col("rating").sum().alias("total_rating"))
    .sort("total_rating", descending=True)
)


top_movies_with_titles = (
    top_movies
    .join(df_titles, on="movie_id", how="left")  
    .select(["movie_name", "total_rating"])  
)

print(top_movies_with_titles.collect().head())  





