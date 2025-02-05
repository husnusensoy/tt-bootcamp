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

   


if __name__ == "__main__":

    print("this is cold start recommandations: \n")
    cold_start_df = cold_start()
    df = pd.DataFrame(cold_start_df)


    print(df.info())