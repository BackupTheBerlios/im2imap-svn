#!/usr/bin/python
# -*- coding: utf-8 -*- 

##############################################
# converts kopete-xml-log file to ascii
##############################################

import sys
import xml.dom.minidom
from xml.dom.minidom import Node


doc = xml.dom.minidom.parse(sys.argv[1])
 
mapping = {}
text=""
 
for node in doc.getElementsByTagName("kopete-history"):
 H = node.getElementsByTagName("head")
 for node4 in H:
 	date = node4.getElementsByTagName("date")
 	month = date[0].getAttribute("month")
 	year = date[0].getAttribute("year")

 L = node.getElementsByTagName("msg")
 
 for node2 in L:
	time = node2.getAttribute("time")
	day = time[0:time.find(" ")]
	date = day + "." + month + "." + year + " " + time[time.find(" ")+1:]
	
  	text+= node2.getAttribute("from") + "(" + date + ")" + ":"  
	for node3 in node2.childNodes:
      		if node3.nodeType == Node.TEXT_NODE:
			text += node3.data + "\n"	

if sys.argv[1][-3:] == "xml":
	f=open(sys.argv[1][:-4],"w")
	f.write(text.encode("utf-8"))
	f.close()
