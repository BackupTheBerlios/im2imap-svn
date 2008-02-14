import os
import os.path
import shelve
import datetime
import imaplib
import time

class pidgin2imap:
	logdir="~/.purple/logs/"
	logdir=os.path.expanduser(logdir)


	persistantDataFile =  "~/.pidgin2imapdb"
	
	persistantData = shelve.open(os.path.expanduser(persistantDataFile))
	
	if not persistantData.has_key("filelist"):
		persistantData["filelist"]=[]
	
	fileList = persistantData["filelist"]

	def __init__(self,imapObject,debug):
		self.imapObject = imapObject
		self.debug = debug

	def parseLogs(self):
		if not os.path.exists(self.logdir):
			print "No logfiles available"
			return False

		if self.debug: print "[PIDGIN] LOGFILEDIR: " + self.logdir
		protocols = []
		protocols = os.listdir(self.logdir)
		
		if len(protocols) == 0:
			print "no protocols available"
			return False
		
		for protocol in protocols:
			accounts = os.listdir(os.path.join(self.logdir,protocol))
			for account in accounts:
				rosterItems = os.listdir(os.path.join(self.logdir,protocol,account))
				for contact in rosterItems:
			
					#don't archive offline/online notifications
					if contact == ".system":
						continue

					logItems =  os.listdir(os.path.join(self.logdir,protocol,account,contact))
					for logfile in logItems:
						fileName=os.path.join(self.logdir,protocol,account,contact,logfile)
						if fileName in self.fileList:
							pass
						else:
							if self.debug: print "[PIDGIN] filename not in List"
							self.fileList.append(fileName)
							in_file = open(fileName,"r")
							body = ""
							for line in in_file:
								body += line

							dateString = logfile[:-4]

							year = int(dateString[:4])
							month = int(dateString[5:7])
							day = int(dateString[8:10])
							

							hour = int(dateString[11:13])	
							minute = int(dateString[13:15])
							second = int(dateString[15:17])

							timeZone = dateString[17:25]


							date = datetime.datetime(year,month,day,hour,minute,second,0)
							self.imapObject.log2imap(contact,account,"[pidgin]",body,date,None)
							

		self.persistantData["filelist"]=self.fileList
		self.persistantData.close()


