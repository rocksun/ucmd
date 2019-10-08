#!/bin/sh
printUsage()
{
    echo "Usage: "
    echo "  "${0}" [APPID] [VERSION]";
    echo "  "${0}" [APPID]";
}

WASBASEDIR=$(dirname "$0")
export WASBASEDIR

# Read default config
. ${WASBASEDIR}/was-config-default.sh
echo "Use default config "

# Read local config

if [ -f ${WASBASEDIR}/config/config.sh ]; then
	echo "Use User setting config "
	. ${WASBASEDIR}/config/config.sh
fi

export APPSROOT LOCALAPPSROOT

if [[ $# -ne 2 ]] && [[ $# -ne 1 ]]; then
	printUsage
	exit
fi

APPID=$1
if [ $# == 2 ] ; then
    APPVERSION=$2
else
    APPVERSION="None"
fi

if [ ! -f ${WASBASEDIR}/profiles/${APPID}.sh ]; then
	echo "The APPID "${APPID}" is not exist in profiles!"
	exit
fi

echo "Deploy "${APPID}" with version "${APPVERSION}"."

. ${WASBASEDIR}/profiles/${APPID}.sh
export USERNAME PASSWORD PORT HOST APPID APPVERSION LOCALPKG APPPKGNAME DEPLOYNAME DEPLOYMETHOD 
export DEPLOYTARGETTYPE DEPLOYTARGET NEEDRESTART CLEANCMD CHECKURL CHECKSTR


wsadmin.sh -lang jython -user ${USERNAME} -password ${PASSWORD} -port ${PORT} -host ${HOST} -f ${WASBASEDIR}/lib/deploy/wdeploy.py
state=$?
echo ret ${state}
exit ${state}