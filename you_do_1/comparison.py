import duckdb

con = duckdb.connect(database='my_database.db')

movie_1_id = 3  
movie_2_id = 2  

query = f"""
    SELECT 
        f1.film_adi AS film_1,
        f1.yayım_yili AS yayım_yili_1,  
        f2.film_adi AS film_2,
        f2.yayım_yili AS yayım_yili_2  
    FROM df_movies f1, df_movies f2
    WHERE f1.movie_id = {movie_1_id} AND f2.movie_id = {movie_2_id}
"""

result = con.execute(query).fetchall()

for row in result:
    print(f"{row[0]} ({row[1]}) vs {row[2]} ({row[3]})")
    
    if row[1] > row[3]:
        print(f"{row[0]} ({row[1]}) daha yeni bir film.")
    elif row[1] < row[3]:
        print(f"{row[2]} ({row[3]}) daha yeni bir film.")
    else:
        print(f"Her iki film de aynı yayım yılına sahip ({row[1]}).")

con.close()