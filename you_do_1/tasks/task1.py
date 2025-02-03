from pathlib import Path
import pandas as pd
import numpy as np
from loguru import logger

class Task1:
    def __init__(self, input_files, titles_file):
        """
        Initialize Task1 with a list of input text files containing movie ratings and
        the path to the cleaned movie titles file.
        
        Parameters:
            input_files (list): List of file paths (as strings or Path objects) to the rating text files.
            titles_file (str or Path): Path to the cleaned_movie_titles.csv file.
        """
        self.input_files = [Path(f) for f in input_files]
        self.titles_file = Path(titles_file)
        self.movie_ratings_df = None  # Will hold the processed movie ratings DataFrame

    @staticmethod
    def compute_weighted_metrics(group):
        """
        Given a group (DataFrame) of ratings for a specific movie,
        compute the weighted average rating using the square of the counts.
        
        Each rating is weighted by (count^2). For example, if a movie received 
        a rating of 4 three times, it contributes 4 * (3^2) to the weighted sum.
        
        Returns:
            A pandas Series with:
                - average_rating: the weighted average rating.
                - count: the total number of ratings (sum of counts).
        """
        cnt_squared = group['cnt'] ** 2
        weighted_sum = (group['rating'] * cnt_squared).sum()
        total_weight = cnt_squared.sum()
        avg_rating = weighted_sum / total_weight if total_weight != 0 else np.nan
        total_cnt = group['cnt'].sum()
        return pd.Series({
            'average_rating': avg_rating,
            'count': total_cnt
        })

    def process_movie_ratings(self):
        """
        Processes the raw rating text files in chunks, computes weighted metrics per movie,
        applies log normalization on the rating counts, and calculates a final score.
        
        The final score is computed as:
        
            score = 0.8 * average_rating + 0.2 * normalized_rating_count
            
        where:
            normalized_rating_count = (log(1 + count) - min_log) / (max_log - min_log)
        
        The processed results are stored in self.movie_ratings_df.
        
        Returns:
            A pandas DataFrame with columns: ['movie_id', 'average_rating', 'count',
            'log_count', 'normalized_rating_count', 'score']
        """
        # Generator to read each file in chunks (each chunk has 100,000 rows)
        def read_large_txt(files):
            for file in files:
                for chunk in pd.read_csv(
                    file,
                    chunksize=100000,
                    names=['movie_id', 'user_id', 'date', 'rating'],
                    header=None
                ):
                    # Yield only the required columns
                    yield chunk[['movie_id', 'rating']]
        
        # Concatenate all the chunks from all files into a single DataFrame
        logger.info("start reading")
        df = pd.concat(read_large_txt(self.input_files), ignore_index=True)
        logger.info("end reading")
        # Group by both movie_id and rating to count the number of each rating per movie
        rating_counts = df.groupby(['movie_id', 'rating']).size().reset_index(name='cnt')
        
        # Group by movie_id and apply the weighted metric computation
        result = rating_counts.groupby('movie_id').apply(Task1.compute_weighted_metrics).reset_index()
        
        # Log-normalize the total count for each movie
        result['log_count'] = np.log1p(result['count'])
        min_log = result['log_count'].min()
        max_log = result['log_count'].max()
        if max_log - min_log == 0:
            result['normalized_rating_count'] = 0
        else:
            result['normalized_rating_count'] = (result['log_count'] - min_log) / (max_log - min_log)
        
        # Compute the final score using the weighted combination
        result['score'] = 0.78 * result['average_rating'] + 0.22 * result['normalized_rating_count']
        
        self.movie_ratings_df = result
        return result

    def get_top_movies(self, top_n=10):
        """
        Returns the top 'top_n' movies sorted by final score in descending order.
        This method assumes that process_movie_ratings() has been called.
        
        Parameters:
            top_n (int): Number of top movies to return (default is 10).
            
        Returns:
            A pandas DataFrame with the top 'top_n' movies.
        """
        if self.movie_ratings_df is None:
            self.process_movie_ratings()
        top_movies = self.movie_ratings_df.sort_values(by='score', ascending=False).head(top_n)
        return top_movies

    def get_top_movies_with_titles(self, top_n=10):
        """
        Returns the top 'top_n' movies with their details including movie_id, year, title,
        and the computed rating metrics.
        
        This method first gets the top movies by score, then merges these with the 
        cleaned movie titles from self.titles_file.
        
        Parameters:
            top_n (int): Number of top movies to return (default is 10).
            
        Returns:
            A pandas DataFrame with merged columns from movie ratings and movie titles.
        """
        # Get top movies by score
        top_movies = self.get_top_movies(top_n=top_n)
        
        # Read the cleaned movie titles
        titles_df = pd.read_csv(self.titles_file)
        
        # Ensure that the movie_id columns are of the same type (string in this example)
        top_movies['movie_id'] = top_movies['movie_id'].astype(str)
        titles_df['movie_id'] = titles_df['movie_id'].astype(str)
        
        # Merge on movie_id
        merged_df = pd.merge(top_movies, titles_df, on='movie_id', how='left')
        
        # Reorder columns for clarity (optional)
        cols_order = ['movie_id', 'year', 'title', 'average_rating', 'count', 'log_count', 'normalized_rating_count', 'score']
        merged_df = merged_df[cols_order]
        
        return merged_df

# Example usage:
if __name__ == '__main__':
    data_dir = Path("data")
    
    # Define the paths to the rating text files.
    ratings_files = [
        data_dir / 'rating_1.txt',
        data_dir / 'rating_2.txt',
        data_dir / 'rating_3.txt',
        data_dir / 'rating_4.txt'
    ]
    
    # Define the path to the cleaned movie titles CSV file.
    titles_file = data_dir / "cleaned_movie_titles.csv"
    
    # Create an instance of Task1.
    task1 = Task1(ratings_files, titles_file)
    
    # Process the movie ratings.
    task1.process_movie_ratings()
    
    # Retrieve and display the top 10 movies with their titles.
    top10_with_titles = task1.get_top_movies_with_titles(top_n=10)
    print("Top 10 Movies by Score with Titles:")
    print(top10_with_titles["title"])
