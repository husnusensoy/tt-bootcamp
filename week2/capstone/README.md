# Capstone: Guardians of Churn

Bu capstone görevinde hedefimiz olası müşteri göçlerinin önüne geçmek. Farklı servislerimize ait müşteri verileri sizlerle paylaşıldı. 

Call center ekibimiz aramalar için pazarlama ekibimiz ise karşı teklifler vermek için hazır ama onlara sıralı bir liste iletmemiz var. Soru basit kimler bizden ayrılmayı düşünüyor ?

Aksiyon öncesinde yönetim ekibimizi ikna edecek somut bir sunum yapacaksınız. 5 dk süreniz var.

Kolaylıklar,

Hüsnü 

## Veri Kaynağı

Toplamda 10 milyon müşterimize ait veri sizlerlerle 10 parça halinde paylaşıldı

```
https://storage.googleapis.com/sadedegel/dataset/tt-capstone/capstone.1.jsonl.gz
https://storage.googleapis.com/sadedegel/dataset/tt-capstone/capstone.2.jsonl.gz
https://storage.googleapis.com/sadedegel/dataset/tt-capstone/capstone.3.jsonl.gz
https://storage.googleapis.com/sadedegel/dataset/tt-capstone/capstone.4.jsonl.gz
https://storage.googleapis.com/sadedegel/dataset/tt-capstone/capstone.5.jsonl.gz
https://storage.googleapis.com/sadedegel/dataset/tt-capstone/capstone.6.jsonl.gz
https://storage.googleapis.com/sadedegel/dataset/tt-capstone/capstone.7.jsonl.gz
https://storage.googleapis.com/sadedegel/dataset/tt-capstone/capstone.8.jsonl.gz
https://storage.googleapis.com/sadedegel/dataset/tt-capstone/capstone.9.jsonl.gz
https://storage.googleapis.com/sadedegel/dataset/tt-capstone/capstone.10.jsonl.gz
```

## Yapılacaklar

* Metriğinizi iyi belirleyin. (Unutmayın ki her ay sadece abone kitlesinden 1000'de birlik kısmı kaybediyoruz.)

* Modellemenizi gerçekleştirin. Tercihen yorumlaması ve açıklaması kolay olan bir model olsun. Regülasyon sağlayan kurum açıklanması zor modellerde bizi zorlayacaktır.

* Yapacağınız sunumda iş birimimiz olacak. En basit bir şekilde onlara çözümümüzü aktarmamız gerekiyor.

## Veri Alanları

* **id**: Müşteri IDsi
* **age**: Müşterinin yaşı
* **tenure**: Müşterinin operatörde geçirdiği toplam süre (ay cinsinden)
* **service_type**: Ön Ödemeli, Peşin Ödemeli veya Geniş Bant internet müşterisi
* **avg_call_duration**: Ortalama sesli görüşme süresi (saniye)
* **data_usage**: GB Upload + Download
* **roaming_usage**: Ortalama roaming sesli görüşme süresi
* **monthly_charge**: Aylık ortalama fatura
* **overdue_payments**: Ödemesi geçen fatura adedi
* **auto_payment**: Otomatik ödeme talimatı
* **avg_top_up_count**: Ön yüklemeli abone için aylık yükleme sayısı ortalaması
* **call_drops**: Şebekede yaşadığı sesli görüşme kesilmesi
* **customer_support_calls**: Toplam çağrı merkezi araması
* **satisfaction_score**: Müşteri çağrı merkezi değerlendirme skoru 
* **apps**: Müşterinin kullandığı diğer servislerimiz
    * İzleGo 
    * RitimGo
    * CüzdanX
    * HızlıPazar
    * Konuşalım
* **churn**: bool