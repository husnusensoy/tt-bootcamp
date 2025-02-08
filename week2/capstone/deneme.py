import duckdb
db_path = "../Data/capstone.db"
with duckdb.connect(db_path) as con:
    con.execute("create table if not exists churn as select * from read_json('../Data/*.jsonl')")
with duckdb.connect(db_path) as con:
    con.sql("select * from churn limit 5").show()
with duckdb.connect(db_path) as con:
    con.sql("select count(Distinct COLUMNS(*) ) from churn").show()
#apps = ['İzleGo', 'RitimGo', 'CüzdanX', 'HızlıPazar', 'Konuşalım']
query = f"""
create table if not exists unpacked_app as (SELECT 
    *,
    (CASE WHEN 'İzleGo' = ANY(apps) THEN 1 ELSE 0 END) AS İzleGo,
    (CASE WHEN 'RitimGo' = ANY(apps) THEN 1 ELSE 0 END) AS RitimGo,
    (CASE WHEN 'CüzdanX' = ANY(apps) THEN 1 ELSE 0 END) AS CüzdanX,
    (CASE WHEN 'HızlıPazar' = ANY(apps) THEN 1 ELSE 0 END) AS HızlıPazar,
    (CASE WHEN 'Konuşalım' = ANY(apps) THEN 1 ELSE 0 END) AS Konuşalım
FROM churn);

"""
with duckdb.connect(db_path) as con:
    con.execute(query)
with duckdb.connect(db_path) as con:
    con.sql("select * from unpacked_app limit 5").show()
con = duckdb.connect(db_path)
query = """
select distinct service_type from unpacked_app

"""
con.sql(query).show()
con.sql("select * from unpacked_app limit 5").show()
con.execute("alter table unpacked_app drop column if exists apps")
con.sql("select * from unpacked_app limit 5").show()
con.sql("select count(*) from unpacked_app where service_type is null")
con.sql( 'select distinct service_type from unpacked_app')
query = """
CREATE TABLE IF NOT EXISTS encoded_service_type AS (
    SELECT 
        *,
        (CASE WHEN service_type = 'Prepaid' THEN 1 ELSE 0 END) AS Prepaid,
        (CASE WHEN service_type = 'Broadband' THEN 1 ELSE 0 END) AS Broadband,
        (CASE WHEN service_type = 'Postpaid' THEN 1 ELSE 0 END) AS Postpaid
    FROM unpacked_app
);
"""
con.sql(query)
con.sql("select * from encoded_service_type limit 5").show()
query = """
ALTER table encoded_service_type
ALTER COLUMN auto_payment TYPE INT
USING CASE WHEN auto_payment THEN 1 ELSE 0 END;

ALTER table encoded_service_type
ALTER COLUMN churn TYPE INT
USING CASE WHEN churn THEN 1 ELSE 0 END;
"""
con.execute(query)
con.sql("select * from encoded_service_type limit 5")
con.sql("select count(*) from encoded_service_type where overdue_payments is null")
con.sql("select overdue_payments , count(overdue_payments ) from encoded_service_type group by overdue_payments ")
df = con.sql("select * from encoded_service_type").df()
con.execute("drop table churn")
con.execute("drop table unpacked_app")
con.execute("drop table encoded_service_type")

df.head()
df["id"] = df["id"].astype(str)
df.isna().sum()
df.loc[df["call_drops"].isna(),["call_drops", "roaming_usage", "avg_call_duration","Broadband"]]["Broadband"].value_counts()
df.loc[df["Broadband"] == 1,["call_drops", "roaming_usage", "avg_call_duration"] ].notna().sum().sum() 
df.loc[df["Broadband"] == 1,["call_drops", "roaming_usage", "avg_call_duration"] ] = 0
df.isna().sum()
def analyze_data(dataframe, cat_th=10, car_th=20):
    """
    It gives the names of categorical, numerical and categorical but cardinal variables in the data set. It also performs incomplete data analysis.
    Parameters
    ------
        dataframe: dataframe
            The dataframe from which variable names are to be retrieved
        cat_th: int, optional
            Class threshold value for numeric but categorical variables
        car_th: int, optional
            Class threshold for categorical but cardinal variables

    Returns
    ------
        cat_cols: list
            Categorical variable list
        num_cols: list
            Numerik değişken listesi
        cat_but_car: list
            Categorical view cardinal variable list
    """
    cat_cols = [col for col in dataframe.columns if dataframe[col].dtype == "O"]
    num_cols = [col for col in dataframe.columns if dataframe[col].dtype != "O"]

    num_but_cat = [col for col in num_cols if dataframe[col].nunique() < cat_th]
    cat_but_car = [col for col in cat_cols if dataframe[col].nunique() > car_th]

    cat_cols = [col for col in cat_cols if col not in cat_but_car]
    num_cols = [col for col in num_cols if col not in num_but_cat]

    cat_cols = cat_cols + num_but_cat
    
    print(f"Number of Observations: {dataframe.shape[0]}")
    print(f"Number of Variables: {dataframe.shape[1]}")
    print(f'Cat cols: {len(cat_cols)}, Num cols: {len(num_cols)}, Cat but car cols: {len(cat_but_car)}')

    return cat_cols, num_cols, cat_but_car
cat_cols, num_cols, cat_but_car = analyze_data(df)
cat_cols
df[cat_cols].nunique()
df[num_cols].isna().sum()
features_to_impute = ["tenure", "avg_call_duration", "data_usage", "monthly_charge"]

for feature in features_to_impute:
    if feature == "monthly_charge":
        df[feature] = df[feature].fillna(
            df.groupby(["age", "service_type"])[feature].transform("median")
        ).fillna(df[feature].median())
    else:
        df[feature] = df[feature].fillna(
            df.groupby(["age", "service_type"])[feature].transform("mean")
        ).fillna(df[feature].mean())
df.isna().sum()

with duckdb.connect(db_path) as con:
    con.execute("create table if not exists preprocessed_churn as select * from df")
con.close()



import duckdb
import pandas as pd
import numpy as np
with duckdb.connect("../Data/capstone.db") as con:
    df = con.sql("select * from preprocessed_churn").df()
df.head()
df["tenure"].plot.hist()
df["tenure/age"] = df["tenure"] / (df["age"]*12) 
df["age-tenure"] = (df["age"]*12) - df["tenure"]
df["tenure/age"].plot.hist()
df["age-tenure"].plot.hist()
(df["age-tenure"] // 12).min()
df = df[df["age-tenure"] > (18*12)] # outlier olarak değerlendireceğim 18 yaşından sonra müşteri olunabilir ancak veride -7 yaşında müşteri olmuş gibi görünen kişiler var
df["age-tenure"].plot.hist()
df["tenure/age"].plot.hist()
df["tenure"].describe()[["min", "25%","50%", "75%", "max"]]
bins = [18, 25, 35, 45, 55, 65, np.inf]
labels = ['18-24', '25-34', '35-44', '45-54', '55-64', '65+']
df['age_group'] = pd.cut(df['age'], bins=bins, labels=labels, right=False)
df['tenure_years'] = df['tenure'] / 12
df['tenure_group'] = pd.cut(df['tenure'], 
                           bins=[0, 47, 106, 188, 300, 500, np.inf],
                           labels=['0, 47', '48-106','107-188', '189-300', '301-500', '501-inf'],
                           right=False)
df['tenure_squared'] = df['tenure'] ** 2
df['data_efficiency'] = df['data_usage'] / (df['monthly_charge'] + 1e-6)  # +1e-6 division by zero koruması
df['has_roaming'] = df['roaming_usage'].apply(lambda x: 1 if x > 0 else 0)
df['overdue_frequency'] = df['overdue_payments'] / (df['tenure'] + 1e-6)
df['call_drop_rate'] = df['call_drops'] / (df['tenure'] + 1e-6)
df['support_call_rate'] = df['customer_support_calls'] / (df['tenure'] + 1e-6)
for service in df['service_type'].unique():
    df[f'{service}_data_interaction'] = df[service] * df['data_usage']
df['auto_payment_overdue'] = df['auto_payment'] * df['overdue_payments']
df['satisfaction_support_interaction'] = df['satisfaction_score'] * df['customer_support_calls']
df['any_overdue'] = df['overdue_payments'].apply(lambda x: 1 if x > 0 else 0)
df['high_cost'] = np.where(df['monthly_charge'] > df['monthly_charge'].quantile(0.75), 1, 0)
median_calls = df['customer_support_calls'].median()
df['low_satisfaction_high_support'] = np.where((df['satisfaction_score'] < 3) & 
                                              (df['customer_support_calls'] > median_calls), 1, 0)
df['is_prepaid'] = df['service_type'].apply(lambda x: 1 if x == 'Prepaid' else 0)
df['prepaid_top_ups'] = df['is_prepaid'] * df['avg_top_up_count']
df['voice_data_ratio'] = df['avg_call_duration'] / (df['data_usage'] + 1)
df['age_squared'] = df['age'] ** 2
tenure_dummies  = pd.get_dummies(df["tenure_group"])
age_dummies  = pd.get_dummies(df["age_group"])
df = pd.concat([df, tenure_dummies, age_dummies], axis=1)
df.info()
path = "../Data/capstone_final.csv"
df.to_csv(path)
import duckdb

import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
import optuna
from sklearn.metrics import confusion_matrix, average_precision_score, classification_report, fbeta_score

from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from xgboost import XGBRegressor
import lightgbm as lgb

def find_threshold(y_pred_final, target_rate=0.01, tolerance=0.00001, max_iter=1000):    
    left = float(y_pred_final.min())
    right = float(y_pred_final.max())
    
    iteration = 0
    best_threshold = None
    best_diff = float('inf')
    
    while iteration < max_iter:
        mid = (left + right) / 2
        current_rate = (y_pred_final > mid).sum() / len(y_pred_final)
        diff = abs(current_rate - target_rate)
        
        if diff < best_diff:
            best_threshold = mid
            best_diff = diff
        
        if diff <= tolerance:
            return mid
        
        # Binary search
        if current_rate > target_rate:
            left = mid
        else:
            right = mid
            
        iteration += 1
        
        if abs(right - left) < tolerance:
            return best_threshold
    
    return best_threshold
df = pd.read_csv("../Data/capstone_final.csv")
df.info()
df.head()


import re
import pandas as pd

def clean_feature_names(df):
    """
    Clean DataFrame column names to be compatible with LightGBM JSON format.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Input DataFrame with potentially problematic column names
    
    Returns:
    --------
    pandas.DataFrame
        DataFrame with cleaned column names and a mapping of old to new names
    """
    # Create a copy of the DataFrame
    df_clean = df.copy()
    
    # Dictionary to store original and cleaned column names
    name_mapping = {}
    
    for col in df.columns:
        # Replace special characters with underscore
        cleaned_name = re.sub(r'[^\w\s]', '_', str(col))
        # Replace spaces with underscore
        cleaned_name = cleaned_name.replace(' ', '_')
        # Ensure the name starts with a letter or underscore
        if not cleaned_name[0].isalpha() and cleaned_name[0] != '_':
            cleaned_name = 'f_' + cleaned_name
        # Remove multiple consecutive underscores
        cleaned_name = re.sub(r'_+', '_', cleaned_name)
        # Remove trailing underscores
        cleaned_name = cleaned_name.rstrip('_')
        
        name_mapping[col] = cleaned_name
        
    # Rename the columns
    df_clean.columns = [name_mapping[col] for col in df.columns]
    
    return df_clean, name_mapping
df, name_mapping = clean_feature_names(df)
X = df.drop(axis=1, columns=["id", "churn", "service_type", "age_group", "tenure_group"])
y = df["churn"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)
from imblearn.over_sampling import SMOTE

smote = SMOTE(random_state=42)
X_resampled, y_resampled = smote.fit_resample(X_train, y_train)

def objective(trial):
    params = {
        "objective": "binary",
        "metric": "binary_error",
        "boosting_type": "gbdt",
        "lambda_l1": trial.suggest_loguniform("lambda_l1", 1e-8, 10.0),
        "lambda_l2": trial.suggest_loguniform("lambda_l2", 1e-8, 10.0),
        "num_leaves": trial.suggest_int("num_leaves", 2, 256),
        "feature_fraction": trial.suggest_uniform("feature_fraction", 0.4, 1.0),
        "bagging_fraction": trial.suggest_uniform("bagging_fraction", 0.4, 1.0),
        "bagging_freq": trial.suggest_int("bagging_freq", 1, 7),
        "min_child_samples": trial.suggest_int("min_child_samples", 5, 100),
    }
    
    # Modeli Eğitme
    dtrain = lgb.Dataset(X_resampled, label=y_resampled)
    gbm = lgb.train(params, dtrain, valid_sets=[dtrain], num_boost_round=100)
    
    # Test Seti Üzerinde Tahmin Yapma
    y_pred = gbm.predict(X_test)
    y_pred = pd.Series(y_pred > find_threshold(y_pred)).astype(int)
    return fbeta_score(y_test, y_pred,beta=2)
#study = optuna.create_study(direction="maximize")
#study.optimize(objective, n_trials=50,show_progress_bar=True)
#print("En İyi Parametreler:", study.best_params)
# lgb 
best_params = {'lambda_l1': 9.220621228154233, 'lambda_l2': 3.406326025123661e-05, 'num_leaves': 123, 'feature_fraction': 0.7741812226877789, 'bagging_fraction': 0.5694104742723753, 'bagging_freq': 6, 'min_child_samples': 20}
# Optimum Parametrelerle Model Eğitme
#best_params = study.best_params
best_params["objective"] = "binary"
best_params["metric"] = "binary_error"

final_model = lgb.train(best_params, lgb.Dataset(X_train, label=y_train), num_boost_round=100)

# Test Verisinde Son Modelin Başarısı
y_pred_final = final_model.predict(X_test)
average_precision_score(y_test,y_pred_final)
y_pred_bool = pd.Series(y_pred_final > find_threshold(y_pred_final)).astype(int)
confusion_matrix(y_test,y_pred_bool)
print(classification_report(y_test, y_pred_bool))
