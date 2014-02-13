#!/usr/bin/python

#For use with Google Docs API
#Authenticate with OAuth2 Credentials
#Get JSON list of JSON blobs for Revision history on a file
#Loop over items in API reponse to get files
#Download and save .txt files in a directory for the GDoc

from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from apiclient.discovery import build
import ujson as json
import os
import time
import httplib2
import sys
import requests

def revFile(file_ID):
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

	data_file = time.strftime("Hackathons/" + file_ID + "/revision_")

	try:
		directory = os.path.dirname(data_file)
		os.makedirs(directory)
	except:
		print "directory already exists"

	
	count = 0
	for item in revisions['items']:
		fd = open(data_file + "%d" % count, "a+")
		print item['id']
		fileLocation = item['exportLinks']['text/plain']
		myFile = requests.get(fileLocation)
		fd.write(myFile.content)
		fd.close()
		count += 1
	print "Saved %d revisions" % count


if __name__ == "__main__":
	revFile(str(sys.argv[1]))





