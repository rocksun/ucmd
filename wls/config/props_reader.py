#!/usr/bin/env python
'''
    File name: props_reader.py
    Author: Rock Sun
    Mail: daijun@gmail.com
    WLST for WebLogic:  12.2.1.3.0
'''

import time
import getopt
import sys
import re
import os

class Server(object):
    name=""
    address=""
    port=""
    cluster=""

class DomainConfig(object):

    wlsHome=""
    domainPath=""

    adminUsername=""
    adminPassword=""
    adminAddress=""
    adminPort=""
    adminServerName=""
    clusters=[]
    servers={}   

    props=None
    def getProperty(self, key):
        if self.props.get(key)==None or self.props.get(key)=="":
            return None
        else:
            return self.props.get(key)

def readDomainProperties(propertyFile):
    from java.io import FileInputStream
    from java.util import Properties
 
    propInputStream = FileInputStream(propertyFile)
    configProps = Properties()
    configProps.load(propInputStream)

    dc=DomainConfig()
    dc.wlsHome=os.environ.get('WLS_HOME')
    # print dc.wlsHome
    dc.props=configProps

    dc.domainPath=configProps.get("domain.path")

    dc.adminUsername=configProps.get("admin.username")
    dc.adminPassword=configProps.get("admin.password")
    dc.adminAddress=configProps.get("admin.address")
    dc.adminPort=configProps.get("admin.port")
    dc.adminServerName=configProps.get("admin.serverName")

    clusters=configProps.get("domain.clusters")
    for cluster in clusters.split(","):
        if cluster!="":
            print "Parse Cluster:", cluster
            dc.clusters.append(cluster)

    servers=configProps.get("domain.servers")
    for s in servers.split(","):
        if s!="":
            server=Server()
            print "Parse Server:", s
            server.name=configProps.get(s+".name")
            server.address=configProps.get(s+".address")
            server.port=configProps.get(s+".port")
            server.cluster=configProps.get(s+".cluster")
            dc.servers[s]=server
            
            

        

    return dc
    # wlsPath=configProps.get("path.wls")


    # domainConfigPath=configProps.get("path.domain.config")
    # appConfigPath=configProps.get("path.app.config")
    # domainName=configProps.get("domain.name")
    # username=configProps.get("domain.username")
    # password=configProps.get("domain.password")
    # adminPort=configProps.get("domain.admin.port")
    # adminAddress=configProps.get("domain.admin.address")
    # adminPortSSL=configProps.get("domain.admin.port.ssl")
    # Set all variables from values in properties file.
