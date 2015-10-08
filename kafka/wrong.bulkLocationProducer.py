#!/usr/bin/python

# Kafka producer that reads the input data in a loop in order to simulate real time events
import csv
import json
import sys
import time
import datetime
import java.util.Random;
#from geopy.geocoders import Nominatim
from kafka import KafkaClient, SimpleProducer


class Producer():
    def __init__(self, topic, source_file):
        self.topic = topic
        self.source_file = source_file
        with open("../config/config.json", 'rb') as file:
            self.config = json.load(file)
    /**
     * Returns a pseudo-random number between min and max, inclusive.
     * The difference between min and max can be at most
     * <code>Integer.MAX_VALUE - 1</code>.
     *
     * @param min Minimum value
     * @param max Maximum value.  Must be greater than min.
     * @return Integer between min and max, inclusive.
     * @see java.util.Random#nextInt(int)
     */
    public static int randInt(int min, int max) {

        // NOTE: This will (intentionally) not run as written so that folks
        // copy-pasting have to think about how to initialize their
        // Random instance.  Initialization of the Random instance is outside
        // the main scope of the question, but some decent options are to have
        // a field that is initialized once and then re-used as needed or to
        // use ThreadLocalRandom (if using at least Java 1.7).
        Random rand = new Random();

        // nextInt is normally exclusive of the top value,
        // so add 1 to make it inclusive
        int randomNum = rand.nextInt((max - min) + 1) + min;

        return randomNum;
    }

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
        #while True:
        while (count < 5):
            for loc in crimeLocations:
#                print loc.keys()
                #print "loc is :" + str(loc) + " and loc.keys() is: " + str(loc.keys);
                #print "kafka.conn is: " + kafka_producer.conn;
		
                crimeId = loc["crime_id"]
		crimeType = loc["crimeType"]
		#date_rptd = loc["date_rptd"]
		date_rptd = str(datetime.datetime.now().month) + "/"  + str(datetime.datetime.now().day) + "/" + str(datetime.datetime.now().year);
		#time_rptd = loc["time_rptd"]
		time_rptd = str(datetime.datetime.now().hour).zfill(2) + str(datetime.datetime.now().minute).zfill(2);
		#dateTemp = datetime.datetime.strptime(date_rptd_raw, '%m/%d/%y').strftime('%Y-%m-%d')
		locationObj = "";
		'''
		try:
		    locationObj = geolocator.reverse(loc['latitude'] + ", " + loc['longitude'])
		except:
		    pass;
		'''
		#timestamp
                latitude = float(loc['latitude'])
                longitude = float(loc['longitude'])
                msg = {}
                msg['crime_id'] = crimeId
                location = {
                    'latitude': latitude,
                    'longitude': longitude
                }
		String[] statesArray = {"Alabama","Alaska","Arizona","Arkansas","California","Colorado","Connecticut","Delaware","Florida","Georgia","Hawaii","Idaho","Illinois","Indiana","Iowa","Kansas","Kentucky","Louisiana","Maine","Maryland""Massachusetts","Michigan","Minnesota","Mississippi","Missouri","Montana","Nebraska","Nevada","New Hampshire","New Jersey","New Mexico","New York","North Carolina","North Dakota","Ohio","Oklahoma","Oregon","Pennsylvania","Rhode Island","South Carolina","South Dakota","Tennessee","Texas","Utah","Vermont","Virginia","Washington","West Virginia","Wisconsin","Wyoming"};
                msg['location'] = location
		msg['crimetype'] = crimeType
		msg['date_rptd'] = date_rptd
		msg['time_rptd'] = time_rptd
		msg['zip']= ""
		msg['city']=""
		msg['state']=statesArray[randInt(0,49)]
		msg['country']="usa"
		'''
		try:
		    msg['zip'] = (locationObj.raw)['address']['postcode'].encode('utf-8')		
		except:
		    pass;
		try:
		    msg['city'] = (locationObj.raw)['address']['city'].encode('utf-8')
		except:
		    pass;
		try:
		    msg['state'] = (locationObj.raw)['address']['state'].encode('utf-8')
		except:
		    pass;
		try:
		    msg['country'] = (locationObj.raw)['address']['country'].encode('utf-8')
		except:
		    pass;
		'''
		#time.sleep(10);
                kafka_producer.send_messages(self.topic, json.dumps(msg))
                time.sleep(10);
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
        topic='test18',
        source_file=sys.argv[1]
    )

    producer.genData()
