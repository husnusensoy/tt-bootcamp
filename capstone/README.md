# Churn Prediction 

Telekomisyon bünyesindeki müşteri kaybını (churn) tahmin etmek için makine öğrenmesi modellerini kullanarak geliştirildi. Müşterilerin geçmiş verileri analiz edilerek, belirli özelliklere sahip müşterilerin ayrılma olasılıkları hesaplandı ve pazarlama ekibinin ilgisini çekebilecek görselleştirmeler oluşturuldu.

### İş Süreçleri

Veri Ön İşleme: Eksik verilerin doldurulması, aykırı değerlerin tespiti ve düzenlenmesi.

Özellik Mühendisliği: Kullanışlı değişkenler üretildi ve mevcut değişkenler dönüştürüldü.

Dengeleme (SMOTE): Dengesiz veri setinde azınlık sınıfı artırılarak daha dengeli bir model eğitimi sağlandı.

Model Eğitimi: LightGBM ve XGBoost algoritmaları kullanılarak churn tahminleme modeli eğitildi.

Performans Değerlendirmesi: ROC-AUC eğrisi, confusion matrix, accuracy, precision, recall gibi metrikler kullanılarak modelin başarısı ölçüldü.

Veri Görselleştirme: Pazarlama ekibine yönelik çeşitli analizler ve grafikler oluşturuldu.

### Kullandığım Kütüphaneler

*pandas
*numpy
*sklearn
*seaborn
*matplotlib
*xgboost
*imblearn.over_sampling 


### My Scores

AUC: 0.7306
Precision: 0.0270
Recall: 0.5932
F1-score: 0.0516
Confussion Matrix:
array([[622088, 236009],
       [  4491,   6548]])
