xms=512
xmx=512

def app_server_tuning(server_confid):
    server_name=AdminConfig.showAttribute(server_confid, "name")
    jvm_path="/Server:%s/JavaProcessDef:/JavaVirtualMachine:/" % server_name
    jvm_confid=AdminConfig.getid(jvm_path)
    print "Modify Server '%s' Heap Min=%dM, Max=%dM"% (server_name, xms, xmx)
    AdminConfig.modify(jvm_confid, [["initialHeapSize", xms],["maximumHeapSize", xmx]])

def dmgr_server_tuning(server_confid):
    print 'dmgrServerTuning'

def node_server_tuning(server_confid):
    print 'dmgrServerTuning'
