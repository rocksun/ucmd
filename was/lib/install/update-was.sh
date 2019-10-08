#!/bin/sh

printUsage()
{
    echo "Usage: "
    echo "  "${0}" ${WAS_SOFTWARE_UPDATE_BASE} ${LOG_BASE} ${IM_INSTALL_BASE} ${WAS_INSTALL_BASE}"
}

if [[ $# -ne 4 ]]; then
	printUsage
	exit -1
fi

WAS_SOFTWARE_UPDATE_BASE=$1
LOG_BASE=$2
IM_INSTALL_BASE=$3
WAS_INSTALL_BASE=$4

# /home/was/IBM/InstallationManager/eclipse/tools/imcl install com.ibm.websphere.ND.v85 
# -repositories /home/was/software/UPDATE/repository.config 
# -installationDirectory /home/was/was85/AppServer -acceptLicense 

cmd="${IM_INSTALL_BASE}/InstallationManager/eclipse/tools/imcl install com.ibm.websphere.ND.v85 -repositories ${WAS_SOFTWARE_UPDATE_BASE}/repository.config -installationDirectory ${WAS_INSTALL_BASE}/WebSphere/AppServer -acceptLicense"
# com.ibm.websphere.IBMJAVA.v70 
echo "Update with command:"
echo ${cmd}
${cmd}

# wasInstallCmd="${IM_INSTALL_BASE}/InstallationManager/eclipse/tools/imcl -acceptLicense input ${responseFile} -log ${LOG_BASE}/install_was.log"
# echo "Install with command:"
# echo ${wasInstallCmd}
# ${wasInstallCmd}