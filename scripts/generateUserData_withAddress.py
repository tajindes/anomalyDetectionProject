import sys;
from geopy.geocoders import Nominatim

inputfile = sys.argv[1];
file1 = open(inputfile, "r");
outputfile = sys.argv[2];
file2 = open(outputfile, "w");

line = file1.readline();
line = file1.readline();
geolocator = Nominatim()
#line = line.strip();
#temp_list = line.split(',');
#print 'temp_list is' + str(temp_list);

while(line):
    line = line.strip();
    temp_list = line.split(',');
    latitude = temp_list[13];
    longitude = temp_list[14];
    locationObj = "";
    try:
	locationObj = geolocator.reverse(latitude + ', ' + longitude, timeout=10)
    except:
	pass;
    zipVar = ""
    cityVar = ""
    stateVar = ""
    countryVar = ""

    try:
	zipVar = (locationObj.raw)['address']['postcode'].encode('utf-8')
    except:
	pass;

    try:
	cityVar = (locationObj.raw)['address']['city'].encode('utf-8')
    except:
	pass;

    try:
	stateVar = (locationObj.raw)['address']['state'].encode('utf-8')
    except:
	pass;

    try:
	countryVar = (locationObj.raw)['address']['country'].encode('utf-8')
    except:
	pass;

    file2.write(line + ", " + zipVar + ", " + cityVar + ", " + stateVar + ", " + countryVar + "\n");
    line = file1.readline();

file2.close();
file1.close();
