# README

## 1. Veri Ön İşleme (Preprocessing)

Verinin temizlenmesi ve modellenmeye hazır hale getirilmesi için aşağıdaki dosyalar kullanılmaktadır:

### `missing_value.py`

- Gereksiz kolonları kaldırarak veriyi temizler.
- Eksik değerlerin tespit edilmesi ve uygun bir şekilde doldurulmasını sağlar.

### `parquet_check.py`

- Parquet formatındaki veri dosyalarının bütünlük ve doğruluk testlerini gerçekleştirir.
- Veri tipleri ve kolon isimleri kontrol edilir.

### `group_by.py`

- JSON formatındaki veri dosyalarını okuyarak `service_type` değişkenine göre gruplar.
- Gruplanan veriler daha sonra ilgili segmentlere ayrılarak Parquet formatında saklanır.

---

## 2. XGBoost Model Geliştirme (Training & Evaluation)

Veri ön işleme tamamlandıktan sonra, her segment için XGBoost modeli eğitilir ve değerlendirilir.

### `XGBoost Model Geliştirme (broadband_xgboost.py, postpaid_xgboost.py, prepaid_xgboost.py)`

Bu aşamada, üç farklı müşteri segmenti için (Broadband, Postpaid, Prepaid) XGBoost modelleri eğitilir ve değerlendirilir. Model geliştirme süreci aşağıdaki adımları içerir:

- **5 Katlı Çapraz Doğrulama (5-Fold CV)** kullanılarak model performansı değerlendirilir.
- **Stratify** yöntemi ile veri ayrımı yapılarak, sınıf dengesizliği korunur.
- **Test verisi** üzerinde model performansı analiz edilerek doğrulama yapılır.
- **Feature importance hesaplanır ve görselleştirilir.**
- **Confusion Matrix** oluşturularak model tahmin performansı değerlendirilir.
- **Threshold Seçimi** için analiz yapılarak en uygun eşik değeri belirlenir.
- **Sonuçlar**, ilgili segmentlerin `broadband_results/`, `postpaid_results/`, `prepaid_results/` klasörlerinde saklanır.

---

## 3. Counterfactual Explanation

### `Counterfactual Analiz (broadband_counterfactual.py, postpaid_counterfactual.py, prepaid_counterfactual.py)`

Bu aşamada, her XGBoost modelinin belirlediği **threshold** değerinin üzerinde olup churn riski taşıyan en düşük 20 gözlem için counterfactual analizler gerçekleştirilir. Amaç, bu müşterilerin **churn olmamasını** sağlamak için en düşük maliyetli çözümü belirlemektir.

- **Actionable değişkenler** belirlenir, yani değiştirilebilir olan müşteri özellikleri seçilir.
- Her actionable değişken için **alt ve üst limitler** belirlenir.
- **Distance hesaplaması**, max-min farkı ile ters orantılı şekilde yapılır, böylece değişkenler arasında ölçek dengesi sağlanır.
- **DiCE (Diverse Counterfactual Explanations)** yöntemi kullanılarak churn riskini düşürecek **en az maliyetli 3 farklı öneri** üretilir.
- Eğer **Türk Telekom** için actionable belirlenen her bir feature için birim değişikliğin maliyeti hesaplanabilirse, bu analiz doğrudan **en düşük maliyetle churn olmaması için minimum stratejiyi belirleyebilir.**
- Sonuçlar ilgili segmentlerin `broadband_results/`, `postpaid_results/`, `prepaid_results/` klasörlerinde csv formatında saklanır.
