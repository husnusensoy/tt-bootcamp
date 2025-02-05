import duckdb

# DuckDB veritabanı oluşturma (veya açma)
conn = duckdb.connect('mydatabase.db')

# CSV dosyasını içe aktarma
#conn.execute("CREATE TABLE my_table AS SELECT * FROM read_csv_auto('C:/Users/VICTUS/OneDrive/Masaüstü/Python/movie_titles.csv')")
conn.execute("CREATE TABLE my_tables AS SELECT * FROM read_csv_auto('C:/Users/VICTUS/OneDrive/Masaüstü/Python/merged_ratings.csv')")

# Veritabanı bağlantısını kapatma
conn.close()



