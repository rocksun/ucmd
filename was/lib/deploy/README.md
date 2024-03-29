# wdeploy使用手册

## 安装

### 前置条件

 * Linux环境，BASH正常
 * 已经安装了WebSphere 8 ND版， wsadmin.sh 已经加入到了PATH中
 * 相应的应用包服务器可以通过ssh和scp直接访问
 * 本机可以通过网络访问各个DMGR的SOAP端口

### 安装

解压缩wdeploy.zip目录，修改config.sh文件：

APPSROOT=root@localhost:/tmp/appsroot
LOCALAPPSROOT=/tmp/localappsroot

config.sh中定义了两个目录，APPSROOT是远程文件服务器的根目录，符合scp命令的语法，包括了用户名、主机和根目录。如果没有配置APPSROOT，则不会执行远程复制动作，直接使用LOCALAPPSROOT的文件。LOCALAPPSROOT是应用包的本地存放路径。APPROOT和LOCALAPPSROOT下的某个应用包路径为：

    ./[APPID]/[VERSION]/[APPPKGNAME]

（[APPID]、[VERSION]和[APPPKGNAME]的说明见文档的“配置profile”部分）

## 配置profile

对于每个需要部署的应用，我们需要在profiles目录下为其配置一个profile，命名为[APPID].sh，内容如下：

    # WebSphere DMGR 连接参数
    USERNAME=root
    PASSWORD=root123
    PORT=8879
    HOST=localhost

    # 应用信息
    APPPKGNAME=DefaultApplication.ear # 应用包的名字
    DEPLOYNAME=DefaultApplication # 应用发布的名字（在DMGR上可以看到部署名）
    DEPLOYTARGETTYPE=Cluster # 发布目标类型，可以是Cluster或Server
    DEPLOYTARGET=cluster1 # 发布目标的名字，cluster名或server名
    DEPLOYMETHOD=full # 全量发布还是增量发布， 可以是full或delta
    LOCALPKG=true # 默认都是从远程复制包，如果为true则直接取本地文件（可选）

    # 其他参数
    NEEDRESTART=true # 如果发布后需要重启server，写true
    CHECKURL=http://172.16.0.91:9080/snoop # 测试发布完成的url，如不指定，不测
    CLEANCMD="ssh rm root@localhost:/somedir" # 重启过程中可以执行的清理命令

注：本工具执行的发布，其实是WebSphere的重新发布功能。因为应用首次发布时，可能需要指定很多参数，用脚本难以覆盖所有的场景。而日常工作中，其实最常见的操作就是应用包的重新发布，并不会修改应用包的配置。所以本工具执行时，特定的应用应该已经部署到了WebSphere，本工具实现了重新发布。

## 执行部署

完成了Profile的配置后，即可实现发布工作。在wdeploy目录下，执行；

    ./wdeploy.sh [APPID] [VERSION]

我们的发布工具会到profiles下找到[APPID].sh，执行相应的发布工作。

这里简单说一下发布过程。我们的工具会首先将 /APPSROOT/[APPID]/[VERSION]/[APPPKGNAME] 复制到 /LOCALAPPSROOT/[APPID]/[VERSION]/[APPPKGNAME]；然后连接到DMGR，针对发布名（DEPLOYNAME）执行全量或增量（DEPLOYMETHOD）发布；如果需要重启（NEEDRESTART），则执行重启，重启过程中如果需要执行命令（CLEANCMD），则执行相应的命令


## TODO

部分功能还需要现场测试。

