from sys import argv
import random;
#script, filename = argv

#print "We're going to erase %r." % filename
#print "If you don't want that, hit CTRL-C (^C)."
#print "If you do want that, hit RETURN."

#raw_input("?")

print "Opening the file..."
target = open('test.txt', 'w')

print "Truncating the file.  Goodbye!"
target.truncate()

print "Now I'm going to ask you for three lines."

''' line1 = raw_input("line 1: ")
line2 = raw_input("line 2: ")
line3 = raw_input("line 3: ")
'''
crimeTypeArray = ["Robbery","Robbery","Battery","Burglary","Criminal Threats","Vandalism","Traffic Dr","Vehicle Stolen","Abusement","Abusement"];

for i in range(0, 6644):
	index = random.randrange(0,9);
	line1 = str(crimeTypeArray[index]);
	target.write(line1)
	target.write("\n")


print "I'm going to write these to the file."

'''target.write(line2)
target.write("\n")
target.write(line3)
target.write("\n")
'''

print "And finally, we close it."
target.close()