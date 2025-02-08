import pandas as pd
from collections import defaultdict

# 1️⃣ Verileri oku
customer_avg_ratings = pd.read_csv('/Users/2na/Documents/tt-bootcamp/you_do_1/organized_data/customer_avg_ratings.csv')
movie_avg_ratings = pd.read_csv('/Users/2na/Documents/tt-bootcamp/you_do_1/organized_data/movie_avg_ratings_v2.csv')

# 2️⃣ Müşterileri %20'lik dilimlere ayır ve sözlük oluştur
customer_avg_ratings['Quantile'] = pd.qcut(customer_avg_ratings['Avg_Rating'], 5, labels=[1, 2, 3, 4, 5])
customer_quantile_map = dict(zip(customer_avg_ratings['Customer_ID'], customer_avg_ratings['Quantile']))

# 3️⃣ Movie_ID -> Index eşleşmesini oluştur (hızlı erişim için)
movie_index_map = {movie_id: idx for idx, movie_id in enumerate(movie_avg_ratings['Movie_ID'])}

# 4️⃣ Frekansları tutmak için geçici sözlük
freq_counter = defaultdict(lambda: [0, 0, 0, 0, 0])  # Her movie için 5 quantile frekansı

# 5️⃣ Rating dosyalarını satır bazlı oku
file_path = "/Users/2na/Documents/binge/"
file_names = ["rating_1.txt", "rating_2.txt", "rating_3.txt", "rating_4.txt"]

for file_name in file_names:
    with open(file_path + file_name, 'r') as file:
        for line in file:
            try:
                # Satırı parçala: movie_id, customer_id
                movie_id, customer_id, *_ = line.strip().split(',')
                movie_id = int(movie_id)
                customer_id = int(customer_id)

                # Customer'ın quantile'ını bul
                quantile = customer_quantile_map.get(customer_id)
                if quantile is None:
                    continue  # Customer bulunamazsa atla

                # Frekansları güncelle (sözlük tabanlı)
                freq_counter[movie_id][int(quantile) - 1] += 1

            except:
                continue  # Hatalı satır varsa atla

# 6️⃣ Toplu olarak movie_avg_ratings DataFrame'ine frekansları uygula
for movie_id, freqs in freq_counter.items():
    movie_idx = movie_index_map.get(movie_id)
    if movie_idx is not None:
        for i, freq in enumerate(freqs):
            movie_avg_ratings.at[movie_idx, f'Quantile_{i+1}_Freq'] = freq

# 7️⃣ Sonucu kaydet
output_path = '/Users/2na/Documents/tt-bootcamp/you_do_1/organized_data/movie_avg_ratings_with_quantiles.csv'
movie_avg_ratings.to_csv(output_path, index=False)

print("Frekanslar başarıyla eklendi ve yeni CSV dosyası oluşturuldu.")
