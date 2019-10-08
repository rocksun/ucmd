import os
import commands
import sys
import time
import traceback
import urllib

from os.path import join as join_paths


username = os.environ.get('username')
# password = os.environ.get('password')
# print username
# print password

class Options:
	def __init__(self):
		pass

def getOptions():
	options = Options()
	options.appsRoot = os.environ.get('APPSROOT')
	options.localAppsRoot = os.environ.get('LOCALAPPSROOT')
	if options.localAppsRoot==None:
		options.localAppsRoot=""

	options.appId = os.environ.get('APPID')
	if options.appId==None:
		options.appId=""

	options.appVersion = os.environ.get('APPVERSION')
	if options.appVersion == None or options.appVersion == "" or options.appVersion == "None" :
		options.appVersion = None

	options.localPkg = os.environ.get('LOCALPKG')
	options.appPkgName = os.environ.get('APPPKGNAME')
	if options.appPkgName==None:
		options.appPkgName=""
	options.deployName = os.environ.get('DEPLOYNAME')
	if  options.deployName != None:
		options.deployName = options.deployName.strip()
	options.deployMethod = os.environ.get('DEPLOYMETHOD')
	if  options.deployMethod != None:
		options.deployMethod = options.deployMethod.strip()
	options.deployTargetType = os.environ.get('DEPLOYTARGETTYPE')
	options.deployTarget = os.environ.get('DEPLOYTARGET')
	options.needRestart = os.environ.get('NEEDRESTART')
	options.cleanCmd = os.environ.get('CLEANCMD')
	options.checkUrl = os.environ.get('CHECKURL')
	options.checkStr = os.environ.get('CHECKSTR')
	if options.checkStr==None:
		options.checkStr = ""
	options.method = os.environ.get('METHOD')

	if options.localPkg == "true" or options.appsRoot == None:
		localDir = os.path.join(options.localAppsRoot, options.appId)
		if options.appVersion != None:
			localDir = os.path.join(options.localAppsRoot, options.appId, options.appVersion)		
		if localDir==None:
			localDir=""
		options.localPath = os.path.join(localDir, options.appPkgName)	
	# print options.deployName
	return options

def convertToList( inlist ):
	outlist = []
	if (len(inlist) > 0):
	   if (inlist[0] == '[' and inlist[len(inlist) - 1] == ']'):
		  # Special checking when the config name contain space 
		  if (inlist[1] == "\"" and inlist[len(inlist)-2] == "\""):
			 clist = inlist[1:len(inlist) -1].split(")\" ")
		  else:
			 clist = inlist[1:len(inlist) - 1].split(" ")
		  #endIf
	   else:
		  clist = inlist.split(java.lang.System.getProperty("line.separator"))
	   #endIf
		
	   for elem in clist:
		   elem = elem.rstrip();
		   if (len(elem) > 0):
			  if (elem[0] == "\"" and elem[len(elem) -1] != "\""):
				 elem = elem+")\""
			  #endIf   
			  outlist.append(elem)
		   #endIf
		#endFor
	#endIf    
	return outlist

def mkDirRecursive(dir_path):

	if os.path.isdir(dir_path):
		return
	h, t = os.path.split(dir_path)  # head/tail
	if not os.path.isdir(h):
		mkDirRecursive(h)

	new_path = join_paths(h, t)
	if not os.path.isdir(new_path):
		os.mkdir(new_path)

def fetchDataToLocal(options):
	remotePath = os.path.join(options.appsRoot, options.appId, options.appPkgName)
	localDir = os.path.join(options.localAppsRoot, options.appId)
	if options.appVersion != None:
		remotePath = os.path.join(options.appsRoot, options.appId, options.appVersion, options.appPkgName)
		localDir = os.path.join(options.localAppsRoot, options.appId, options.appVersion)
	
	options.localDir = localDir
	mkDirRecursive(localDir)
	localPath = os.path.join(localDir, options.appPkgName)
	scplog = os.path.join(localDir, "scplog.out")
	# print remotePath
	# print localPath
	# print scplog
	cmd = "scp "+ remotePath +" "+localPath + " &> " + scplog +" 2>&1"
	
	print cmd
	os.system(cmd)
	scplogfile = open(scplog)
	ret = scplogfile.read()
	if len(ret.strip()) > 0:
		raise Exception(ret)
	else:
		options.localPath = localPath


def getAppDeploymentTarget (appName):
	try:
		global AdminConfig
		targets = ""
		if (appName == ""):
			return 0

		deployment = AdminConfig.getid("/Deployment:"+appName+"/" )
		if (len(deployment) == 0):
			return 0
		else:
			targets = AdminConfig.showAttribute(deployment, "deploymentTargets")
			targets = convertToList(targets)
		#endIf
		return targets
	except:
		typ, val, tb = sys.exc_info()
		if (typ==SystemExit):  raise SystemExit,`val`
		if (failonerror != "true"):
			print "Exception: %s %s " % (sys.exc_type, sys.exc_value)
			val = "%s %s" % (sys.exc_type, sys.exc_value)
			raise "ScriptLibraryException: ", `val`
			return 0
		else:   
			return 0

def updateApp (options):
	# print "update"
	if options.deployMethod == "delta":
		AdminApp.update( options.deployName, 
			'partialapp', ['-contents', options.localPath])
	else:
		AdminApp.update( options.deployName, 
			'app', ['-operation', 'update', '-contents', options.localPath]) 
	AdminConfig.save()


def inState(target, aimState):
	state = AdminControl.getAttribute(target,"state")
	if state.find(aimState) >= 0:
		return 1
	else:
		return 0

def waitState(target,aimState):
	for i in range(20):
		if(inState(target, aimState)):
			print "Target "+aimState+"."
			return 1
		else:
			print "Target had not get in '"+aimState+"', wait and trying ..."
		time.sleep(10)
	print "Target not get in state '"+aimState+"' on time"
	return 0



def ensureRestartIfNeeded (options):
	if options.needRestart == "true":
		print "Need restart servers."
		# target = AdminControl.completeObjectName('type='+options.deployTargetType
		# 	+',name='+options.deployTarget+',*')
		# print target
		# if not inState(target,"stopped"):
		# 	AdminControl.invoke(target, 'stop')

		if ensureState(options,"stopped","stop"):				
			if options.cleanCmd != None and options.cleanCmd != "":
				print "Need exceute clean command."
				executeCleanCmd(options)
			print "Trying to start."
			# AdminControl.invoke(target, 'start')		
			if ensureState(options,"running","start"):
				print "Target started successful."
			else:
				raise Exception("Start Target failed, please check it manually.")
		else: 
			raise Exception("Stop Target failed, please check it manually.")


def executeCleanCmd(options):
	cleanlog = os.path.join(options.localDir, "cleanlog.out")
	cmd = options.cleanCmd + " &> " + cleanlog +" 2>&1"
	print cmd
	os.system(cmd)
	cleanlogfile = open(cleanlog)
	ret = cleanlogfile.read()
	print ret

def checkUrl(options):
	if options.checkUrl != None and options.checkUrl != "":
		print "Check Url: " + options.checkUrl
		ret = urllib.urlopen(options.checkUrl)
		print "Return Info: " 
		print ret.info()
		html = ret.read()
		if html.find(options.checkStr) >=0:
			print "URL check OK for string '"+options.checkStr+"'"
			return 1
		else:
			print html
			print "URL check failed for string '"+options.checkStr+"'"
			return 0
	else:
		print "No Check URL."
		return 1

def simpleDeploy(options):
	if options.localPkg == "true" or options.appsRoot == None:
		print "Use local file "+ options.localPath
	else:
		print "Fetch data from remote file server"
		fetchDataToLocal(options)

	if getAppDeploymentTarget(options.deployName):
		updateApp(options)
		return 1
	else:
		print "Not a exist deploy name: "+options.deployName
		return 0

def fullDeploy(options):
	if options.localPkg == "true" or options.appsRoot == None:
		print "Use local file "+ options.localPath
	else:
		print "Fetch data from remote file server"
		fetchDataToLocal(options)
	
	if getAppDeploymentTarget(options.deployName):
		updateApp(options)
		ensureRestartIfNeeded(options)
		time.sleep(10)
		return checkUrl(options)
	else:
		print "Not a exist deploy name: "+options.deployName
		return 0
	
def ensureClusterState(options, targetState, targetCmd):
	target = AdminControl.completeObjectName('type='+options.deployTargetType
			+',name='+options.deployTarget+',*')
	if not inState(target, targetState):
		if targetCmd=="start":
			print "Starting Cluster "+target
		else:
			print "Stopping Cluster "+target
		AdminControl.invoke(target, targetCmd)		
		return waitState(target, targetState)
	else:
		print "Targets "+target+" already get in state "+targetState
		return 1


def ensureState(options, targetState, targetCmd):

	if options.deployTargetType == "Cluster":
		return ensureClusterState(options, targetState, targetCmd)
	else:
		return ensureServerState(options, targetState, targetCmd)

def ensureServerState(options, targetState, targetCmd):		
	if targetState=="running":
		targetState = "STARTED"
	targets = getTargetList(options.deployTargetType,targetState, options.deployTarget)
	for target in targets:
		if targetCmd == "stop":
			
			nodeName = None
			serverName = None
			if len(target.split("."))==2:
				nodeName = target.split(".")[0]
				serverName = target.split(".")[1]
				# AdminControl.stopServer(target.split(".")[1],target.split(".")[0])
			else:
				nodeName = getServerNode(target)
				serverName = target 
			targetObject = AdminControl.completeObjectName('type=Server,node='
				+nodeName+',name='+serverName+',*')
			print "stopping server "+target+" ..."
			AdminControl.invoke(targetObject, targetCmd)
				# AdminControl.stopServer(target,nodeName)
		else:
			# nodeName = getServerNode(target)
			print "starting server "+target+" ..."
			if len(target.split("."))==2:
				AdminControl.startServer(target.split(".")[1],target.split(".")[0],1)
			else:
				nodeName = getServerNode(target)
				AdminControl.startServer(target,nodeName,1)
	return waitServersToState(targets, targetState)


def waitServersToState(targets,targetState):
	
	ts = targets
	for i in range(180):
		ts = getTargetStateServers(ts,targetState)
		if len(ts)>0:
			time.sleep(15)
		else:
			return 1		
	print "Target not get in state '"+aimState+"' on time"
	return 0


def getTargetStateServers(targets,targetState):
	rets = []
	for t in targets:
		if targetState!=getServerStatus(t):
			print "Target "+t+" not get in state "+targetState+", trying ..."
			rets.append(t)
		else:
			print "Target "+t+" get in state "+targetState+" successfully "
	return rets


def serverInConfig(server, allServers):
	if len(server.split("."))==2:
		return server in allServers
	else:
		for s in allServers:
			sName = s.split(".")[1]
			if server==sName:
				return 1
		return 0

	
def getTargetList(targetType, targetState, targetstr):
	allServers = getServerList()
	targetArray = targetstr.split(",")
	targets = []
	for t in targetArray:
		if not serverInConfig(t,allServers):
			raise Exception("Please Provide a valid target: "+ t)
		else:
			# print targetState+"--"+getServerStatus(t)
			if targetState==getServerStatus(t):
				print "Target "+ t +" already get in "+targetState+" state"
			else:
				targets.append(t)		
	print "Process targets: "+str(targets)
	return targets

def getServerStatus(serverName):
	target = None
	if len(serverName.split("."))==2:
		target = AdminControl.completeObjectName('type=Server,node='
			+serverName.split(".")[0]+',name='+serverName.split(".")[1]+',*')
	else:
		target = AdminControl.completeObjectName('type=Server,name='+serverName+',*')
	if target:
		return AdminControl.getAttribute(target,"state")
	else:
		return "stopped"

def getServerList():
	servers = []
	serverlist=AdminConfig.list('Server').split('\n')
	for serverObj in serverlist:
		# print serverObj
		servers.append(serverObj[serverObj.find("nodes")+6:serverObj.find("servers")-1]+"."+serverObj.split('(')[0])
	print servers
	return servers

def getServerNode(serverName):
	serverlist=AdminConfig.list('Server').split('\n')
	for serverObj in serverlist:
		s = serverObj.split('(')[0]
		if s==serverName:
			nodeName = serverObj[serverObj.find("nodes")+6:serverObj.find("servers")-1]
			# print nodeName
			return nodeName



try:
	# print AdminApp.list()
	options = getOptions()
	ret = 0
	print options.method
	if options.method == None:
		ret = fullDeploy(options)
	elif options.method == "deploy":
		ret = simpleDeploy(options)
	elif options.method == "stop":
		ret = ensureState(options, "stopped", "stop")
	elif options.method == "start":
		ret = ensureState(options, "running", "start")
	elif options.method == "restart":
		ret = ensureState(options, "stopped", "stop")
		ret = ensureState(options, "running", "start")
	elif options.method == "check":
		ret = checkUrl(options)

	if ret:
		pass
	else:
		sys.exit(1)
	# sys.exit(ret)
except Exception, e:
	print "Executed Failed with messages:"
	print str(e)
	traceback.print_exc()
	sys.exit(1)

