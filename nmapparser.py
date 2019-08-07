#!/usr/bin/python
"""
	Description: Command Line Nmap Parser for valid XML results from an nmap scan. 
		    This program is based on (and includes some code from) Alton Johnson 's Nmap parser
		     
	Author: mark thorburn (snar5) 
	Created: 07/17/2013
	Updated: 07/28/2014 -- Added Text Search  Option 
	Updated: 12/15/2015 -- Added Total Count, display IPs and Export to file
        Updated: 08/06/2016 -- Make all Files

	Package files
		  sample.xml	a sample XML file to test with 
		  colors.py	a simple colors class 
		  nmapsort.py	the parser engine 
		  nmapparser.py this file  
	Usage:
		python nmapparser.py <path to valid xml file> 

"""
import re
from sys import argv
import colors
import os
import getopt
import nmapsort
import shlex


# Color file input 
colors = colors.colors
nm = nmapsort.NmapSortClass()
data = []   # -- This global to hold the data at any given point in time. I.E. to print to file the latest output. 

banner = "\n " + "-" * 72 + "\n " + colors.white + " Command Line XML Parser \n " + colors.normal + "-" * 72 + "\n "

def help():
	print banner
	print " Usage: ./nmapparse.py results.xml"
	print "\n Note: This script must point to a XML output file from nmap to work properly.\n"
	exit()

def optionshelp(err=None):
	os.system('clear')
	print banner 
	if err !=None:
		print colors.red +  ' Unknown command: ' 
		print err 
		print colors.normal
		print ''
	print ' ----------------------------------------'
	print ' Option - Command '
	print '   .sort\t\t Sort Entire List '
	print '   .ip <ip address>\t Select Individual IP address'
	print '   .port <port Number>\t Enter port Number to filter on'
	print '   .file\t\t Make a file based on port selected' 
	print '   .text\t\t Search Version Information ' 
	print '   .help\t\t Displays this screen'
	print '   .portlist\t\t unique ports list'
	print '   .count\t\t Return Number of IPs'
	print '   .export\t\t Export results to file'
        print '   .makeall\t\t Make a file for each port'
	print '   .quit\t\t Quit Program'  

	
def main ():
	os.system('clear')
	options = ''
	option = ''
	port = ''
	if len(xmlfile) == 0:
		help()
	else:
		scanfile(xmlfile)
	print banner
	while not option == 'q':
		print "Enter option (type '.help' for help, '.quit' to quit)"
		options = shlex.split(raw_input('#nmcmd:> '))
		try:
			if len(options[0]) < 1:
				optionshelp()
			elif options[0] == '.sort':
				sort(port)
			elif options[0] == '.ip':
				getip(options[1])
			elif options[0] == '.port':
				if len(options[1]) > 0:
					sort(options[1])	
			elif options[0] =='.file':
				makefile()
			elif options[0] =='.text':
				txtsearch()
			elif options[0] =='.portlist':
				listports()
			elif options[0] == '.export':
				export()
			elif options[0] == '.count':
				count()
                        elif options[0] == '.makeall':
                                makefiles()
			elif options[0] == '.summary':
				scanSummary()

	# System Commands ------------------------------------------------
			elif options[0] == 'ls':
				os.system('clear;ls -l')
				print 
			elif options[0] == '.help':
				optionshelp()
			elif options[0] == '.pwd':
				os.system('clear;pwd')
			elif options[0] =='.clear':
				os.system('clear')
			elif options[0] =='.quit':
				exit()
			else:
				optionshelp(options[0])	
		except Exception, err:
			optionshelp(err)

def scanfile(xmlfile):
	try:
		os.system('clear')
		print 'Scanning File: ', xmlfile[0]
		nm.scanFile(xmlfile[0])
	except Exception, err:
		print 'Error Reading File ', xmlfile[0]
		print 'Error from file:'
		print err
		print colors.blue + 'The progam will now exit.' + colors.normal
		exit()
	
def makefile(portnumber=None):
        #
        # Make a file for the selected port 
        # 
	portnumber = raw_input('Create file for port? ')
	if len(portnumber) < 1:
		return
	filename = raw_input('Directory to save file (default: current directory): >')
	if len(filename) < 1:
		filename = 'port'+portnumber
	else:
		filename += '/port' + portnumber

	data = nm.displaySinglePort(portnumber) 
	if len(data) > 0:
		target = open(filename,'w')
		target.truncate()
		for ip in data:
			target.write(str(ip[0] +'\n'))
		target.close()
		print colors.blue + 'File: ' + filename + ' created.' + colors.normal
		print ''
	else:
		print colors.red + ' No file created as no ip was found with port ' + portnumber + colors.normal

def makefiles():
    #
    # Make a file for each port  
    #
    directory = "ports"
    ports = nm.uniquePorts()
    if len(ports) < 1:
       return
    data = []
    for port in ports:
        data = nm.displaySinglePort(port)
        if not os.path.exists(directory):
                os.makedirs(directory)
        filename = 'ports/' + str(port) + ".port.txt"
        target = open (filename, 'w')
        target.truncate()
        for ip in data:
            target.write(str(ip[0] +'\n'))
        target.close()



def export():
	data =[]
	scandata = nm.displayPorts()
	if len(scandata) > 0:
		filename = raw_input('Save File as: ')
		target = open(filename,'w')
	 	target.truncate()
		for ip_addr in sorted(scandata):
			for portkey,values in sorted(scandata[ip_addr].items()):
				target.write(str(ip_addr) + ' ' + str(portkey) + ' ' + str(values) + '\n')
				
		target.close()	
def count():
	data = nm.displayPorts()
	print len(data)

def sort(port=None):

	data = []
	pdata = []
	
	if len(port) < 1:
		scanData = nm.displayPorts() 
		for ip_addr in sorted(scanData):
        		for portkey,values in sorted(scanData[ip_addr].items()):
				data.append([ip_addr, portkey,values])        
		if len(data) > 0:
			print_to_screen(data)
	else:
		data = nm.displaySinglePort(port)
		if len(data) > 0:
			print_to_screen(data)
		else:
			print colors.red + '>> No ports retreived <<' + colors.normal 
def listports():
	data = nm.uniquePorts()
	print 'Unique Port List for Nmap Results:\n'

	if len(data) > 0:
		for port in data:
			print port
		print 
	else:
		print colors.red + '>> Error Getting List <<' + colors.normal 

def getip(ipaddr=None):
	os.system('clear')
	print ''
	print 'IP:' + colors.blue + ipaddr + colors.normal 
	if ipaddr != 'None':
		for portkey, values in nm.displaySingleIp(ipaddr).items():
			print colors.green + '  [*] '+ colors.normal + portkey + '\t'  + values
		print ''
	else:
		print 'No information for ' + ipaddr + ' found'
		print ''
def txtsearch():
	global data 
	txt_to_search = raw_input('Enter text to Search for (Text is case sensitive): ')
	data = nm.displayTextSearch(txt_to_search)
	if len(data) > 0:
		print_to_screen(data)
	else:
		print colors.red + '>> No results retreived <<' + colors.normal
###
# Print Summary for Neat Reporting 
###
def scanSummary():
	scanSummary = nm.getScanCommand() 
	scanTime = nm.getScanTime()
	scanScanType = nm.getScanType()
	scanScanInfo = nm.getScanInfo() 
	scanFileName = nm.getFilename() 
	scanHostsup = nm.getHosts()
	scanAllHosts = nm.getHostsall() 
	ports = nm.uniquePorts()
	data =[]
 	portString = ''
	if len(ports) > 0:
		for ip in ports:
			portString = portString + ip + ","
	else:
        	portString = "No Ports" 

		
	os.system('clear')
	print "+--------------------------------------------------+"
	print "Network Scan Summary:\n"
	print "Nmap Run Start: " + colors.green + nm.getScanTime() + colors.normal 
	print "Nmap Run End: " + colors.green + nm.getEndTime() + colors.normal
	print "Nmap ScanType: " + colors.green + scanScanType + colors.normal
	print "Hosts Found: " + colors.green + scanHostsup + colors.normal + " out of: " + colors.green + scanAllHosts + colors.normal + " hosts" 
	print "Nmap Command: " + colors.green + scanSummary + colors.normal 
	print "Unique Ports Discovered:"
	print colors.green +  portString + colors.normal
	print "+--------------------------------------------------+"
	print 	
###
# Print to Screen (display results) 
###

def print_to_screen(data):
	#grab offset
	offset = [0,0,0,0]
	for row in data:
		for num in range(0,len(row)):
			if len(row[num]) > offset[num]:
				offset[num] = len(row[num])

	#print pretty lines
	row_lines = " +" + "-" * (offset[0]+3) + "+" + "-" * (offset[1]+3) + "+" + \
	"-" * (offset[2]+3) + "+"

	print
	print row_lines
	print " | " + colors.blue + "IP Address " + colors.normal + \
	" " * (offset[0]-9) + "|" + colors.blue + " Port" + colors.normal + \
	" " * (offset[1]-2) + "|" + colors.blue + " Service" + colors.normal + \
	" " * (offset[2]-5) + "|"

	#output
	ip = ''
	for line in data:
		if line[0] != ip:
			print row_lines
			ip = line[0]
		for num in range(0,len(line)):
			print " | " + line[num] + (" " * (offset[num]-len(line[num]))), 
		print " |"

	print row_lines
	print
	
try:
	xmlfile = argv[1:]
	main()
except Exception, err:
	print err
