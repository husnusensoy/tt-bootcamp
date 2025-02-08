Churn Tahminleme Projesi

Bu proje, müşteri kaybını (churn) tahmin etmek için makine öğrenmesi modellerini kullanarak geliştirildi. Müşterilerin geçmiş verileri analiz edilerek, belirli özelliklere sahip müşterilerin ayrılma olasılıkları hesaplandı ve pazarlama ekibinin ilgisini çekebilecek görselleştirmeler oluşturuldu.

🚀 Proje İçeriği

Veri Ön İşleme: Eksik verilerin doldurulması, aykırı değerlerin tespiti ve düzenlenmesi.

Özellik Mühendisliği: Kullanışlı değişkenler üretildi ve mevcut değişkenler dönüştürüldü.

Dengeleme (SMOTE): Dengesiz veri setinde azınlık sınıfı artırılarak daha dengeli bir model eğitimi sağlandı.

Model Eğitimi: LightGBM ve XGBoost algoritmaları kullanılarak churn tahminleme modeli eğitildi.

Performans Değerlendirmesi: ROC-AUC eğrisi, confusion matrix, accuracy, precision, recall gibi metrikler kullanılarak modelin başarısı ölçüldü.

Veri Görselleştirme: Pazarlama ekibine yönelik çeşitli analizler ve grafikler oluşturuldu.

📂 Kullanılan Kütüphaneler

Bu projede aşağıdaki Python kütüphaneleri kullanılmıştır:

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, roc_curve, auc
from imblearn.over_sampling import SMOTE

📊 Veri Seti ve Değişkenler

Bu proje için kullanılan veri seti aşağıdaki değişkenleri içermektedir:

age: Müşteri yaşı

app_count: Kullanılan uygulama sayısı

auto_payment: Otomatik ödeme durumu

avg_call_duration: Ortalama çağrı süresi

avg_top_up_count: Ortalama bakiye yükleme sayısı

call_drops: Çağrı düşme oranı

customer_support_calls: Müşteri hizmetleri çağrı sayısı

data_usage: Veri kullanımı (MB)

monthly_charge: Aylık ücret

overdue_payments: Gecikmiş ödeme sayısı

roaming_usage: Dolaşım kullanımı

satisfaction_level: Müşteri memnuniyeti düzeyi

satisfaction_score: Memnuniyet skoru

service_type_Broadband: Genişbant hizmeti kullanımı (0 veya 1)

service_type_Postpaid: Faturalı hat kullanımı (0 veya 1)

service_type_Prepaid: Ön ödemeli hat kullanımı (0 veya 1)

start_age: Hizmeti kullanmaya başlama yaşı

tenure: Abonelik süresi (ay)

total_usage: Toplam kullanım

usage_intensity: Kullanım yoğunluğu

churn_probability: Churn olasılığı

churn: Müşteri kaybı durumu (0: Kalmış, 1: Ayrılmış)

🏆 Model Eğitimi

Veri seti eğitim ve test olarak ikiye ayrıldı ve farklı algoritmalar ile eğitildi:

X = df.drop(columns=['churn'])
y = df['churn']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# SMOTE Uygulaması
smote = SMOTE(sampling_strategy=0.5, random_state=42)
X_train_resampled, y_train_resampled = smote.fit_resample(X_train, y_train)

# LightGBM Modeli
lgbm = LGBMClassifier()
lgbm.fit(X_train_resampled, y_train_resampled)
y_pred = lgbm.predict(X_test)

# Model Performansı
print(classification_report(y_test, y_pred))

# ROC-AUC Eğrisi

fpr, tpr, _ = roc_curve(y_test, lgbm.predict_proba(X_test)[:,1])
roc_auc = auc(fpr, tpr)

plt.figure(figsize=(8,6))
plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (AUC = {roc_auc:.2f})')
plt.plot([0, 1], [0, 1], color='navy', linestyle='--')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC - AUC Curve')
plt.legend(loc="lower right")
plt.show()

# Kullandığım Kütüphaneler

- pandas
- numpy
- seaborn
- matplotlib
- sklearn
- xgboost
- lightgbm
- imblearn.over_sampling

# My Scores

AUC: 0.7306
Precision: 0.0270
Recall: 0.5932
F1-score: 0.0516
Confussion Matrix:
array([[622088, 236009],
       [  4491,   6548]])