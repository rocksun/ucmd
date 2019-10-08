#!/bin/sh

# echo test


USERNAME=root
PASSWORD=root123
PORT=8879
HOST=localhost

APPPKGNAME=DefaultApplication.zip
DEPLOYNAME=DefaultApplication
CHECKURL=http://172.16.0.91:9081/test.jsp
CHECKSTR="This is test a"
DEPLOYMETHOD=delta

DEPLOYTARGETTYPE=Server
DEPLOYTARGET=server1,server2

