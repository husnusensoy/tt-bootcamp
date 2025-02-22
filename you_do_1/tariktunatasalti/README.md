# ReadMe

## DOSYALAR VE AÇIKLAMALARI

### `soru1.py`

Bu dosya:

- `DuckDB` kullanarak `ratings` ve `movies` tablolarını oluşturur.
- Filmlerin ortalama puanlarını hesaplar.
- **Bayesian ağırlıklı bir skorlama yöntemi** kullanarak en iyi 30 filmi belirler.
- Sonuçları `soru1.csv` dosyasına kaydeder.

#### **Bayesian Ağırlıklı Skorlama Formülü:**

$$
\text{Bayesian Score} = \frac{\text{izlenme sayısı}}{\text{izlenme sayısı} + w} \times \text{ortalama puan} + \frac{w}{\text{izlenme sayısı} + w} \times \text{genel ortalama puan}
$$

Burada `w`, Bayesian ağırlık parametresidir.

### `soru1.csv`

- `soru1.py` çalıştırıldığında oluşturulan film öneri listesini içerir.
- Bayesian skora göre sıralanmış 30 filmi içerir.

---

### `soru2.py`

Bu dosya:

- `DuckDB` kullanarak `ratings` ve `movies` tablolarını oluşturur.
- **Belirtilen bir hedef kullanıcı (`target_user_id`)** için kişiselleştirilmiş film önerileri oluşturur.
- Kullanıcının daha önce izlediği filmleri belirler (`WatchedMovies`).
- Kullanıcı ile benzer film geçmişine sahip olan diğer kullanıcıları **Jaccard Benzerliği** kullanarak tespit eder (`JaccardSimilarity`).
- Bu benzer kullanıcıların izlediği ancak hedef kullanıcının izlemediği filmleri belirler (`CandidateMovies`).
- **Jaccard benzerliği ile belirlenen filmler için Bayesian ağırlıklı bir skorlama yöntemiyle** en iyi 30 filmi belirler.

### `soru2.csv`

- Kullanıcının izlemediği ancak **benzer kullanıcıların yüksek puan verdiği** filmleri içerir.
- Bayesian skora ve Jaccard benzerliğine göre sıralanmış **30 öneriyi** gösterir.

---

### `soru3.py`

Bu dosya:

- `DuckDB` kullanarak `ratings` ve `movies` tablolarını oluşturur.
- **KL Divergence (Kullback-Leibler Ayrıklığı) metriğini kullanarak** filmler arasındaki benzerliği hesaplar.
- En az **30 kez izlenen filmleri seçer** ve çiftler halinde karşılaştırır.
- **Bayesian Normalization** ile her filmin derecelendirme dağılımını düzeltir.
- **KL Divergence** hesaplamaları sonucunda filmleri üç kategoriye ayırır:
  - **Çok benzer filmler** (Biri kaldırılabilir)
  - **Biraz farklı ama benzer bir kitleye hitap eden filmler**
  - **Oldukça farklı filmler (İkisi de sistemde kalmalı)**
- Sonuçları ekrana yazdırır.

