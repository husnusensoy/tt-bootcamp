
from annoy import AnnoyIndex
from tqdm import tqdm
from loguru import logger

def build_annoy_index(item_factors, n_trees=10):
    """
    Create an Annoy index from the item latent factors.
    """
    logger.info("Start of building Annoy index")
    num_movies, n_components = item_factors.shape
    annoy_index = AnnoyIndex(n_components, metric="euclidean")
    for i in range(num_movies):
        annoy_index.add_item(i, item_factors[i])
    annoy_index.build(n_trees)
    return annoy_index


def precompute_topk_neighbors(annoy_index, num_movies, k=50):
    """
    Precompute the top-k nearest neighbors for each item in the Annoy index.
    """
    logger.info("Start of precomputing top-k neighbors")
    item_to_neighbors = {}
    for i in tqdm(range(num_movies), desc="Computing neighbors"):
        neighbor_ids, distances = annoy_index.get_nns_by_item(i, k + 1, include_distances=True)
        # Exclude the item itself (distance == 0)
        neighbors_filtered = [(nid, dist) for nid, dist in zip(neighbor_ids, distances) if nid != i]
        item_to_neighbors[i] = neighbors_filtered
    return item_to_neighbors