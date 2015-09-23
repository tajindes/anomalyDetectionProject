add jar /usr/local/elasticsearch-hadoop-2.1.1/dist/elasticsearch-hadoop-hive-2.1.1.jar;

--Manually create the index for crime_info table and define crimelocation as geopoint for the first time (if you drop the index itself).

drop table crime_info;

CREATE EXTERNAL TABLE crime_info (
  crime_timestamp TIMESTAMP,
  crimecode STRING,
  crimecodedesc STRING,
  crimetype STRING,
  crimeLocation string,
  zip STRING,
  city STRING,
  state STRING,
  country STRING
  )
STORED BY 'org.elasticsearch.hadoop.hive.EsStorageHandler'
TBLPROPERTIES('es.resource' = 'crimes/crime',
              'es.mapping.names' = 'crime_timestamp:crime_ts, date:@timestamp');


--describe crime_info;

--select "2015-03-07T16:12:00Z", crm_cd as crime_code, crm_cd_desc as crime_cd_desc, crimtetype as crimetype, regexp_extract(latitude, '[-]*[0-9]*[.][0-9]*', 0),regexp_extract(longitude, '[-]*[0-9]*[.][0-9]*', 0), null, null, null, null from ladsraw limit 10;

--concat(substr(regexp_replace(date_occ, '/', ''),5,4),'-',substr(regexp_replace(date_occ, '/', ''),3,2),'-',substr(regexp_replace(date_occ, '/', ''),1,2), 'T', substr(lpad(time_occ,4,0),1,2),':', substr(lpad(time_occ,4,0),3,2),':','00Z')

--select date_occ, time_occ, substr(regexp_replace(date_occ, '/', ''),5,4), substr(regexp_replace(date_occ, '/', ''),3,2), substr(regexp_replace(date_occ, '/', ''),1,2), 
--substr(lpad(time_occ,4,0),1,2), substr(lpad(time_occ,4,0),3,2), unix_timestamp(concat(substr(regexp_replace(date_occ, '/', ''),5,4),'-',
--substr(regexp_replace(date_occ, '/', ''),1,2),'-',
--substr(regexp_replace(date_occ, '/', ''),3,2), ' ', substr(lpad(time_occ,4,0),1,2),':', substr(lpad(time_occ,4,0),3,2),':','00'))*1000,  crm_cd as crime_code,
--crm_cd_desc as crime_cd_desc, crimtetype as crimetype, named_struct('lat', regexp_extract(latitude, '[-]*[0-9]*[.][0-9]*', 0),
-- 'lon', regexp_extract(longitude, '[-]*[0-9]*[.][0-9]*', 0)), null, null, null, null from ladsraw limit 50;

INSERT OVERWRITE TABLE crime_info select unix_timestamp(concat(substr(regexp_replace(date_occ, '/', ''),5,4),'-',substr(regexp_replace(date_occ, '/', ''),1,2),'-', 
substr(regexp_replace(date_occ, '/', ''),3,2), ' ', substr(lpad(time_occ,4,0),1,2),':', substr(lpad(time_occ,4,0),3,2),':','00'))*1000,  crm_cd as crime_code, 
crm_cd_desc as crime_cd_desc, crimtetype as crimetype, concat(regexp_extract(latitude, '[-]*[0-9]*[.][0-9]*', 0), ',', regexp_extract(longitude, '[-]*[0-9]*[.][0-9]*', 0)),
null, null, null, null from ladsraw 
where length(regexp_extract(latitude, '[-]*[0-9]*[.][0-9]*', 0)) > 0 and length(regexp_extract(longitude, '[-]*[0-9]*[.][0-9]*', 0)) > 0;


--INSERT OVERWRITE TABLE crime_info select concat(substr(regexp_replace(date_occ, '/', ''),5,4),'-',substr(regexp_replace(date_occ, '/', ''),3,2),'-',
--substr(regexp_replace(date_occ, '/', ''),1,2), ' ', substr(lpad(time_occ,4,0),1,2),':', substr(lpad(time_occ,4,0),3,2),':','00'), crm_cd as crime_code, 
--crm_cd_desc as crime_cd_desc, crimtetype as crimetype, regexp_extract(latitude, '[-]*[0-9]*[.][0-9]*', 0), regexp_extract(longitude, '[-]*[0-9]*[.][0-9]*', 0), 
--null, null, null, null from ladsraw;

describe crime_info;

--select count(*) from crime_info;

select * from crime_info limit 10;
select count(*) from crime_info;
