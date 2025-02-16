create or replace table dam as select
    date,
    general_dam_occupancy_rate as occ
from read_csv('data/dam_occupancy.csv');

-- DQ check
select diff
, count(1) n from
(select date - lag(date, 1) over(order by date) diff 
  from dam) group by 1;


COPY (select date
,occ
,lag(occ,90) over(order by date) l90
,lag(occ,91) over(order by date) l91
,lag(occ,92) over(order by date) l92
,lag(occ,93) over(order by date) l93
,lag(occ,94) over(order by date) l94
,lag(occ,95) over(order by date) l95
,lag(occ,96) over(order by date) l96
,lag(occ,97) over(order by date) l97
,lag(occ,120) over(order by date) l_m4
,lag(occ,150) over(order by date) l_m5
,lag(occ,180) over(order by date) l_m6
,max(occ) over(order by date rows between 120 preceding and 90 preceding) mx120
,max(occ) over(order by date rows between 150 preceding and 90 preceding) mx150
,max(occ) over(order by date rows between 180 preceding and 90 preceding) mx180
,min(occ) over(order by date rows between 120 preceding and 90 preceding) mn120
,min(occ) over(order by date rows between 150 preceding and 90 preceding) mn150
,min(occ) over(order by date rows between 180 preceding and 90 preceding) mn180
,avg(occ) over(order by date rows between 120 preceding and 90 preceding) mean120
,avg(occ) over(order by date rows between 150 preceding and 90 preceding) mean150
,avg(occ) over(order by date rows between 180 preceding and 90 preceding) mean180
,median(occ) over(order by date rows between 120 preceding and 90 preceding) med120
,median(occ) over(order by date rows between 150 preceding and 90 preceding) med150
,median(occ) over(order by date rows between 180 preceding and 90 preceding) med180
from dam order by date desc)  TO 'dam-features.csv' (HEADER, DELIMITER ',');
