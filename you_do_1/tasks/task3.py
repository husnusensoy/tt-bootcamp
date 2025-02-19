import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from loguru import logger

import pandas as pd
from modules.data_loader import load_data, build_sparse_matrix
from modules.dimensionality import reduce_dimensionality

import numpy as np
from numpy.linalg import norm

def compare_movies(movie_id1, movie_id2, ratings_df, item_factors, similarity_threshold=0.8):
    """
    Compare two movies and return them they are different or same 
    """

    film1 = ratings_df.loc[ratings_df["movie_id"] == movie_id1, "movie_enc"]
    film2 = ratings_df.loc[ratings_df["movie_id"] == movie_id2, "movie_enc"]

    if film1.empty or film2.empty:
        print("One or both movie IDs were not found!")
        return None
    
    movie_enc1 = film1.iloc[0]
    movie_enc2 = film2.iloc[0]
    
    vec1 = item_factors[movie_enc1]
    vec2 = item_factors[movie_enc2]
    
    cos_sim = np.dot(vec1, vec2) / (norm(vec1) * norm(vec2))
    
    similarity_status = "Benzer" if cos_sim >= similarity_threshold else "Farklı"
    print(f"Film {movie_id1} ile Film {movie_id2} arasındaki kosinüs benzerliği: {cos_sim:.3f} ({similarity_status})")
    
    return cos_sim, similarity_status


if __name__ == '__main__':

    files = [
        "data/rating_1.txt",
        "data/rating_2.txt",
        "data/rating_3.txt",
        "data/rating_4.txt",
    ]
    
    ratings_df = load_data(files)
    ratings_df, sparse_mat = build_sparse_matrix(ratings_df)
    n_components = 25  
    item_factors = reduce_dimensionality(sparse_mat, n_components=n_components)
    

    print("\n--- TASK3: Comparing movies ---")
    compare_movies(1, 5, ratings_df, item_factors, similarity_threshold=0.8)
