import pandas as pd
from tqdm import tqdm
from scipy.sparse import csr_matrix
from loguru import logger

def load_data(files):
    """
    Load the data files and concatenate them.
    """
    col_names = ["movie_id", "user_id", "date", "rating"]
    dfs = []
    for filename in tqdm(files, desc="Loading files"):
        df = pd.read_csv(filename, header=None, names=col_names)
        dfs.append(df)
    return pd.concat(dfs, ignore_index=True)


def build_sparse_matrix(ratings_df):
    """
    Drop the redundant date column and create a sparse matrix.
    """
    logger.info("Start of creating sparse matrix")
    ratings_df = ratings_df.copy()
    ratings_df.drop(columns=["date"], inplace=True)

    ratings_df["user_enc"] = ratings_df["user_id"].astype("category").cat.codes
    ratings_df["movie_enc"] = ratings_df["movie_id"].astype("category").cat.codes

    num_users = ratings_df["user_enc"].nunique()
    num_movies = ratings_df["movie_enc"].nunique()

    rows = ratings_df["movie_enc"].values
    cols = ratings_df["user_enc"].values
    data = ratings_df["rating"].values

    sparse_mat = csr_matrix((data, (rows, cols)), shape=(num_movies, num_users))
    return ratings_df, sparse_mat
