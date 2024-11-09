-- Copyright (c) 2024, UChicago Argonne, LLC
-- BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
DROP TABLE IF EXISTS tnc_times_by_tnc_operator;
CREATE TABLE tnc_times_by_tnc_operator as
SELECT 
    tnc_operator, 
    service_mode, 
    avg(assignment_time-request_time)/60.0 as time_to_assign, 
    avg(pickup_time-request_time)/60.0 as wait,
    avg(dropoff_time-pickup_time)/60.0 as ivtt,
    scaling_factor*count(*) as demand
FROM 
    "TNC_Request"
where
    assigned_vehicle is not null
group by
    tnc_operator,
    service_mode;

DROP TABLE IF EXISTS pmt_pht_by_tnc_mode;
CREATE TABLE pmt_pht_by_tnc_mode AS 
SELECT 
    service_mode, 
    scaling_factor*sum(distance) as pmt,
    scaling_factor*sum(dropoff_time-request_time)/3600 as pht,
    scaling_factor*count(*) as demand
FROM "TNC_Request"
where
    assigned_vehicle is not null
GROUP BY 
    service_mode;

DROP TABLE IF EXISTS vmt_vht_by_tnc_mode;
CREATE TABLE vmt_vht_by_tnc_mode AS 
SELECT
    mode,
    scaling_factor*sum(travel_distance)/1609.34 as vmt,
    scaling_factor*sum(end-start)/3600 as vht
FROM TNC_Trip
    Group By mode;

DROP TABLE IF EXISTS vmt_vht_by_tnc_operator;
CREATE TABLE vmt_vht_by_tnc_operator AS 
SELECT
    tnc_operator,
    case
        when final_status = -1 then 'PICKUP'
        when final_status = -2 then 'DROPOFF'
        when final_status = -4 then 'CHARGING'
    end as status,
    scaling_factor*sum(travel_distance)/1609.34 as vmt, 
    scaling_factor*sum(end-start)/3600 as vht
FROM TNC_Trip
Group by
    tnc_operator,
    status;

DROP TABLE IF EXISTS empty_vmt_vht_by_tnc_operator;
CREATE TABLE empty_vmt_vht_by_tnc_operator AS 
SELECT 
    tnc_operator,
    case 
        when passengers = 0 then 'UNOCCUPIED'
        else 'OCCUPIED'
    end as occupied_status,
    scaling_factor*sum(travel_distance)/1609.34 as vmt, 
    scaling_factor*sum(end-start)/3600 as vht
FROM TNC_Trip
Group by
    tnc_operator,
    occupied_status;

DROP TABLE IF EXISTS avo_by_tnc_operator;
CREATE TABLE avo_by_tnc_operator AS 
SELECT
    tnc_operator,
    'AVO_trips' as metric,
    avg(passengers) as AVO 
FROM TNC_Trip
GROUP by
    tnc_operator
UNION
SELECT
    tnc_operator,
    'AVO_dist' as metric,
    sum(passengers*1.0*travel_distance)/sum(travel_distance) as AVO
FROM TNC_Trip
GROUP by 
    tnc_operator
UNION
SELECT
    tnc_operator,
    'AVO_trips_revenue' as metric,
    avg(passengers) as AVO
FROM TNC_Trip
WHERE passengers > 0
GROUP by tnc_operator
UNION
SELECT
    tnc_operator,
    'AVO_dist_revenue' as metric, 
    sum(passengers*1.0*travel_distance)/sum(travel_distance) as AVO
FROM TNC_Trip 
WHERE passengers > 0 and travel_distance > 0 
GROUP by 
    tnc_operator;