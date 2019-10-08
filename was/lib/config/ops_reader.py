#!/usr/bin/env python
'''
    File name: ops_reader.py
    Author: Rock Sun
    Mail: daijun@gmail.com
'''

import time
import getopt
import sys
import re
import os

class Server:
    host=""
    profile=""
    name=""
    node=None

class Profile:
    name=""
    host=""
    def getNodeName(self):
        return self.host+self.name+"Node"

# DSJNDINAME DSHELPERCLASS DSPROPERTIES
class Datasource:
    dbType=""
    dbProviderType=""
    dbImpType=""
    dbProviderName=""
    dbDriverPath=""

    dbUser=""
    dbPassword=""

    dsName=""
    dsJndiName=""
    dsHelperClass=""
    dsProperties=""

    dsMinConn="10"
    dsMaxConn="10"


class CellConfig:
    user=""
    appServerPath=""

    adminUser=""
    adminPassword=""

    dmgrProfile=None
    profiles=[]
    cluster=""
    servers=[]

    datasource=None



    def getServerNodeName(self, server):
        for profile in self.profiles:
            if profile.name == server.profile and profile.host == server.host:
                return profile.getNodeName()
        return None


    def getProfilePath(self, profileName):
        return self.appServerPath+"/profiles/"+profileName        

    def addDMGRProfile(self, str):
        kv = str.split(".")
        if len(kv)==2:
            self.dmgrProfile=Profile()
            self.dmgrProfile.host=kv[0]
            self.dmgrProfile.name=kv[1] 
    
    def addProfiles(self, str):
        profiles = str.split(",")
        for kvs in profiles:
            kv = kvs.split(".")
            if len(kv)==2:
                profile=Profile()
                profile.host=kv[0]
                profile.name=kv[1]
                print "Find profile config '%s' on host '%s'" % (kv[1], kv[0])
                self.profiles.append(profile)
            else:
                print "Wrong Was Profile config '%s', ignored" % kvs
    
    def addServers(self, str):
        servers = str.split(",")
        for kvs in servers:
            kv = kvs.split(".")
            if len(kv)==3:
                server=Server()
                server.host=kv[0]
                server.profile=kv[1]
                server.name=kv[2]
                print "Find Server config '%s' in profile '%s' on host '%s' " % (server.name, server.profile, server.host)

                self.servers.append(server)
            else:
                print "Wrong Was Server config '%s', ignored" % kvs
           

    # props=None
    # def getProperty(self, key):
    #     if self.props.get(key)==None or self.props.get(key)=="":
    #         return None
    #     else:
    #         return self.props.get(key)

def readCellConfig():
    cellConfig=CellConfig()
    # ${WAS_INSTALL_BASE}/WebSphere/AppServer
    cellConfig.appServerPath=str(os.environ.get('WAS_INSTALL_BASE'))+"/WebSphere/AppServer"
    cellConfig.user = os.environ.get('USER')
    cellConfig.cluster = os.environ.get('CLUSTER')

    cellConfig.adminUsername=os.environ.get('USERNAME')
    cellConfig.adminPassword=os.environ.get('PASSWORD')

    cellConfig.addDMGRProfile(os.environ.get('DMGR_PROFILE'))
    cellConfig.addProfiles(os.environ.get('MANAGED_PROFILES'))

    cellConfig.addServers(os.environ.get('MANAGED_SERVERS'))

    dsname=os.environ.get('DSNAME')
    if dsname!=None:
        ds=Datasource()
        ds.dbType=os.environ.get('DBTYPE')
        ds.dbProviderType=os.environ.get('DBPROVIDERTYPE')
        ds.dbImpType=os.environ.get('DBIMPTYPE')
        ds.dbProviderName=os.environ.get('DBPROVIDERNAME')
        ds.dbDriverPath=os.environ.get('DBDRIVERPATH')

        ds.dbUser=os.environ.get('DBUSER')
        ds.dbPassword=os.environ.get('DBPASSWORD')

        ds.dsName=os.environ.get('DSNAME')
        ds.dsJndiName=os.environ.get('DSJNDINAME')
        ds.dsHelperClass=os.environ.get('DSHELPERCLASS')
        ds.dsProperties=os.environ.get('DSPROPERTIES')

        minConn=os.environ.get('DSMINCONN')
        if minConn!=None and minConn!="":
            ds.dsMinConn=minConn

        maxConn=os.environ.get('DSMAXCONN')
        if maxConn!=None and maxConn!="":
            ds.dsMaxConn=maxConn


        cellConfig.datasource=ds
    return cellConfig
    # cellConfig.dmgrProfile = os.environ.get('MANAGED_PROFILES')
# DSJNDINAME DSHELPERCLASS DSPROPERTIES
    
    # print cellConfig

# DBTYPE=Oracle
# DBPROVIDERTYPE="Oracle JDBC Driver"
# DBIMPTYPE="XA data source"
# DBPROVIDERNAME="Oracle JDBC Driver (XA)"
# DBDRIVERPATH="/home/oracle/drivers/ojdbc.jar"

# DBUSER=user1
# DBPASSWORD=password1
# DBURL="jdbc:oracle:thin:@localhost:1521:testdb "

# DSNAME=testds
