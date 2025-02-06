import duckdb
from scipy import stats

class RecommendationEngine:
    def __init__(self, db_path):
        self.con = duckdb.connect(database=db_path)
        self._prepare_aggregates()
    
    def _prepare_aggregates(self):
        self.con.execute("""
            CREATE OR REPLACE TABLE movie_stats AS
            SELECT 
                movie_id, 
                COUNT(ratings.rating) AS rating_count, 
                AVG(ratings.rating) AS rating_mean, 
                STDDEV_SAMP(ratings.rating) AS rating_std
            from ratings
            GROUP BY movie_id
        """)
        self.con.execute("""
            CREATE OR REPLACE TABLE movie_stats_full AS
            SELECT 
                ms.movie_id, 
                ms.rating_count, 
                ms.rating_mean, 
                ms.rating_std,
                m.year,
                m.title
            FROM movie_stats ms
            JOIN movies m ON ms.movie_id = m.movie_id
        """)
    
    def cold_start_recommendations(self, n=10):
        quantile_query = """
        SELECT GREATEST(10, quant) AS min_ratings FROM (
            SELECT percentile_cont(0.75) WITHIN GROUP (ORDER BY rating_count) AS quant
            FROM movie_stats_full
        ) sub
        """
        min_ratings = self.con.execute(quantile_query).fetchone()[0]
        
        query = f"""
            SELECT title, year, rating_mean, rating_count
            FROM movie_stats_full
            WHERE rating_count >= {min_ratings}
            ORDER BY rating_mean DESC, rating_count DESC
            LIMIT {n}
        """
        recommendations = self.con.execute(query).fetchdf()
        return recommendations
    
    def get_user_recommendations(self, user_id, n=10):
        user_ratings_df = self.con.execute(f"""
            SELECT movie_id, rating 
            from ratings 
            WHERE user_id = {user_id}
        """).fetchdf()
        
        if user_ratings_df.empty:
            print("buralarda yenisin galiba")
            return  self.cold_start_recommendations(n)
        
        user_favorites = user_ratings_df[user_ratings_df['rating'] >= 4]['movie_id'].tolist()
        if not user_favorites:
            print("buralarda yenisin galiba")
            return self.cold_start_recommendations(n)
        
        favs_str = ",".join(map(str, user_favorites))
        similar_users_df = self.con.execute(f"""SELECT DISTINCT user_id from ratings WHERE movie_id IN ({favs_str})""").fetchdf()
        similar_users = similar_users_df['user_id'].tolist()
        similar_users_str = ",".join(map(str, similar_users))
        
        user_movies = user_ratings_df['movie_id'].tolist()
        user_movies_str = ",".join(map(str, user_movies))
        
        query = f"""
            SELECT rec.movie_id, rec.rating_mean, rec.rating_count, m.title, m.year
            FROM (
                SELECT movie_id, COUNT(ratings.rating) AS rating_count, AVG(ratings.rating) AS rating_mean
                from ratings
                WHERE user_id IN ({similar_users_str})
                  AND movie_id NOT IN ({user_movies_str})
                GROUP BY movie_id
            ) rec
            JOIN movies m ON rec.movie_id = m.movie_id
            ORDER BY rec.rating_mean DESC, rec.rating_count DESC
            LIMIT {n}
        """
        recommendations = self.con.execute(query).fetchdf()
        return recommendations[['title', 'year', 'rating_mean', 'rating_count']]
    
    def compare_movies(self, movie_id1, movie_id2):
        ratings1 = self.con.execute(f"""SELECT rating from ratings WHERE movie_id = {movie_id1}""").fetchdf()['rating']
        ratings2 = self.con.execute(f"""SELECT rating from ratings WHERE movie_id = {movie_id2}""").fetchdf()['rating']
        
        t_stat, p_value = stats.ttest_ind(ratings1, ratings2, equal_var=False)
        
        movie1_info = self.con.execute(f"""SELECT title, year FROM movies WHERE movie_id = {movie_id1}""").fetchdf().iloc[0]
        movie2_info = self.con.execute(f"""SELECT title, year FROM movies WHERE movie_id = {movie_id2}""").fetchdf().iloc[0]
        
        return {
            'movie1': {
                'title': movie1_info['title'],
                'year': movie1_info['year'],
                'mean_rating': ratings1.mean(),
                'rating_count': len(ratings1)
            },
            'movie2': {
                'title': movie2_info['title'],
                'year': movie2_info['year'],
                'mean_rating': ratings2.mean(),
                'rating_count': len(ratings2)
            },
            'statistical_test': {
                't_statistic': t_stat,
                'p_value': p_value,
                'significantly_different': p_value < 0.05
            }
        }
