"""Simple Naive Bayes for Binary classification

This one is pretty slow in first implementation: 16 sec for 2000 docs (125 doc/sec)
    * Vocabulary build 30K doc/s
    * Parameter fit 105 doc/s
    * Prediction 8K doc/s
"""

from collections import defaultdict
from math import log10 as log
from typing import List

import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, confusion_matrix
from tqdm import tqdm


class Probability:
    def __init__(self, N: int, alpha: float = 1.0):
        """
        - Laplace smoothing
        """
        self.freq = {}
        self.cardinality_vocabulary = N
        self.alpha = alpha
        self.N = 0

    def add(self, w: str, count: int = 1):
        self.freq[w] = self.freq.get(w, 0) + count
        self.N = sum(self.freq.values())

    def proba(self, w: str) -> float:
        return (self.freq.get(w, 0) + self.alpha) / (
            self.N + self.cardinality_vocabulary * self.alpha
        )

    def log_proba(self, w: str) -> float:
        """Caution: Log at base 10"""
        return log(self.proba(w))

    def __str__(self):
        return ", ".join(
            f"P({w})={self.log_proba(w):.4f}"
            for w, _ in sorted(self.freq.items(), key=lambda wf: wf[1], reverse=True)[
                :10
            ]
        )


class NBBinary:
    def __init__(self):
        self.prior = Probability(2, 0)

        self.proba_pos = None
        self.proba_neg = None

    def _tokenize(self, s: str) -> List[str]:
        """_summary_

        - Poor mans lemmatizer using prefix 5
        """
        return [w.lower()[:5] for w in s.split()]

    def fit(self, corpus: List[str], labels: List[int]):
        vocab = set()

        for doc in tqdm(corpus, desc="Building vocabulary...", unit="doc"):
            for w in self._tokenize(doc):
                vocab.add(w)

        self.proba_neg = Probability(len(vocab))
        self.proba_pos = Probability(len(vocab))

        for doc, label in tqdm(
            zip(corpus, labels), desc="Calculating probabilities...", unit="doc"
        ):
            if label == 0:
                self.prior.add("neg", 1)

                for w in self._tokenize(doc):
                    self.proba_neg.add(w, 1)
            else:
                self.prior.add("pos", 1)

                for w in self._tokenize(doc):
                    self.proba_pos.add(w, 1)

    def predict(self, corpus: List[str]) -> np.array:
        """Use log probabilities instead of raw probabs."""
        result = []
        for doc in tqdm(corpus, desc="Inferring..."):
            pos = self.prior.log_proba("pos")
            neg = self.prior.log_proba("neg")

            for w in self._tokenize(doc):
                pos += self.proba_pos.log_proba(w)
                neg += self.proba_neg.log_proba(w)

            result.append(int(pos > neg))

        return np.array(result)


def prior_model(df) -> np.array:
    counter = defaultdict(int)
    for y in df["label"]:
        counter[y] += 1

    top_class = max(counter.items(), key=lambda kv: kv[1])[0]

    return np.ones(len(df)) * top_class


def main():
    df = pd.read_csv("Train.csv", nrows=2_000)

    eighty_pct = 0.8 * df.shape[0]

    train_df = df.loc[: eighty_pct - 1, :]
    test_df = df.loc[eighty_pct:, :]

    nb = NBBinary()

    nb.fit(list(train_df["text"]), list(train_df["label"]))

    print(f"Prior Probabilities {nb.prior}")

    y_pred = nb.predict(list(test_df["text"]))

    print(
        f"My accuracy by Naive Bayesian classifier is {accuracy_score(test_df['label'], y_pred)}"
    )

    print(confusion_matrix(test_df["label"], y_pred))


if __name__ == "__main__":
    main()
