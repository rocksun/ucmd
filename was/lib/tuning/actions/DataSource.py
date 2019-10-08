minConnections="10"
maxConnections="80"
connectionTimeout="60"
unusedTimeout="300"

webSphereDefaultIsolationLevel="2"
statementCacheSize="100"

internalds="DefaultEJBTimerDataSource,DefaultEJBTimerDataSource,OTiSDataSource"

def modifyProps(ds_confid):
    propertySet = AdminConfig.showAttribute(ds_confid,'propertySet')
    propertyList = AdminConfig.list('J2EEResourceProperty', propertySet).splitlines()
    for property in propertyList:
        if ('webSphereDefaultIsolationLevel' == AdminConfig.showAttribute(property, 'name')):
            AdminConfig.modify(property, [["value", webSphereDefaultIsolationLevel]])
            print property
            print 'Modify webSphereDefaultIsolationLevel with value: %s.' % webSphereDefaultIsolationLevel



def global_tuning(confid):
    print "Create DataSource."

    dsArray=internalds.split(",")

    ds_confids=AdminConfig.list("DataSource").split('\n')
    for ds_confid in ds_confids:
        ds_confid=ds_confid.strip()
        # print ds_confid
        dsName=AdminConfig.showAttribute(ds_confid,'name')
        if dsName not in dsArray:
            pool=AdminConfig.showAttribute(ds_confid,'connectionPool')
            poolParams=[["minConnections", minConnections],["maxConnections", maxConnections]
                ,["connectionTimeout", connectionTimeout],["unusedTimeout", unusedTimeout]]
            print "Modify DataSource %s with options:" % dsName
            print poolParams
            AdminConfig.modify(pool, poolParams)

            modifyProps(ds_confid)
            print "Modify statementCacheSize with value %s." % statementCacheSize
            AdminConfig.modify(ds_confid, [['statementCacheSize',statementCacheSize]]) 


            