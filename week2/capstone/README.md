# Customer Churn Prediction

This repository contains a machine learning pipeline for predicting customer churn. The project includes data loading, exploratory data analysis (EDA), preprocessing, feature engineering, model training, evaluation, and hyperparameter tuning using LightGBM and other boosting algorithms.

## Project Structure

- **Data Loading**:  
  Reads data from CSV files (`data/train.csv` and `data/new_test.csv`).

- **Exploratory Data Analysis (EDA)**:  
  Performs initial data inspection by checking for missing values and visualizing distributions (e.g., histograms based on churn status).

- **Preprocessing & Feature Engineering**:  
  - Fills missing values and handles edge cases (e.g., when call duration is missing).  
  - Applies feature extraction (e.g., calculating ratios such as `overdue_payment_ratio`, `lifetime_value`, and `call_drop_ratio`).  
  - Encodes categorical variables using MultiLabelBinarizer and OneHotEncoder.  

- **Handling Class Imbalance**:  
  Implements undersampling (with a majority multiplier of 5) and includes a function for oversampling using SMOTE.

- **Model Training and Evaluation**:  
  - Uses LightGBM as the main classifier.  
  - Performs cross-validation using StratifiedKFold (with 5 folds) to evaluate model performance on undersampled data.  
  - Evaluates performance using Accuracy, Precision, Recall, F1 Score, ROC AUC, and a confusion matrix.  

- **Hyperparameter Tuning**:  
  Uses Optuna to tune LightGBM hyperparameters by maximizing the average F1 score across folds.

- **Feature Importance**:  
  Visualizes feature importances with a horizontal bar chart.

## Dependencies

Ensure you have Python 3.x installed along with the following libraries:

- numpy
- pandas
- scikit-learn
- matplotlib
- seaborn
- lightgbm
- catboost
- xgboost
- optuna
- imbalanced-learn

You can install the required packages using pip:

```bash
pip install numpy pandas scikit-learn matplotlib seaborn lightgbm catboost xgboost optuna imbalanced-learn

My score on each metric:
Accuracy: 0.9752305
Precision: 0.09028526262844004
Recall: 0.09401069918820845
F1 Score: 0.09211032713277742
auc: 0.7988360693082897
Confussion matrix:
[[1947948   25321]
[  24218    2513]]