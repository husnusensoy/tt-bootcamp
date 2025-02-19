# src/feature_importance.py
import matplotlib.pyplot as plt
import pandas as pd

def plot_feature_importance(model, feature_names, top_n=20):
    importances = model.feature_importances_
    importance_df = pd.DataFrame({
        'feature': feature_names,
        'importance': importances
    }).sort_values(by='importance', ascending=False)
    
    top_features = importance_df.head(top_n)
    plt.figure(figsize=(8, 6))
    plt.barh(top_features['feature'], top_features['importance'], color='skyblue')
    plt.xlabel("Feature Importance")
    plt.title("Top Feature Importances")
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.show()
