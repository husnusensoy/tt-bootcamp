import pandas as pd
import numpy as np
import os
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import roc_auc_score, accuracy_score, recall_score, precision_score, f1_score
import dice_ml
from dice_ml import Dice
from dice_ml.utils import helpers

########################################
# 1) Veri Yükleme ve Train-Test Ayrımı
########################################
THRESHOLD = 0.5428
RESULTS_DIR = "postpaid_results"
os.makedirs(RESULTS_DIR, exist_ok=True)

# **Yeni Actionable Değişkenler Güncellendi**
actionable_numeric = ["apps_count",
                      "satisfaction_score",
                      "data_usage",
                      "monthly_charge",
                      "customer_support_calls",
                      "avg_call_duration"]  # **YENİ: avg_call_duration artık actionable!**

# **Aşağıdaki değişkenler postpaid datasetinde var ama actionable değil**
non_actionable = ["avg_top_up_count", "call_drops"]

df = pd.read_parquet("../../../tt_data/processed/Postpaid.parquet")
df = df.drop(columns=["id"], errors='ignore')

X = df.drop(columns=["churn"])
y = df["churn"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.15,
    stratify=y,
    random_state=42
)

########################################
# 2) XGBoost Modeli Eğitme
########################################
final_model = xgb.XGBClassifier(
    objective="binary:logistic",
    scale_pos_weight=len(y_train[y_train == 0]) / len(y_train[y_train == 1]),
    use_label_encoder=False,
    eval_metric="auc",
    random_state=42,
    n_estimators=300,
    learning_rate=0.02,
    max_depth=6,
    subsample=0.85,
    colsample_bytree=0.85,
    gamma=0.3,
    reg_alpha=0.3,
    reg_lambda=1.5
)
final_model.fit(X_train, y_train)

########################################
# 3) Model Performans Değerlendirme (Test Set)
########################################
test_proba = final_model.predict_proba(X_test)[:, 1]
test_pred = (test_proba >= THRESHOLD).astype(int)

auc = roc_auc_score(y_test, test_proba)
accuracy = accuracy_score(y_test, test_pred)
recall = recall_score(y_test, test_pred)
precision = precision_score(y_test, test_pred)
f1 = f1_score(y_test, test_pred)

print("\n=== Postpaid Test Set Model Performansı ===")
print(f"AUC Score       : {auc:.4f}")
print(f"Accuracy        : {accuracy:.4f}")
print(f"Recall          : {recall:.4f}")
print(f"Precision       : {precision:.4f}")
print(f"F1 Score        : {f1:.4f}")

########################################
# 4) THRESHOLD Üzerinde Olan En Düşük 20 Kayıt Seçimi
########################################
above_threshold_indices = np.where(test_pred == 1)[0]

if len(above_threshold_indices) < 20:
    print("Threshold'u aşan yeterli sayıda veri bulunamadı.")
    exit()

sorted_indices = np.argsort(test_proba[above_threshold_indices])[:20]  # En düşük churn olasılığı olan 20 kayıt
selected_indices = above_threshold_indices[sorted_indices]

print(f"Seçilen 20 gözlem: {selected_indices}")

x_originals = X_test.iloc[selected_indices].copy()

########################################
# 5) Değişken Ağırlıklarını (Weights) Hesaplama
########################################
feature_ranges = {}
permitted_range = {}

for col in actionable_numeric:
    min_val = X_train[col].min()
    max_val = X_train[col].max()
    feature_ranges[col] = max_val - min_val
    permitted_range[col] = [min_val, max_val]  # **Her değişkenin min-max aralığını belirle**

# Ağırlık hesaplaması (max-min'e ters orantılı)
feature_weights = {col: 1 / feature_ranges[col] if feature_ranges[col] != 0 else 1 for col in actionable_numeric}

########################################
# 6) DiCE ile Counterfactual Açıklamalar
########################################
dice_data = dice_ml.Data(
    dataframe=pd.concat([X_train, y_train], axis=1),
    continuous_features=actionable_numeric,
    outcome_name="churn"
)

dice_model = dice_ml.Model(model=final_model, backend="sklearn", model_type="classifier")
dice_exp = Dice(dice_data, dice_model)

########################################
# 7) Counterfactual Önerilerini Üretme
########################################
all_results = []

for i, idx in enumerate(selected_indices):
    print(f"\nProcessing index {idx} ({i+1}/20)")

    x_instance = x_originals.iloc[[i]]
    
    # **Counterfactual üretme (3 öneri)**
    cf_examples = dice_exp.generate_counterfactuals(
        x_instance,
        total_CFs=3,  # **Her gözlem için 3 counterfactual**
        desired_class=0,
        features_to_vary=actionable_numeric,
        proximity_weight=feature_weights,
        permitted_range=permitted_range
    )

    # **Orijinal Gözlemi Ekleyelim**
    original_record = x_instance.copy()
    original_record["Type"] = "Actual"
    all_results.append(original_record)

    # **Counterfactualları Ekleyelim**
    cf_df = cf_examples.cf_examples_list[0].final_cfs_df.copy()
    cf_df["Type"] = "Counterfactual"
    all_results.append(cf_df)

########################################
# 8) Sonuçları CSV Olarak Kaydetme
########################################
final_df = pd.concat(all_results, ignore_index=True)

csv_path = os.path.join(RESULTS_DIR, "postpaid_counterfactual_results.csv")
final_df.to_csv(csv_path, index=False)

print(f"\n=== Counterfactual Sonuçları Kaydedildi: {csv_path} ===")
