import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.metrics import (
    roc_auc_score, accuracy_score, precision_score, recall_score,
    balanced_accuracy_score, f1_score, roc_curve, confusion_matrix
)
import xgboost as xgb
import matplotlib.pyplot as plt
import seaborn as sns

def evaluate_metrics(y_true, y_pred, y_proba):
    auc = roc_auc_score(y_true, y_proba)
    accuracy = accuracy_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred)
    recall = recall_score(y_true, y_pred)
    balanced_acc = balanced_accuracy_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred)
    return auc, accuracy, precision, recall, balanced_acc, f1

def find_optimal_threshold(y_true, y_proba):
    fpr, tpr, thresholds = roc_curve(y_true, y_proba)
    gmeans = np.sqrt(tpr * (1 - fpr))
    idx = np.argmax(gmeans)
    return thresholds[idx]

# Çıktıları kaydedeceğimiz klasör
output_dir = "prepaid_results"
os.makedirs(output_dir, exist_ok=True)

# Veri yükleme (Prepaid dataset)
df = pd.read_parquet("../../../tt_data/processed/Prepaid.parquet")
df = df.drop(columns=["id"], errors='ignore')
print(df.columns)
# Özellik (X) ve hedef (y)
X = df.drop(columns=["churn"])
y = df["churn"]

# %85 Train - %15 Test (Stratify)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, 
    test_size=0.15, 
    random_state=42, 
    stratify=y
)

# XGBoost model
model = xgb.XGBClassifier(
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

# 5-Katlı CV
skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

fold_aucs, fold_accuracies, fold_precisions, fold_recalls, fold_balanced, fold_f1 = [], [], [], [], [], []
oof_probas = np.zeros(len(X_train))
oof_true = np.array(y_train)

for train_idx, val_idx in skf.split(X_train, y_train):
    X_tr, X_val = X_train.iloc[train_idx], X_train.iloc[val_idx]
    y_tr, y_val = y_train.iloc[train_idx], y_train.iloc[val_idx]

    model.fit(X_tr, y_tr)
    val_proba = model.predict_proba(X_val)[:, 1]
    val_pred = (val_proba >= 0.5).astype(int)

    auc, acc, prec, rec, bal_acc, f1 = evaluate_metrics(y_val, val_pred, val_proba)
    fold_aucs.append(auc)
    fold_accuracies.append(acc)
    fold_precisions.append(prec)
    fold_recalls.append(rec)
    fold_balanced.append(bal_acc)
    fold_f1.append(f1)

    oof_probas[val_idx] = val_proba

optimal_threshold = find_optimal_threshold(oof_true, oof_probas)

print(f"Validation (5-Fold Mean) - AUC: {np.mean(fold_aucs):.4f}, "
      f"Accuracy: {np.mean(fold_accuracies):.4f}, Precision: {np.mean(fold_precisions):.4f}, "
      f"Recall: {np.mean(fold_recalls):.4f}, Balanced Acc: {np.mean(fold_balanced):.4f}, "
      f"F1 Score: {np.mean(fold_f1):.4f}")
print(f"Optimal Threshold (from CV OOF): {optimal_threshold:.4f}")

# Final model (Tüm train verisi)
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

# Test tahminleri
test_proba = final_model.predict_proba(X_test)[:, 1]
test_pred = (test_proba >= optimal_threshold).astype(int)

test_auc, test_acc, test_prec, test_rec, test_bal_acc, test_f1 = evaluate_metrics(y_test, test_pred, test_proba)
print(f"Test - AUC: {test_auc:.4f}, Accuracy: {test_acc:.4f}, Precision: {test_prec:.4f}, "
      f"Recall: {test_rec:.4f}, Balanced Acc: {test_bal_acc:.4f}, F1 Score: {test_f1:.4f}")

# Feature importance
booster = final_model.get_booster()
raw_importances = booster.get_score(importance_type='gain')
total_gain = sum(raw_importances.values())

sorted_importances = sorted(raw_importances.items(), key=lambda x: x[1], reverse=True)
feature_names = [feat for feat, _ in sorted_importances[:9]]
feature_percents = [(val / total_gain) * 100 for _, val in sorted_importances[:9]]

plt.figure(figsize=(8, 6))
plt.barh(feature_names[::-1], feature_percents[::-1], color='navy')
plt.xlabel("Importance (%)")
plt.title("XGBoost Feature Importance (Top 9 by % Gain)")
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "prepaid_feature_importance.png"), dpi=300)
plt.close()

# Confusion Matrix (Test)
cm = confusion_matrix(y_test, test_pred)

fig, ax = plt.subplots(figsize=(4, 2))
ax.set_axis_off()
table = ax.table(
    cellText=[[str(cm[0,0]), str(cm[0,1])], [str(cm[1,0]), str(cm[1,1])]],
    rowLabels=["Actual No Churn", "Actual Churn"],
    colLabels=["Pred No Churn", "Pred Churn"],
    loc='center',
    cellLoc='center'
)
table.set_fontsize(14)
table.scale(1, 2)
plt.savefig(os.path.join(output_dir, "prepaid_test_confusion_matrix_table.png"), dpi=300, bbox_inches='tight')
plt.close()

# Test Probability Distribution
plt.figure(figsize=(8, 5))
sns.kdeplot(test_proba[y_test == 0], fill=True, color='blue', alpha=0.3, label='No Churn Probability Dist')
sns.kdeplot(test_proba[y_test == 1], fill=True, color='red', alpha=0.3, label='Churn Probability Dist')
plt.axvline(x=0.5, color='black', linestyle='--', label='Threshold=0.5')
plt.axvline(x=optimal_threshold, color='darkred', linestyle='-', label='Optimal Threshold')
plt.legend()
plt.title('Test Probability Distribution\n(Churn=Red, No Churn=Blue)')
plt.xlabel('Predicted Probability')
plt.ylabel('Density')
plt.savefig(os.path.join(output_dir, 'prepaid_test_threshold_comparison.png'), dpi=300, bbox_inches='tight')
plt.close()


# -- Metrikleri TXT dosyasına kaydetme ---

test_metrics_path = os.path.join(output_dir, "prepaid_test_metrics.txt")

with open(test_metrics_path, "w") as f:
    f.write("Test Metrics\n")
    f.write(f"AUC: {test_auc:.4f}\n")
    f.write(f"Accuracy: {test_acc:.4f}\n")
    f.write(f"Precision: {test_prec:.4f}\n")
    f.write(f"Recall: {test_rec:.4f}\n")
    f.write(f"Balanced Accuracy: {test_bal_acc:.4f}\n")
    f.write(f"F1 Score: {test_f1:.4f}\n")

print(f"Metrikler txt dosyasına kaydedildi: {test_metrics_path}")
