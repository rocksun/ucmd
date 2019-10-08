#!/bin/sh

printUsage()
{
    echo "Usage: "
    echo "  "${0}" ${IM_SOFTWARE_BASE} ${LOG_BASE} ${IM_INSTALL_BASE}"
}

if [[ $# -ne 3 ]]; then
	printUsage
	exit -1
fi

IM_SOFTWARE_BASE=$1
LOG_BASE=$2
IM_INSTALL_BASE=$3

if [ -d ${IM_INSTALL_BASE}"/InstallationManager" ];then
	echo "It looks already installed IM in ${IM_INSTALL_BASE}, just skip to install."
else 
    if [ ! -f ${LOG_BASE}"/install-cu.xml" ]; then
        echo "No ${LOG_BASE}/install-cu.xml, will generate new one"
        insertLine="<profile kind='self' installLocation='${IM_INSTALL_BASE}/InstallationManager/eclipse' id='IBM Installation Manager'></profile>"
        sed "3i${insertLine}" ${IM_SOFTWARE_BASE}/install.xml > ${LOG_BASE}/install-cu.xml.tmp

        str="location='"${IM_SOFTWARE_BASE}"'"
        sed "s,location='.',${str},g" ${LOG_BASE}/install-cu.xml.tmp>${LOG_BASE}/install-cu.xml
    fi

    imInstallCmd="${IM_SOFTWARE_BASE}/userinstc -acceptLicense -log ${LOG_BASE}/install_im.log -input ${IM_SOFTWARE_BASE}/install-cu.xml"
    echo "Install with command:"
    echo ${imInstallCmd}
    ${imInstallCmd}
fi

