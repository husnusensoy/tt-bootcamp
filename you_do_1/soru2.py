import pandas as pd
import random
import csv

# 1️⃣ Verileri oku
movie_avg_ratings = pd.read_csv('/Users/2na/Documents/tt-bootcamp/you_do_1/organized_data/movie_avg_ratings_with_quantiles.csv')
customer_avg_ratings = pd.read_csv('/Users/2na/Documents/tt-bootcamp/you_do_1/organized_data/customer_avg_ratings.csv')

# 2️⃣ Müşterileri %20'lik dilimlere ayır (Quantile)
customer_avg_ratings['Quantile'] = pd.qcut(customer_avg_ratings['Avg_Rating'], 5, labels=[1, 2, 3, 4, 5])

# 3️⃣ En az 10 film izlemiş kullanıcıları filtrele
eligible_customers = customer_avg_ratings[customer_avg_ratings['Watch_Count'] >= 10]['Customer_ID'].unique()

# 4️⃣ Rastgele bir kullanıcı seç (seed ile sabitlenmiş)
random.seed(42)
random_customer = random.choice(eligible_customers)

# 5️⃣ Movie titles dosyasını satır bazlı oku
movie_titles_path = '/Users/2na/Documents/binge/movie_titles.csv'
movie_titles_dict = {}

with open(movie_titles_path, 'r', encoding='ISO-8859-1') as file:
    reader = csv.reader(file)
    for row in reader:
        if len(row) >= 3:
            movie_id = int(row[0])
            movie_title = row[2]  # 3. kolon (index 2)
            movie_titles_dict[movie_id] = movie_title

# 6️⃣ Quantile bazlı en yüksek skorlu filmleri önerme fonksiyonu
def recommend_movies_for_customer(customer_id):
    # Kullanıcının quantile'ını bul
    quantile = customer_avg_ratings.loc[customer_avg_ratings['Customer_ID'] == customer_id, 'Quantile']
    
    if quantile.empty:
        return [], None  # Kullanıcı bulunamazsa boş liste döner
    
    quantile = int(quantile.values[0])
    
    # O quantile'daki en yüksek skora sahip 30 filmi öner
    movie_avg_ratings['Score'] = (movie_avg_ratings[f'Quantile_{quantile}_Freq'] / movie_avg_ratings['Watch_Count']) * movie_avg_ratings['Avg_Rating']
    recommended_movies = movie_avg_ratings.sort_values(by='Score', ascending=False).head(30)
    
    # Film adlarını ekle
    recommended_movies['Movie_Title'] = recommended_movies['Movie_ID'].apply(lambda x: movie_titles_dict.get(x, 'Unknown'))
    
    return recommended_movies[['Movie_ID', 'Movie_Title', 'Avg_Rating', 'Score']], quantile

# 7️⃣ Önerileri al
recommendations, user_quantile = recommend_movies_for_customer(random_customer)

# 8️⃣ Önerileri CSV olarak kaydet
output_path = '/Users/2na/Documents/tt-bootcamp/you_do_1/organized_data/soru2.csv'
recommendations.to_csv(output_path, index=False)

# 9️⃣ Bilgileri ekrana yazdır
print(f"Öneriler başarıyla kaydedildi: {output_path}")
print(f"Öneriler yapılan kullanıcı ID: {random_customer}")
print(f"Kullanıcının Quantile'ı: {user_quantile}")
