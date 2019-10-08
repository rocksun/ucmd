#!/bin/sh

printUsage()
{
    echo "Usage: "
    echo "  "${0}" [APPID] [VERSION]";
    echo "  "${0}" [APPID]";
}

. ${BASEDIR}/config.sh
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


# echo ${APPID}

if [ ! -f ${BASEDIR}/profiles/${APPID}.sh ]; then
	echo "The APPID "${APPID}" is not exist in profiles!"
	exit
fi

echo "Deploy "${APPID}" with version "${APPVERSION}"."

. ${BASEDIR}/profiles/${APPID}.sh
export USERNAME PASSWORD PORT HOST APPID APPVERSION LOCALPKG APPPKGNAME DEPLOYNAME DEPLOYMETHOD 
export DEPLOYTARGETTYPE DEPLOYTARGET NEEDRESTART CLEANCMD CHECKURL CHECKSTR





