import os
import tarfile
import urllib.request
import pandas as pd
import glob
import csv

# Veri setini indir ve çıkar
url = "https://storage.googleapis.com/sadedegel/dataset/binge.tar.gz"
output_file = "binge.tar.gz"

urllib.request.urlretrieve(url, output_file)

with tarfile.open(output_file) as tar:
   tar.extractall()

# rating dosyalarını birleştir
rating_files = glob.glob("rating_*.txt")
print(f"Bulunan dosyalar: {rating_files}")

if not rating_files:
    raise FileNotFoundError("Puan dosyaları bulunamadı. Lütfen veri setini kontrol edin.")

ratings_list = [pd.read_csv(file, sep=",", names=["movie_id", "user_id", "date", "rating"]) for file in rating_files]
ratings = pd.concat(ratings_list, ignore_index=True)

movie_titles = pd.read_csv("movie_titles_cleaned.csv", names=["movie_id", "release_year", "movie_title"], quotechar='"', sep=',', encoding='ISO-8859-1')

# Örnek veri göster
print("\nPuan Verileri:")
print(ratings.head())

print("\nFilm Başlıkları:")
print(movie_titles.head())

# Veri tiplerini kontrol et
print("\nVeri tipleri:")
print(ratings.dtypes)

print("\n===== 1. Soru: Yeni Kullanıcılar İçin Film Önerileri =====")

# Toplam benzersiz film ve kullanıcı sayısını hesapla
total_movies = ratings["movie_id"].nunique()
total_users = ratings["user_id"].nunique()

print(f"Toplam film sayısı: {total_movies}")
print(f"Toplam kullanıcı sayısı: {total_users}")

# Her film için ortalama rating ve oylama sayısını hesapla
rating_summary = ratings.groupby("movie_id").agg(
    average_rating=("rating", "mean"),
    rating_count=("rating", "count")
).reset_index()

# Sırala
recommended_movies = rating_summary.sort_values(by=["average_rating", "rating_count"], ascending=[False, False])

# Film başlıklarını birleştir
top_movies = recommended_movies.merge(movie_titles, on="movie_id", how="inner")

# İlk 10 öneriyi göster
print("\nYeni kullanıcılar için önerilen ilk 10 film:")
print(top_movies[["movie_id", "movie_title", "release_year", "average_rating", "rating_count"]].head(10))

print("\n===== 2. Soru: Belirli Bir Kullanıcıya Film Önerisi =====")

# Kullanıcıdan bir ID al
user_id = int(input("Lütfen kullanıcı ID'sini girin: ")) 
user_movies = ratings[ratings["user_id"] == user_id]["movie_id"].tolist()

if not user_movies:
    print("Bu kullanıcı için herhangi bir izlenmiş film bulunamadı.")
    exit()

print(f"\nKullanıcının izlediği filmler: {len(user_movies)} adet")

# Kullanıcının izlediği filmlerin yayın yıllarını al
watched_movie_info = movie_titles[movie_titles["movie_id"].isin(user_movies)]
common_years = watched_movie_info["release_year"].value_counts().index[:2].tolist()

# Benzer yıllardaki popüler filmleri bul
similar_movies = movie_titles[movie_titles["release_year"].isin(common_years)]
popular_movies = ratings[ratings["movie_id"].isin(similar_movies["movie_id"])].groupby("movie_id").agg(
    average_rating=("rating", "mean"),
    rating_count=("rating", "count")
).reset_index()

# Filmleri sırala ve kullanıcının izlediklerini çıkar
recommended_movies = popular_movies.sort_values(by=["average_rating", "rating_count"], ascending=[False, False])
recommended_movies = recommended_movies.merge(movie_titles, on="movie_id", how="inner")
recommended_movies = recommended_movies[~recommended_movies["movie_id"].isin(user_movies)]

# İlk 10 öneriyi göster
print("\nKullanıcıya önerilen filmler:")
print(recommended_movies[["movie_id", "movie_title", "release_year", "average_rating", "rating_count"]].head(10))

print("\n===== 3. Soru: İki Film Arasındaki Benzerliği Kıyaslama =====")

# İki film belirle
film1_id = int(input("Lütfen ilk film ID'sini girin: "))   
film2_id = int(input("Lütfen ikinci film ID'sini girin: "))  

film1 = movie_titles[movie_titles["movie_id"] == film1_id].iloc[0]
film2 = movie_titles[movie_titles["movie_id"] == film2_id].iloc[0]

print(f"\nFilm 1: {film1['movie_title']} ({film1['release_year']})")
print(f"Film 2: {film2['movie_title']} ({film2['release_year']})")

def calculate_similarity(title1, title2):
    common_chars = sum(1 for c1, c2 in zip(title1, title2) if c1 == c2)  # Ortak karakter sayısı
    max_length = max(len(title1), len(title2))
    return (common_chars / max_length) * 100  # Benzerlik yüzdesi

title_similarity = calculate_similarity(film1["movie_title"], film2["movie_title"])
print(f"\nFilm adlarının benzerlik skoru: {title_similarity:.2f}%")

# Kullanıcı puanlarını karşılaştır
degerlendirme_film1 = ratings[ratings["movie_id"] == film1_id]["rating"].agg(["mean", "count"]).rename({"mean": "ortalama_puan", "count": "oy_sayisi"})
degerlendirme_film2 = ratings[ratings["movie_id"] == film2_id]["rating"].agg(["mean", "count"]).rename({"mean": "ortalama_puan", "count": "oy_sayisi"})

print(f"\nFilm 1 Ortalama Puan: {degerlendirme_film1['ortalama_puan']} - Oylama Sayısı: {degerlendirme_film1['oy_sayisi']}")
print(f"Film 2 Ortalama Puan: {degerlendirme_film2['ortalama_puan']} - Oylama Sayısı: {degerlendirme_film2['oy_sayisi']}")

# Seri filmlerin kontrolü için anahtar kelimeler
seri_anahtar_kelimeler = ["Lord of the Rings", "Harry Potter", "Star Wars", "The Hobbit", "Marvel", "Avengers"]

def seri_kontrolu(film_basligi):
    for kelime in seri_anahtar_kelimeler:
        if kelime.lower() in film_basligi.lower():
            return True
    return False

# Seri film olup olmadığını kontrol et
if seri_kontrolu(film1["movie_title"]) or seri_kontrolu(film2["movie_title"]):
    print("\nBu filmler bir serinin parçası, kaldırılması önerilmez.")
else:
    # Benzerlik kriterlerini kontrol et
    if title_similarity > 80 and abs(film1["release_year"] - film2["release_year"]) <= 1:
        print("\nBu filmler benzer olabilir. Detaylı analiz yapılıyor...")
        
        # Popülerlik kontrolü
        if degerlendirme_film1["oy_sayisi"] > degerlendirme_film2["oy_sayisi"]:
            print(f"\nÖneri: {film2['movie_title']} (ID: {film2_id}) sistemden kaldırılabilir. Daha az popüler.")
        elif degerlendirme_film1["oy_sayisi"] < degerlendirme_film2["oy_sayisi"]:
            print(f"\nÖneri: {film1['movie_title']} (ID: {film1_id}) sistemden kaldırılabilir. Daha az popüler.")
        else:
            print("\nHer iki film de benzer popülerlikte. Hiçbirini kaldırmamanız önerilir.")
    else:
        print("\nBu filmler arasında yeterli benzerlik bulunamadı, her ikisini sistemde tutabilirsiniz.")
