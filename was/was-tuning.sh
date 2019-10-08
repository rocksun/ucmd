#!/bin/sh

printUsage()
{
    echo "Usage: "
    echo "${0} [PROFILE]"
}

if [[ $# -ne 1 ]]; then
	printUsage
	exit
fi


WASBASEDIR=$(dirname "$0")
export WASBASEDIR

ABSWASBASEDIR=$(cd "$(dirname "$0")"; pwd)  
export ABSWASBASEDIR
PYTHONPATH=${ABSWASBASEDIR}/lib/tuning
export PYTHONPATH

# Read default config
. ${WASBASEDIR}/was-config-default.sh
echo "Use default config "

# Read local config

if [ -f ${WASBASEDIR}/config/config.sh ]; then
	echo "Use User setting config "
	. ${WASBASEDIR}/config/config.sh
fi

if [ -f ${WASBASEDIR}/config/was-tuning-pre.sh ]; then
	echo "Use was-tuning-pre.sh "
	. ${WASBASEDIR}/config/was-tuning-pre.sh
fi


APPID=$1

if [ ! -f ${WASBASEDIR}/profiles/${APPID}.sh ]; then
	echo "The APPID "${APPID}" is not exist in profiles!"
	exit
fi

. ${WASBASEDIR}/profiles/${APPID}.sh
export TUNINGACTIONS 

wsadmin.sh -lang jython -javaoption "-Dpython.path=${PYTHONPATH}" -user ${USERNAME} -password ${PASSWORD} -port ${PORT} -host ${HOST} -f ${WASBASEDIR}/lib/tuning/tuning.py
state=$?
echo ret ${state}
exit ${state}

# HOST=${1}
# PORT=${2}
# USERNAME=${3}
# PASSWORD=${4}



