import json
import logging
import random
import time
import pyelasticsearch
from datetime import datetime 
from pyleus.storm import SimpleBolt

from kafka import KafkaClient, SimpleProducer

#INDEX_NAME = 'crime_index'
INDEX_NAME = 'crime-subscribe-users'
QUERY_SIZE = 10

with open("/home/ubuntu/crimeAnalysis/config/config.json", 'rb') as file:
    config = json.load(file)

# GOTCHA:
# have to include "http://" and ends with "/", else will throw error
ELASTIC_SEARCH_CLUSTER = config['es_cluster']

KAFKA_CLUSTER = config['kafka_cluster']

log = logging.getLogger("user_rt_processing_topology.user_bolt")

es = pyelasticsearch.ElasticSearch(urls=ELASTIC_SEARCH_CLUSTER)
kafka_client = KafkaClient(hosts=KAFKA_CLUSTER)
producer = SimpleProducer(kafka_client)


class userProcessingBolt(SimpleBolt):
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


	#res = es.search('crimecode:354', index='crimes')
        log.debug("++++++++++++++++executing search query+++++++++++++++")


	try:
	    es.create_index("crime-subscribe-users", settings=None)
	except:
	    pass
	

	
	userlocation = {
            "lat": parsed_msg['location']['latitude'],
            "lon": parsed_msg['location']['longitude']
        }

	modeldocument = {
	    "userID":parsed_msg['userID'],
	    "userName":parsed_msg['userName'],
	    "userlocation": userlocation
	}

	
	es.index("crime-subscribe-users","crime", modeldocument, overwrite_existing=True)
	
	#print "DONE - LAST STATEMENT"
	


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        filename='/home/ubuntu/crimeAnalysis/storm/logdetails/request_bolt.log',
        format="%(message)s",
        filemode='a'
    )

    userProcessingBolt().run()

