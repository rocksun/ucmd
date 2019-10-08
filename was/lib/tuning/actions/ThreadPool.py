import os

min=512
max=512

def app_server_tuning(server_confid):
    server_name=AdminConfig.showAttribute(server_confid, "name")
    threadpool_list=AdminConfig.list('ThreadPool',server_confid).split("\n")
    for tp in threadpool_list:
        if tp.count('WebContainer')==1:
            print "Modify Server '%s' WebContainer Pool Min=%d, Max=%d"% (server_name, min, max)
            AdminConfig.modify(tp,[["minimumSize" ,min],["maximumSize" ,max]])


