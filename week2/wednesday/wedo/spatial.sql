INSTALL spatial;
LOAD spatial;

COPY (
select *
, hour(pickup_datetime) as hh24
, month(pickup_datetime) as month
, st_distance_spheroid(st_point(pickup_latitude,pickup_longitude), st_point(dropoff_latitude,dropoff_longitude)) l2
, st_distance_spheroid(st_point(pickup_latitude,0), st_point(dropoff_latitude,0)) + st_distance_spheroid(st_point(0,pickup_longitude), st_point(0,dropoff_longitude)) l1
from read_csv("test20.csv") ) TO 'test20-rich.csv' (HEADER, DELIMITER ',');

COPY (
select *
, log(trip_duration) as ln_td
, hour(pickup_datetime) as hh24
, month(pickup_datetime) as month
, st_distance_spheroid(st_point(pickup_latitude,pickup_longitude), st_point(dropoff_latitude,dropoff_longitude)) l2
, st_distance_spheroid(st_point(pickup_latitude,0), st_point(dropoff_latitude,0)) + st_distance_spheroid(st_point(0,pickup_longitude), st_point(0,dropoff_longitude)) l1
from read_csv("train80.csv") ) TO 'train80-rich.csv' (HEADER, DELIMITER ',');
