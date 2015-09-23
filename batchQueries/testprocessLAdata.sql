--CREATE EXTERNAL TABLE IF NOT EXISTS ladsprocessed (crimeTS timestamp, crimeCode string, crimeCodeDesc string, crimeType string, latitude int, longitude int, city string, state string, country string, zip int) ROW FORMAT DELIMITED FIELDS TERMINATED BY '\054' STORED AS TEXTFILE LOCATION '/user/la_processedData';

describe ladsprocessed;

--INSERT INTO ladsprocessed 

select unix_timestamp(concat(substr(regexp_replace(date_occ, '/', ''),5,4),'-',substr(regexp_replace(date_occ, '/', ''),3,2),'-',substr(regexp_replace(date_occ, '/', ''),1,2), ' ', substr(lpad(time_occ,4,0),1,2),':', substr(lpad(time_occ,4,0),3,2),':','00')) as crime_ts, crm_cd as crime_code, crm_cd_desc as crime_cd_desc, crimtetype as crimetype ,regexp_extract(latitude, '[-]*[0-9]*[.][0-9]*', 0),regexp_extract(longitude, '[-]*[0-9]*[.][0-9]*', 0), null, null,null,null  from ladsraw limit 30;


select * from ladsprocessed limit 20;

