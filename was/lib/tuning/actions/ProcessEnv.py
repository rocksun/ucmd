# import java

# lineSeparator = java.lang.System.getProperty('line.separator')
# appServer_gc_verbose = "TRUE"

envs=""

def getExistEnvList(str):
    pureStr = str[1:len(str)-1]
    evnIdArr = pureStr.split(")")
    # print str
    # print pureStr
    # print evnIdArr
    retArr=[]
    for retId in evnIdArr[0:len(evnIdArr)-1]:
        retArr.append(retId.strip()+")")
    # print retArr
    return retArr

def exist(name, processDefPath_confid):
    existEnvs=getExistEnvList(AdminConfig.showAttribute(processDefPath_confid, 'environment'))
    for eEnv in existEnvs:
        eName=AdminConfig.showAttribute(eEnv, "name")
        if name==eName:
            return eEnv

    return ""

# def removeEnv(env,Envs):
#     for target_list in expression_list:
#         pass


def app_server_tuning(server_confid):
    server_name=AdminConfig.showAttribute(server_confid, "name")
    processDefPath_confid = AdminConfig.list('JavaProcessDef', server_confid)

    # existEnvs=getExistEnvList(AdminConfig.showAttribute(processDefPath_confid, 'environment'))
    

    if envs!="":    
        envArr = envs.split(",")
        for envNameAndValue in envArr:
            name = envNameAndValue.split(":")[0]
            value = envNameAndValue.split(":")[1]
            print "Set ProcessDef Env with '%s' : '%s'" % (name,value)
            eEnv = exist(name, processDefPath_confid)
            if eEnv!="":
                print "Env %s is Exist, remove old first." % name
                AdminConfig.remove(eEnv)

            nameAndValue = [["name", name], ["value", value]]
            AdminConfig.modify(processDefPath_confid, [['environment', [nameAndValue]]])
            