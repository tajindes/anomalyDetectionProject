#!/usr/bin/python

# Kafka producer that reads the input data in a loop in order to simulate real time events
import csv
import json
import sys

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

        count = 0
        # while True:
        while (count < 2):
            for loc in crimeLocations:
#                print loc.keys()
                #print "loc is :" + str(loc) + " and loc.keys() is: " + str(loc.keys);
                #print "kafka.conn is: " + kafka_producer.conn;
                crimeId = loc["crime_id"]
                latitude = float(loc['latitude'])
                longitude = float(loc['longitude'])
                msg = {}
                msg['crime_id'] = crimeId
                location = {
                    'latitude': latitude,
                    'longitude': longitude
                }
                msg['location'] = location
                kafka_producer.send_messages(self.topic, json.dumps(msg))
                
                #producerSimple.send_messages(self.topic, json.dumps(msg))
                #producerSimple.send_messages('crimeLocation1', 'tajmessage1');
                
                print "sending location update for crime %s" % crimeId
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
        topic='crimeLocation1',
        source_file=sys.argv[1]
    )

    producer.genData()
