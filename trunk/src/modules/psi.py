import random
import os
import os.path
import shelve
import time
import datetime
from urllib import unquote

class fileObject:
	fileName = ""
	randomNumber = 0

	def __init__(self,fileName,randomNumber):
		self.fileName = fileName
		self.randomNumber = randomNumber

class psi2imap:
	
	#
	# psi has just one big file for every contact. 
	# im2imap uses ids (random numbers) to track which logfiles are already processed.
	# the id is saved in the "cc" header field.
	# if im2imap wants to push a new logfile to our imap-server, it looks there first for a message
	# with cc=$id. if a logfile with that id exists already, im2imap deletes it and the new lookfile will be uploaded...
	# the ids are stored in .psi2imapdb and are generated when a logfile is discoverd which has no entry in .psi2imapdb.
	
	
	logdir="~/.psi/profiles/"
	logdir=os.path.expanduser(logdir)


	persistantDataFile =  "~/.psi2imapdb"
	
	persistantData = shelve.open(os.path.expanduser(persistantDataFile))
	
	if not persistantData.has_key("filehash"):
		persistantData["filehash"]={}
	
	fileHash = persistantData["filehash"]



	def __init__(self,imapObject,debug):
		random.seed(None)
		self.imapObject = imapObject
		self.debug = debug

	def parseLogs(self):
		if not os.path.exists(self.logdir):
			return false

		if self.debug: print "[PSI] LOGFILEDIR: " + self.logdir
		accounts = []
		accounts = os.listdir(self.logdir)
		
		if len(accounts) == 0:
			print "no accounts available"
			return false
		
		for account in accounts:
			account = os.path.join(account,"history")
			contacts = os.listdir(os.path.join(self.logdir,account))
			for contact in contacts:
				contactName = unquote(contact)[:-8]
				fileName=os.path.join(self.logdir,account,contact)
				
				if self.fileHash.has_key(fileName):
					if os.path.getsize(fileName) > self.fileHash[fileName][1]:
						if self.debug: print "[PSI]" + fileName
						self.imapObject.delete(self.fileHash[fileName][0])
	
						in_file = open(fileName,"r")
						body=""
						for line in in_file:
							body+=line
						self.imapObject.log2imap(contactName,account,"[psi]",body,datetime.datetime(2000,1,1),self.fileHash[fileName][0])
						self.fileHash[fileName][1] = os.path.getsize(fileName)

				else:
					if seld.debug: print "[PSI] filename not in List"
					self.fileHash[fileName]=[int(random.random()*1000000000),os.path.getsize(fileName)]
					in_file = open(fileName,"r")
					body=""
					for line in in_file:
						body+=line

					self.imapObject.log2imap(contactName,account,"[psi]",body,datetime.datetime(2000,1,1),self.fileHash[fileName][0])
							
		self.persistantData["filehash"]=self.fileHash
		self.persistantData.close()
