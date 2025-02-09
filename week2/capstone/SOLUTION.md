# A Solution to Capstone

<!-- TOC -->
* [A Solution to Capstone](#a-solution-to-capstone)
  * [Data](#data)
    * [Features](#features)
      * [Features and Service Type Relevancy](#features-and-service-type-relevancy)
  * [Broadband](#broadband)
    * [Predictive Model](#predictive-model)
  * [Postpaid](#postpaid)
    * [Predictive Model](#predictive-model-1)
  * [Prepaid](#prepaid)
    * [Predictive Model](#predictive-model-2)
<!-- TOC -->

## Data

* Data format is currently in `Json Line` format.

Parallel reading files using PySpark

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("Tokenizer Application").master("local[2]").getOrCreate()

spark.read.json("capstone.*.jsonl.gz").count()
# 10000000
```

* Churn rate is `0.133%`. So data is imbalanced by the nature of churn in Telco.

```python

df = spark.read.json("capstone.*.jsonl.gz")

df.groupBy("churn").count().show()

"""
+-----+-------+
|churn|  count|
+-----+-------+
| true| 133653|
|false|9866347|
+-----+-------+
"""
```

* Same is true per `service_type`.
  * `Prepaid` churn rate is found to be `1.87%`
  * `Broadband` churn rate is found to be `0.286%`
  * `PostPaid` churn rante is found to be `1.85%`


```python

df.groupBy("service_type", "churn").count().show()


+------------+-----+-------+
|service_type|churn|  count|
+------------+-----+-------+
|     Prepaid| true|  62381|
|     Prepaid|false|3274061|
|   Broadband| true|   9541|
|   Broadband|false|3321671|
|    Postpaid| true|  61731|
|    Postpaid|false|3270615|
+------------+-----+-------+

```

### Features

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

#### Features and Service Type Relevancy

Each feature is only relevant for a subset of **Service Type**. You can find the relevancy in following table.


|                                      | Prepaid | Postpaid | Broadband |
|--------------------------------------|:-------:|:--------:|:---------:|
| app (as `size (app)`)                |    x    |    x     |     x     |
| avg_call_duration                    |    x    |    x     |           |
| avg_top_up_count                     |    x    |          |           |
| call_drops                           |    x    |    x     |           |
| roaming_usage                        |    x    |    x     |           |
| auto_payment                         |         |    x     |     x     |
| tenure                               |    x    |    x     |     x     |
| age                                  |    x    |    x     |     x     |
| customer_support_calls               |    x    |    x     |     x     |
| satisfaction_score                   |    x    |    x     |     x     |
| data_usage                           |    x    |    x     |     x     |
| monthly_charge                       |    x    |    x     |     x     |
| overdue_payments                     |         |    x     |     x     |
| **churn** (Target, as `cast("int")`) |    x    |    x     |     x     |



So, feature analysis and predictive model build only uses those relevant features and drop the rest.

## Broadband


```python
pand = df.filter(df.service_type == "Broadband") \
   .withColumn("apps_count",size(df["apps"])) \
   .drop("service_type", "app", "avg_call_duration", "avg_top_up_count","call_drops","id","roaming_usage","apps")\
   .sample(0.06,seed=42).toPandas()
   
pand.to_csv("broadband.sample.csv",index=False)
```


To perform uni-variate analysis simply use `pandas-profiling` on sample dataset.

Use following for installation

```shell
uv add ydata-profiling
```

```python

from ydata_profiling import ProfileReport
import pandas as pd

df = pd.read_csv('broadband.sample.csv')
profile = ProfileReport(df)
profile.to_file("broadband.html")

```

Note that it is hard to see any correlation with `churn` because of unbalanced dataset.

### Predictive Model

We simply build a predictive model using only [relevant columns](#features-and-service-type-relevancy) on Random Forest Classifier of Spark ML.

We achieve **0.6284** AUC and 0.9971 accuracy.

Use `train.py --service-type Broadband` to replicate results.

## Postpaid

### Predictive Model

We simply build a predictive model using only [relevant columns](#features-and-service-type-relevancy) on Random Forest Classifier of Spark ML.

We achieve **0.7792** AUC and 0.9812 accuracy.

Use `train.py --service-type Postpaid` to replicate results.

## Prepaid

### Predictive Model

We simply build a predictive model using only [relevant columns](#features-and-service-type-relevancy) on Random Forest Classifier of Spark ML.

We achieve **0.7099** AUC with 0.9815 accuracy.

Use `train.py --service-type Prepaid` to replicate results.