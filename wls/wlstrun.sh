#!/bin/sh
#
# Author: Rock Sun
# Mail: daijun@gmail.com
#

printUsage()
{
    echo "Usage: "
    echo "${0} [WLST-SCRIPT] [PROPERTIES]"
}

if [[ $# -ne 2 ]] ; then
	printUsage
	exit
fi

WLSTOOLSHOME=$(cd "$(dirname "$0")"; pwd)  
export ORACLE_HOME=/weblogic/orahome1
export WLS_HOME=${ORACLE_HOME}/wlserver
export JAVA_HOME=/weblogic/jdk1.8.0_171
export PATH=$JAVA_HOME/bin:$PATH
export CONFIG_JVM_ARGS=-Djava.security.egd=file:/dev/./urandom

export WLSTOOLSHOME


if [ -f ${WLSTOOLSHOME}/config.sh ]; then
	echo "Use User setting config: ${WLSTOOLSHOME}/config.sh"
	. ${WLSTOOLSHOME}/config.sh
fi

. $WLS_HOME/server/bin/setWLSEnv.sh


# Create the domain.
java weblogic.WLST  $1 -p $2 