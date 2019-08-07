#!/usr/bin/env python

import pprint
import re
import string
import sys
import xml.dom.minidom
import collections
import os 
from collections import defaultdict

""" 

	This class does the sorting of the XML file for the front end 
	Only returns ports marked as "OPEN". Anything filtered is disregarded. 

	Parameters: <valid XML file>

	Update 7/28/2014 -- Added Text Search To do: Parital String Seach		
	
"""

class NmapSortClass():

     # --Constructor -- 
     def __init__(self):
	self._HostDictionary ={}
	self._ScanInfo = {}


     # -- Scan File ---
     def scanFile (self,filename):
       HostDictionary ={}
       dom = xml.dom.minidom.parse(filename)
       HostDictionary['device'] = {}
       HostDictionary['host']={}
       scanFilename = filename 
       scanType = dom.getElementsByTagName('scaninfo')[0].getAttributeNode('protocol').value
       scanTime = dom.getElementsByTagName('nmaprun')[0].getAttributeNode('startstr').value
       for stats in dom.getElementsByTagName('runstats'):
       	 scanEndTime = stats.getElementsByTagName('finished')[0].getAttributeNode('timestr').value
       scanHosts = dom.getElementsByTagName('hosts')[0].getAttributeNode('up').value
       scanCommand = dom.getElementsByTagName('nmaprun')[0].getAttributeNode('args').value
       scanHostsall = dom.getElementsByTagName('hosts')[0].getAttributeNode('total').value
       self._ScanInfo = {'filename':scanFilename,'scanType':scanType,'scanTime':scanTime,'scanCommand':scanCommand,'scanEndTime':scanEndTime,'scanHosts':scanHosts,'scanHostsall':scanHostsall}
      
        # -- Start Host --
       for dhost in dom.getElementsByTagName('host'):     
	   hostip = ''        
	   portProduct = ''
	   hostOS = ''
	   portService = ''
	   portProduct = ''
	   portNumber = ''
	   ostype = ''
	   osinfo = '' 
	   osfamily= ''   	
           # -- Check first to see if there is at least 1 open port on the list otherwise skip    
           for ports in dhost.getElementsByTagName('port'):
             if (ports.getElementsByTagName('state')[0].getAttributeNode('state').value == "open"):
	        portNumber = ports.getAttributeNode('portid').value
	        hostip = dhost.getElementsByTagName('address')[0].getAttributeNode('addr').value
                if not hostip in list(HostDictionary['device'].keys()):
			HostDictionary['device'][hostip]={}
		if ports.getElementsByTagName('service')[0].getAttributeNode('product'):
	           portProduct = ports.getElementsByTagName('service')[0].getAttributeNode('product').value			
		HostDictionary['device'][hostip][portNumber]= ''
                HostDictionary['device'][hostip][portNumber] = portProduct
           for os in dhost.getElementsByTagName('osclass'):
	     hostip = dhost.getElementsByTagName('address')[0].getAttributeNode('addr').value
             if not hostip in list(HostDictionary['host'].keys()):
                HostDictionary['host'][hostip]={}
             if os.getAttributeNode('osfamily'):
		osfamily = os.getAttributeNode('osfamily').value
             if os.getAttributeNode('osgen'):
		ostype = os.getAttributeNode('osgen').value
	     if os.getAttributeNode('accuracy'):
		osaccuracy = os.getAttributeNode('accuracy').value
	     osinfo = ostype + '  Accuracy: ' + osaccuracy + '%'
	     HostDictionary['host'][hostip][osfamily] = osinfo

       self._HostDictionary = HostDictionary
       return HostDictionary
    # -- END HOST --

       
     # -- Return Scan Type Information --
     def getScanInfo(self):
	return self._ScanInfo
     def getScanType(self):
	return self._ScanInfo['scanType']
     def getScanTime(self):
	return self._ScanInfo['scanTime']
     def getScanCommand(self):
	return self._ScanInfo['scanCommand']
     def getFilename(self):
	return self._ScanInfo['filename']
     def getEndTime(self):
	return self._ScanInfo['scanEndTime']
     def getHosts(self):
	return self._ScanInfo['scanHosts']
     def getHostsall(self):
	return self._ScanInfo['scanHostsall']

      # -- Functions to Return Results in different formats  -- 
     def displayPorts(self):
	return self._HostDictionary['device']
     def displayIpByPort(self):
	p = defaultdict(list)
	for key in self._HostDictionary['device']:
		for port in self._HostDictionary['device'][key]:
			p[port].append(key)
	return p 

     #------ Search for Single Port -------------
     def displaySinglePort(self,in_port):
	displaylist = []
	for key in self._HostDictionary['device']:
		for port,version in self._HostDictionary['device'][key].items():
			if port == in_port:
				displaylist.append([key,port,version])	
	return displaylist

     #------ Return Unique Ports ----------------
     def uniquePorts(self):
	portlist = []
	uniqlist = []	
	for key in self._HostDictionary['device']:
       	       for port,version in self._HostDictionary['device'][key].items():
               	        portlist.append(port)
	uniqlist=set(portlist)
	return uniqlist



     # -------- Search By Text -----------	
     def displayTextSearch(self,in_text): 
	displaylist = []
	for key in self._HostDictionary['device']:
		for port,version in self._HostDictionary['device'][key].items():
			if in_text in version:
				displaylist.append([key,port,version])
	return displaylist
	
     def displaySingleIp(self,in_ip):
	return self._HostDictionary['device'].get(in_ip,"None")

# -- End of Program -- 	

