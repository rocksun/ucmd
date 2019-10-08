#!/bin/sh

printUsage()
{
    echo "Usage: "
    echo "  "${0}" "
    echo "  "${0}" im"
	echo "  "${0}" was"
}

uninstallAll()
{
    echo "uninstallAll: "	
	uninstallWAS
    # uninstallIM
}

uninstallIM()
{
    echo "uninstallIM: "
	. ${WASBASEDIR}/lib/install/uninstall-im.sh
}

uninstallWAS()
{
    echo "uninstallWAS: "
    . ${WASBASEDIR}/lib/install/uninstall-was.sh ${WAS_SOFTWARE_BASE} ${LOG_BASE} ${IM_INSTALL_BASE} ${WAS_INSTALL_BASE} ${WAS_UNINSTALL_RESPONSEFILE_TPL}
}

WASBASEDIR=$(dirname "$0")
export WASBASEDIR

# Read default config
. ${WASBASEDIR}/was-config-default.sh
echo "Use default config "

# Read local config

if [ -f ${WASBASEDIR}/config/config.sh ]; then
	echo "Use User setting config "
	. -e ${WASBASEDIR}/config/config.sh
fi

if [ -f ${WASBASEDIR}/config/was-uninstall-pre.sh ]; then
	echo "Use was-install-pre.sh "
	. -e ${WASBASEDIR}/config/was-uninstall-pre.sh
fi

if [[ $# -ne 0 ]] && [[ $# -ne 1 ]]; then
	printUsage
	exit
fi

if [[ $# -ne 1 ]]; then
	uninstallAll
	exit
fi