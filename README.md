My first work with python nmap parser, which is probably equvilant to the a 
'hello world' program. Oddly, though I keep needing/adding to it as I have found it to 
suite my needs. I still like the idea of command prompt to stay and work with data object without 
re-running commands. 

*Note lists only "OPEN" ports 

Package files
      sample.xml    a sample XML file to test with
      colors.py     a simple colors class
      nmapsort.py   the parser engine
      nmapparser.py this file

USAGE:
      python nmapparser.py sample.xml

OPTIONS 

 Option - Command 
   .sort		 Sort Entire List 
   .ip <ip address>	 Select Individual IP address
   .port <port Number>	 Enter port Number to filter on
   .file		 Make a file based on port selected
   .text		 Search Version Information 
   .help		 Displays this screen
   .count		 Count of IPs found
   .export		 Export entire list to file
   .quit		 Quit Program

Enter option (type 'h' for help, 'q' to quit)
nmcmd:>     
