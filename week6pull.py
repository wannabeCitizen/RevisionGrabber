#!/usr/bin/env python

# Coded by: Michael Skirpan
# For obtaining a folder of student folders, iterating over the folder's children for 'id'
# and 'title' to find the individual student folders, then listing the children of that folder,
# and getting a list of student journal files.  Finally, you can select journal file by title
# using a regex.

# Call __main__ with student or parent

from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from apiclient.discovery import build

import ujson as json
import os
import time
import httplib2
import sys
import requests
import re

#Get Credential object for making requests and return drive_service
def set_cred():
	print "pulling credentials"
	myCreds = Storage('my_credentials.json')
	credentials = myCreds.get()

	print "authorizing HTTP request"
	http = httplib2.Http()
	http = credentials.authorize(http)

	print "building API resource"
	drive_service = build('drive', 'v2', http=http)

	return drive_service

#Returns list of students with tuple of their individual folder IDs and names
def child_o_folder(credentials, ID):
	myChildren = credentials.children().list(folderId=ID).execute()
	people = []

	for child in myChildren['items']:
		myID = child['id']
		whostuff = credentials.files().get(fileId=myID).execute()
		name = whostuff['title']
		myTuple = (name, myID)
		people.append(myTuple)

	return people



#Takes a tuple with a person's name and folder ID - downloads files
def get_info(credentials, person):
	myName = person[0]
	myID = person[1]

	myPath = time.strftime("Week6/" + myName)


	myFiles = credentials.children().list(folderId=myID).execute()
	for hw in myFiles['items']:
		thisFile = hw['id']
		check = credentials.files().get(fileId=thisFile).execute()
		if re.search('6', check['title']):
			print 'found one!'
			try:
				link = check['exportLinks']['text/plain']
			except:
				print "Not a File"
				continue
			resp, myFile = credentials._http.request(link)
			fd = open(myPath, 'a+')
			fd.write(myFile)
			fd.close()
			print "Got %s Journal" % myName
			return
	print "%s had bad naming!" % myName






if __name__ == "__main__":
	folder = str(sys.argv[1])
	api_caller = set_cred()
	classList = child_o_folder(api_caller, folder)
	try:
		os.makedirs("Week6")
	except:
		print "directory already exists"

	for student in classList:
		get_info(api_caller, student)





