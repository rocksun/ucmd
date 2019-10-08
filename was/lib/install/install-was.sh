#!/bin/sh

printUsage()
{
    echo "Usage: "
    echo "  "${0}" ${WAS_SOFTWARE_BASE} ${LOG_BASE} ${IM_INSTALL_BASE} ${WAS_INSTALL_BASE} ${WAS_INSTALL_RESPONSEFILE_TPL}"
}

if [[ $# -ne 5 ]]; then
	printUsage
	exit -1
fi

WAS_SOFTWARE_BASE=$1
LOG_BASE=$2
IM_INSTALL_BASE=$3
WAS_INSTALL_BASE=$4
WAS_INSTALL_RESPONSEFILE_TPL=$5

responseFile=${LOG_BASE}/was-install-response.xml
tmpresponseFile=${LOG_BASE}/was-install-response.xml.tmp

if [ ! -f ${responseFile} ]; then
	echo "Use Template Response File: "${WAS_INSTALL_RESPONSEFILE_TPL}
    cp ${WAS_INSTALL_RESPONSEFILE_TPL} ${tmpresponseFile}

    echo "Use Repository ${WAS_SOFTWARE_BASE}"
    repoLocation="${WAS_SOFTWARE_BASE}"
    # echo 'sed -i "s,WasRepositoryLocation,${repoLocation},g" ${tmpresponseFile}>${responseFile}'
    sed "s,WasRepositoryLocation,${repoLocation},g" ${tmpresponseFile}>${responseFile}

    installLocaion=${WAS_INSTALL_BASE}/WebSphere/AppServer
    # echo "Install to ${installLocaion}"
    installLocaion="${installLocaion}"
    sed "s,WasInstallLocation,${installLocaion},g" ${responseFile}>${tmpresponseFile}

    cacheLocation=${WAS_INSTALL_BASE}/IMShare
    cacheLocation="${cacheLocation}"
    sed "s,WasCacheLocation,${cacheLocation},g" ${tmpresponseFile}>${responseFile}
fi



wasInstallCmd="${IM_INSTALL_BASE}/InstallationManager/eclipse/tools/imcl -acceptLicense input ${responseFile} -log ${LOG_BASE}/install_was.log"
echo "Install with command:"
echo ${wasInstallCmd}
${wasInstallCmd}