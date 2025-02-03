
from sklearn.decomposition import TruncatedSVD
from loguru import logger
import numpy as np

def reduce_dimensionality(sparse_mat, n_components=25):
    """
    Reduce dimensionality by applying TruncatedSVD to the sparse matrix.
    """
    logger.info("Start of reducing dimensionality")
    sparse_mat = sparse_mat.astype(np.float32)
    svd = TruncatedSVD(n_components=n_components,algorithm="arpack" ,random_state=42)
    item_factors = svd.fit_transform(sparse_mat)
    return item_factors