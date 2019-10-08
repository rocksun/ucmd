#!/bin/sh

printUsage()
{
    echo "Usage: "
    echo "  "${0}" "
    echo "  "${0}" im"
	echo "  "${0}" was"
}

installAll()
{
    echo "installAll: "
	installIM
	installWAS
}

installIM()
{
    echo "installIM: "
	. ${WASBASEDIR}/lib/install/install-im.sh ${IM_SOFTWARE_BASE} ${LOG_BASE} ${IM_INSTALL_BASE}
}

installWAS()
{
    echo "installWAS: "
	. ${WASBASEDIR}/lib/install/install-was.sh ${WAS_SOFTWARE_BASE} ${LOG_BASE} ${IM_INSTALL_BASE} ${WAS_INSTALL_BASE} ${WAS_INSTALL_RESPONSEFILE_TPL}
}


if [[ $# -ne 0 ]] && [[ $# -ne 1 ]]; then
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

# Read Pre Install Shell
if [ -f ${WASBASEDIR}/config/was-install-pre.sh ]; then
	echo "Use was-install-pre.sh "
	. ${WASBASEDIR}/config/was-install-pre.sh
fi


if [[ $# -ne 1 ]]; then
	installAll
	exit
fi

