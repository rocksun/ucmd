import time
import getopt
import sys
import re
import os
import os.path
import socket


sys.path.append(os.environ.get('WLSTOOLSHOME')+"/config")
import props_reader


def startAdmin(dc):
    binPath = os.path.join(dc.domainPath,"bin")
    print "Start Admin Server with '%s' ." % ("start_"+dc.adminServerName+".sh")
    outputPath=os.path.join(binPath, ("start_"+dc.adminServerName+".sh"))
    os.system(outputPath)
    # changed to RUNNING

    nohupFile = os.path.join(dc.domainPath,"servers",dc.adminServerName,"logs", "nohup.out")

    i=0
    while True:
        print "Check Server Start Status ..."
        f = open(nohupFile,"r")
        content = f.read()
        if content.find("changed to RUNNING")!=-1:
            print "Server Started"
            break
        
        if i>20:
            print " Start Timeout, quit."

        i=i+1
        time.sleep(5) 
    



properties = ''

try:
   opts, args = getopt.getopt(sys.argv[1:],"p:h::",["properies="])
except getopt.GetoptError:
   printUsage()
   sys.exit(2)
for opt, arg in opts:
   if opt == '-h':
      printUsage()
      sys.exit()
   elif opt in ("-p", "--properties"):
      properties = arg

dc = props_reader.readDomainProperties(properties)
startAdmin(dc)