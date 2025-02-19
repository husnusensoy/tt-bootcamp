# src/data_loader.py
import os
import pandas as pd

def load_data(train_path, test_path):
    """
    Load the train and test datasets.
    """
    train = pd.read_csv(train_path)
    test = pd.read_csv(test_path)
    return train, test
