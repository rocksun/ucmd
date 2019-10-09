# Create WLS Env Automatically 

weblogic用户登录，进入wls目录

## 创建域

./wlstrun.sh  config/create_domain.py  props/loan.properties 

## 创建启动脚本

创建启动脚本，boot.properties以及logs目录。如果是多个主机的集群，需要在每个主机上执行。

./wlstrun.sh  config/create_scripts.py  props/loan.properties 

## 启动AdminServer

./wlstrun.sh  oper/start_admin.py  props/loan.properties

## 创建Clusters和Servers

./wlstrun.sh  config/create_clusters_and_servers.py  props/loan.properties 

会连接上一步的启动的admin server，并创建clusters和servers。

## 对Server执行调优

./wlstrun.sh  tuning/tune_servers.py  props/loan.properties   
