import os
import csv
import re
from datetime import datetime

# Veri yolu tanımı
BASE_PATH = "/Users/2na/Documents/binge"
FILE_NAMES = ["rating_1.txt", "rating_2.txt", "rating_3.txt", "rating_4.txt"]
OUTPUT_DIR = "organized_data"
FINAL_FILE = os.path.join(OUTPUT_DIR, "customer_avg_ratings.csv")

# Klasör kontrolü ve oluşturma
def ensure_directory_exists(directory: str):
    if not os.path.exists(directory):
        os.makedirs(directory)

# Tarih doğrulama fonksiyonu
def is_valid_date(date_str: str) -> bool:
    return bool(re.match(r"^\d{4}-\d{2}-\d{2}$", date_str))

# Tarih farkı hesaplama
def calculate_date_difference(min_date: str, max_date: str) -> int:
    min_date_dt = datetime.strptime(min_date, "%Y-%m-%d")
    max_date_dt = datetime.strptime(max_date, "%Y-%m-%d")
    return (max_date_dt - min_date_dt).days

# Müşteri bazlı veriyi CSV formatında yazma
def process_customer_data(file_paths: list, final_file: str):
    """Müşteri bazında ortalama rating ve tarih bilgilerini hesaplayıp CSV'ye kaydeder."""
    customer_summary = {}
    
    for file_path in file_paths:
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            
            for row in reader:
                assert len(row) == 4, f"Hata: Beklenen 4 sütun, ancak {len(row)} sütun bulundu -> {row}"
                
                movie_id = int(row[0])
                customer_id = row[1]
                watch_date = row[2]
                rating = float(row[3])
                
                assert 0 <= rating <= 5, f"Hata: Rating 0-5 arasında olmalı! -> {rating}"
                
                # Müşteri yeni mi?
                if customer_id not in customer_summary:
                    customer_summary[customer_id] = {
                        "total_rating": 0,
                        "count": 0,
                        "min_date": watch_date,
                        "max_date": watch_date
                    }
                
                # Bilgileri güncelle
                customer_summary[customer_id]["total_rating"] += rating
                customer_summary[customer_id]["count"] += 1
                customer_summary[customer_id]["min_date"] = min(customer_summary[customer_id]["min_date"], watch_date)
                customer_summary[customer_id]["max_date"] = max(customer_summary[customer_id]["max_date"], watch_date)
    
    # CSV formatında yazma
    with open(final_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Customer_ID", "Avg_Rating", "Watch_Count", "Min_Date", "Max_Date", "Date_Diff"])
        
        for customer_id, data in customer_summary.items():
            avg_rating = data["total_rating"] / data["count"]
            date_diff = calculate_date_difference(data["min_date"], data["max_date"])
            writer.writerow([customer_id, avg_rating, data["count"], data["min_date"], data["max_date"], date_diff])

# Ana çalışma fonksiyonu
def main():
    file_paths = [os.path.join(BASE_PATH, fn) for fn in FILE_NAMES]
    ensure_directory_exists(OUTPUT_DIR)
    
    # Müşteri bazlı hesaplamaları CSV'ye yaz
    process_customer_data(file_paths, FINAL_FILE)
    
    print(f"Müşteri bazlı hesaplamalar tamamlandı. Çıkış dosyası: {FINAL_FILE}")

if __name__ == "__main__":
    main()
