import os
import csv
import re
from datetime import datetime

# Veri yolu tanımı
BASE_PATH = "/Users/2na/Documents/binge"
FILE_NAMES = ["rating_1.txt", "rating_2.txt", "rating_3.txt", "rating_4.txt"]
OUTPUT_DIR = "/Users/2na/Documents/tt-bootcamp/you_do_1/organized_data"  # Kayıtların tutulacağı klasör
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "movie_avg_ratings_fixed.txt")
METADATA_FILE = os.path.join(OUTPUT_DIR, "movie_metadata.txt")  # Metadata dosyası

# Dosya yollarının oluşturulmasıß
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

# Fixed-length formatta veriyi kaydetme
def save_fixed_length(filename: str, movie_id: int, avg_rating: float, watch_count: int, min_date: str, max_date: str, date_diff: int):
    """Veriyi fixed-length formatında dosyaya ekler."""
    assert 0 <= avg_rating <= 5, f"Hata: Ortalama rating değeri geçersiz! -> {avg_rating}"
    assert watch_count > 0, f"Hata: İzlenme sayısı sıfır veya negatif olamaz! -> {watch_count}"
    assert is_valid_date(min_date), f"Hata: Min tarih formatı hatalı! -> {min_date}"
    assert is_valid_date(max_date), f"Hata: Max tarih formatı hatalı! -> {max_date}"
    assert date_diff >= 0, f"Hata: Tarih farkı negatif olamaz! -> {date_diff}"

    with open(filename, "a") as f:  # Append modunda aç (Her seferinde yazabilmek için)
        line = f"{movie_id:<6} {avg_rating:.2f} {watch_count:>5} {min_date:<10} {max_date:<10} {date_diff:>5}\n"
        f.write(line)

# Metadata dosyasını oluşturma
def save_metadata(metadata_file: str):
    """Metadata dosyasını oluşturur ve veri setinin formatını kaydeder."""
    metadata_content = """# Metadata Dosyası
# Bu dosya, fixed-length formatındaki verinin sütun bilgilerini içerir.

COLUMN_NAME    TYPE       LENGTH
Movie_ID      int        6
Avg_Rating    float      4
Watch_Count   int        5
Min_Date      str       10
Max_Date      str       10
Date_Diff     int        5
"""

    with open(metadata_file, "w") as f:
        f.write(metadata_content)

# Satır bazlı okuma ve işlem yapma
def process_movie_ratings(file_paths: list, output_file: str, metadata_file: str):
    """Veriyi film bazlı okuyarak ortalama rating, izlenme sayısı ve min/max tarih hesaplar ve kaydeder."""
    
    current_movie_id = None  # Şu an işlenen film ID
    total_rating = 0  # Şu anki filmin toplam ratingi
    rating_count = 0  # Şu anki filmin rating sayısı
    min_date = None  # Minimum tarih
    max_date = None  # Maksimum tarih

    # Çıkış dosyasını temizle (varsa sil ve yeniden başlat)
    open(output_file, "w").close()
    save_metadata(metadata_file)  # Metadata dosyasını kaydet

    for file_path in file_paths:
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)

            for row in reader:
                assert len(row) == 4, f"Hata: Beklenen 4 sütun, ancak {len(row)} sütun bulundu -> {row}"

                movie_id = int(row[0])
                watch_date = row[2]
                rating = float(row[3])

                assert 0 <= rating <= 5, f"Hata: Rating 0-5 arasında olmalı! -> {rating}"

                if current_movie_id is None:
                    current_movie_id = movie_id
                    min_date = watch_date
                    max_date = watch_date

                if movie_id != current_movie_id:
                    if rating_count > 0:
                        avg_rating = total_rating / rating_count
                        date_diff = calculate_date_difference(min_date, max_date)
                        save_fixed_length(output_file, current_movie_id, avg_rating, rating_count, min_date, max_date, date_diff)

                    current_movie_id = movie_id
                    total_rating = 0
                    rating_count = 0
                    min_date = watch_date
                    max_date = watch_date

                total_rating += rating
                rating_count += 1
                min_date = min(min_date, watch_date)
                max_date = max(max_date, watch_date)

    if rating_count > 0:
        avg_rating = total_rating / rating_count
        date_diff = calculate_date_difference(min_date, max_date)
        save_fixed_length(output_file, current_movie_id, avg_rating, rating_count, min_date, max_date, date_diff)

# Ana çalışma fonksiyonu
def main():
    file_paths = get_file_paths(BASE_PATH, FILE_NAMES)
    ensure_directory_exists(OUTPUT_DIR)
    process_movie_ratings(file_paths, OUTPUT_FILE, METADATA_FILE)
    print(f"Ortalama rating hesaplamaları tamamlandı. Çıkış dosyası: {OUTPUT_FILE}")
    print(f"Metadata dosyası oluşturuldu: {METADATA_FILE}")

if __name__ == "__main__":
    main()
