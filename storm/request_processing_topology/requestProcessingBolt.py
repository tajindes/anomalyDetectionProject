import json
import logging
import random
import time
import pyelasticsearch
from datetime import datetime 
from pyleus.storm import SimpleBolt

from kafka import KafkaClient, SimpleProducer

#INDEX_NAME = 'crime_index'
INDEX_NAME = 'crimes'
QUERY_SIZE = 10

with open("/home/ubuntu/crimeAnalysis/config/config.json", 'rb') as file:
    config = json.load(file)

# GOTCHA:
# have to include "http://" and ends with "/", else will throw error
ELASTIC_SEARCH_CLUSTER = config['es_cluster']

KAFKA_CLUSTER = config['kafka_cluster']

log = logging.getLogger("request_processing_topology.request_bolt")

es = pyelasticsearch.ElasticSearch(urls=ELASTIC_SEARCH_CLUSTER)
kafka_client = KafkaClient(hosts=KAFKA_CLUSTER)
producer = SimpleProducer(kafka_client)


class RequestProcessingBolt(SimpleBolt):
    def process_tuple(self, tup):
        #print "taj in bolt1";
        
        
	request = tup.values

        # convert the extract value to a JSON object
        parsed_msg = json.loads(request[0])
        log.debug("++++++++++++++++++RECEIVING MSG+++++++++++++++")
        log.debug(parsed_msg['location'])

        location = {
            "lat": parsed_msg['location']['latitude'],
            "lon": parsed_msg['location']['longitude']
        }

	'''
	query = {
          "query": {
           "filtered" : {
                  "query" : {
                     "range" : {
                        "crime_ts" : { "from" : "2014-12-10", "to" : "2015-12-12" }
                      }
                   },
                  "filter" : {
                      "geo_distance" : {
                          "distance" : "100km",
                          "crimelocation" : location
                      }
                  }     
              }
          }
        }
	'''

	#res = es.search('crimecode:354', index='crimes')
        log.debug("++++++++++++++++executing search query+++++++++++++++")
        '''res = es.search(query, index=INDEX_NAME)

        hits = res['hits']['hits']
        hits_count = len(hits)

        log.debug("++++++++++++++++hits count: %d+++++++++++++++\n", hits_count)
        # error handle, no cab available
        if hits_count == 0:
            return
	
	monthsDictionary = {}
	
	for crimeIndex in range(0, hits_count):
	    #hits[crimeIndex]
	    #hits[crimeIndex]['_id']
	    #hits[crimeIndex]['_source']
	    crimeTimestamp = hits[crimeIndex]['_source']['crime_ts']
	    dateValue = time.strptime(crimeTimestamp, "%Y-%m-%dT%H:%M:%SZ")

	    if((str(dateValue.tm_mon) + '-' + str(dateValue.tm_year)) in monthsDictionary):
		monthsDictionary[str(dateValue.tm_mon) + '-' + str(dateValue.tm_year)] = monthsDictionary[str(dateValue.tm_mon) + '-' + str(dateValue.tm_year)] + 1;
	    else:
		monthsDictionary[str(dateValue.tm_mon) + '-' + str(dateValue.tm_year)] = 1;
	    
	
	'''

        #index = random.randint(0, hits_count - 1)
        #crime_id = hits[index]['_id']
	
	# send to kafka
	
	#es.create_index("test12_index", settings=None)
	#delete it after testing -start
	#log.debug(parsed_msg['location_taj'])
	# delete it after testing - end

	# storing data in elastic search:
	#es = ElasticSearch('http://localhost:9200/')
	#es.index(', 'person', {'name': 'Joe Tester', 'age': 25, 'title': 'QA Master'}, id=1);

	try:
	    es.create_index("crime_realtime", settings=None)
	except:
	    pass

	time_raw = parsed_msg['time_rptd'].zfill(4);
	timeTempStr = time_raw[:2]+ ":"+ time_raw[2:] + ":" + "00"
      	crime_rptd_ts = datetime.strptime(parsed_msg['date_rptd']+ " " + timeTempStr, '%m/%d/%Y %H:%M:%S')
	#crime_rptd_ts = datetime.strptime('30/03/09 16:31:32.123', '%d/%m/%y %H:%M:%S.%f')
	

	#dateTemp = datetime.datetime.strptime(date_rptd_raw, '%m/%d/%y').strftime('%Y-%m-%d')
	#datetime.datetime.now().strftime("%Y-%m-%d %H:%M"
	#crime_rptd_ts = datetime.datetime.strptime(parsed_msg['date_rptd'], '%m/%d/%y').strftime('%Y-%m-%d')

	crimelocation = {
            "lat": parsed_msg['location']['latitude'],
            "lon": parsed_msg['location']['longitude']
        }

	modeldocument = {
	    "crime_id":parsed_msg['crime_id'],
	    "crimelocation":crimelocation,
	    "crimetype":parsed_msg['crimetype'],
	    "crime_rptd_ts":crime_rptd_ts
	}

	'''	
	modeldocument = {
            "lat": parsed_msg['location']['latitude'],
            "lon": parsed_msg['location']['longitude'],
            "monthsDictionary": monthsDictionary
	}
	'''
	
	es.index("crime_realtime","crime", modeldocument, overwrite_existing=True)

	#print "DONE - LAST STATEMENT"
	


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        filename='/home/ubuntu/crimeAnalysis/storm/logdetails/request_bolt.log',
        format="%(message)s",
        filemode='a'
    )

    RequestProcessingBolt().run()

