
# WAS自动化发布（was）

WebSphere自动化脚本

## 目录说明

### lib

实现功能的代码存放的目录，可以按模块存放，例如deploy存放的是发布相关的内容。

### config

客户的全局配置，例如WebSphere安装路径等。

### profiles

存放某个业务的或某个系统的具体配置，例如某WebSphere的DMGR连接信息，发布的应用信息等。

### was-*.sh

具体的业务执行脚本。

## 使用说明

### was-tuning.sh



### was-config.sh

通过这个命令，可以根据配置的UCMD Profile创建Profile，创建Cluster和Server。

这个命令只能在DMGR Profile所在主机上执行

#### 前提条件

所有参与到集群的主机都已经配置好了/etc/hosts文件，所有用到的主机名都已经配置到该文件。

操作需要在DMGR所在主机执行，需要配置DMGR主机到本机以及其他主机的WAS用户的SSH认证。具体步骤使用以下命令：

```
    # 创建密钥
    ssh-keygen

    # 将密钥加到需要SSH访问的主机，有多少个主机参与，需要配置多少次，DMGR主机本身也要运行，[username]和[hostname]配置成相应的用户和主机名
    ssh-copy-id [username]@[hostname]

    # 如果正常运行，说明已经配置完成
    ssh [username]@[hostname] date
```

#### 配置UCMD Profile

首先创建一个profile，例如，可以复制profiles/cluster.sh.tmpl为profiles/cluster.sh。其中内容类似以下形式：


···
    #!/bin/sh

    DMGR_PROFILE=was1.dmgr01
    # 主机名.DMGRProfile名

    MANAGED_PROFILES=was1.cust01,was1.cust02
    # “,”隔开的主机名.Profile名
    # 要保证“主机名.Profile名”的唯一性

    CLUSTER=cluster01
    # 需要创建的Cluster名

    MANAGED_SERVERS=was1.cust01.server01,was1.cust02.server02
    # “,”隔开的主机名.Profile名.Server名

    USERNAME=root
    PASSWORD=root123
    # WAS管理控制台用户名密码
···


#### 运行

在was目录下运行：

```
    ./was-config.sh cluster
```

cluster即是前面创建的UCMD Profile名，不需要加.sh后缀。


#### 创建DataSource的说明

通过以下命令在wsadmin中获取provider列表

```
    wsadmin>print AdminConfig.listTemplates('JDBCProvider')
    "Cloudscape JDBC Provider (XA)(templates/servertypes/APPLICATION_SERVER/servers/defaultZOS_60X|resources.xml#builtin_jdbcprovider)"
    "Cloudscape JDBC Provider (XA)(templates/servertypes/APPLICATION_SERVER/servers/default_60X|
    ...
    jdbc-resource-provider-only-templates.xml#JDBCProvider_DataDirect_1a)"
    "WebSphere embedded ConnectJDBC driver for MS SQL Server(templates/system|jdbc-resource-provider-templates.xml#JDBCProvider_DataDirect_1a)"
```

并获取详细信息

···
    wsadmin>AdminConfig.show("DB2 Universal JDBC Driver Provider (XA)(templates/system|jdbc-resource-provider-templates.xml#JDBCProvider_DB2_UNI_2)")
    '[classpath ${DB2UNIVERSAL_JDBC_DRIVER_PATH}/db2jcc.jar;${UNIVERSAL_JDBC_DRIVER_PATH}/db2jcc_license_cu.jar;${DB2UNIVERSAL_JDBC_DRIVER_PATH}/db2jcc_license_cisuz.jar]\n[description "minVer null - maxVer null - Two-phase commit DB2 JCC provider that supports JDBC 3.0. Data sources that use this provider support the use of XA to perform 2-phase commit processing. Use of driver type 2 on the application server for z/OS is not supported for data sources created under this provider."]\n[implementationClassName com.ibm.db2.jcc.DB2XADataSource]\n[isolatedClassLoader false]\n[name "DB2 Universal JDBC Driver Provider (XA)"]\n[nativepath ${DB2UNIVERSAL_JDBC_DRIVER_NATIVEPATH}]\n[providerType "DB2 Universal JDBC Driver Provider (XA)"]\n[xa true]'
···