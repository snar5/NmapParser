DESCRIPTION:
Command Line Nmap Parser for valid XML results from an nmap scan.
This program includes some code from Alton Johnson 's Nmap parser

        Author: mark thorburn (markt@tracesecurity)
        Created: 07/17/2013
        Updated: 07/28/2014 -- Added Text Search  Option

        Package files
                  sample.xml    a sample XML file to test with
                  colors.py     a simple colors class
                  nmapsort.py   the parser engine
                  nmapparser.py this file
        Usage:
                python nmapparser.py sample.xml

OPTIONS 

 Option - Command 
   sort			 Sort Entire List 
   ip <ip address>	 Select Individual IP address
   port <port Number>	 Enter port Number to filter on
   file			 Make a file based on port selected
   text			 Search Version Information 
   h			 Displays this screen
   q			 Quit Program

SAMPLE USAGE :

Scanning File:  sample.xml

 ------------------------------------------------------------------------
  Command Line XML Parser 
 ------------------------------------------------------------------------
 
Enter option (type 'h' for help, 'q' to quit)
"""
#nmcmd:> sort

 +----------------+-------+-------------------------------+
 | IP Address     | Port  | Service                       |
 +----------------+-------+-------------------------------+
 | 192.168.6.1    | 2105  | AOLserver httpd               |
 | 192.168.6.1    | 22    | OpenSSH                       |
 | 192.168.6.1    | 2525  | Sendmail                      |
 | 192.168.6.1    | 3128  | Squid webproxy                |
 | 192.168.6.1    | 443   | AOLserver httpd               |
 | 192.168.6.1    | 444   | AOLserver httpd               |
 | 192.168.6.1    | 53    | ISC BIND                      |
 | 192.168.6.1    | 8086  | Squid webproxy                |
 | 192.168.6.1    | 8088  | Squid webproxy                |
 +----------------+-------+-------------------------------+
 | 192.168.6.155  | 1066  | Microsoft Windows RPC         |
 | 192.168.6.155  | 1110  | Microsoft Windows RPC         |
 | 192.168.6.155  | 1137  | Microsoft Windows RPC         |
 | 192.168.6.155  | 135   | Microsoft Windows RPC         |
 | 192.168.6.155  | 902   | VMware Authentication Daemon  |
 | 192.168.6.155  | 912   | VMware Authentication Daemon  |
 +----------------+-------+-------------------------------+
 | 192.168.6.200  | 8080  | Burp Suite Pro http proxy     |
 +----------------+-------+-------------------------------+

Enter option (type 'h' for help, 'q' to quit)
#nmcmd:>      <-- Enter Command Here  
"""
