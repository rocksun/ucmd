# import java

# lineSeparator = java.lang.System.getProperty('line.separator')
# appServer_gc_verbose = "TRUE"

arguments=""

def app_server_tuning(server_confid):
    server_name=AdminConfig.showAttribute(server_confid, "name")
    jvm_path="/Server:%s/JavaProcessDef:/JavaVirtualMachine:/" % server_name
    jvm_confid=AdminConfig.getid(jvm_path)
    print "Modify Server '%s' genericJvmArguments to %s" % (server_name, arguments)
    AdminConfig.modify(jvm_confid, [["genericJvmArguments", arguments]])

