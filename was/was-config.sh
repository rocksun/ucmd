#!/bin/sh
printUsage()
{
    echo "Usage: "
    echo "  "${0}" [UCMDProfileName]";
}

WASBASEDIR=$(dirname "$0")
export WASBASEDIR

ABSWASBASEDIR=$(cd "$(dirname "$0")"; pwd)  
export ABSWASBASEDIR
PYTHONPATH=${ABSWASBASEDIR}/lib/config
export PYTHONPATH

# Read default config
. ${WASBASEDIR}/was-config-default.sh
echo "Use default config "

# Read local config

if [ -f ${WASBASEDIR}/config/config.sh ]; then
	echo "Use User setting config "
	. ${WASBASEDIR}/config/config.sh
fi

if [[ $# -ne 1 ]]; then
	printUsage
	exit
fi

APPID=$1
if [ ! -f ${WASBASEDIR}/profiles/${APPID}.sh ]; then
	echo "The ProfileID "${APPID}" is not exist in profiles!"
	exit
fi

echo "Config "${APPID}""

. ${WASBASEDIR}/profiles/${APPID}.sh
export USERNAME PASSWORD PORT HOST APPID APPVERSION LOCALPKG APPPKGNAME DEPLOYNAME DEPLOYMETHOD 
export DEPLOYTARGETTYPE DEPLOYTARGET NEEDRESTART CLEANCMD CHECKURL CHECKSTR
export WAS_INSTALL_BASE
export DMGR_PROFILE MANAGED_PROFILES CLUSTER MANAGED_SERVERS ADMIN_USERNAME ADMIN_PASSWORD

export DBTYPE DBPROVIDERTYPE DBIMPTYPE DBPROVIDERNAME DBDRIVERPATH
export DBUSER DBPASSWORD
export DSNAME DSJNDINAME DSHELPERCLASS DSPROPERTIES
export DSMINCONN DSMAXCONN

# if [ -d ${IM_INSTALL_BASE}"/InstallationManager" ];then
# 	echo "It looks already installed IM in ${IM_INSTALL_BASE}, just skip to install."
# else 

# --- Create DMGR Profile

rhname=$(hostname)

# Read Array only worked on UNIX
#
# IFS='. ' read -r -a array <<< "$DMGR_PROFILE"
# if [[ ${#array[@]} -ne 2 ]]; then
# 	echo "Not a valid DMGR_PROFILE config: '"$DMGR_PROFILE"'"  
# 	exit
# fi

# chname=${array[0]}
# dmgrProfileName=${array[1]}

chname=`echo $DMGR_PROFILE | awk '{split($0,a,".");print a[1]}'` 
dmgrProfileName=`echo $DMGR_PROFILE | awk '{split($0,a,".");print a[2]}'` 


if [ "$rhname" != "$chname" ]; then 
	echo "Please Run Script in DMGR Host: '"$chname"'"  
	exit
fi;

appServerPath=${WAS_INSTALL_BASE}/WebSphere/AppServer

dmgrProfilePath=${WAS_INSTALL_BASE}/WebSphere/AppServer/profiles/${dmgrProfileName}
if [ -d ${dmgrProfilePath} ];then
	echo "It looks like Profile already exist: ${dmgrProfilePath}, just skip to create."
else
	createDMGRScripts="${appServerPath}/bin/manageprofiles.sh -create -templatePath ${appServerPath}/profileTemplates/dmgr -enableAdminSecurity true -adminUserName ${USERNAME} -adminPassword ${PASSWORD} -profileName ${dmgrProfileName}"
	echo $createDMGRScripts
	$createDMGRScripts
fi

# --- Start DMGR
# /home/was/was/WebSphere/AppServer/profiles/dmgr01/logs/dmgr/dmgr.pid

if [ ! -f ${appServerPath}/profiles/${dmgrProfileName}/logs/dmgr/dmgr.pid ]; then
	startDMGRCMD=${dmgrProfilePath}/bin/startManager.sh
	echo "Try to start DMGR ..."
	echo ${startDMGRCMD}
	${startDMGRCMD}
else
	echo "Dmgr looks like already running, skip to start."
fi


# --- Create Other Profiles, AddNode and StartNode

# wsadmin.sh -user ${USERNAME} -password ${PASSWORD} -profileName ${dmgrProfileName} -lang jython -javaoption "-Dpython.path=${PYTHONPATH}" -f ${WASBASEDIR}/lib/config/createProfiles.py
# state=$?
# echo ret ${state}
# exit ${state}


# --- Config Cluster and Server
# wsadmin.sh -user ${USERNAME} -password ${PASSWORD} -profileName ${dmgrProfileName} -lang jython -javaoption "-Dpython.path=${PYTHONPATH}" -f ${WASBASEDIR}/lib/config/createCluster.py


# --- Config Cluster and Server
wsadmin.sh -user ${USERNAME} -password ${PASSWORD} -profileName ${dmgrProfileName} -lang jython -javaoption "-Dpython.path=${PYTHONPATH}" -f ${WASBASEDIR}/lib/config/createDatasource.py
