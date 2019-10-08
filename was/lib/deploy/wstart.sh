#!/bin/sh


BASEDIR=$(dirname "$0")
export BASEDIR

. ${BASEDIR}/init.sh

METHOD="start"
export METHOD

wsadmin.sh -lang jython -user ${USERNAME} -password ${PASSWORD} -port ${PORT} -host ${HOST} -f ${BASEDIR}/wdeploy.py
state=$?
echo ret ${state}
exit ${state}
