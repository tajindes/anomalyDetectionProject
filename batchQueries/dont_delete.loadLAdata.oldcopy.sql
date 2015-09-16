DROP TABLE price_data;

CREATE EXTERNAL TABLE IF NOT EXISTS price_data ( time string, price double, volume int)

ROW FORMAT DELIMITED FIELDS TERMINATED BY "\073" LINES TERMINATED BY "\n"

STORED AS TEXTFILE LOCATION '/user/testData';

DESCRIBE price_data;

LOAD data inpath '/user/price_data*.txt' into table price_data;

INSERT OVERWRITE DIRECTORY '/user/price_data_output_hive'

SELECT min30, AVG(price), SUM(volume)

FROM (

SELECT concat(substr(time,1,11), if(substr(time,12,2)<"30","00","30"), "00") AS min30, price, volume

FROM price_data) a

GROUP BY a.min30

