rolloverType="SIZE"
maxNumberOfBackupFiles=5
rolloverSize=1

def app_server_tuning(server_confid):
    server_name=AdminConfig.showAttribute(server_confid, "name")
    logConf = []
    logConf.append(['rolloverType', rolloverType])
    logConf.append(['maxNumberOfBackupFiles', maxNumberOfBackupFiles])
    logConf.append(['rolloverSize', rolloverSize])

    systemOutLog = AdminConfig.showAttribute(server_confid, "outputStreamRedirect")
    systemErrLog = AdminConfig.showAttribute(server_confid, "errorStreamRedirect")

    print "Modify SystemOut and SystemErr Config with options:"
    print logConf

    AdminConfig.modify(systemOutLog, logConf)
    AdminConfig.modify(systemErrLog, logConf)
