# main.py
import os
from src.data_loader import load_data
from src.preprocessing import preprocess
from src.models import cross_validate_lgb, train_final_lgb
from src.evaluation import print_all_metrics
from src.optuna_tuning import run_optuna
from src.feature_importance import plot_feature_importance

def main():
    # Define paths for your data
    train_path = os.path.join("data", "train.csv")
    test_path = os.path.join("data", "new_test.csv")
    
    # Load the data
    train_df, test_df = load_data(train_path, test_path)
    
    # Preprocess the data
    processed_train, mlb, encoder = preprocess(train_df, train=True)
    processed_test, _, _ = preprocess(test_df, train=False, mlb=mlb, encoder=encoder)
    
    # Split features and target
    x_train = processed_train.drop(columns=["churn"])
    y_train = processed_train["churn"]
    x_test = processed_test.drop(columns=["churn"])
    y_test = processed_test["churn"]
    
    # Define initial LightGBM parameters
    lgb_params = {
        "objective": "binary",
        "boosting_type": "gbdt",
        'n_estimators': 309,
        'learning_rate': 0.01716029728096218,
        'num_leaves': 22,
        'max_depth': 6,
        'min_child_samples': 10,
        'subsample': 0.737440646376928,
        'colsample_bytree': 0.9862597807809604,
        'reg_alpha': 8.985515005642144e-07,
        'reg_lambda': 1.00016444438518084528,
        "random_state": 42,
        "verbose": -1,
        "n_jobs": -1
    }
    
    # Cross-validation
    #print("Starting cross-validation...")
    #models, metrics = cross_validate_lgb(x_train, y_train, lgb_params)
    
    # Train final model on the full training set
    print("Training final model on full training data...")
    final_model = train_final_lgb(x_train, y_train, lgb_params)
    
    # Evaluate the final model on the test set
    y_pred = final_model.predict(x_test)
    y_pred_proba = final_model.predict_proba(x_test)[:, 1]
    print("Evaluation on test set:")
    print_all_metrics(y_test, y_pred, y_pred_proba)
    
    # Hyperparameter tuning with Optuna
    #print("Starting hyperparameter tuning with Optuna...")
    #best_params = run_optuna(x_train, y_train, n_trials=50)
    
    # Optionally retrain using the best hyperparameters and evaluate again
    #print("Retraining model with best hyperparameters...")
    #final_model_best = train_final_lgb(x_train, y_train, best_params)
    #y_pred_best = final_model_best.predict(x_test)
    #y_pred_proba_best = final_model_best.predict_proba(x_test)[:, 1]
    #print("Evaluation on test set with tuned hyperparameters:")
    #print_all_metrics(y_test, y_pred_best, y_pred_proba_best)
    
    # Plot feature importance
    print("Plotting feature importance...")
    plot_feature_importance(final_model, x_train.columns)
    
if __name__ == "__main__":
    main()
