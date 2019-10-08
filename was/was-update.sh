#!/bin/sh

printUsage()
{
    echo "Usage: "
    echo "  "${0}" "
}

if [[ $# -ne 0 ]]; then
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

if [ -f ${WASBASEDIR}/config/was-update-pre.sh ]; then
	echo "Use was-install-pre.sh "
	. ${WASBASEDIR}/config/was-update-pre.sh
fi


echo "updateWAS: "
. ${WASBASEDIR}/lib/install/update-was.sh ${WAS_SOFTWARE_UPDATE_BASE} ${LOG_BASE} ${IM_INSTALL_BASE} ${WAS_INSTALL_BASE}