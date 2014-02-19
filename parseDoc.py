#!/usr/bin/python

#This file is for parsing a document based on a field in a text file.
#The parser is written with the expectation that we are collecting
#data from a Google Doc that we have downloaded the .txt file of and are
#trying to obtain specific information.

import re
import os
import sys
import json

def parseMe(myFile):
	print "Creating a JSON object out of %s" % myFile

	jsonRep = {}

	with open(myFile, "r") as pd:
		currTeam = ""
		for line in pd:
			if re.match('Team', line):
				currTeam = line.strip()
				teamDict = parseTeam(pd)
				jsonRep[currTeam] = teamDict
			elif line == "\n":
				continue
			else:
				newSegment = parseSegment(pd, line)
				jsonRep[currTeam].update(newSegment)

	myJson = json.dumps(jsonRep)
	print myJson

def parseTeam(currFile):
	team = {}
	team['members'] = ""
	nextLine = currFile.next()
	while nextLine != "\n":
		team['members'] += nextLine.strip()
		nextLine = currFile.next()
	return team

def parseSegment(currFile, thisLine):
	newSeg = {}
	myVal = thisLine.strip()
	newSeg[myVal] = ""
	nextLine = currFile.next()
	while nextLine != "\n":
		newSeg[myVal] += nextLine.strip()
		try:
			nextLine = currFile.next()
		except:
			print "End of File"
			break
	return newSeg

	

if __name__ == "__main__":
	theFile = str(sys.argv[1])
	parseMe(theFile)

