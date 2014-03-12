#!/usr/bin/python

#For use with Google Docs API
#Authenticate with OAuth2 Credentials
#Get JSON list of JSON blobs for Revision history on a file
#Save JSON Blobs in accordance with file

from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from apiclient.discovery import build
import ujson as json
import os
import time
import httplib2
import sys
import requests

def revJSON(file_ID, file_Name):
	print "pulling credentials"
	myCreds = Storage('my_credentials.json')
	credentials = myCreds.get()

	print "authorizing HTTP request"
	http = httplib2.Http()
	http = credentials.authorize(http)

	print "building API resource"
	drive_service = build('drive', 'v2', http=http)

	print "calling API"
	revisions = drive_service.revisions().list(fileId=file_ID).execute()

	data_file = time.strftime("Challenges/" + file_Name + ".json")

	try:
		directory = os.path.dirname(data_file)
		os.makedirs(directory)
	except:
		print "directory already exists"


	rev =  open(data_file, "a+")
	jRevs = json.dump(revisions, rev)
	rev.close()

	print "Saved %s" % file_Name


if __name__ == "__main__":
	myFile = str(sys.argv[1])
	fileName = str(sys.argv[2])
	revJSON(myFile, fileName)
