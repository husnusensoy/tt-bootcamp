import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from loguru import logger

import pandas as pd

# Import functions from your modules
from modules.data_loader import load_data, build_sparse_matrix
from modules.dimensionality import reduce_dimensionality
from modules.index_builder import build_annoy_index, precompute_topk_neighbors
from modules.recommender import recommend_for_user  # New import for user recommendations


def find_similar_movies(movie_id, ratings_df, item_to_neighbors, top_k=5):
    """
    Given a movie (by its original movie_id), return the top-k most similar movies.

    Returns a list of tuples: (movie_enc, orig_movie_id, similarity_score)
    """
    # Find the encoded movie id
    movie_enc_series = ratings_df.loc[ratings_df["movie_id"] == movie_id, "movie_enc"]
    if movie_enc_series.empty:
        logger.info(f"Movie ID {movie_id} not found!")
        return []
    movie_enc = movie_enc_series.iloc[0]
    
    # Get the neighbors from the precomputed dictionary
    neighbors = item_to_neighbors.get(movie_enc, [])
    # Sort neighbors by distance (lower distance means more similar)
    neighbors_sorted = sorted(neighbors, key=lambda x: x[1])
    
    results = []
    for nbr_enc, distance in neighbors_sorted[:top_k]:
        nbr_movie_id = ratings_df.loc[ratings_df["movie_enc"] == nbr_enc, "movie_id"].iloc[0]
        # Transform the distance into a similarity score (using an inverse transformation)
        similarity_score = 1 / (distance + 1e-9)
        results.append((nbr_enc, nbr_movie_id, similarity_score))
    
    return results


if __name__ == '__main__':
    # Define file paths for the ratings data
    files = [
        "data/rating_1.txt",
        "data/rating_2.txt",
        "data/rating_3.txt",
        "data/rating_4.txt",
    ]
    
    # Load and prepare data
    ratings_df = load_data(files)
    ratings_df, sparse_mat = build_sparse_matrix(ratings_df)
    
    # Dimensionality reduction (using TruncatedSVD, for example)
    n_components = 25  # Adjust as needed
    item_factors = reduce_dimensionality(sparse_mat, n_components=n_components)
    
    # Build the Annoy index and precompute the neighbors
    annoy_index = build_annoy_index(item_factors, n_trees=10)
    num_movies = sparse_mat.shape[0]
    item_to_neighbors = precompute_topk_neighbors(annoy_index, num_movies, k=50)
    
    # Load movie titles for display purposes
    df_titles = pd.read_csv("data/cleaned_movie_titles.csv")

    user_id = 1488844  # Change this to the desired user_id


    user_enc_series = ratings_df.loc[ratings_df["user_id"] == user_id, "user_enc"]
    if user_enc_series.empty:
        logger.info(f"User_id {user_id} not found in the dataset!")
    else:
        user_enc = user_enc_series.iloc[0]
        logger.info("\n--- TASK2: Recommending movies for user_id {} ---".format(user_id))
        recommended_movies = recommend_for_user(user_enc, sparse_mat, item_to_neighbors, ratings_df, top_n=5)
        for movie_enc, movie_id, score in recommended_movies:
            title = df_titles.loc[df_titles['movie_id'] == movie_id, 'title'].iloc[0]
            logger.info(f"Movie_id {movie_id} (title: {title}) with recommendation score: {score:.3f}")
