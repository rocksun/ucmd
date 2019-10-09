#!/usr/bin/env python
'''
    File name: create_domain.py
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

sys.path.append(os.environ.get('WLSTOOLSHOME')+"/config")
import props_reader

# Get location of the properties file.



def printUsage():
    print 'create_domain.py -p <path-to-properties-file>'

def createDomain(dc):
    if os.path.isdir(dc.domainPath) :
        print "Domain Path %s Exists, skip create domain." % dc.domainPath
        return 

    print "Create Domain at '%s'" % dc.domainPath
    
    readTemplate(dc.wlsHome + '/common/templates/wls/wls.jar')
    # selectTemplate('Base WebLogic Server Domain','12.2.1.3.0')
    # loadTemplates()
    print "Admin User : '%s'" % dc.adminUsername
    cd('/Security/base_domain/User/' + dc.adminUsername)

    cmo.setPassword(dc.adminPassword)
    print "Admin Password : '%s'" % "*******"
    cd('/Server/AdminServer')
    cmo.setName(dc.adminServerName)

    print "Admin Address : '%s'" % dc.adminAddress
    print "Admin Port : '%s'" % dc.adminPort
    cmo.setListenPort(int(dc.adminPort))
    cmo.setListenAddress(dc.adminAddress)

    # Enable SSL. Attach the keystore later.
    # create(dc.adminServerName,'SSL')
    # cd('SSL/'+dc.adminServerName)
    # set('Enabled', 'True')
    # set('ListenPort', int(adminPortSSL))
# If the domain already exists, overwrite the domain
    # setOption('OverwriteDomain', 'true')
    setOption('ServerStartMode','prod')
    # setOption('AppDir', appConfigPath + '/' + domainName)
    writeDomain(dc.domainPath)
    



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
createDomain(dc)
# print 'properties=', properties