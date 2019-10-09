import time
import getopt
import sys
import re
import os
import os.path
import socket


sys.path.append(os.environ.get('WLSTOOLSHOME')+"/config")
import props_reader



def tuneServer(server):
    ref = getMBean('/Servers/' + server.name)
    if (ref == None):
        print "Server not already exist , please create first." % server.name
    else:
        cd('/Servers/' + server.name + '/Log/' + server.name)
        cmo.setRotationType('byTime')
        cmo.setFileCount(30)
        cmo.setRedirectStderrToServerLogEnabled(true)
        cmo.setRedirectStdoutToServerLogEnabled(true)
        cmo.setMemoryBufferSeverity('Debug')
        cmo.setLogFileSeverity('Notice')

        cd('/Servers/'+server.name+'/WebServer/'+server.name+'/WebServerLog/'+server.name)
        cmo.setLoggingEnabled(true)
        cmo.setRotationType('byTime')
        cmo.setFileTimeSpan(24)
        cmo.setNumberOfFilesLimited(true)
        cmo.setFileCount(50)
        cmo.setRotationTime('00:00')
        

def tuneServers(dc):
    listenAddress="t3://"+dc.adminAddress+":"+dc.adminPort
    print "Connect to %s " % listenAddress
    connect(dc.adminUsername, dc.adminPassword, listenAddress)

    edit()
    startEdit()

    for key, server in dc.servers.items():
        tuneServer(server)

    save()
    activate()
    disconnect()





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
tuneServers(dc)