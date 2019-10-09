#!/usr/bin/env python
'''
    File name: create_clusters_and_servers.py
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


def createClusterIfNeeded(clusterName):
    ref = getMBean('/Clusters/' + clusterName)
    # print clusterNames
    if (ref != None):
        print "Cluster '%s' already exist , skip create." % clusterName
    else: 
        print "Create Cluster '%s'." %  clusterName
        cd('/')
        cmo.createCluster(clusterName)

        cd('/Clusters/' + clusterName)
        cmo.setClusterMessagingMode('unicast')
        cmo.setClusterBroadcastChannel('')

def createServerIfNeeded(server):
    # print server.name, server.address, server.port, server.cluster
    ref = getMBean('/Servers/' + server.name)
    # print clusterNames
    if (ref != None):
        print "Server '%s' already exist , skip create." % server.name
    else:
        print "Create Server '%s' with:" %  server.name
        print "IP: '%s'" %  server.address
        print "Port: '%s'" %  server.port
        print "Cluster: '%s'" %  server.cluster
        cd('/')
        cmo.createServer(server.name)
        # print "111"
        cd('/Servers/' + server.name)
        # print "222"
        cmo.setListenAddress(server.address)
        # print "333"
        cmo.setListenPort(int(server.port))
        # print "444"

        if server.cluster!=None and server.cluster!="":
            # print "555"
            cmo.setCluster(getMBean('/Clusters/' + server.cluster))
            # print "666"

def createClusterAndServers(dc):
    listenAddress="t3://"+dc.adminAddress+":"+dc.adminPort
    print "Connect to %s " % listenAddress
    connect(dc.adminUsername, dc.adminPassword, listenAddress)

    edit()
    startEdit()
    for clusterName in dc.clusters:
        createClusterIfNeeded(clusterName)

    for key, server in dc.servers.items():
        createServerIfNeeded(server)

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
createClusterAndServers(dc)