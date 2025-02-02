import pandas as pd
import csv

# 1️⃣ Verileri oku
movie_avg_ratings = pd.read_csv('/Users/2na/Documents/tt-bootcamp/you_do_1/organized_data/movie_avg_ratings_with_quantiles.csv')

# 2️⃣ Movie titles dosyasını satır bazlı oku (encoding ve virgül sorununu çöz)
movie_titles_path = '/Users/2na/Documents/binge/movie_titles.csv'

# Movie_ID ve Movie_Title eşleşmelerini bir sözlükte tut
movie_titles_dict = {}

with open(movie_titles_path, 'r', encoding='ISO-8859-1') as file:
    reader = csv.reader(file)
    for row in reader:
        if len(row) >= 3:
            movie_id = int(row[0])
            movie_title = row[2]  # 3. kolon (index 2)
            movie_titles_dict[movie_id] = movie_title

# 3️⃣ Watch_Count > 1000 olanları filtrele
filtered_movies = movie_avg_ratings[movie_avg_ratings['Watch_Count'] > 1000].copy()

# 4️⃣ Skor hesaplama: (Quantile_1_Freq / Watch_Count) * Avg_Rating
filtered_movies['Score'] = (filtered_movies['Quantile_1_Freq'] / filtered_movies['Watch_Count']) * filtered_movies['Avg_Rating']

# 5️⃣ En yüksek 30 filmi bul (azalan sırada)
top_30_movies = filtered_movies.sort_values(by='Score', ascending=False).head(30)

# 6️⃣ Film adlarını ekle
top_30_movies['Movie_Title'] = top_30_movies['Movie_ID'].apply(lambda x: movie_titles_dict.get(x, 'Unknown'))

# 7️⃣ CSV olarak kaydet
output_path = '/Users/2na/Documents/tt-bootcamp/you_do_1/organized_data/soru1.csv'
top_30_movies.to_csv(output_path, index=False)

print(f"Top 30 film başarıyla kaydedildi: {output_path}")
