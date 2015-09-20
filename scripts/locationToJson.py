#!/usr/bin/python
import csv
import json
import sys

__author__ = 'myho'

filename = sys.argv[1]
output = sys.argv[2]

def extractOnlyInitialLocationIntoJson(filename, output):
    with open(filename, 'rb') as file:
        reader = csv.reader(file)
        locations = list(reader)

    locationsMap = []
    for loc in locations:
        crimeId = loc[0]
        latitude = loc[1]
        longitude = loc[2]
        data = {}
        data['crimeId'] = crimeId
        data['latitude'] = latitude
        data['longitude'] = longitude
        locationsMap.append(data)

    print json.dumps(locationsMap)

    with open(output, 'wb') as outfile:
        json.dump(locationsMap, outfile)

extractOnlyInitialLocationIntoJson(filename, output)
