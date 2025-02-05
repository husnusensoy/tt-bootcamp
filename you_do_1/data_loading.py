import duckdb
import glob

con = duckdb.connect(database='my_database.db')

rating_files = glob.glob("rating_*.txt")

con.execute("""
    CREATE TABLE df_ratings AS
    SELECT * FROM read_csv_auto(?, columns={
        'movie_id': 'INTEGER',
        'user_id': 'INTEGER',
        'tarih': 'DATE',
        'rating': 'INTEGER'
    })
""", [rating_files])

con.execute("""
    CREATE TABLE df_movies AS
    SELECT * FROM read_csv('movie_titles.csv', 
        delim=',', 
        header=True, 
        columns={'movie_id': 'INTEGER', 'yayım_yili': 'INTEGER', 'film_adi': 'VARCHAR'}, 
        ignore_errors=True
    )
""")

query = """
    SELECT
        m.movie_id,
        m.film_adi,
        m.yayım_yili,
        r.user_id,
        r.tarih,
        r.rating
    FROM df_movies AS m
    JOIN df_ratings AS r ON m.movie_id = r.movie_id
    LIMIT 5
"""

result = con.execute(query).fetchall()

print("\nMerged Data:")
for row in result:
    print(row)

df = con.execute(query).df()
df.to_csv("merged_data.csv", index=False)