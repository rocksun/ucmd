############################数据源配置############################

############################创建JDBC连接程序############################
AdminTask.createJDBCProvider('[-scope Cell=JingxiangNode01Cell -databaseType Oracle -providerType "Oracle JDBC Driver" -implementationType 连接池数据源 -name "Oracle JDBC Driver" -description "Oracle JDBC Driver" -classpath [${ORACLE_JDBC_DRIVER_PATH}/ojdbc6.jar ] -nativePath "" ]')
AdminConfig.list('JDBCProvider', AdminConfig.getid( '/Cell:JingxiangNode01Cell/'))
# AdminConfig.list('DataSource', AdminConfig.getid( '/Cell:JingxiangNode01Cell/JDBCProvider:Oracle JDBC Driver/'))
#          	作用域（Cell、Node、Server、Cluster）可配置	默认Cluster（可选）
# 			数据库类型	db2
# 			提供程序类型	DB2 Universal JDBC Driver Provider
# 			实现类型	连接池数据源
# 			名称	DB2 Universal JDBC Driver Provider
# 			db2驱动程序另存目录路径	/WAS/IBM/WebSphere/AppServer/lib/driver
############################J2C认证数据############################
# JDBC 提供程序 > Oracle JDBC Driver > 数据源 > JAAS － J2C 认证数据 > JingxiangNode01/w
AdminTask.listAuthDataEntries()
# [[alias JingxiangNode01/w] [userId w] [description ] [_Websphere_Config_Data_Id cells/JingxiangNode01Cell|security.xml#JAASAuthData_1529550601223] [_Websphere_Config_Data_Type JAASAuthData] [password *******] ]
#           别名	XXXX（可配置）alias
# 			用户标识	XXXX（可配置）userId
# 			密码	XXXX（可配置）password
############################创建数据源############################
# C:\Program Files (x86)\IBM\WebSphere\AppServer\profiles\AppSrv01\wstemp\3506402\workspace\cells\JingxiangNode01Cell\resources.xml
AdminTask.createDatasource('"Oracle JDBC Driver(cells/JingxiangNode01Cell|resources.xml#JDBCProvider_1529550306918)"', '[-name "Oracle JDBC Driver DataSource" -jndiName jndi -dataStoreHelperClassName com.ibm.websphere.rsadapter.Oracle11gDataStoreHelper -containerManagedPersistence true -componentManagedAuthenticationAlias JingxiangNode01/w -configureResourceProperties [[URL java.lang.String jdbc:oracle:thin:@localhost:1521:orcl]]]')
AdminConfig.create('MappingModule', '(cells/JingxiangNode01Cell|resources.xml#DataSource_1529575817988)', '[[authDataAlias ""] [mappingConfigAlias ClientContainer]]')
AdminConfig.modify('(cells/JingxiangNode01Cell|resources.xml#CMPConnectorFactory_1529575818009)', '[[name "Oracle JDBC Driver DataSource_CF"] [authDataAlias "JingxiangNode01/w"] [xaRecoveryAuthAlias ""]]')
AdminConfig.create('MappingModule', '(cells/JingxiangNode01Cell|resources.xml#CMPConnectorFactory_1529575818009)', '[[authDataAlias ""] [mappingConfigAlias ClientContainer]]')
AdminConfig.list('DataSource', AdminConfig.getid( '/Cell:JingxiangNode01Cell/JDBCProvider:Oracle JDBC Driver/'))
#           作用域（Cell、Node、Server、Cluster）可配置	默认Cluster（可选）
# 			数据源名	XXXX（可配置）
# 			JNDI名称	jdbc/XXXX（可配置）
# 			选择JDBC提供程序	选择现有的JDBC提供程序（DB2 Universal JDBC Driver Provider）
# 			驱动程序类型	默认4
# 			数据库名	XXXX（可配置）
# 			服务器名称	XXXX（可配置）
# 			端口号	5000
# 			组件管理的认证别名	选择之前配置的J2C认证
# 			容器管理的认证别名	选择之前配置的J2C认证

newds = AdminConfig.getid('/Cell:mycell/Node:mynode/JDBCProvider:JDBC1/DataSource:DS1/')
print AdminConfig.create('ConnectionPool', newds, [])
############################数据库连接池配置############################
# <resources.jdbc:JDBCProvider xmi:id="JDBCProvider_1183122153343" name="Derby JDBC Provider" description="Derby embedded non-XA  JDBC Provider" providerType="Derby JDBC Provider" implementationClassName="org.apache.derby.jdbc.EmbeddedConnectionPoolDataSource" xa="false">
#  <classpath>${DERBY_JDBC_DRIVER_PATH}/derby.jar</classpath>
#  <factories xmi:type="resources.jdbc:DataSource" xmi:id="DataSource_1183122153625" name="Default Datasource" jndiName="DefaultDatasource" description="Datasource for the WebSphere Default Application" providerType="Derby JDBC Provider" authMechanismPreference="BASIC_PASSWORD" relationalResourceAdapter="builtin_rra" statementCacheSize="10" datasourceHelperClassname="com.ibm.websphere.rsadapter.DerbyDataStoreHelper">
#    <propertySet xmi:id="J2EEResourcePropertySet_1183122153625">
#      <resourceProperties xmi:id="J2EEResourceProperty_1183122153625" name="databaseName" type="java.lang.String" value="${APP_INSTALL_ROOT}/${CELL}/DefaultApplication.ear/DefaultDB" description="adminRequired=true - This is a required property. This property must be set and it identifies which database to access. For example, g:/db/wombat." required="true"/>
#      <resourceProperties xmi:id="J2EEResourceProperty_1183122153626" name="shutdownDatabase" type="java.lang.String" value="" description="If set to the string 'shutdown', this will cause the database to shutdown when a java.sql.Connection object is obtained from the Data Source. E.g., If the Data Source is an XADataSource, a getXAConnection().getConnection() is necessary to cause the database to shutdown" required="false"/>
#      <resourceProperties xmi:id="J2EEResourceProperty_1183122153627" name="dataSourceName" type="java.lang.String" value="" description="Name for ConnectionPooledDataSource. Not used by the Data Source object. Used for informational purpose only." required="false"/>
#      <resourceProperties xmi:id="J2EEResourceProperty_1183122153628" name="description" type="java.lang.String" value="" description="Description of the Data Source. Not used by the Data Source object. Used for informational purpose only." required="false"/>
#      <resourceProperties xmi:id="J2EEResourceProperty_1183122153629" name="connectionAttributes" type="java.lang.String" value="upgrade=true" description="Connection attributes specific to Derby. Please see Derby documentation for a complete list of features." required="false"/>
#      <resourceProperties xmi:id="J2EEResourceProperty_1183122153630" name="createDatabase" type="java.lang.String" value="" description="If set to the string 'create', this will cause a new database of DatabaseName if that database does not already exist. The database is created when a connection object is obtained from the Data Source." required="false"/>
#    </propertySet>
#    <connectionPool xmi:id="ConnectionPool_1183122153625" connectionTimeout="8989898" maxConnections="12" minConnections="12" reapTime="100" unusedTimeout="1000" agedTimeout="1" purgePolicy="EntirePool"/>
#  </factories>
# </resources.jdbc:JDBCProvider>
# todo 事务隔离级别	2(CS隔离级别)
# todo 语句高速缓存	100-200（默认100）
reapTime = 100
# 最小连接数	10
minConnections = 10
# 最大连接数	80
maxConnections = 80
# 连接超时	60
connectionTimeout = 60
# 未使用超时	300
unusedTimeout = 300
jdbc_conn_conf = []
jdbc_conn_conf.append(["minConnections", minConnections])
jdbc_conn_conf.append(["maxConnections", maxConnections])
jdbc_conn_conf.append(["connectionTimeout", connectionTimeout])
jdbc_conn_conf.append(["unusedTimeout", unusedTimeout])


node_confids = AdminConfig.list("Node")
for node in node_confids.split("\n"):
    node = node.strip()
    AdminConfig.list('JDBCProvider', AdminConfig.getid(node))

