add jar /usr/local/elasticsearch-hadoop-2.1.1/dist/elasticsearch-hadoop-hive-2.1.1.jar;


--add jar /usr/local/elasticsearch-hadoop-2.1.1/dist/elasticsearch-hadoop-hive-2.1.1.jar;

drop table test5;

CREATE EXTERNAL TABLE test5 (
  location string
  )
STORED BY 'org.elasticsearch.hadoop.hive.EsStorageHandler'
TBLPROPERTIES('es.resource' = 'test5/pin');


--describe crime_info;

--select "2015-03-07T16:12:00Z", crm_cd as crime_code, crm_cd_desc as crime_cd_desc, crimtetype as crimetype, regexp_extract(latitude, '[-]*[0-9]*[.][0-9]*', 0),regexp_extract(longitud$

--concat(substr(regexp_replace(date_occ, '/', ''),5,4),'-',substr(regexp_replace(date_occ, '/', ''),3,2),'-',substr(regexp_replace(date_occ, '/', ''),1,2), 'T', substr(lpad(time_occ,4,$

--select date_occ, time_occ, substr(regexp_replace(date_occ, '/', ''),5,4), substr(regexp_replace(date_occ, '/', ''),3,2), substr(regexp_replace(date_occ, '/', ''),1,2),
--substr(lpad(time_occ,4,0),1,2), substr(lpad(time_occ,4,0),3,2), unix_timestamp(concat(substr(regexp_replace(date_occ, '/', ''),5,4),'-',
--substr(regexp_replace(date_occ, '/', ''),1,2),'-',
--substr(regexp_replace(date_occ, '/', ''),3,2), ' ', substr(lpad(time_occ,4,0),1,2),':', substr(lpad(time_occ,4,0),3,2),':','00'))*1000,  crm_cd as crime_code,
--crm_cd_desc as crime_cd_desc, crimtetype as crimetype, named_struct('lat', regexp_extract(latitude, '[-]*[0-9]*[.][0-9]*', 0),
-- 'lon', regexp_extract(longitude, '[-]*[0-9]*[.][0-9]*', 0)), null, null, null, null from ladsraw limit 50;

--select concat(regexp_extract(latitude, '[-]*[0-9]*[.][0-9]*', 0), regexp_extract(longitude, '[-]*[0-9]*[.][0-9]*', 0)) from ladsraw limit 10;

--select concat(regexp_extract(latitude, '[-]*[0-9]*[.][0-9]*', 0), ',', regexp_extract(longitude, '[-]*[0-9]*[.][0-9]*', 0)) from ladsraw
--where cast(regexp_extract(latitude, '[-]*[0-9]*[.][0-9]*', 0) as double) != null and cast(regexp_extract(longitude, '[-]*[0-9]*[.][0-9]*', 0) as double) != null limit 1;


--select  cast(regexp_extract(latitude, '[-]*[0-9]*[.][0-9]*', 0) as INT),  cast(regexp_extract(longitude, '[-]*[0-9]*[.][0-9]*', 0) as INT), 
--concat(regexp_extract(latitude, '[-]*[0-9]*[.][0-9]*', 0), ',', regexp_extract(longitude, '[-]*[0-9]*[.][0-9]*', 0)) from ladsraw
--where cast((regexp_extract(latitude, '[-]*[0-9]*[.][0-9]*', 0)) as INT) <> "NULL" OR cast((regexp_extract(latitude, '[-]*[0-9]*[.][0-9]*', 0)) as INT) <> NULL;




select concat(regexp_extract(latitude, '[-]*[0-9]*[.][0-9]*', 0), ',', regexp_extract(longitude, '[-]*[0-9]*[.][0-9]*', 0)) from ladsraw 
where length(regexp_extract(latitude, '[-]*[0-9]*[.][0-9]*', 0)) > 0 and length(regexp_extract(longitude, '[-]*[0-9]*[.][0-9]*', 0)) > 0 limit 50;


INSERT OVERWRITE TABLE test5 select concat(regexp_extract(latitude, '[-]*[0-9]*[.][0-9]*', 0), ',', regexp_extract(longitude, '[-]*[0-9]*[.][0-9]*', 0)) from ladsraw 
where length(regexp_extract(latitude, '[-]*[0-9]*[.][0-9]*', 0)) > 0 and length(regexp_extract(longitude, '[-]*[0-9]*[.][0-9]*', 0)) > 0;













--INSERT OVERWRITE TABLE test5 select concat("34.4444", ',', "-118.8888") from ladsraw limit 5;

--INSERT OVERWRITE TABLE crime_info select concat(substr(regexp_replace(date_occ, '/', ''),5,4),'-',substr(regexp_replace(date_occ, '/', ''),3,2),'-',
--substr(regexp_replace(date_occ, '/', ''),1,2), ' ', substr(lpad(time_occ,4,0),1,2),':', substr(lpad(time_occ,4,0),3,2),':','00'), crm_cd as crime_code,
--crm_cd_desc as crime_cd_desc, crimtetype as crimetype, regexp_extract(latitude, '[-]*[0-9]*[.][0-9]*', 0), regexp_extract(longitude, '[-]*[0-9]*[.][0-9]*', 0),
--null, null, null, null from ladsraw;

describe test5;

--select count(*) from crime_info;

--select * from test5 limit 10;


--cc, '/', ''),3,2),'-',substr(regexp_replace(date_occ, '/', ''),1,2), 'T', substr(lpad(time_occ,4,0),1,2),':', substr(lpad(time_occ,4,0),3,2),':','00Z')

--describe test_crime_info;

--INSERT OVERWRITE TABLE crime_info select "2015-03-07T16:12:00Z", "taj", "ttt","bbb", "ccc", "ddd", "eee","fff", "ttt","pPP" from ladsraw;

--INSERT OVERWRITE TABLE test_crime_info select "taj","singh" from ladsraw;

--drop table 
--describe crime_info;

--select count(*) from crime_info;

--select concat(substr(regexp_replace(date_occ, '/', ''),5,4),'-',substr(regexp_replace(date_occ, '/', ''),3,2),'-',
--substr(regexp_replace(date_occ, '/', ''),1,2), ' ', substr(lpad(time_occ,4,0),1,2),':', substr(lpad(time_occ,4,0),3,2),':','00'), "56789",
--crm_cd_desc as crime_cd_desc, crimtetype as crimetype, regexp_extract(latitude, '[-]*[0-9]*[.][0-9]*', 0), regexp_extract(longitude, '[-]*[0-9]*[.][0-9]*', 0),
--null, null, null, null from ladsraw limit 10;

--describe crime_info;

--select * from crime_info where crimecode="taj2";

--describe crime_info;
