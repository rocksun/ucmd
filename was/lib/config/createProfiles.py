#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Set up
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import os
import sys
import ops_reader
import java


def createProfile (profile):
    createProfileCmd = "ssh %s@%s '%s/bin/manageprofiles.sh -create -templatePath %s/profileTemplates/managed -nodeName %s -profileName %s'" % (config.user, profile.host, config.appServerPath, config.appServerPath, profile.getNodeName(), profile.name)
    print "Create managed profile with command:"
    print createProfileCmd
    os.system(createProfileCmd)

def addNode(profile, port):
    addNodeCmd = "ssh %s@%s '%s/bin/addNode.sh %s %s -username %s -password %s'" % (config.user, profile.host,  config.getProfilePath(profile.name), config.dmgrProfile.host, port, config.adminUsername, config.adminPassword )
    print "AddNode with command:"
    print addNodeCmd
    os.system(addNodeCmd)


def createProfiles (config,nodes,port):
    for profile in config.profiles:
        if profile.getNodeName() not in nodes:
            createProfile(profile)
            addNode(profile, port)
        else:
            print "%s.%s with node name %s already exist, skipped to create and add." % (profile.host, profile.name, profile.getNodeName() )



def getDmgrSoapPort():
    server_confids=AdminConfig.list("ServerEntry")
    for server_confid in server_confids.split("\n"):
        server_confid=server_confid.strip()
        server_type=AdminConfig.showAttribute(server_confid, "serverType")
        # print server_type
        if server_type == "DEPLOYMENT_MANAGER":
            NamedEndPoints = AdminConfig.list("NamedEndPoint", server_confid).split("\n")
            for namedEndPoint in NamedEndPoints:
                endPointName = AdminConfig.showAttribute(namedEndPoint, "endPointName" )
                endPoint = AdminConfig.showAttribute(namedEndPoint, "endPoint" )
                host = AdminConfig.showAttribute(endPoint, "host" )
                port = AdminConfig.showAttribute(endPoint, "port" )
                if endPointName == "SOAP_CONNECTOR_ADDRESS":
                    return port
    return None

def getAllNodes():
    nodes=[]
    node_confids=AdminConfig.list("Node")
    for node_confid in node_confids.split("\n"):
        node_confid=node_confid.strip()
        nodeName = AdminConfig.showAttribute(node_confid, "name" )
        # print node_confid, nodeName
        nodes.append(nodeName)
    return nodes


  
config = ops_reader.readCellConfig()
port = getDmgrSoapPort()
print "DMGR Port: ", port
nodes = getAllNodes()
print "Available Nodes: ", nodes
createProfiles(config,nodes,port)



# print config.user
# ssh was@was1 '/home/was/was/WebSphere/AppServer/bin/manageprofiles.sh -create -templatePath /home/was/was/WebSphere/AppServer/profileTemplates/managed -nodeName nodename'