import pandas as pd
import csv

# 1🌟 Verileri oku
movie_avg_ratings = pd.read_csv('/Users/2na/Documents/tt-bootcamp/you_do_1/organized_data/movie_avg_ratings_with_quantiles.csv')

# 2🌟 Movie titles dosyasını oku
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

# 3🌟 Watch_Count > 1000 olanları filtrele
filtered_movies = movie_avg_ratings[movie_avg_ratings['Watch_Count'] > 1000].copy()

# 4🌟 Quantile ağırlıkları
quantile_weights = {1: 0.5, 2: 0.75, 3: 1.0, 4: 1.25, 5: 1.5}

# 5🌟 Skor hesaplama: Her quantile için ayrı ağırlıklandırılmış puan
score = sum(
    (filtered_movies[f'Quantile_{q}_Freq'] / filtered_movies['Watch_Count']) * filtered_movies['Avg_Rating'] * weight
    for q, weight in quantile_weights.items()
)
filtered_movies['Score'] = score

# 6🌟 En yüksek 30 filmi bul (azalan sırada)
top_30_movies = filtered_movies.sort_values(by='Score', ascending=False).head(30)

# 7🌟 Film adlarını ekle
top_30_movies['Movie_Title'] = top_30_movies['Movie_ID'].apply(lambda x: movie_titles_dict.get(x, 'Unknown'))

# 8🌟 CSV olarak kaydet
output_path = '/Users/2na/Documents/tt-bootcamp/you_do_1/organized_data/soru1.csv'
top_30_movies.to_csv(output_path, index=False)

print(f"Top 30 film başarıyla kaydedildi: {output_path}")