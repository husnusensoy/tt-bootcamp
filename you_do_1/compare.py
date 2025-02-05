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

df_titles=df_titles.collect()
df_ratings=df_ratings.collect()


# İki filmi karşılaştıran fonksiyon
def compare_movies(movie_name1, movie_name2):
    # Filmleri bul
    movie1 = df_titles.filter(pl.col("movie_name") == movie_name1)
    movie2 = df_titles.filter(pl.col("movie_name") == movie_name2)

    if movie1.is_empty() or movie2.is_empty():
        return "Filmlerden biri sistemde bulunamadı."

    movie1_id = movie1["movie_id"][0]
    movie2_id = movie2["movie_id"][0]

    # Filmlerin puanlarını al
    ratings1 = df_ratings.filter(pl.col("movie_id") == movie1_id)["rating"]
    ratings2 = df_ratings.filter(pl.col("movie_id") == movie2_id)["rating"]

    # Ortalama ve toplam puanı hesapla
    avg_rating1 = ratings1.mean()
    avg_rating2 = ratings2.mean()
    total_rating1 = ratings1.sum()
    total_rating2 = ratings2.sum()
    count_rating1 = ratings1.len()
    count_rating2 = ratings2.len()

    # Sonuçları göster
    print(f"🎬 {movie_name1} vs {movie_name2}")
    print(f"📊 Ortalama Puan: {avg_rating1:.2f} vs {avg_rating2:.2f}")
    print(f"🔢 Toplam Puan: {total_rating1} vs {total_rating2}")
    print(f"👥 Oylayan Kişi Sayısı: {count_rating1} vs {count_rating2}")

# Örnek Karşılaştırma
compare_movies("The Green Mile", "Forrest Gump")
