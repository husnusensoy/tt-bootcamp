from collections import defaultdict
from typing import List

import numpy as np
import pandas as pd
import streamlit as st
from sklearn.metrics import accuracy_score, confusion_matrix


class NBBinary:
    def __init__(self):
        self.pos = 0
        self.neg = 0
        
        self.pos_prior = 0.0
        self.neg_prior = 0.0

        self.freq_pos = defaultdict(int)
        self.freq_neg = defaultdict(int)

    def fit(self, corpus: List[str], labels: List[int]):
        for doc, label in zip(corpus, labels):            
            if label  == 0 :
                self.neg +=1
                
                for w in doc.split():
                    self.freq_pos[w.lower()[:5]] +=1
            else:
                self.pos +=1
                
                for w in doc.split():
                    self.freq_neg[w.lower()[:5]] +=1
                    
        self.pos_prior = self.pos/(self.neg + self.pos)
        self.neg_prior = self.neg/(self.neg + self.pos)
        
        self.pos_doc_word_prob = {}
        self.neg_doc_word_prob = {}
        
        for w in self.freq_pos:
            self.pos_doc_word_prob[w] = self.freq_pos[w] / sum(self.freq_pos.values())
            
        for w in self.freq_neg:
            self.neg_doc_word_prob[w] = self.freq_neg[w] / sum(self.freq_neg.values())           
        
        


    def predict(self, corpus: List[str]) -> np.array: ...


def prior_model(df) -> np.array:
    counter = defaultdict(int)
    for y in df["label"]:
        counter[y] += 1

    top_class = max(counter.items(), key=lambda kv: kv[1])[0]

    return np.ones(len(df)) * top_class


def main():
    st.header("Sentiment Analysis")

    st.markdown("Let's do some naive bayes")

    st.subheader("Documentation")

    df = pd.read_csv("Train.csv")

    st.dataframe(df)

    y_pred = prior_model(df)

    st.text(f"My accuracy by prior classifier is {accuracy_score(df['label'], y_pred)}")

    st.dataframe(confusion_matrix(df["label"], y_pred))
    
    nb = NBBinary()
    
    nb.fit(list(df['text']), list(df['label']))
    
    st.text(f"Total pos {nb.pos} neg {nb.neg}")
    st.text(nb.pos_doc_word_prob)


if __name__ == "__main__":
    main()
