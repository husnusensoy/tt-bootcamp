import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
from sklearn.datasets import make_blobs
from sklearn.metrics import accuracy_score


def stupid_classifier(x, y)-> np.array:
    
    m,_ = x.shape
    
    return np.random.randint(0,5,m)

def euc(x1,x2) -> float:
    return np.dot((x1-x2),(x1-x2))

def knn(x,y,k,dist_fn=euc) -> np.array:
    
    m, _ = x.shape
    
    dist = np.zeros((m,m))
    
    for i in range(m):
        for j in range(m):
            if i == j:
                continue
        
            if i < j:
                dist[i,j] =dist_fn(x[i,:], x[j,:])
            else:
                dist[i,j] = dist[j,i]
                
    y_pred = []
    for i in range(m):
        idx = np.argsort(dist[i,:])[:k]
        
        counter = {}
        for color in y[idx]:
            counter[color] = counter.get(color,0) + 1
        
        y_pred.append(max(counter.items(), key=lambda x: x[1])[0])
        
    return np.array(y_pred)
    
    

def main():
    st.header("Let's Generate a Blob")

    n = st.slider("Number of samples", 10, 10_000, value=500)

    sd = st.slider("Noise", 0.0, 10.0, value=2.0)

    n_center = st.slider("Number of centers", 2, 5, value=3)

    x, y = make_blobs(
        n_samples=n, centers=n_center, n_features=2, random_state=42, cluster_std=sd
    )
    
    df = pd.DataFrame(dict(x1=x[:,0], x2=x[:,1],y=y))
    
    fig = px.scatter(df, x="x1", y="x2", color="y")
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("### Let's do the implementation")
    
    st.dataframe(df)
    
    
    k = st.slider("Neighbour Count", 1,5, value=2)
    
    y_pred = stupid_classifier(x,y)
    
    st.text(f"My accuracy by stupid_classified is {accuracy_score(y, y_pred)}")
    
    y_pred =knn(x,y,k,dist_fn=euc)
   
    st.text(f"My accuracy by knn is {accuracy_score(y, y_pred)}")
   


if __name__ == "__main__":
    main()
