#!/bin/sh

printUsage()
{
    echo "Usage: "
    echo "  "${0}" ${WAS_SOFTWARE_BASE} ${LOG_BASE} ${IM_INSTALL_BASE} ${WAS_INSTALL_BASE} ${WAS_UNINSTALL_RESPONSEFILE_TPL}"
}

WAS_SOFTWARE_BASE=$1
LOG_BASE=$2
IM_INSTALL_BASE=$3
WAS_INSTALL_BASE=$4
WAS_UNINSTALL_RESPONSEFILE_TPL=$5

if [[ $# -ne 5 ]]; then
	printUsage
    echo "xxxxxxx"
	exit -1
fi

responseFile=${LOG_BASE}/was-uninstall-response.xml
tmpresponseFile=${LOG_BASE}/was-install-response.xml.tmp

if [ ! -f ${responseFile} ]; then
    echo "Use Template Response File: "${WAS_UNINSTALL_RESPONSEFILE_TPL}
    cp ${WAS_UNINSTALL_RESPONSEFILE_TPL} ${responseFile}

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

# if [ ! -f  ${LOG_BASE}/WASv85.nd.install-cu.xml ]; then
# 	echo "No WASv85.nd.install-cu.xml file， will generate new one."
#     cp ${WAS_SOFTWARE_BASE}/responsefiles/samples/WASv85.nd.install.xml ${LOG_BASE}/WASv85.nd.install-cu.xml
#     origin="C:\\\Program Files\\\IBM\\\WebSphere\\\AppServer"
#     # origin='WebSphere\\\AppServer'
#     replaceWith="${WAS_INSTALL_BASE}/WebSphere/AppServer"
#     # replaceWith="AAAAA"
#     _r1="${replaceWith//\//\\/}"

#     sed -i "s/${origin}/${_r1}/g" ${LOG_BASE}/WASv85.nd.install-cu.xml

#     o="http://www.ibm.com/software/repositorymanager/com.ibm.websphere.ND.v85"
#     r=$WAS_SOFTWARE_BASE
#     o="${o//\//\\/}"
#     r="${r//\//\\/}"
#     sed -i "s/${o}/${r}/g" ${LOG_BASE}/WASv85.nd.install-cu.xml
# fi

wasInstallCmd="${IM_INSTALL_BASE}/InstallationManager/eclipse/tools/imcl -acceptLicense input ${responseFile} -log ${LOG_BASE}/uninstall_was.log"
echo "Uninstall with command:"
echo ${wasInstallCmd}
${wasInstallCmd}