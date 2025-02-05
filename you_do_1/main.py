# main.py

import pandas as pd

# Import modules
from modules.data_loader import load_data, build_sparse_matrix
from modules.dimensionality import reduce_dimensionality
from modules.index_builder import build_annoy_index, precompute_topk_neighbors
from modules.recommender import recommend_for_user

# Import task functions
from tasks.task2 import find_similar_movies
from tasks.task3 import compare_movies

def main():
    # File paths for ratings
    files = [
        "data/rating_1.txt",
        "data/rating_2.txt",
        "data/rating_3.txt",
        "data/rating_4.txt",
    ]
    
    # Load and prepare data
    ratings_df = load_data(files)
    ratings_df, sparse_mat = build_sparse_matrix(ratings_df)
    
    # Dimensionality reduction
    n_components = 100  # Adjust as needed
    item_factors = reduce_dimensionality(sparse_mat, n_components=n_components)
    
    # Build Annoy index and precompute neighbors
    annoy_index = build_annoy_index(item_factors, n_trees=10)
    num_movies = sparse_mat.shape[0]
    item_to_neighbors = precompute_topk_neighbors(annoy_index, num_movies, k=50)
    
    # Example: Recommend movies for a given user
    target_user_id = 1488844
    user_encoded_vals = ratings_df.loc[ratings_df['user_id'] == target_user_id, 'user_enc'].unique()
    if len(user_encoded_vals) == 0:
        print(f"User ID {target_user_id} not found in data!")
    else:
        example_user_enc = user_encoded_vals[0]
        print(f"Original user_id={target_user_id} is encoded as user_enc={example_user_enc}")
    
        recommendations = recommend_for_user(example_user_enc, sparse_mat, item_to_neighbors, ratings_df, top_n=5)
    
        # Load movie titles
        df_titles = pd.read_csv('data/cleaned_movie_titles.csv')
        for movie_enc, movie_id, score in recommendations:
            title = df_titles.loc[df_titles['movie_id'] == movie_id, 'title'].iloc[0]
            print(f"Recommendation: movie_id {movie_id}, title: {title}, score: {score:.3f}")
    
    # TASK2: Find similar movies for a given movie
    print("\n--- TASK2: Finding similar movies for movie_id 1 ---")
    similar_movies = find_similar_movies(1, ratings_df, item_to_neighbors, top_k=5)
    for movie_enc, movie_id, sim_score in similar_movies:
        title = df_titles.loc[df_titles['movie_id'] == movie_id, 'title'].iloc[0]
        print(f"Movie_id {movie_id} (title: {title}) with similarity score: {sim_score:.3f}")
    
    # TASK3: Compare two movies
    print("\n--- TASK3: Comparing movies ---")
    compare_movies(1, 50, ratings_df, item_factors, similarity_threshold=0.8)

if __name__ == "__main__":
    main()
