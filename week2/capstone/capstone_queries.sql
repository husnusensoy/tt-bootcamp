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
