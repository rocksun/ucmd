#!/usr/bin/env python
'''
    File name: create_scripts.py
    Author: Rock Sun
    Mail: daijun@gmail.com
    WLST for WebLogic:  12.2.1.3.0
'''

import time
import getopt
import sys
import re
import os
import os.path
import socket


sys.path.append(os.environ.get('WLSTOOLSHOME')+"/config")
import props_reader

startAdminTmpl=os.environ.get('WLSTOOLSHOME')+"/tmpl/startAdminServer.sh.tmpl"
startServerTmpl=os.environ.get('WLSTOOLSHOME')+"/tmpl/startServer.sh.tmpl"

def printUsage():
    print 'create_scripts.py -p <path-to-properties-file>'

def writeFile(outputPath, output):
    if os.path.isfile(outputPath) :
        print "Output File exists: '%s', ignored" % outputPath
    else:
        print "Generate File: '%s'" % outputPath
        logfile = open(outputPath, 'w')
        logfile.write(output)
        logfile.close()

def ensureDir(dir):
    if os.path.isdir(dir) :
        print "Output Dir exists: '%s', ignored" % dir
    else:
        os.mkdir(dir)



def createServerScript(domainPath, serverName, adminAddress, adminPort, adminUsername, adminPassword, isAdmin,dc):
    tmpl=""
    if isAdmin:     
        f = open(startAdminTmpl,"r")
        tmpl = f.read()
        f.close()
    else:
        f = open(startServerTmpl,"r")
        tmpl = f.read()
        f.close()

    output = tmpl.replace("{serverName}",serverName)
    output = output.replace("{adminAddress}",adminAddress)
    output = output.replace("{adminPort}",adminPort)


    xms="1024"
    xmx="1024"
    adminXms="512"
    adminXmx="512"
    if dc.getProperty("tuning.server.heap.xms")!=None:
        xms = dc.getProperty("tuning.server.heap.xms")

    if dc.getProperty("tuning.server.heap.xmx")!=None:
        xmx = dc.getProperty("tuning.server.heap.xmx")
    
    if dc.getProperty("tuning.admin.server.heap.xms")!=None:
        adminXms = dc.getProperty("tuning.admin.server.heap.xms")

    if dc.getProperty("tuning.admin.server.heap.xmx")!=None:
        adminXmx = dc.getProperty("tuning.admin.server.heap.xmx")

    if isAdmin:
        output = output.replace("{xms}",adminXms)
        output = output.replace("{xmx}",adminXmx)
    else:
        output = output.replace("{xms}",xms)
        output = output.replace("{xmx}",xmx)

    outputPath = os.path.join(domainPath,"bin", "start_"+serverName+".sh")

    writeFile(outputPath, output)
    command = ['chmod', '+x', outputPath]
    os.system(r'chmod +x '+outputPath)
    # os.spawnlp(os.P_NOWAIT, *command)
    # os.chmod(outputPath, 0755)

    ensureDir(os.path.join(domainPath, "servers"))
    ensureDir(os.path.join(domainPath, "servers",serverName))
    ensureDir(os.path.join(domainPath, "servers",serverName, "logs"))

    serverSecurityDir =os.path.join(domainPath, "servers", serverName, "security")
    ensureDir(serverSecurityDir)

    bootPropFilePath = os.path.join(serverSecurityDir, "boot.properties")
    bootPropOutput="username="+adminUsername+"\npassword="+adminPassword
    writeFile(bootPropFilePath, bootPropOutput)


    

    # print bootPropFilePath
    # print bootPropOutput
    # print output
    # print outputPath



def createScripts(dc):
    localIP = socket.gethostbyname(socket.gethostname())
    if localIP==dc.adminAddress:
        createServerScript(dc.domainPath, dc.adminServerName,dc.adminAddress,dc.adminPort,dc.adminUsername,dc.adminPassword,1,dc)

    for key, server in dc.servers.items():
        if server.address == localIP:
            print server.name
            createServerScript(dc.domainPath, server.name,dc.adminAddress,dc.adminPort,dc.adminUsername,dc.adminPassword,0,dc)



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
createScripts(dc)