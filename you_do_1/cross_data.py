import pandas as pd
import numpy as np

# Verileri oku
customer_avg_ratings = pd.read_csv('/Users/2na/Documents/tt-bootcamp/you_do_1/organized_data/customer_avg_ratings.csv')
movie_avg_ratings = pd.read_csv('/Users/2na/Documents/tt-bootcamp/you_do_1/organized_data/movie_avg_ratings_v2.csv')

# Müşteri Avg_Rating'e göre sıralama ve %20'lik dilimlere ayırma
customer_avg_ratings['Quantile'] = pd.qcut(customer_avg_ratings['Avg_Rating'], 5, labels=[1, 2, 3, 4, 5])

# Başlangıç için frekans sütunları oluştur
for quantile in range(1, 6):
    movie_avg_ratings[f'Quantile_{quantile}_Freq'] = 0

# Müşteri-Film izleme verisi olmadığından, varsayım olarak tüm müşteriler tüm filmleri izlemiş gibi hesaplıyoruz.
# Bu senaryoda daha gerçekçi bir yapı için müşteri-film izleme ilişkisi eklenebilir.

# Her film için, her quantile'daki müşteri sayısını sayma
for quantile in range(1, 6):
    # O quantile'daki müşteri ID'lerini al
    quantile_customers = customer_avg_ratings[customer_avg_ratings['Quantile'] == quantile]['Customer_ID']
    
    # Her film için bu müşterilerin kaçının izlediğini say (varsayımsal olarak her müşteri izledi)
    movie_avg_ratings[f'Quantile_{quantile}_Freq'] = len(quantile_customers)

# Yeni CSV dosyasını kaydet
movie_avg_ratings.to_csv('/Users/2na/Documents/tt-bootcamp/you_do_1/organized_data/movie_avg_ratings_with_quantiles.csv', index=False)

print("Frekanslar eklendi ve yeni CSV dosyası oluşturuldu.")
