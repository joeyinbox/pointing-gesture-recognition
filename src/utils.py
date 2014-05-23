#! /usr/bin/python


# Write array values to a file
def writeToFile(data):
    f = open('result.txt','w')
    for x in xrange(len(data)):
        f.write("[")
        for y in xrange(len(data[0])):
            f.write(("%.3f,"%(data[x,y])))
        f.write("]\n")