import pandas as pd
import csv

# 1️⃣ Verileri oku
input_path = '/Users/2na/Documents/tt-bootcamp/you_do_1/organized_data/movie_with_confidence_intervals.csv'
movies_df = pd.read_csv(input_path)

# 2️⃣ Movie titles dosyasını oku
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

# 3️⃣ CI_Lower_95'e göre büyükten küçüğe sırala
sorted_movies = movies_df.sort_values(by='CI_Lower_95', ascending=False)

# 4️⃣ İlk 30 filmi seç
top_30_movies = sorted_movies.head(30).copy()

# 5️⃣ Movie Title ekle
top_30_movies['Movie_Title'] = top_30_movies['Movie_ID'].apply(lambda x: movie_titles_dict.get(x, 'Unknown'))

# 6️⃣ Sonucu CSV olarak kaydet
output_path = '/Users/2na/Documents/tt-bootcamp/you_do_1/organized_data/soru1_cozum2.csv'
top_30_movies.to_csv(output_path, index=False)

print(f"Top 30 film başarıyla kaydedildi: {output_path}")
