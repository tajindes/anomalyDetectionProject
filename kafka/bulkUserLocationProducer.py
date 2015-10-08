#!/usr/bin/python

# Kafka producer that reads the input data in a loop in order to simulate real time events
import csv
import json
import sys
import time
import datetime
import random
#from geopy.geocoders import Nominatim
from kafka import KafkaClient, SimpleProducer


class Producer():
    def __init__(self, topic, source_file):
        self.topic = topic
        self.source_file = source_file
        with open("../config/config.json", 'rb') as file:
            self.config = json.load(file)

    def genData(self):
        with open(self.source_file) as f:
            reader = csv.DictReader(f)
            crimeLocations = list(reader)

        kafka_cluster = self.config['kafka_cluster']

        print "kafka_cluster is:" + kafka_cluster + " done";
        kafka_client = KafkaClient(kafka_cluster)
        kafka_producer = SimpleProducer(kafka_client)

        # To send messages synchronously
#        kafkaSimple = KafkaClient('52.10.17.219:9092')
#        producerSimple = SimpleProducer(kafkaSimple, async=True)
#	geolocator = Nominatim()
        count = 0
        while True:
        #while (count < 5):
            for loc in crimeLocations:
		
               	userID = loc["userID"]
		userName = loc["userName"]
	
		'''
		#date_rptd = loc["date_rptd"]
		date_rptd = str(datetime.datetime.now().month) + "/"  + str(datetime.datetime.now().day) + "/" + str(datetime.datetime.now().year);
		#time_rptd = loc["time_rptd"]
		time_rptd = str(datetime.datetime.now().hour).zfill(2) + str(datetime.datetime.now().minute).zfill(2);
		#dateTemp = datetime.datetime.strptime(date_rptd_raw, '%m/%d/%y').strftime('%Y-%m-%d')
		

		locationObj = "";
		#timestamp
		'''
		
                latitude = float(loc['latitude'])
                longitude = float(loc['longitude'])
                msg = {}
                msg['userID'] = userID
		msg['userName'] = userName
                location = {
                    'latitude': latitude,
                    'longitude': longitude
                }
		

                msg['location'] = location
		
		#time.sleep(10);
                kafka_producer.send_messages(self.topic, json.dumps(msg))
                #time.sleep(10);
                #producerSimple.send_messages(self.topic, json.dumps(msg))
                #producerSimple.send_messages('crimeLocation1', 'tajmessage1');
                
                print "sending location update for user %s" % userID
            count += 1

            print "+++++++++++++FINISH ROUND %d+++++++++++++++++" % count


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Usage: [*.py] [source-file]"
        sys.exit(0)
        # logging.basicConfig(filename='error.log',level=logging.DEBUG)

    # logger = logging.getLogger('geo_app')
    # # create file handler which logs even debug messages
    # fh = logging.FileHandler('geoupdate.log')
    # fh.setLevel(logging.INFO)
    # logger.addHandler(fh)
    producer = Producer(
        topic='user_rt',
        source_file=sys.argv[1]
    )

    producer.genData()
