import json
import logging
import random
import time
import pyelasticsearch
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
	                  "crimelocation" : {
        	            "lat" : 34.0442,
                	    "lon" : -118.2519
	                  }
        	      }
	          }	
	      }
	  }
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


	#res = es.search('crimecode:354', index='crimes')
        log.debug("++++++++++++++++executing search query+++++++++++++++")
        res = es.search(query, index=INDEX_NAME)

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
	    
	

        #index = random.randint(0, hits_count - 1)
        #crime_id = hits[index]['_id']
	
	# send to kafka
        '''
	msg = {}
        msg['crime_id'] = crime_id
        msg['occupancy_status'] = 1

        crime_doc = {
            "is_occupied": "1"
        }

        crime_type = 'crime'
	'''
	
	#es.create_index("test12_index", settings=None)
	#delete it after testing -start
	#log.debug(parsed_msg['location_taj'])
	# delete it after testing - end

	# storing data in elastic search:
	#es = ElasticSearch('http://localhost:9200/')
	#es.index(', 'person', {'name': 'Joe Tester', 'age': 25, 'title': 'QA Master'}, id=1);

	try:
	    es.create_index("crimeanalysis", settings=None)
	except:
	    pass
	
	modeldocument = {
            "lat": parsed_msg['location']['latitude'],
            "lon": parsed_msg['location']['longitude'],
            "monthsDictionary": monthsDictionary
	}
	'''
	modeldocument = {
	    "lat": parsed_msg['location']['latitude'],
	    "lon": parsed_msg['location']['longitude'],
	    "jan": "11",
	    "feb":"22",
            "mar":"33",
            "apr":"44",
            "may":"55",
            "jun":"66",
            "jul":"77",
            "aug":"88",
            "sep":"99",
            "oct":"87",
            "nov":"76",
            "dec":"65",
            "jan1": "11",
            "feb1":"22",
            "mar1":"33",
            "apr1":"44",
            "may1":"55",
            "jun1":"66",
            "jul1":"77",
            "aug1":"88",
            "sep1":"99",
            "oct1":"87",
            "nov1":"76",
            "dec1":"65",
	}
	'''
	
	es.index("crimeanalysis","crime", modeldocument, overwrite_existing=True)

	'''	
        try:
            res = es.update(index="crimesanalysis",
                            id=crime_id,
                            doc="taj_doc",
                            doc_type=crime_type,
                            retry_on_conflict=2)

            log.debug("+++++++++++++++++++updated occupancy for crime %s++++++++++++++++++++\n", crime_id)
            log.debug(res)
        except Exception as e:
            log.error("++++++++++FAILED TO UPDATE OCCUPANCY+++++++++")
            log.error("%s\n", str(e))

            #
            # log.debug("+++++++++++++++++++sending occupancy_update event for crime %s++++++++++++++++++++\n", crime_id)
            # producer.send_messages(
            #     "occupancy_update",
            #     json.dumps(msg))
        
	'''
	#print "DONE - LAST STATEMENT"
	


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        filename='/home/ubuntu/crimeAnalysis/storm/logdetails/request_bolt.log',
        format="%(message)s",
        filemode='a'
    )

    RequestProcessingBolt().run()

