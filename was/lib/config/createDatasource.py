#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Set up
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import os
import sys
import ops_reader




def createProvider(ds):
      # print AdminConfig.listTemplates('JDBCProvider')
      # print "Creating JDBC Provider"
      cell_confids=AdminConfig.list("Cell")
      cellName = AdminConfig.showAttribute(cell_confids, "name" )

      providers=AdminTask.listJDBCProviders(['-scope', 'Cell='+cellName]).split('\n')
      for provider in providers:
            provider = provider.strip()
            if provider!="":
                  providerName = AdminConfig.showAttribute(provider, "name" )
                  if providerName == ds.dbProviderName:
                        print "Provider %s already Created, skip to Create." % ds.dbProviderName
                        return provider

      args=['-scope', 'Cell='+cellName, '-name', ds.dbProviderName,'-databaseType', ds.dbType, 
      '-providerType', ds.dbProviderType, '-implementationType', ds.dbImpType]

      if ds.dbDriverPath!=None and ds.dbDriverPath!="":
            args.append('-classpath')
            args.append(ds.dbDriverPath)

      print "Create JDBCProvider "+ds.dbProviderName+" with options :"
      print args
      provider = AdminTask.createJDBCProvider(args) 

      return provider

def createAuthAlias(ds):

      aliasName=ds.dsName+'_alias'
      jaas_confids=AdminConfig.list("JAASAuthData").split('\n')
      for jaas_confid in jaas_confids:
            jaas_confid=jaas_confid.strip()
            if jaas_confid!="":
                  alias = AdminConfig.showAttribute(jaas_confid, "alias" )
                  if alias==aliasName:
                        print "Alias %s already created, skip to create." % alias
                        return jaas_confid
            
      
      security = AdminConfig.getid('/Security:/')
      alias = ['alias', aliasName]
      userid = ['userId', ds.dbUser]
      pw = ['password', ds.dbPassword]
      jaasAttrs = [alias, userid, pw]
      print "Creating Auth Alias "+ aliasName +" with options: "
      print jaasAttrs
      aliasId = AdminConfig.create('JAASAuthData', security, jaasAttrs)
      return aliasId

def createDataSource(provider, aliasId, ds):
      ds_confids=AdminConfig.list("DataSource").split('\n')
      for ds_confid in ds_confids:
            ds_confid=ds_confid.strip()
            if ds_confid!="":
                  dsName = AdminConfig.showAttribute(ds_confid, "name" )
                  if dsName==ds.dsName:
                        print "DataSource %s already created, skip to create." % dsName
                        return ds_confid

      aliasName =  AdminConfig.showAttribute(aliasId, 'alias') 
      options=['-name', ds.dsName, '-jndiName', ds.dsJndiName,
       '-dataStoreHelperClassName', ds.dsHelperClass, 
       '-componentManagedAuthenticationAlias', aliasName,
       '-xaRecoveryAuthAlias', aliasName, '-configureResourceProperties',ds.dsProperties]
      print "Create Datasource %s with options: " % ds.dsName
      print options
      retds = AdminTask.createDatasource(provider,options ) 
      # print ds
      
      AdminConfig.create('MappingModule', retds, '[[authDataAlias '+aliasName+'] [mappingConfigAlias ""]]')  
     
      return retds




config = ops_reader.readCellConfig()
ds=config.datasource

if ds!=None:
      provider = createProvider(ds)
      aliasId = createAuthAlias(ds)
      dataSource = createDataSource(provider, aliasId, ds)
      AdminConfig.save()

      poolParams=[["minConnections", ds.dsMinConn],["maxConnections", ds.dsMaxConn]]
      pool=AdminConfig.showAttribute(dataSource,'connectionPool')
      print "Modify Connection Params With:"
      print pool
      print poolParams
      AdminConfig.modify(pool, poolParams)
      AdminConfig.save()
      
