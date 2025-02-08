import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv(r'C:\Users\utkub\OneDrive\Masaüstü\Code\Capstone\filtered_merged_churn_df.csv')
df = df[df["predicted_proba"] > 0.7]

# st.title("Customer Churn")

# Sidebar with options
option = st.sidebar.radio("Select an option:", ["Dengesizlik", "Data","Scoring" ,"Feature Importances","SHAP", "Search List","Conclusion"])

if option == "Feature Importances":
    st.write("## Feature Importances")
    st.write("### Prepaid")
    st.image("prepaid.png")
    st.write("### Postpaid")
    st.image("postpaid.png")
    st.write("### Broadband")
    st.image("broadband.png")
elif option == "Scoring":
    st.image("score.png")
elif option == "Data":
    st.image("sampling.png")
    st.write("## Yapılan:")
    st.write("### - One Hot Encoding")
    st.write("### - SMOTE")
    st.write("### - Random Under Sampling")
    st.write("### - Feature Engineering")
    st.write("### - Imputing Missing Values")
elif option == "SHAP":
    st.write("## SHAP Values")
    st.image("shap.png")
    
elif option == "Search List":
    st.write("### Table View")
    st.dataframe(df)

elif option == "Conclusion":
    # Option 1: Display a plot
    # st.write("### Müşteri Erime Analysis", unsafe_allow_html=True)
    # st.markdown("<style> .stMarkdown { color: white; } </style>", unsafe_allow_html=True)
    fig, ax = plt.subplots(figsize=(5, 5), facecolor='#0e1117')
    labels = ['Tespit Edilen', 'Tespit Edilemeyen']
    values = [81, 19]
    ax.bar(labels, values, color=['#23a8f2', 'red'])
    ax.set_ylabel("Yüzde (%)", color='white')
    ax.set_title("Müşteri Erime", color='white')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    st.pyplot(fig)
elif option == "Dengesizlik":
    st.write("## Sınıf Dengesizliği")
    st.image("churn.png")