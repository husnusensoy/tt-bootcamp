import os
import csv
import re
from datetime import datetime
from statistics import stdev  # Standart sapma hesaplamak için

# Veri yolu tanımı
BASE_PATH = "/Users/2na/Documents/binge"
FILE_NAMES = ["rating_1.txt", "rating_2.txt", "rating_3.txt", "rating_4.txt"]
OUTPUT_DIR = "/Users/2na/Documents/tt-bootcamp/you_do_1/organized_data"  # Kayıtların tutulacağı klasör
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "movie_avg_ratings.csv")

# Dosya yollarının oluşturulması
def get_file_paths(base_path: str, file_names: list) -> list:
    """Verilen dosya adlarını tam dosya yollarına dönüştürür."""
    full_paths = [os.path.join(base_path, filename) for filename in file_names]
    
    # Dosyaların var olup olmadığını kontrol et
    for path in full_paths:
        assert os.path.exists(path), f"Hata: Dosya bulunamadı -> {path}"
        assert os.path.isfile(path), f"Hata: {path} bir dosya değil!"
        assert os.access(path, os.R_OK), f"Hata: {path} okunamıyor (izin hatası)"

    return full_paths

# Klasör kontrolü ve oluşturma
def ensure_directory_exists(directory: str):
    """Eğer klasör yoksa oluştur."""
    if not os.path.exists(directory):
        os.makedirs(directory)

# Tarih doğrulama fonksiyonu
def is_valid_date(date_str: str) -> bool:
    """Tarihin YYYY-MM-DD formatında olup olmadığını kontrol eder."""
    return bool(re.match(r"^\d{4}-\d{2}-\d{2}$", date_str))

# Tarih farkı hesaplama fonksiyonu
def calculate_date_difference(min_date: str, max_date: str) -> int:
    """Max ve Min tarih arasındaki farkı gün olarak hesaplar."""
    min_date_dt = datetime.strptime(min_date, "%Y-%m-%d")
    max_date_dt = datetime.strptime(max_date, "%Y-%m-%d")
    return (max_date_dt - min_date_dt).days

# CSV formatında veriyi kaydetme
def save_to_csv(filename: str, data: list):
    """Veriyi CSV formatında kaydeder."""
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        # Std_Dev (Standart Sapma) kolonu eklendi
        writer.writerow(["Movie_ID", "Avg_Rating", "Watch_Count", "Std_Dev", "Min_Date", "Max_Date", "Date_Diff"])
        writer.writerows(data)

# Satır bazlı okuma ve işlem yapma
def process_movie_ratings(file_paths: list, output_file: str):
    """Veriyi film bazlı okuyarak ortalama rating, izlenme sayısı,
    min/max tarih ve standart sapma hesaplar ve kaydeder."""
    current_movie_id = None  # Şu an işlenen film ID
    ratings_list = []        # Şu anki filmin rating listesini tutmak için
    min_date = None          # Minimum tarih
    max_date = None          # Maksimum tarih
    result_data = []

    for file_path in file_paths:
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            
            for row in reader:
                assert len(row) == 4, f"Hata: Beklenen 4 sütun, ancak {len(row)} sütun bulundu -> {row}"
                
                movie_id = int(row[0])
                watch_date = row[2]
                rating = float(row[3])
                
                assert 0 <= rating <= 5, f"Hata: Rating 0-5 arasında olmalı! -> {rating}"
                
                # Yeni filme geçiş kontrolü
                if current_movie_id is None:
                    # İlk satırda current_movie_id atayalım
                    current_movie_id = movie_id
                    min_date = watch_date
                    max_date = watch_date

                # Farklı bir movie_id'ye geçtiysek, önce önceki filmin verilerini kaydet
                if movie_id != current_movie_id:
                    if len(ratings_list) > 0:
                        # Ortalama
                        avg_rating = sum(ratings_list) / len(ratings_list)
                        # Standart sapma (sample stdev); eğer izlenme sayısı 1 ise 0 kabul ediyoruz
                        std_dev = stdev(ratings_list) if len(ratings_list) > 1 else 0.0
                        # Tarih farkı
                        date_diff = calculate_date_difference(min_date, max_date)
                        
                        result_data.append([
                            current_movie_id,
                            avg_rating,
                            len(ratings_list),
                            std_dev,
                            min_date,
                            max_date,
                            date_diff
                        ])
                    
                    # Yeni film için değişkenleri sıfırla
                    current_movie_id = movie_id
                    ratings_list = [rating]
                    min_date = watch_date
                    max_date = watch_date
                else:
                    # Hâlâ aynı filmdeysek verileri biriktir
                    ratings_list.append(rating)
                    min_date = min(min_date, watch_date)
                    max_date = max(max_date, watch_date)

    # Döngü bittiğinde elde kalan son filmi kaydet
    if len(ratings_list) > 0:
        avg_rating = sum(ratings_list) / len(ratings_list)
        std_dev = stdev(ratings_list) if len(ratings_list) > 1 else 0.0
        date_diff = calculate_date_difference(min_date, max_date)
        
        result_data.append([
            current_movie_id,
            avg_rating,
            len(ratings_list),
            std_dev,
            min_date,
            max_date,
            date_diff
        ])
    
    # CSV'ye kaydet
    save_to_csv(output_file, result_data)

# Ana çalışma fonksiyonu
def main():
    file_paths = get_file_paths(BASE_PATH, FILE_NAMES)
    ensure_directory_exists(OUTPUT_DIR)
    process_movie_ratings(file_paths, OUTPUT_FILE)
    print(f"Ortalama rating ve standart sapma hesaplamaları tamamlandı. Çıkış dosyası: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
