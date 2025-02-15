create table if not exists rating as
select *
from read_csv(
        'rating_*.txt',
        columns = { 'MovieId': 'int',
        'UserId': 'int',
        'Date': 'date',
        'Rate' :'int' }
    );

CREATE TABLE IF NOT EXISTS titles AS
SELECT * 
FROM read_csv(
        'movie_titles_new.csv',
        columns = {
            "index": "int",
            'MovieId': 'int',
            'Year': 'varchar',
            "Title" : 'text'
        },
        delim = ',',
        quote = '"',
        null_padding = TRUE,
        header = TRUE
    );


CREATE TABLE IF NOT EXISTS normalized_rates AS(
    SELECT MovieId, UserId, Date, NormalizedRate
    FROM (
        WITH user_info AS (
            SELECT UserId, AVG(Rate) as RateAVG, NULLIF(STDDEV(Rate),0) as RateSTD
            FROM rating
            GROUP BY UserId
        )
        SELECT  a.MovieId, a.UserId, a.Date, a.Rate AS OldRate, (a.Rate - b.RateAVG)/b.RateSTD AS NormalizedRate
        FROM rating a
        LEFT JOIN user_info b
        USING(UserId)
    )
);

-- cold start recommendation:

-- izlenme sayısı düşük olan filmleri henüz eleyemedim ancak ilerlememi paylaşmak istedim.
-- Bu sorunu çözdükten sonra diğer 2 maddedeki talepler için geliştirmeye devam edeceğim.
SELECT a.Title, a.MovieId, AVG(b.NormalizedRate) AS NormalizedRateAVG, MEDIAN(b.NormalizedRate) AS NormalizedRateMEDIAN, COUNT(UserId) AS WatchCount
FROM titles a 
LEFT JOIN normalized_rates b
USING(MovieId)
GROUP BY a.Title, a.MovieId
ORDER BY NormalizedRateMEDIAN DESC;

-- normalize edilmiş film skorlarının güven aralığının alt sınırını hesaplayarak filmlerin ortalama skorlarını izlenme sayısına göre cezalandırdım.
SELECT a.Title, a.MovieId, COUNT(UserId) AS WatchCount, AVG(b.NormalizedRate) AS NormalizedRateAVG, AVG(b.NormalizedRate) -1.96 * (STDDEV(NormalizedRate) / SQRT(COUNT(UserId))) AS AdjustedScore
FROM titles a 
LEFT JOIN normalized_rates b
USING(MovieId)
GROUP BY a.Title, a.MovieId
ORDER BY AdjustedScore DESC
LIMIT 30;

WITH UserMap AS ( SELECT UserId, ROW_NUMBER() OVER (ORDER BY UserId) - 1 AS user_index FROM (SELECT DISTINCT UserId FROM rating) AS unique_users),
MovieMap AS (SELECT MovieId, ROW_NUMBER() OVER (ORDER BY MovieId) - 1 AS movie_index FROM (SELECT DISTINCT MovieId FROM rating) AS unique_movies)
SELECT r.MovieId, m.movie_index, r.UserId, u.user_index
FROM rating r
JOIN UserMap u ON r.UserId = u.UserId
JOIN MovieMap m ON r.MovieId = m.MovieId;

-- churn veri setinin elde edilmesi
drop table churn_data;

create table if not exists churn_data as
select *
from read_json(
        "capstone_data/capstone.*.jsonl",
        columns = {"id":"varchar",
        "age":"int",
        "tenure":"int",
        "service_type":"varchar",
        "avg_call_duration":"float",
        "data_usage":"float",
        "roaming_usage":"float",
        "monthly_charge":"float",
        "overdue_payments":"int",
        "auto_payment":"bool",
        "avg_top_up_count":"float",
        "call_drops":"int",
        "customer_support_calls":"int",
        "satisfaction_score":"float",
        "apps":"varchar",
        "churn":"bool"
         }
    );

CREATE OR REPLACE TABLE churn_data as (SELECT a.*, 
       b.izlego, b.ritimgo, b.cuzdanx, b.hizlipazar, b.konusalim,
       b.prepaid, b.postpaid, b.broadband
FROM churn_data a
LEFT JOIN (
    SELECT 
        id, 
        apps, 
        service_type,
        CASE WHEN apps LIKE '%İzleGo%' THEN 1 ELSE 0 END AS izlego,
        CASE WHEN apps LIKE '%RitimGo%' THEN 1 ELSE 0 END AS ritimgo,
        CASE WHEN apps LIKE '%CüzdanX%' THEN 1 ELSE 0 END AS cuzdanx,
        CASE WHEN apps LIKE '%HızlıPazar%' THEN 1 ELSE 0 END AS hizlipazar,
        CASE WHEN apps LIKE '%Konuşalım%' THEN 1 ELSE 0 END AS konusalim,
        CASE WHEN service_type = 'Prepaid' THEN 1 ELSE 0 END AS prepaid,
        CASE WHEN service_type = 'Postpaid' THEN 1 ELSE 0 END AS postpaid,
        CASE WHEN service_type = 'Broadband' THEN 1 ELSE 0 END AS broadband
    FROM churn_data
) b 
USING(id));

-- boş veriler için sorgular
SELECT 
    'id' AS column_name, COUNT(*) - COUNT(id) AS null_count FROM churn_data
UNION ALL
SELECT 
    'age', COUNT(*) - COUNT(age) FROM churn_data
UNION ALL
SELECT 
    'tenure', COUNT(*) - COUNT(tenure) FROM churn_data
UNION ALL
SELECT 
    'service_type', COUNT(*) - COUNT(service_type) FROM churn_data
UNION ALL
SELECT 
    'avg_call_duration', COUNT(*) - COUNT(avg_call_duration) FROM churn_data
UNION ALL
SELECT 
    'data_usage', COUNT(*) - COUNT(data_usage) FROM churn_data
UNION ALL
SELECT 
    'roaming_usage', COUNT(*) - COUNT(roaming_usage) FROM churn_data
UNION ALL
SELECT 
    'monthly_charge', COUNT(*) - COUNT(monthly_charge) FROM churn_data
UNION ALL
SELECT 
    'overdue_payments', COUNT(*) - COUNT(overdue_payments) FROM churn_data
UNION ALL
SELECT 
    'auto_payment', COUNT(*) - COUNT(auto_payment) FROM churn_data
UNION ALL
SELECT 
    'avg_top_up_count', COUNT(*) - COUNT(avg_top_up_count) FROM churn_data
UNION ALL
SELECT 
    'call_drops', COUNT(*) - COUNT(call_drops) FROM churn_data
UNION ALL
SELECT 
    'customer_support_calls', COUNT(*) - COUNT(customer_support_calls) FROM churn_data
UNION ALL
SELECT 
    'satisfaction_score', COUNT(*) - COUNT(satisfaction_score) FROM churn_data
UNION ALL
SELECT 
    'apps', COUNT(*) - COUNT(apps) FROM churn_data
UNION ALL
SELECT 
    'churn', COUNT(*) - COUNT(churn) FROM churn_data;


