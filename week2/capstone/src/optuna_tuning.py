# src/optuna_tuning.py
import optuna
import numpy as np
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import f1_score
import lightgbm as lgb
from src.preprocessing import undersample_data

def objective(trial, x_train, y_train, majority_multiplier=5, random_state=42):
    params = {
        "objective": "binary",
        "boosting_type": "gbdt",
        'n_estimators': trial.suggest_int('n_estimators', 100, 500),
        'learning_rate': trial.suggest_float('learning_rate', 1e-3, 0.1, log=True),
        'num_leaves': trial.suggest_int('num_leaves', 10, 50),
        'max_depth': trial.suggest_int('max_depth', 3, 10),
        'min_child_samples': trial.suggest_int('min_child_samples', 5, 20),
        'subsample': trial.suggest_float('subsample', 0.5, 1.0),
        'colsample_bytree': trial.suggest_float('colsample_bytree', 0.5, 1.0),
        'reg_alpha': trial.suggest_float('reg_alpha', 1e-8, 1e-1, log=True),
        'reg_lambda': trial.suggest_float('reg_lambda', 1e-8, 1e-1, log=True),
        "random_state": random_state,
        "verbose": -1,
        "n_jobs": -1
    }
    
    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=random_state)
    f1_scores = []
    
    for train_idx, val_idx in skf.split(x_train, y_train):
        X_train_fold = x_train.iloc[train_idx]
        y_train_fold = y_train.iloc[train_idx]
        X_val_fold = x_train.iloc[val_idx]
        y_val_fold = y_train.iloc[val_idx]
        
        X_train_res, y_train_res = undersample_data(X_train_fold, y_train_fold, majority_multiplier, random_state)
        model = lgb.LGBMClassifier(**params)
        model.fit(X_train_res, y_train_res)
        
        y_val_pred = model.predict(X_val_fold)
        f1_scores.append(f1_score(y_val_fold, y_val_pred))
    
    return np.mean(f1_scores)

def run_optuna(x_train, y_train, n_trials=50):
    study = optuna.create_study(direction="maximize")
    study.optimize(lambda trial: objective(trial, x_train, y_train), n_trials=n_trials)
    
    print("\nBest trial:")
    best_trial = study.best_trial
    print(f"  F1 Score: {best_trial.value:.4f}")
    print("  Best hyperparameters:")
    for key, value in best_trial.params.items():
        print(f"    {key}: {value}")
    return best_trial.params
