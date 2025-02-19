# src/preprocessing.py
import numpy as np
import pandas as pd
import ast
from sklearn.preprocessing import MultiLabelBinarizer, OneHotEncoder
from sklearn.utils import resample
from imblearn.over_sampling import SMOTE

def filling_null_values(df):
    # Service Type:
    mask = (df['service_type'] == 'Prepaid') & (df['auto_payment'].isna())
    df.loc[mask, 'auto_payment'] = 0
    df["auto_payment"].fillna(0, inplace=True)
    
    # For rows with zero customer support calls, set avg_call_duration to 0 if missing
    mask = (df['customer_support_calls'] == 0) & (df['avg_call_duration'].isna())
    df.loc[mask, 'avg_call_duration'] = 0
    
    # Fill 'tenure' and 'monthly_charge' with their median values
    df['tenure'].fillna(df['tenure'].median(), inplace=True)
    df['monthly_charge'].fillna(df['monthly_charge'].median(), inplace=True)
    
    # Fill selected columns using a uniform distribution within the observed range
    for col in ['avg_call_duration', 'data_usage', 'roaming_usage', 'call_drops']:
        min_val = df[col].min()
        max_val = df[col].max()
        df[col] = df[col].apply(lambda x: np.random.uniform(min_val, max_val) if pd.isna(x) else x)
    return df

def feature_extraction(df):
    df = df.copy()
    eps = 1e-5  # To avoid division by zero
    df['overdue_payment_ratio'] = df['overdue_payments'] / (df['tenure'] + eps)


    df['total_call_duration'] = df['avg_call_duration'] * df['customer_support_calls']
    df['lifetime_value'] = df['monthly_charge'] * df['tenure']
    df['age_tenure_ratio'] = df['tenure'] / (df['age'] + eps)
    df['satisfaction_support'] = df['satisfaction_score'] / (df['customer_support_calls'] + eps)
    df['call_drop_ratio'] = np.where(
        df['customer_support_calls'] != 0,
        df['call_drops'] / df['customer_support_calls'],
        0
    )
    # If the app columns exist, compute total apps used
    app_columns = ['İzleGo', 'RitimGo', 'CüzdanX', 'HızlıPazar', 'Konuşalım']
    if all(col in df.columns for col in app_columns):
        df['total_apps_used'] = df[app_columns].sum(axis=1)
    return df

def preprocess(df, train=True, mlb=None, encoder=None):
    """
    Preprocess the dataframe by:
      - Dropping the id column.
      - Filling missing values.
      - Converting the "apps" column from a string to a list.
      - One-hot encoding the "service_type" column and multi-label binarizing the "apps" column.
      - Performing feature extraction.
    """
    df = df.drop(columns=["id"], axis=1)
    df = filling_null_values(df)
    
    # Convert string representation of lists to actual lists.
    df['apps'] = df['apps'].apply(ast.literal_eval)
    
    if train:
        mlb = MultiLabelBinarizer()
        one_hot_apps = mlb.fit_transform(df['apps'])
        df_onehot = pd.DataFrame(one_hot_apps, columns=mlb.classes_, index=df.index)
        df_encoded = df.join(df_onehot)
        
        encoder = OneHotEncoder(sparse=False)
        one_hot_encoded = encoder.fit_transform(df_encoded[['service_type']])
        df_one_hot_new = pd.DataFrame(one_hot_encoded, columns=encoder.categories_[0], index=df_encoded.index)
        df_encoded_new = pd.concat([df_encoded, df_one_hot_new], axis=1)
    else:
        one_hot_apps = mlb.transform(df['apps'])
        df_onehot = pd.DataFrame(one_hot_apps, columns=mlb.classes_, index=df.index)
        df_encoded = df.join(df_onehot)
        
        one_hot_encoded = encoder.transform(df_encoded[['service_type']])
        df_one_hot_new = pd.DataFrame(one_hot_encoded, columns=encoder.categories_[0], index=df_encoded.index)
        df_encoded_new = pd.concat([df_encoded, df_one_hot_new], axis=1)
    
    df_encoded_new = df_encoded_new.drop(columns=["service_type", "apps"], axis=1)
    df_final = feature_extraction(df_encoded_new)
    return df_final, mlb, encoder

def undersample_data(X, y, majority_multiplier=5, random_state=42):
    """
    Undersample the majority classes.
    """
    train_data = X.copy()
    train_data['target'] = y
    target_counts = train_data['target'].value_counts()
    minority_class = target_counts.idxmin()
    minority_count = target_counts.min()

    desired_counts = {}
    for cls, count in target_counts.items():
        desired_counts[cls] = minority_count if cls == minority_class else majority_multiplier * minority_count

    resampled_list = []
    for cls in train_data['target'].unique():
        cls_data = train_data[train_data['target'] == cls]
        n_samples = min(desired_counts[cls], len(cls_data))
        cls_data_downsampled = resample(cls_data, replace=False, n_samples=n_samples, random_state=random_state)
        resampled_list.append(cls_data_downsampled)
    
    undersampled_data = pd.concat(resampled_list).sample(frac=1, random_state=random_state).reset_index(drop=True)
    X_res = undersampled_data.drop(columns=['target'])
    y_res = undersampled_data['target']
    return X_res, y_res

def oversample_data(X, y, random_state=42):
    """
    Oversample the minority class using SMOTE.
    """
    smote = SMOTE(random_state=random_state)
    X_res, y_res = smote.fit_resample(X, y)
    return X_res, y_res
