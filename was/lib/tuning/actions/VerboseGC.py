# import java

# lineSeparator = java.lang.System.getProperty('line.separator')
# appServer_gc_verbose = "TRUE"

verbose="false"

def app_server_tuning(server_confid):
    server_name=AdminConfig.showAttribute(server_confid, "name")
    jvm_path="/Server:%s/JavaProcessDef:/JavaVirtualMachine:/" % server_name
    jvm_confid=AdminConfig.getid(jvm_path)
    print "Modify Server '%s' VerboseGC to %s" % (server_name, verbose)
    AdminConfig.modify(jvm_confid, [["verboseModeGarbageCollection", verbose]])

