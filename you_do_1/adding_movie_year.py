import os
from datetime import datetime

# Dosya yolları
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
INPUT_DIR = os.path.join(BASE_DIR, "tt-bootcamp", "you_do_1", "organized_data")
TITLES_FILE = os.path.join(BASE_DIR, "binge", "movie_titles.csv")

METADATA_FILE = os.path.join(INPUT_DIR, "movie_metadata_v1.txt")
INPUT_FILE = os.path.join(INPUT_DIR, "movie_avg_ratings_fixed_v1.txt")
OUTPUT_FILE = os.path.join(INPUT_DIR, "movie_avg_ratings_v2.txt")
UPDATED_METADATA_FILE = os.path.join(INPUT_DIR, "movie_metadata_v2.txt")

# **1️⃣ movie_titles.csv'yi oku ve movie_id → year eşleşmesi oluştur**
def load_movie_years(title_file):
    movie_years = {}
    with open(title_file, "r", encoding="ISO-8859-1", errors="replace") as f:
        for line in f:
            parts = line.strip().split(",")
            if len(parts) < 2:
                continue  # Eksik satırları atla
            movie_id = parts[0].strip()
            year = parts[1].strip()
            if year.isdigit():
                movie_years[movie_id] = int(year)  # Yılı integer olarak kaydet
    return movie_years

# **2️⃣ Tarih farkı hesaplama fonksiyonu**
def calculate_year_diff(min_date, year):
    """Min_Date ile Year farkını hesaplar."""
    try:
        min_year = int(min_date[:4])  # YYYY-MM-DD formatından yılı al
        return min_year - year  # Artık integer işlemi doğru çalışacak
    except ValueError:
        return 0  # Varsayılan olarak fark 0 al

# **3️⃣ movie_avg_ratings_fixed.txt'yi oku, year ekle ve yeni dosyaya yaz**
def process_movie_data(input_file, output_file, movie_years):
    with open(input_file, "r", encoding="utf-8") as infile, open(output_file, "w", encoding="utf-8") as outfile:
        for line in infile:
            movie_id = line[:6].strip()  # İlk 6 karakter Movie_ID
            year = movie_years.get(movie_id, 0)  # Varsayılan 0

            min_date = line[18:28].strip()  # Min_Date sütunu (16-26 arası)
            year_diff = calculate_year_diff(min_date, year)

            # **Güncellenmiş Fixed-Length Format**
            new_line = f"{line.strip()} {year:<4} {year_diff:>2}\n"
            outfile.write(new_line)

# **4️⃣ Metadata dosyasını güncelle**
def update_metadata(metadata_file, updated_metadata_file):
    """Metadata dosyasına Year ve Year_Diff ekler."""
    new_columns = """Year          int        4
Year_Diff     int        2
"""
    with open(metadata_file, "r", encoding="utf-8") as f:
        metadata = f.read()

    with open(updated_metadata_file, "w", encoding="utf-8") as f:
        f.write(metadata.strip() + "\n" + new_columns)

# **5️⃣ Ana Çalıştırma Fonksiyonu**
def main():
    movie_years = load_movie_years(TITLES_FILE)
    process_movie_data(INPUT_FILE, OUTPUT_FILE, movie_years)
    update_metadata(METADATA_FILE, UPDATED_METADATA_FILE)

    print(f"Yeni dosya oluşturuldu: {OUTPUT_FILE}")
    print(f"Metadata güncellendi: {UPDATED_METADATA_FILE}")

if __name__ == "__main__":
    main()
