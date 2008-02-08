#!/usr/bin/python


#####################################################################
# Copyright (C) 2007 Sebastian Moors <mauser@smoors.de>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published
# by the Free Software Foundation; version 2 only.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
####################################################################




import sys
import os
import os.path
import imaplib
import shelve
import getopt
import ConfigParser
import time

sys.path.append("/usr/lib/im2imap/modules")

DEBUG = False

class imap:
	imapObject = None

	def __init__(self,user,pwd,server,mailbox):
		self.imapObject = imaplib.IMAP4_SSL(server)
		self.imapObject.login(user,pwd)
		self.imapObject.select(mailbox)

	def log2imap(self,headerFrom,headerTo,subject,body,date,id):
		if not id == None:
			mail = "From: %s\nTo: %s\nSubject: %s\nDate: %s\nCC: %s\n\n" % (headerFrom,headerTo,subject,date.ctime(),id)
		else:
			mail = "From: %s\nTo: %s\nSubject: %s\nDate: %s\n\n" % (headerFrom,headerTo,subject,date.ctime())
			
		mail += "\n" + body
		self.imapObject.append("im_mailbox",None,time.time(),mail)

	def delete(self,id):
		id=str(int(id))
		searchString = '(CC ' +  id  + ' )'
		print searchString
		typ, data = self.imapObject.search(None, searchString)
		print typ,data
		for num in data[0].split():
			self.imapObject.store(num, '+FLAGS', '\\Deleted')
		self.imapObject.expunge()	

	def logout(self):
		self.imapObject.close()
		self.imapObject.logout()


supportedClients = ["pidgin","psi","kopete"]
client="";


#read configuration file
config = ConfigParser.ConfigParser()

fname = os.path.expanduser("~/.im2imaprc")

if not os.path.isfile(fname):
	print fname + "does not exists, creating sample configuration"


config.readfp(open(fname))



#parse commandline arguments
try:
	long_opts=["client"]
	opts, args = getopt.getopt(sys.argv[1:], "c:d" )
except getopt.GetoptError:
	sys.exit(2)

for option, argument in opts:
	
	# -c , --client: defines which logfiles should be archived (for example "psi","pidgin")
	if option in ("-c"):
		if argument not in supportedClients:
			print "%s is not supported." % argument
			sys.exit(1)
		else:
			client = argument

	# -d , --debug: enable debug output
	if option in ("-d"):
			DEBUG = True
	

#no client was specified, exit
if  client not in supportedClients:
	print " No valid client specified. Exmaple: im2imap -c pidgin"
	sys.exit(1)


#get imap configuration settings
imapUser = config.get("Imap","user")
imapPassword = config.get("Imap","password")
imapMailbox = config.get("Imap","mailbox")
imapServer = config.get("Imap","server")


if client == "pidgin":
	from pidgin import pidgin2imap
	
	i=imap(imapUser,imapPassword,imapServer,imapMailbox)
	
	if DEBUG: print "client is pidgin"
	g=pidgin2imap(i)
	g.parseLogs()

if client == "psi":
	from psi import psi2imap
		
	
	i=imap(imapUser,imapPassword,imapServer,imapMailbox)
	
	if DEBUG: print "client is psi"
	p=psi2imap(i)
	p.parseLogs()
	
if client == "kopete":
	from kopete import kopete2imap
	
	i=imap(imapUser,imapPassword,imapServer,imapMailbox)
	
	if DEBUG: print "client is kopete"
	k=kopete2imap(i)
	
	k.parseLogs()
