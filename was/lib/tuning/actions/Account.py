users="monitor:monitor:monitor,deployer:deployer:deployer"

def global_tuning(confid):
    print "Create User."

    userArrays=users.split(",")
    for userStr in userArrays:
        userInfo=userStr.split(":")
        username=userInfo[0]
        password=userInfo[1]
        role=userInfo[2]

        createUser(username, password, role)        

def createUser(username, password, role):
    theUser=AdminTask.searchUsers(['-uid', username])
    if theUser=="":
        print "Create User '%s' with Role '%s'" % (username, role)
        AdminTask.createUser(['-uid',username, 
            '-password', password, '-confirmPassword', password, '-cn', username, '-sn', username ])
        AdminTask.mapUsersToAdminRole(['-roleName',role,'-userids',username])
    else:
        print "User '%s' already exist, skip to create." % username
        print "The User '%s'" % theUser






    # ds_confids=AdminConfig.list("DataSource").split('\n')
    # for ds_confid in ds_confids:
    #     ds_confid=ds_confid.strip()
    #     # print ds_confid
    #     dsName=AdminConfig.showAttribute(ds_confid,'name')
    #     if dsName not in dsArray:
    #         pool=AdminConfig.showAttribute(ds_confid,'connectionPool')
    #         poolParams=[["minConnections", minConnections],["maxConnections", maxConnections]
    #             ,["connectionTimeout", connectionTimeout],["unusedTimeout", unusedTimeout]]
    #         print "Modify DataSource %s with options:" % dsName
    #         print poolParams
    #         AdminConfig.modify(pool, poolParams)

    #         modifyProps(ds_confid)
    #         print "Modify statementCacheSize with value %s." % statementCacheSize
    #         AdminConfig.modify(ds_confid, [['statementCacheSize',statementCacheSize]]) 


            