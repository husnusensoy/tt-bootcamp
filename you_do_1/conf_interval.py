import os
import csv
import math

INPUT_DIR = "you_do_1/organized_data"
INPUT_FILE = os.path.join(INPUT_DIR, "movie_avg_ratings_with_quantiles.csv")
OUTPUT_FILE = os.path.join(INPUT_DIR, "movie_with_confidence_intervals.csv")

# %95 güven aralığı için Z değeri
Z_VALUE = 1.96

def main():
    result_data = []

    # Kaynak CSV'yi oku
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames
        
        # Yeni CSV'de ek sütunlar ekleyeceğiz
        # (Varsayılan kolonlara "CI_Lower" ve "CI_Upper" ekliyoruz)
        extended_headers = headers + ["CI_Lower_95", "CI_Upper_95"]
        
        for row in reader:
            # İlgili sütunları çek
            # Aşağıda "Std_Dev" adlı bir sütun olduğu varsayılıyor.
            # Elinizde "Std_Dev" yerine farklı bir sütun adı varsa lütfen düzenleyin.
            movie_id = row["Movie_ID"]
            avg_rating = float(row["Avg_Rating"])
            watch_count = int(row["Watch_Count"])
            
            # Eğer CSV'de standart sapma yoksa kodu buna göre düzenlemelisiniz
            # Örneğin "Std_Dev" sütunu olduğunu varsayıyoruz.
            std_dev = float(row["Std_Dev"]) if "Std_Dev" in row and row["Std_Dev"] else 0.0
            
            # Watch_Count 1 veya 0 ise standart hata 0 olacağından
            # güven aralığının alt/üst sınırı aynı olur
            if watch_count > 1:
                se = std_dev / math.sqrt(watch_count)      # Standart hata
                margin = Z_VALUE * se                      # Hata payı
                ci_lower = avg_rating - margin
                ci_upper = avg_rating + margin
            else:
                # Tek kişinin oyu varsa belirsizlik çok yüksek,
                # pratikte alt/üst aynıdır
                ci_lower = avg_rating
                ci_upper = avg_rating
            
            # Yeni kolonları row sözlüğüne ekleyelim
            row["CI_Lower_95"] = ci_lower
            row["CI_Upper_95"] = ci_upper
            
            # Sonuç listesine ekle
            result_data.append(row)

    # Yeni CSV dosyasına yaz
    with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=extended_headers)
        writer.writeheader()
        for r in result_data:
            writer.writerow(r)
    
    print(f"%95 Güven aralıkları hesaplandı ve {OUTPUT_FILE} dosyasına kaydedildi.")

if __name__ == "__main__":
    main()
