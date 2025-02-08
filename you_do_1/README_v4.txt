
# 📚 You-do README Dosyası

Bu proje, film tavsiye sistemi ve veri analizi işlemleri üzerine geliştirilmiş Python betiklerinden oluşmaktadır. Aşağıda, projedeki her dosyanın kısa açıklaması bulunmaktadır.

## 📂 Dosya Yapısı

### 1. **adding_movie_year.py**
- **Açıklama:** `movie_avg_ratings.csv` dosyasına her film için yayın yılı (`Year`) ve o yıl ile en eski değerlendirme tarihi arasındaki farkı (`Year_Diff`) ekler.

### 2. **conf_interval.py**
- **Açıklama:** `movie_avg_ratings_with_quantiles.csv` dosyasındaki filmler için %95 güven aralıklarını hesaplar ve sonuçları `movie_with_confidence_intervals.csv` dosyasına kaydeder.

### 3. **cross_data.py**
- **Açıklama:** Müşteri puanlarını beş eşit dilime (quantile) ayırır ve her dilimdeki müşteri sayısını filmler için frekans olarak hesaplar. Sonuçları `movie_avg_ratings_with_quantiles.csv` dosyasına kaydeder.

### 4. **eda.py**
- **Açıklama:** Müşteri değerlendirme verilerini analiz eder. Ortalama puan, izlenme sayısı, tarih farkları gibi değişkenler için histogramlar ve çizgi grafikleri oluşturur, sonuçları `plots` klasörüne kaydeder.

### 5. **eda2.py**
- **Açıklama:** Müşteri değerlendirme verileriyle ilgili ek görselleştirmeler oluşturur. Ortalama puan, izlenme sayısı ve tarih farklılıkları gibi metrikler için histogramlar ve çizgi grafikleri hazırlar, sonuçları `plots2` klasörüne kaydeder.

### 6. **README.txt**
- **Açıklama:** Bu dosya, projedeki tüm betiklerin işlevlerini açıklamaktadır.

### 7. **soru1.py**
- **Açıklama:** `Watch_Count` değeri 1000'den büyük olan filmleri filtreler. Farklı müşteri dilimlerine (quantile) göre ağırlıklandırılmış puanlar hesaplar ve en yüksek skora sahip ilk 30 filmi sıralayarak `soru1.csv` dosyasına kaydeder.

### 8. **soru1_cozum2.py**
- **Açıklama:** Filmleri %95 güven aralığının alt sınırına göre sıralar, en yüksek skora sahip ilk 30 filmi seçer ve film başlıklarını ekleyerek `soru1_cozum2.csv` dosyasına kaydeder.

### 9. **soru2.py**
- **Açıklama:** Kullanıcıları ortalama puanlarına göre %20'lik dilimlere (quantile) ayırır. En az 10 film izlemiş rastgele bir kullanıcı seçilerek, kullanıcının bulunduğu dilimdeki en yüksek skora sahip 30 film önerilir. Öneriler `soru2.csv` dosyasına kaydedilir.

### 10. **soru2_cozum2.py**
- **Açıklama:** **DuckDB ve Jinja2 kullanılarak oluşturulmuş film öneri sistemi**. Bu kod, büyük veri kümeleriyle verimli çalışmak için DuckDB veritabanını kullanır. Kullanıcının izlediği filmleri analiz ederek benzer kullanıcıları tespit eder ve bu kullanıcıların beğendiği, ancak hedef kullanıcının henüz izlemediği filmleri önerir. **Jinja2 ile dinamik SQL sorguları oluşturulur**, ardından **Bayesian Ortalama (Bayesian Average)** yöntemiyle en iyi 30 film önerisi sıralanır. Bu yöntem, izlenme sayısı az olan filmler için belirsizliği azaltarak daha güvenilir öneriler yapılmasını sağlar. Bu, projede DuckDB ve Jinja2'nin birlikte kullanıldığı tek çözümdür.

### 11. **soru3.py**
- **Açıklama:** İki filmi karşılaştırmak için ağırlıklı skor hesaplaması yapar. Quantile frekansları ve ortalama puanlar dikkate alınarak ağırlıklı skor belirlenir. Daha düşük skora sahip film, öneri listesinden çıkarılması gereken film olarak belirlenir.

### 12. **soru3_cozum2.py**
- **Açıklama:** İki filmi karşılaştırarak %95 güven aralığının alt sınırına (CI_Lower_95) göre hangisinin daha güvenilir olduğunu belirler. Daha düşük CI_Lower_95 değerine sahip film öneri listesinden çıkarılması gereken film olarak işaretlenir.

### 13. **write_movie_avg_data.py**
- **Açıklama:** `rating_1.txt`, `rating_2.txt`, `rating_3.txt`, `rating_4.txt` dosyalarındaki film değerlendirme verilerini işleyerek her film için ortalama puan (`Avg_Rating`), izlenme sayısı (`Watch_Count`), standart sapma (`Std_Dev`), en erken ve en geç izlenme tarihleri (`Min_Date`, `Max_Date`) ile tarih farkını (`Date_Diff`) hesaplar. Sonuçları `movie_avg_ratings.csv` dosyasına kaydeder.

### 14. **write_user_avg_data.py**
- **Açıklama:** Müşteri değerlendirme verilerini işleyerek her kullanıcı için ortalama puan (`Avg_Rating`), izlenme sayısı (`Watch_Count`) ve kullanıcının puanlama davranışını temsil eden %20'lik dilimlere (quantile) ayırır. Bu analiz, müşteri bazlı film önerileri yapılmasına olanak sağlar. Sonuçlar `customer_avg_ratings.csv` dosyasına kaydedilir.

---

## ⏳ Daha Fazla Zamanım Olsaydı Yapacaklarım

- **Assert Kullanımının Artırılması:** Kodda veri doğrulama süreçlerini daha güvenilir hale getirmek için daha fazla `assert` ifadesi eklerdim.
- **Pathlib Kullanımı:** Manuel yol tanımlamaları yerine `pathlib` kütüphanesini kullanarak daha temiz ve platformdan bağımsız dosya yolu yönetimi sağlardım.
- **Kod Hakimiyetinin Güçlendirilmesi:** ChatGPT'den alınan destek nedeniyle bazı kodlarda hakimiyetimin düşük olduğunu hissediyorum. Daha fazla zamanım olsaydı, tüm kodları baştan inceleyerek tam anlamıyla kavrardım.
- **DuckDB ve Jinja Kullanımı:** Tüm kodları DuckDB ve Jinja2 formatında yeniden yazarak veri işlemlerini daha verimli ve optimize hale getirirdim.
- **Bayesian Teorik Bilgi Artırımı:** Bayesian yöntemleri daha derinlemesine anlamak için teorik bilgilerimi geliştirir ve tavsiye algoritmalarını daha sağlam temellere oturturdum.

---

## ➕ Addition

You-Do anketinde, **istatistik ve olasılık (statistics and probability)** temellerini empirik bir şekilde anlatan çalışma seçeneği bulunmaktaydı. Bu kapsamda, daha geçen hafta teslim ettiğim yüksek lisans ödevimi bu klasöre ekledim. **Ödev içeriği şunları kapsamaktadır:**

- **R Markdown kodu:** İstatistiksel analizlerin gerçekleştirildiği kodlar.
- **Çalışma dosyası:** Empirik veri analizleri ve sonuçlar.
- **Ödev PDF'i:** Analiz sonuçlarını özetleyen ve yorumlayan rapor.

### 📊 Kullanılan Yöntemler

Bu çalışmada aşağıdaki istatistiksel yöntemler kullanılmıştır:

1. **Tanımlayıcı İstatistikler:** Temel istatistiksel metrikler olan ortalama, medyan ve varyans hesaplamaları yapılmıştır.
2. **Normallik Testleri:** Verilerin normal dağılıma uygunluğunu değerlendirmek için standart testler uygulanmıştır.
3. **Veri Dönüşüm Teknikleri:** Normal dağılıma yaklaşmayan veriler için dönüşüm yöntemleri kullanılmıştır.
4. **Merkezi Limit Teoremi (CLT) Uygulaması:** Farklı örneklem büyüklükleriyle tekrarlı örneklem alımı yapılarak CLT'nin empirik ispatı gerçekleştirilmiştir. Bu çalışma, örneklem dağılımlarının normal dağılıma yakınsamasını göstererek, istatistiksel analizlerin temellerinden biri olan CLT'nin pratikte nasıl işlediğini ortaya koymaktadır.
5. **Güven Aralıkları:** Kitle ortalaması ve varyansı için %99 ve %90 güven aralıkları hesaplanmış, sonuçlar yorumlanmıştır. Bu analizler, güven aralıklarının veri üzerindeki etkisini ve karar alma süreçlerindeki rolünü vurgulamaktadır.
6. **Hipotez Testleri:** İlaç etkisinin değerlendirilmesinde I. Tip ve II. Tip hata ile test gücü analiz edilmiştir. Empirik verilerle desteklenen bu testler, hipotez doğrulama süreçlerinde hata türlerinin ve test gücünün önemini göstermektedir.

