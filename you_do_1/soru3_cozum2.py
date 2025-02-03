import pandas as pd
import random
import csv

# 1️⃣ Verileri oku
movie_avg_ratings = pd.read_csv('/Users/2na/Documents/tt-bootcamp/you_do_1/organized_data/movie_with_confidence_intervals.csv')

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

# 3️⃣ İki filmi CI_Lower_95'e göre karşılaştırma fonksiyonu
def compare_movies_by_ci(movie_id_1, movie_id_2):
    # İki filmi dataframe'den çek
    movie_1 = movie_avg_ratings[movie_avg_ratings['Movie_ID'] == movie_id_1].iloc[0]
    movie_2 = movie_avg_ratings[movie_avg_ratings['Movie_ID'] == movie_id_2].iloc[0]
    
    # CI_Lower_95 değerlerini al
    ci_lower_1 = movie_1['CI_Lower_95']
    ci_lower_2 = movie_2['CI_Lower_95']
    
    # Film isimlerini al
    title_1 = movie_titles_dict.get(movie_id_1, 'Unknown')
    title_2 = movie_titles_dict.get(movie_id_2, 'Unknown')
    
    # Sonuçları yazdır
    print(f"\n🎬 Karşılaştırma Sonucu:")
    print(f"Film 1: {title_1} (ID: {movie_id_1})")
    print(f"  - Avg Rating: {movie_1['Avg_Rating']}, CI_Lower_95: {ci_lower_1:.4f}")
    
    print(f"Film 2: {title_2} (ID: {movie_id_2})")
    print(f"  - Avg Rating: {movie_2['Avg_Rating']}, CI_Lower_95: {ci_lower_2:.4f}")
    
    # CI_Lower_95'i düşük olan filmi kaldır
    if ci_lower_1 < ci_lower_2:
        print(f"\n🚫 Sonuç: {title_1} (ID: {movie_id_1}) kaldırılmalı (daha düşük CI_Lower_95).")
        return movie_id_1
    else:
        print(f"\n🚫 Sonuç: {title_2} (ID: {movie_id_2}) kaldırılmalı (daha düşük CI_Lower_95).")
        return movie_id_2

# 4️⃣ Rastgele iki film seç ve karşılaştır
random.seed(42)
movie_ids = movie_avg_ratings['Movie_ID'].unique()
random_movies = random.sample(list(movie_ids), 2)

# Karşılaştırma yap ve sonucu yazdır
result = compare_movies_by_ci(random_movies[0], random_movies[1])
