drop table ladsraw;

CREATE EXTERNAL TABLE IF NOT EXISTS ladsraw (data_reported string, dr_no int, date_occ string, time_occ int, area int, area_name string, 
rd int, crm_cd int, crm_cd_desc string, status string, status_desc string, 
location string, cross_st string, latitude string, longitude string, crimteType string) 
ROW FORMAT DELIMITED FIELDS TERMINATED BY '\054' STORED AS TEXTFILE LOCATION '/user/la_testData';

--describe ladsraw;

--select * from ladsraw STORED AS TEXTFILE LOCATION '/user/la_testData';

LOAD data inpath '/user/batchRawInput/LaDS.csv' into table ladsraw;

select * from ladsraw limit 10;

describe ladsraw;
