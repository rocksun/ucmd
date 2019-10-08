#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Set up
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import os
import sys
import ops_reader


def isClusterExist(clusterName):
    cluster_confids=AdminConfig.list("ServerCluster")
    # print cluster_confids
    cluster_confids=cluster_confids.strip()
    if cluster_confids != "":
        for cluster_confid in cluster_confids.split("\n"):
            cluster_confid=cluster_confid.strip()
            cName = AdminConfig.showAttribute(cluster_confid, "name" )
            if cName == clusterName:
                return 1
    return 0

def createCluster(cluster):
    if isClusterExist(config.cluster):
        print "Cluster '%s' already exist, skip to create." % cluster
    else:
        print "Create Cluster '%s'" % cluster
        AdminTask.createCluster("[-clusterConfig [-clusterName %s] -replicationDomain [-createDomain true]]" % cluster)

def isServerExist(serverName):
    server_confids=AdminConfig.list("Server")
    # print cluster_confids
    for server_confid in server_confids.split("\n"):
        server_confid=server_confid.strip()
        sName = AdminConfig.showAttribute(server_confid, "name" )
        if sName == serverName:
            return 1
    return 0

def createServers(config):
    for server in config.servers:
        if isServerExist(server.name):
            print "Server '%s' already exist, skip to create." % server.name
        else:                
            print "Create server '%s' in cluster '%s' at node '%s'" % (server.name, config.cluster, config.getServerNodeName(server) )
            AdminTask.createClusterMember("[-clusterName %s -memberConfig [-memberNode %s -memberName %s -memberWeight 2 -replicatorEntry true] ]" % (config.cluster, config.getServerNodeName(server), server.name ))




config = ops_reader.readCellConfig()
createCluster(config.cluster)
createServers(config)
AdminConfig.save()
# port = getDmgrSoapPort()
# print "DMGR Port: ", port
# nodes = getAllNodes()
# print "Available Nodes: ", nodes
# createProfiles(config,nodes,port)



# print config.user
# ssh was@was1 '/home/was/was/WebSphere/AppServer/bin/manageprofiles.sh -create -templatePath /home/was/was/WebSphere/AppServer/profileTemplates/managed -nodeName nodename'