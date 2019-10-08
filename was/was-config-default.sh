#!/bin/sh

#Install Related Config
SOFTWARE_BASE=/vagrant/software
IM_SOFTWARE_BASE=${SOFTWARE_BASE}/was/8.5.5/im
WAS_SOFTWARE_BASE=${SOFTWARE_BASE}/was/8.5.5/was855


INSTALL_BASE=/home/was
IM_INSTALL_BASE=${INSTALL_BASE}/im
WAS_INSTALL_BASE=${INSTALL_BASE}/was

WAS_INSTALL_RESPONSEFILE_TPL=${WASBASEDIR}/lib/install/install_response_855.xml
WAS_UNINSTALL_RESPONSEFILE_TPL=${WASBASEDIR}/lib/install/uninstall_response_855.xml

LOG_BASE=/tmp

#Update Related Config
WAS_SOFTWARE_UPDATE_BASE=${SOFTWARE_BASE}/was/8.5.5/update

#Deploy Related Config
# APPSROOT=root@localhost:/tmp/appsroot
LOCALAPPSROOT=/tmp/localappsroot


#Tuning Relate Config, 512 mean 512M
T_HEAPSIZE_XMS=522
T_HEAPSIZE_XMX=522
export T_HEAPSIZE_XMS T_HEAPSIZE_XMX

T_THREADPOOL_MIN=25
T_THREADPOOL_MAX=25
export T_THREADPOOL_MIN T_THREADPOOL_MAX

