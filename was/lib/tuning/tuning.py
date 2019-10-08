import os
import traceback
# import actions.HeapSize
# print (sys.version_info)

actions = {}

def fetchModules():
    actionPath = os.environ.get('ABSWASBASEDIR')+"/lib/tuning/actions"
    tuningACTIONS = os.environ.get('TUNINGACTIONS')
    print "TUNINGACTIONS: ", tuningACTIONS
    if tuningACTIONS!=None:
        tuningACTIONS=tuningACTIONS.split(",")
    actions = os.listdir(actionPath)
    for action in actions:
        if action.endswith(".py") and action!="__init__.py":
            if len(action.split("."))==2:
                moduleName = action.split(".")[0]
                if tuningACTIONS!=None:
                    if moduleName.upper() in tuningACTIONS:
                        storeAction(moduleName) 
                else:
                    storeAction(moduleName)
            else:
                print "Maybe a invalid module '"+action+"', skipped."

def storeAction(moduleName):
    exec("import actions."+moduleName+" as "+moduleName)
    actions[moduleName]=vars()[moduleName]
    print "Load Action: "+moduleName
    for key in dir(actions[moduleName]):
        if not key.startswith("__") and not callable(getattr(actions[moduleName],key)):
            evn_key = 'T_'+moduleName.upper()+"_"+key.upper()
            env_value = os.environ.get(evn_key)
            if env_value!=None:
                print "Load custom setting: " +evn_key+"="+env_value
                setattr(actions[moduleName], key, env_value)
            # print key,evn_key, env_value
            # print getattr(actions[moduleName],key)

def tuning():
    doTuningAction("global_tuning", "-")
    server_confids=AdminConfig.list("Server")
    for server_confid in server_confids.split("\n"):
        server_confid=server_confid.strip()
        server_type=AdminConfig.showAttribute(server_confid, "serverType")
        # print server_type
        if server_type == "APPLICATION_SERVER":
            doTuningAction("app_server_tuning",server_confid)
        elif server_type == "DEPLOYMENT_MANAGER":
            doTuningAction("dmgr_server_tuning",server_confid)
        elif server_type == "NODE_AGENT":
            doTuningAction("node_server_tuning",server_confid)


def doTuningAction(func_name, server_confid):
    print "Tuning: "+server_confid
    for key,action in actions.items():
        if hasattr(action, func_name):
            method_to_call = getattr(action, func_name)

            try:
                method_to_call(server_confid)
            except Exception, e:
                print "Error in execute action function :"+key+" "+func_name
                print str(e)
                traceback.print_exc()
                print "Just Skipped"


fetchModules()
tuning()
AdminConfig.save()



