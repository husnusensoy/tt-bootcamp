import duckdb

con = duckdb.connect(database='my_database.db', config={'max_temp_directory_size': '50GiB'}) 

# Kullanıcılar arası benzerlik hesaplaması (örneğin, Pearson correlation)
query = """
    SELECT 
        r1.user_id AS user1,
        r2.user_id AS user2,
        AVG(r1.rating * r2.rating) AS similarity
    FROM df_ratings AS r1
    JOIN df_ratings AS r2
        ON r1.movie_id = r2.movie_id
        AND r1.user_id != r2.user_id
    GROUP BY r1.user_id, r2.user_id
    ORDER BY similarity DESC
    LIMIT 10
"""
similar_users = con.execute(query).fetchall()

for user1, user2, similarity in similar_users:
    print(f"User1: {user1}, User2: {user2}, Similarity: {similarity}")
