#!/usr/bin/python

#This file is for parsing a document based on a field in a text file.
#The parser is written with the expectation that we are collecting
#data from a Google Doc that we have downloaded the .txt file of and are
#trying to obtain specific information.

import re
import os
import sys
import json

def parseMe(myFile, field):
	print "Printing all %s fields from %s by team" % (field, myFile)

	jsonRep = {}

	with open(myFile, "r") as pd:
		for line in pd:
			myString = ""
			if re.match('Team', line):
				keyV = line.strip() 
			elif re.match(field, line):
				blank = False
				while not blank:
					nextLine = pd.next()
					if nextLine == "\n":
						blank = True
					else:
						myString += nextLine.strip()
				jsonRep[keyV] = myString

	myJson = json.dumps(jsonRep)
	print myJson

def parseTeam(myFile, team):
	print "Printing all objectives for %s from %s \n" % (team, myFile)

	jsonRep = {}
	myTeam = ""

	with open(myFile, "r") as pd:
		for line in pd:
			if re.match(team, line):
				myTeam = line.strip()
				while nextLine != "\n":
					nextLine = pd.next()
					jsonRep['members'] += nextLine.strip() 
				#print line
				nextTeam = False
				while not nextTeam:
					nextLine = pd.next()
					if re.match("Team", nextLine):
						nextTeam = True
					else:
						goodLines(nextLine)
					
	def goodLines(line):
		while line != "\n":


		elif nextLine == "\n":
			newVal = pd.next().strip()
		else:
			print nextLine.strip()
			



if __name__ == "__main__":
	theFile = str(sys.argv[1])
	theField = str(sys.argv[2])
	if re.match("Team", theField):
		parseTeam(theFile, theField)
	else:
		parseMe(theFile, theField)

