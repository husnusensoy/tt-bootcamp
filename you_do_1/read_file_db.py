import duckdb
import pandas as pd

conn = duckdb.connect('movies.db')

def create_tables():

    conn.execute("""CREATE TABLE IF NOT EXISTS movie_title_6 AS 
                SELECT * FROM read_csv_auto ('D:/TT-bootcamp/tt-bootcamp/you_do_1/cleaned_movie_titles.csv',
        header = true,
        delim==',',
        quote='"');""") 
    
    conn.execute("""create table if not exists ratings as
                 Select * from read_csv('D:/TT-bootcamp/tt-bootcamp/you_do_1/data/rating_*.txt', columns = {'MovieId': 'int', 'UserId': 'int', 'Date': 'date', 'Rate':'int'}) """)

def cold_start():

    top_10 = conn.execute("""
        SELECT m.movie_name ,AVG(Rate) AS avg_rating, COUNT(MovieId) AS vote_count 
        FROM ratings r
        join movie_title_6 m on m.movie_id = r. MovieId 
        GROUP BY MovieId, m.movie_name
        having count(MovieId) > 2000
        order by avg_rating desc
        limit 10
    """).fetchdf()

    return top_10



def our_customer(user_id):

    ## 2. soruyu düzeltemiyorum hocam yıl yaklaşımından gidebildim anca

    query = """
        SELECT m.movie_name, r.Rate
        FROM ratings r
        join movie_title_6 m on m.movie_id = r. MovieId 
        where = ?
"""

    users_movie = conn.execute(query, [user_id]).fetchall()

    


def compare(movie_id, movieid_2):
    query = """
        SELECT AVG(r.Rate) 
        FROM ratings r
        JOIN movie_title_6 m ON m.movie_id = r.MovieId
        WHERE m.movie_id = ?
    """

    avg_rating1 = conn.execute(query, [movie_id]).fetchone()[0]

    avg_rating2 = conn.execute(query, [movieid_2]).fetchone()[0]

 
    fark = abs(avg_rating1 - avg_rating2)

    threshold = 0.5

    if fark >= threshold:
        return f"Filmler arasında fark var! Ortalama puan farkı: {fark:.2f}"
    else:
        return f"Filmler arasında belirgin bir fark yok. Ortalama puan farkı: {fark:.2f}"



if __name__ == "__main__":

    print("this is cold start recommandations: \n")
    cold_start_df = cold_start()
    df = pd.DataFrame(cold_start_df)
    ratings = compare(3,4)

    print(cold_start_df)
    print("************************")
    print(ratings)

