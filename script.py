#!/usr/bin/python
#This script will Save Cisco IOS Configuration Periodically
#Author: azizi.mohdariffin@gmail.com
#Date  : 11 April 2018

import smtplib
import paramiko
import time
import sys
import os

localtime = time.asctime( time.localtime(time.time()) )
log = open('/home/mdazizi/wrmem/log-batch1.txt', 'a')
log.write("\n")
log.write("\n")
log.write("Log for: " + localtime + "\n")

f = open('/home/mdazizi/wrmem/batch1.txt')
for line in iter(f):
        host = line
        host = host.replace('\n','')
        str(host)
        log.write("HOST: " + host +"\n")

	up = os.system("ping -c 1 "+ host +" > /dev/null")	
	
	if up == 0:
	
        	ssh = paramiko.SSHClient()
        	ssh.set_missing_host_key_policy(
        	paramiko.AutoAddPolicy())
        	ssh.connect(host, username='yourusername', password='yourpass')
        	remote = ssh.invoke_shell()
        	output = remote.recv(65535)
        	check = str(output)
        	log.write(str(output))
		if "RP" in check:
                	test = 1
                	#print "This is XR"
                        check = ""
        	else:
			#print "This is IOS"			

                	remote.send("who\n")
                	time.sleep(.5)
                	output = remote.recv(65535)
                	log.write(str(output))
                	#print output
                	who = str(output)
                	checkl = who.count('\n')
			#print checkl
			check = ""

			if checkl == 6:
				remote.send("wr\n")
                		time.sleep(.5)
                		output = remote.recv(65535)
                		log.write(str(output))
				#log.write('ok\n')
			else:
				log.write('There is concurrent SSH Session!\n')

        	ssh.close()
                up = 11
	else:
		log.write('Host is down!\n')
                up = 11
        #print message  

#print message

log.close()
f.close()
