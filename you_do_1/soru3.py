import pandas as pd
import random
import csv

# 1️⃣ Verileri oku
movie_avg_ratings = pd.read_csv('/Users/2na/Documents/tt-bootcamp/you_do_1/organized_data/movie_avg_ratings_with_quantiles.csv')

# 2️⃣ Movie titles dosyasını satır bazlı oku
movie_titles_path = '/Users/2na/Documents/binge/movie_titles.csv'
movie_titles_dict = {}

with open(movie_titles_path, 'r', encoding='ISO-8859-1') as file:
    reader = csv.reader(file)
    for row in reader:
        if len(row) >= 3:
            movie_id = int(row[0])
            movie_title = row[2]  # 3. kolon (index 2)
            movie_titles_dict[movie_id] = movie_title

# 3️⃣ Ağırlıklı skor hesaplama fonksiyonu
def calculate_weighted_score(movie):
    watch_count = movie['Watch_Count']
    avg_rating = movie['Avg_Rating']
    
    # Quantile ağırlıkları (düşük quantile'lara daha fazla önem veriyoruz)
    quantile_weights = {1: 1.5, 2: 1.25, 3: 1.0, 4: 0.75, 5: 0.5}
    
    # Ağırlıklı frekans hesaplama
    weighted_freq = 0
    for q in range(1, 6):
        freq = movie[f'Quantile_{q}_Freq']
        normalized_freq = freq / watch_count if watch_count > 0 else 0
        weighted_freq += quantile_weights[q] * normalized_freq
    
    # Final skor: ağırlıklı frekans * ortalama puan
    score = weighted_freq * avg_rating
    return score

# 4️⃣ İki filmi karşılaştırma fonksiyonu
def compare_movies(movie_id_1, movie_id_2):
    movie_1 = movie_avg_ratings[movie_avg_ratings['Movie_ID'] == movie_id_1].iloc[0]
    movie_2 = movie_avg_ratings[movie_avg_ratings['Movie_ID'] == movie_id_2].iloc[0]
    
    score_1 = calculate_weighted_score(movie_1)
    score_2 = calculate_weighted_score(movie_2)
    
    # Film isimlerini al
    title_1 = movie_titles_dict.get(movie_id_1, 'Unknown')
    title_2 = movie_titles_dict.get(movie_id_2, 'Unknown')
    
    # Sonuçları yazdır
    print(f"\nKarşılaştırma Sonucu:")
    print(f"Film 1: {title_1} (ID: {movie_id_1})")
    print(f"  - Avg Rating: {movie_1['Avg_Rating']}, Watch Count: {movie_1['Watch_Count']}, Skor: {score_1:.4f}")
    
    print(f"Film 2: {title_2} (ID: {movie_id_2})")
    print(f"  - Avg Rating: {movie_2['Avg_Rating']}, Watch Count: {movie_2['Watch_Count']}, Skor: {score_2:.4f}")
    
    # Hangi film kaldırılmalı?
    if score_1 > score_2:
        print(f"\nSonuç: {title_2} (ID: {movie_id_2}) kaldırılmalı.")
        return movie_id_2
    else:
        print(f"\nSonuç: {title_1} (ID: {movie_id_1}) kaldırılmalı.")
        return movie_id_1

# 5️⃣ Rastgele iki film seç ve karşılaştır
random.seed(42)
movie_ids = movie_avg_ratings['Movie_ID'].unique()
random_movies = random.sample(list(movie_ids), 2)

# Karşılaştırma yap ve sonucu yazdır
result = compare_movies(random_movies[0], random_movies[1])
