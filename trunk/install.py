#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# im2imap installer by Sebastian Moors, 01.01.2007
#

import sys
import os
import shutil

import fileinput
from os.path import join

import os

#Warning! This directory will be deleted (if it exists)
LIB_DIR="/usr/lib/im2imap"

print "Welcome to the im2imap Installer.This is free software,you can (re)distribute it under the terms of the GPL\n";

if os.geteuid() <> 0:
	print "Please be sure to run this installer as root."
	sys.exit(0)


#copy our own modules to /usr/lib/im2imap
#delete complete folder to prevent problems with old versions

if os.path.isdir(LIB_DIR): 
	shutil.rmtree(LIB_DIR)

if not os.path.isdir(LIB_DIR):
	os.mkdir(LIB_DIR)


#copy files
shutil.copytree("src/modules",LIB_DIR + "/modules" )
shutil.copytree("src/tools",LIB_DIR + "/tools")

#os.chmod("/etc/init.d/kabbit",0711)

#our main executable
shutil.copyfile("./src/im2imap.py","/usr/bin/im2imap")
os.chmod("/usr/bin/im2imap",0755)

print "Installation successful!"

sys.exit(0)


