
from loguru import logger
import numpy as np

def recommend_for_user(user_id_enc, sparse_mat, item_to_neighbors, ratings_df, top_n=5):
    """
    For a given user (by encoded ID), return the most relevant movies based on user preferences.
    """
    logger.info("Start of recommending for user")
    user_ratings = sparse_mat[:, user_id_enc].toarray().ravel()
    rated_indices = np.where(user_ratings > 0)[0]

    candidate_scores = {}
    for item_idx in rated_indices:
        rating_val = user_ratings[item_idx]
        for nbr_idx, dist in item_to_neighbors.get(item_idx, []):
            # Avoid division by zero
            if dist < 1e-9:
                dist = 1e-9  
            score = rating_val / dist
            candidate_scores[nbr_idx] = candidate_scores.get(nbr_idx, 0) + score

    # Exclude movies already rated by the user
    candidates = [(itm, sc) for itm, sc in candidate_scores.items() if itm not in set(rated_indices)]
    candidates.sort(key=lambda x: x[1], reverse=True)
    top_candidates = candidates[:top_n]

    results = []
    for movie_enc, score in top_candidates:
        orig_movie_id = ratings_df.loc[ratings_df["movie_enc"] == movie_enc, "movie_id"].iloc[0]
        results.append((movie_enc, orig_movie_id, score))
    return results
