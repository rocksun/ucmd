#!/bin/sh

printUsage()
{
    echo "Usage: "
    echo "${0} [start|stop|restart] [profile]"
}


setEnv()
{
    if [ ! -f ${WASBASEDIR}/profiles/${APPID}.sh ]; then
        echo "The APPID "${APPID}" is not exist in profiles!"
        exit
    fi
    echo "${opercmd} targets"

    . ${WASBASEDIR}/profiles/${APPID}.sh
    export DEPLOYTARGETTYPE DEPLOYTARGET 
}


operate()
{
    setEnv
    METHOD=$1
    export METHOD
    wsadmin.sh -lang jython -user ${USERNAME} -password ${PASSWORD} -port ${PORT} -host ${HOST} -f ${WASBASEDIR}/lib/deploy/wdeploy.py
    state=$?
    echo ret ${state}
    exit ${state}
}

if [[ $# -ne 2 ]]; then
	printUsage
	exit
fi

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

opercmd=$1
APPID=$2

if [ $opercmd == "start" ] ; then
    operate "start"
elif [ $opercmd == "stop" ] ; then
    operate "stop"
elif [ $opercmd == "restart" ] ; then
    operate "restart"
else
    echo "No command of '${opercmd}'"
    printUsage
    exit
fi

# Read Pre Oper Shell
# if [ -f ${WASBASEDIR}/config/was-install-pre.sh ]; then
# 	echo "Use was-install-pre.sh "
# 	bash -e ${WASBASEDIR}/config/was-install-pre.sh
# fi