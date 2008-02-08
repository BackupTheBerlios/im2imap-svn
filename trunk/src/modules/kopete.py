import random
import os
import os.path
import shelve
import time
import datetime
from urllib import unquote
import glob



class kopete2imap:
	logdir="~/.kde/share/apps/kopete/logs/"
	logdir=os.path.expanduser(logdir)


	persistantDataFile =  "~/.kopete2imapdb"
	
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

		if self.debug: print "[KOPETE] LOGFILEDIR: " +  self.logdir
		protocols = []
		protocols = os.listdir(self.logdir)
		
		if len(protocols) == 0:
			print "no protocols available"
			return false
		
		for protocol in protocols:
			accounts =  os.listdir(os.path.join(self.logdir,protocol))
			for account in accounts:
				contacts = glob.glob(os.path.join(self.logdir,protocol,account,"*.xml"))
				for contact in contacts:
					f=os.path.basename(contact)
					contactName = f[:f.find(".")].replace("-",".")
					fileName = os.path.join(self.logdir,protocol,account,contact)
					os.system("/usr/lib/im2imap/tools/kopeteXmlConverter.py " + fileName ) 
					if self.fileHash.has_key(fileName):
						if os.path.getsize(fileName) > self.fileHash[fileName][1]:
							self.imapObject.delete(self.fileHash[fileName][0])
							

							in_file = open(fileName[:-4],"r")
							body=""
							for line in in_file:
								body+=line

							self.imapObject.log2imap(contactName,account,"[kopete]",body,datetime.datetime(2000,1,1),self.fileHash[fileName][0])
							self.fileHash[fileName][1] = os.path.getsize(fileName)

					else:
						if self.debug: print "[KOPETE] filename not in List"
						self.fileHash[fileName]=[int(random.random()*1000000000),os.path.getsize(fileName)]
						in_file = open(fileName[:-4],"r")
						body=""
						for line in in_file:
							body+=line

						self.imapObject.log2imap(contactName,account,"[kopete]",body,datetime.datetime(2000,1,1),self.fileHash[fileName][0])
							
		self.persistantData["filehash"]=self.fileHash
		self.persistantData.close()
