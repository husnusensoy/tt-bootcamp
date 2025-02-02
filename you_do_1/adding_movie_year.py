import os
import csv
import re
from datetime import datetime

# Veri yolu tanımı
BASE_PATH = "/Users/2na/Documents/binge"
INPUT_DIR = "you_do_1/organized_data"
TITLES_FILE = os.path.join(BASE_PATH, "movie_titles.csv")
INPUT_FILE = os.path.join(INPUT_DIR, "movie_avg_ratings.csv")
OUTPUT_FILE = os.path.join(INPUT_DIR, "movie_avg_ratings_v2.csv")

# Klasör kontrolü ve oluşturma
def ensure_directory_exists(directory: str):
    if not os.path.exists(directory):
        os.makedirs(directory)

# Film yıllarını yükleme
def load_movie_years(title_file):
    movie_years = {}
    with open(title_file, "r", encoding="ISO-8859-1", errors="replace") as f:
        for line in f:
            parts = line.strip().split(",")
            if len(parts) < 2:
                continue
            movie_id = parts[0].strip()
            year = parts[1].strip()
            if year.isdigit():
                movie_years[movie_id] = int(year)
    return movie_years

# Tarih farkı hesaplama
def calculate_year_diff(min_date, year):
    try:
        min_year = int(min_date[:4])
        return min_year - year
    except ValueError:
        return 0

# CSV formatında veriyi güncelleme
def process_movie_data(input_file, output_file, movie_years):
    with open(input_file, "r", encoding="utf-8") as infile, open(output_file, "w", newline="", encoding="utf-8") as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        headers = next(reader) + ["Year", "Year_Diff"]
        writer.writerow(headers)
        
        for row in reader:
            movie_id = row[0]
            min_date = row[3]
            year = movie_years.get(movie_id, 0)
            year_diff = calculate_year_diff(min_date, year)
            writer.writerow(row + [year, year_diff])

# Ana çalışma fonksiyonu
def main():
    ensure_directory_exists(INPUT_DIR)
    movie_years = load_movie_years(TITLES_FILE)
    process_movie_data(INPUT_FILE, OUTPUT_FILE, movie_years)
    print(f"Yeni dosya oluşturuldu: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()