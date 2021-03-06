from app import app
from flask import render_template
import datetime
from elasticsearch import Elasticsearch
#from pyelasticsearch import ElasticSearch
from flask import render_template, jsonify, request, redirect
from random import randint
import json

es = Elasticsearch([
    "http://52.88.119.135:9200/",
    "http://52.11.180.149:9200/",
    "http://54.69.39.4:9200/"
  ])

@app.route('/')

@app.route('/index')
def index():
   #user = { 'nickname': 'Miguel' } # fake user
   return render_template("start.html", title = 'Home')


@app.route("/groupby_crimetype_month/<latitude>/<longitude>")
@app.route("/groupby_crimetype_month/<latitude>/<longitude>/<distance>")
@app.route("/groupby_crimetype_month/<latitude>/<longitude>/<distance>/<crimeToshow>")
def groupby_crimetype_month(latitude, longitude, distance = 50, crimeToshow = 10, processingType= "batch"):
	print "in groupby_crimetype_month function";
	currentDateStr = str(datetime.datetime.now().year) + "-" + str(datetime.datetime.now().month) + "-" + str(datetime.datetime.now().day)
	pastDateStr = str(datetime.datetime.now().year - 2) + "-" + str(datetime.datetime.now().month) + "-" + str(datetime.datetime.now().day)
	
	monthYearDict = {};

	lineChartResponse = {};
	lineChartResponse['x_axis'] = [];

	yearTemp = datetime.datetime.now().year;
	monthTemp = datetime.datetime.now().month;
	x_axisList = [];
	for countVar in range(0,24):
		if(monthTemp > 1):
			monthTemp = monthTemp - 1;
		elif(monthTemp == 1):
			monthTemp = 12;
			yearTemp = yearTemp - 1;
		else:
			print "ERROR. SHOULD NOT HAPPEN. CHAECK groupby_crimetype_month function in python script."

		monthYearDict[str(yearTemp) + "-" + str(monthTemp).zfill(2)] = 0.0;
		x_axisList.append(str(yearTemp) + "-" + str(monthTemp).zfill(2));

	lineChartResponse['x_axis'] = x_axisList[::-1];

	#print 'monthYearDict is:' + str(monthYearDict);
	#print 'latitude 1 is:' + latitude + ' and longitude is: ' + longitude;
	#print 'pastDateStr 1 is:' + pastDateStr + ' and currentDateStr is: ' + currentDateStr;
	
	res = es.search(index="crimes", body={
  "size" : 0,
  "query": {
   "filtered" : {
          "query" : {
             "range" : {
                "crime_rptd_ts" : { "from" : pastDateStr, "to" : currentDateStr }
              }
           },
          "filter" : {
              "geo_distance" : {
                  "distance" :  str(distance) + "km",
                  "crimelocation" : {
                    "lat" : latitude,
                    "lon" : longitude
                  }
              }
          }
      }
  },
  "aggs": {
    "group_by_crimetype": {
      "terms": {
        "field": "crimetype"
      },
      "aggs" : {
        "crimes_over_time" : {
            "date_histogram" : {
                "field" : "crime_rptd_ts",
                "interval" : "1M",
                "format" : "yyyy-MM-dd" 
            }
        }
      }
    }
  }
}, request_timeout=100);

	#print 'groupby_crimetype_month ==> res is:' + str(res);	
	#print "Got delay of %d minuts:" % res['aggregations']['avg_timediff_mil_seconds']['value']
	
	totalCrimes = 	res['hits']['total']

	crimeCountResponse = [];
	for crimeObj in res['aggregations']['group_by_crimetype']['buckets']:
		#print 'crimeObj is'+str(crimeObj);
		keyVar = crimeObj['key']
		#doc_countVar = crimeObj['doc_count']
		crimeObjTemp = {};
		crimeObjTemp['name'] = keyVar;
		crimeCountList = [];

		for timeObj in crimeObj['crimes_over_time']['buckets']:
			monthyearVar = timeObj['key_as_string']
			#print 'monthYearVar is:' + str(monthyearVar);
			monthyearVar = monthyearVar[:-3]
			#print 'now monthyearVar is:' + str(monthyearVar);
			monthYearDict[monthyearVar] = timeObj['doc_count']
			
		for key in sorted(monthYearDict.keys(), reverse=True):
			#print 'monthYearDict key is:' + str(key) + ' and value is:' + str(monthYearDict[key]);
			crimeCountList.append(monthYearDict[key]);
		
		#print 'monthYearDict is:' + str(monthYearDict);
		crimeObjTemp['data'] = crimeCountList;
		crimeCountResponse.append(crimeObjTemp);

	lineChartResponse['crimeLineGraphObj'] = crimeCountResponse;
	#print 'crimeCountResponse is:' + str(crimeCountResponse);
	return jsonify(lineChartResponse=lineChartResponse)







@app.route("/groupby_crimetype/<latitude>/<longitude>")
@app.route("/groupby_crimetype/<latitude>/<longitude>/<distance>")
@app.route("/groupby_crimetype/<latitude>/<longitude>/<distance>/<crimeToshow>")
def groupby_crimetype(latitude, longitude, distance = 50, crimeToshow = 10, processingType= "batch"):
	currentDateStr = str(datetime.datetime.now().year) + "-" + str(datetime.datetime.now().month) + "-" + str(datetime.datetime.now().day)
	pastDateStr = str(datetime.datetime.now().year - 2) + "-" + str(datetime.datetime.now().month) + "-" + str(datetime.datetime.now().day)
	
	print 'latitude is:' + latitude + ' and longitude is: ' + longitude;
	print 'pastDateStr is:' + pastDateStr + ' and currentDateStr is: ' + currentDateStr;

	res = es.search(index="crimes", body={
	"size" : 0,
  "query": {
   "filtered" : {
          "query" : {
             "range" : {
                "crime_rptd_ts" : { "from" : pastDateStr, "to" : currentDateStr }
              }
           },
          "filter" : {
              "geo_distance" : {
                  "distance" :  str(distance) + "km",
                  "crimelocation" : {
                    "lat" : latitude,
                    "lon" : longitude
                  }
              }
          }
      }
  },
  "aggs": {
    "group_by_crimetype": {
      "terms": {
        "field": "crimetype"
      }
    }
  }
}, request_timeout=100);

	print 'res is:' + str(res);	
	#print "Got delay of %d minuts:" % res['aggregations']['avg_timediff_mil_seconds']['value']
	
	totalCrimes = 	res['hits']['total']
	delay = 0.0;
	crimeTypeResponse = [];
	try:
		for crimeObj in res['aggregations']['group_by_crimetype']['buckets']:
			print 'crimeObj is'+str(crimeObj);

			keyVar = crimeObj['key']
			doc_countVar = crimeObj['doc_count']
			crimeObjTemp = {};
			crimeObjTemp['crimetype'] = keyVar;
			crimeObjTemp['crimecount'] = doc_countVar;
			crimeTypeResponse.append(crimeObjTemp);
	except:
		pass;

	print 'crimeTypeResponse is' + str(crimeTypeResponse);
	return jsonify(crimeTypeResponse=crimeTypeResponse)


@app.route("/crimebatchprocessing/<latitude>/<longitude>")
@app.route("/crimebatchprocessing/<latitude>/<longitude>/<distance>")
@app.route("/crimebatchprocessing/<latitude>/<longitude>/<distance>/<crimeToshow>")
def crimesBatchStatistics(latitude, longitude, distance = 50, crimeToshow = 10, processingType= "batch"):
	print 'inside crimesBatchStatistics function';
	currentDateStr = str(datetime.datetime.now().year) + "-" + str(datetime.datetime.now().month) + "-" + str(datetime.datetime.now().day)
	pastDateStr = str(datetime.datetime.now().year - 2) + "-" + str(datetime.datetime.now().month) + "-" + str(datetime.datetime.now().day)
	#latitude = "42.12401098736007"
	#longitude = "-80.89949698937326"
    
	#latitude = request.form["latitudeName"]
	#longitude = request.form["longitudeName"]
	print 'latitude is:' + str(latitude) + ' and longitude is: ' + str(longitude);
	print 'pastDateStr is:' + str(pastDateStr) + ' and currentDateStr is: ' + str(currentDateStr);

	res = es.search(index="crimes", body={
	"size" : crimeToshow,
  "query": {
   "filtered" : {
          "query" : {
             "range" : {
                "crime_rptd_ts" : { "from" : pastDateStr, "to" : currentDateStr }
              }
           },
          "filter" : {
              "geo_distance" : {
                  "distance" :  str(distance) + "km",
                  "crimelocation" : {
                    "lat" : latitude,
                    "lon" : longitude
                  }
              }
          }
      }
  },
   "aggregations": {
    "avg_timediff_mil_seconds": {
       "avg": {
          "script": "(doc.crime_rptd_ts.value - doc.crime_ts.value)/(1000*60)"
       }
    }
 }
}, request_timeout=100);

	print 'res is:' + str(res);	
	#print "Got delay of %d minuts:" % res['aggregations']['avg_timediff_mil_seconds']['value']
	
	totalCrimes = 	res['hits']['total']
	delay = 0.0;
	try:
		delay = float(res['aggregations']['avg_timediff_mil_seconds']['value'])
	except:
		pass;
	delay = delay/60.0;

	crimesArray = [];
	for hit in res['hits']['hits']:
	    #print("%(timestamp)s %(author)s: %(text)s" % hit["_source"])
		print("source output is: " +  str(hit["_source"]['crimelocation']))
		crimesArray.append(str(hit["_source"]['crimelocation']));
	
	#jsonresponse = {"crime_rptd_ts": str(hit["_source"]['crime_rptd_ts']}
	

	jsonresponse = {"latitude": latitude, "longitude" : longitude, "totalCrimes": totalCrimes, "distance": distance, "delay": delay, "crimeToshow": crimeToshow, "crimesArray": crimesArray}
	if ("real" == processingType):
		return jsonresponse;
	else:
		return jsonify(crimesBatchObj=jsonresponse)

	#return render_template("index_results.html", title = 'Home', jsonresponse = jsonresponse, originalLatitude = latitude, originalLongitude = longitude)


@app.route("/gotoHomepage", methods=['POST'])
@app.route("/gotoHomepage")
def gotoHomepage():	
	#print 'tajinder homepage'
 	return render_template("homepage.html")

@app.route("/gotoIndexpage", methods=['POST'])
@app.route("/gotoIndexpage")
def gotoIndexpage():
        #print 'tajinder homepage'
        return render_template("index.html")


@app.route("/subscribeUser/<username>/<latitude>/<longitude>")
def subscribeUserFunction(username, latitude, longitude):	
	print 'inside subscribeUser function'
	
	userID = "user" + str(randint(1,99999999));
	userlocationVar = { "lat": latitude, "lon": longitude }
	
	doc = {
	    'userID': userID,
	    'userName': username,
	    'userlocation': userlocationVar,
	}
	
	res = es.index(index="crime-subscribe-users", doc_type='crime', body=doc);
	#res['created'] = true    # if the document got indexed successfully.
	isSubscribed = res['created']
	jsonresponse = { "username":username, "latitude":latitude,"longitude":longitude, "created": res['created'] }
	#jsonresponse = { "tajID": "tajValue", "username":username, "latitude":latitude,"longitude":longitude }
	#if(isSubscribed == False):
	#	return jsonify(userResponse=jsonresponse)
	return jsonify(userResponse=jsonresponse)
	#return redirect("homepage.html")
	#return render_template("homepage.html")


@app.route("/submitcrime/")
@app.route("/submitcrime/<crimetype>/<latitude>/<longitude>")
def submitcrime_rtFunction(crimetype, latitude, longitude):	
	print 'inside submitcrime_rt function'
	#return jsonify(userResponse='tajindertesting') # jsonify(crimeResponse="insdie submitcrime_rt")

	crime_id = "crime" + str(randint(1,99999999));
	crimelocationVar = { "lat": latitude, "lon": longitude }
	crime_rptd_ts = str(datetime.datetime.now().year) + "-" + str(datetime.datetime.now().month) + "-" + str(datetime.datetime.now().day) + "T" +  str(datetime.datetime.now().hour) + ":" + str(datetime.datetime.now().minute) + ":"+ str(datetime.datetime.now().second) + "Z"

	doc = {
		'crime_rptd_ts': crime_rptd_ts,
	    'crime_id': crime_id,
	    'crimetype': crimetype,
	    'crimelocation': crimelocationVar
	}
	
	res = es.index(index="crime_realtime", doc_type='crime', body=doc);
	
	jsonresponse = { "crime_rptd_ts": crime_rptd_ts, "crime_id": crime_id, "crimetype": crimetype, "crimelocation":crimelocationVar, "created" : res['created'] }
	return jsonify(crimeResponse=jsonresponse)

@app.route("/getCurrentCrimes/")
def getCurrentCrimes():
	print 'inside getCurrentCrimes function'
	secondVar = "00";
	
	if(datetime.datetime.now().second > 10):
		print 'datetime.dateimte.now().second is: ' + str(datetime.datetime.now().second);
		secondsVar = str(datetime.datetime.now().second - 10).zfill(2);
		print 'after second is:' + secondsVar;
	
	currentDateStr = str(datetime.datetime.now().year) + "-" + str(datetime.datetime.now().month) + "-" + str(datetime.datetime.now().day) + "T" +  str(datetime.datetime.now().hour) + ":" + str(datetime.datetime.now().minute) + ":"+ str(datetime.datetime.now().second) + "Z"
	pastDateStr = str(datetime.datetime.now().year) + "-" + str(datetime.datetime.now().month) + "-" + str(datetime.datetime.now().day) + "T" +  str(datetime.datetime.now().hour) + ":" + str(datetime.datetime.now().minute) + ":"+ str(secondVar) + "Z"

	res = es.search(index="crime_realtime", body={
	"size" : 1,
	  "query": {
	   "filtered" : {
	        "query" : {
	          "range" : {
	            "crime_rptd_ts" : { "from" : pastDateStr, "to" : currentDateStr }
	          }
	        }
	    }
	  }
	},request_timeout=100);

	crimetypeVar = "";
	crime_rptd_tsVar = "";
	latitudeVar ="";
	longitudeVar = "";

	resultLength = len(res['hits']['hits'])
	jsonresponse = {}
	if (resultLength ==1):
		crimetypeVar = 	res['hits']['hits'][0]['_source']['crimetype']
		crime_rptd_tsVar = 	res['hits']['hits'][0]['_source']['crime_rptd_ts']
		latitudeVar = 	res['hits']['hits'][0]['_source']['crimelocation']['lat']
		longitudeVar = 	res['hits']['hits'][0]['_source']['crimelocation']['lon']

		#print 'result of search query is:' + str(res);
		#print 'crimetypeVar is:'+ crimetypeVar + ' and crime_rptd_tsVar is:' + crime_rptd_tsVar
		#print ' and crimelocationVar is: ' + str(latitudeVar) + ', ' + str(longitudeVar);

		jsonresponse = crimesBatchStatistics(latitudeVar, longitudeVar, 100, 10, "real");
		#print 'crimeOutput_rt is:' + str(jsonresponse);
		#print 'crimeOutput_rt delay is:' + str(jsonresponse['delay']);

		userResult = es.search(index="crime-subscribe-users", body={
		 "query": {
		   "filtered" : {
		          "query" : {
		            "match_all" : { }
		           },
		          "filter" : {
		              "geo_distance" : {
		                  "distance" : "100km",
		                  "userlocation" : {
		                    "lat" : latitudeVar,
		                    "lon" : longitudeVar
		                  }
		              }
		          }
		      }
		  }
		},request_timeout=100);
		userArray = [];
		userResultLength = len(userResult['hits']['hits'])
		#print "userResultLength is: " + str(userResultLength);
		if( 0 < userResultLength):
			for userObject in userResult['hits']['hits']:
				userIdVar = userObject['_source']['userID'];
				usernameVar = userObject['_source']['userName'];
				userTemp = { "userID": userIdVar, "userName" : usernameVar }
				userArray.append(userTemp);
		
		jsonresponse['userList'] = userArray;

	return jsonify(crimeRealObj=jsonresponse)
