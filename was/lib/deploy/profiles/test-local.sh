#!/bin/sh


USERNAME=root
PASSWORD=root123
PORT=8879
HOST=localhost

LOCALPKG=true

APPPKGNAME=DefaultApplication.ear

DEPLOYNAME=DefaultApplication
DEPLOYTARGETTYPE=Cluster
DEPLOYTARGET=cluster1
DEPLOYMETHOD=full

NEEDRESTART=false
CHECKURL=http://172.16.0.91:9080/snoop
CHECKSTR=snoop

