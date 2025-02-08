# src/models.py
import numpy as np
import lightgbm as lgb
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix
from src.preprocessing import undersample_data

def cross_validate_lgb(x_train, y_train, params, n_splits=5, majority_multiplier=5, random_state=42):
    """
    Perform cross-validation using LightGBM.
    """
    skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=random_state)
    models = []
    metrics = []
    
    for fold, (train_index, val_index) in enumerate(skf.split(x_train, y_train), 1):
        X_train_fold = x_train.iloc[train_index]
        y_train_fold = y_train.iloc[train_index]
        X_val_fold = x_train.iloc[val_index]
        y_val_fold = y_train.iloc[val_index]
        
        # Apply undersampling on the training fold
        X_train_res, y_train_res = undersample_data(X_train_fold, y_train_fold, majority_multiplier, random_state)
        
        model = lgb.LGBMClassifier(**params)
        model.fit(X_train_res, y_train_res)
        models.append(model)
        
        y_val_pred = model.predict(X_val_fold)
        y_val_proba = model.predict_proba(X_val_fold)[:, 1]
        
        acc = accuracy_score(y_val_fold, y_val_pred)
        prec = precision_score(y_val_fold, y_val_pred)
        rec = recall_score(y_val_fold, y_val_pred)
        f1 = f1_score(y_val_fold, y_val_pred)
        roc_auc = roc_auc_score(y_val_fold, y_val_proba)
        cm = confusion_matrix(y_val_fold, y_val_pred)
        
        print(f"Fold {fold}:")
        print(f"  Accuracy: {acc:.4f}")
        print(f"  Precision: {prec:.4f}")
        print(f"  Recall: {rec:.4f}")
        print(f"  F1 Score: {f1:.4f}")
        print(f"  ROC AUC: {roc_auc:.4f}")
        print(f"  Confusion Matrix:\n{cm}\n")
        
        metrics.append({
            "accuracy": acc,
            "precision": prec,
            "recall": rec,
            "f1": f1,
            "roc_auc": roc_auc,
            "conf_matrix": cm
        })
    return models, metrics

def train_final_lgb(x_train, y_train, params):
    """
    Train a final LightGBM model on the full training set.
    """
    model = lgb.LGBMClassifier(**params)
    model.fit(x_train, y_train)
    return model
