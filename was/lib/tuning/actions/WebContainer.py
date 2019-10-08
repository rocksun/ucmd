import os

props="com.ibm.ws.webcontainer.extractHostHeaderPort:true,trusthostheaderport:true"

def addOrModify(server_confid, name, value):
    server_name=AdminConfig.showAttribute(server_confid, "name")
    wc = AdminConfig.list('WebContainer',server_confid)
    currentProps = AdminConfig.list('Property',wc).splitlines()
    for prop in currentProps:
        if name == AdminConfig.showAttribute(prop, "name"):
            print "Prop %s already set , modify the value with %s" % (name, value)
            AdminConfig.modify(prop, [['value', value]])
            return 
    print "Prop %s Have not set, add prop with value %s" % (name, value)
    attr = [['name',name],['value',value]]
    AdminConfig.create('Property', wc, attr)

def app_server_tuning(server_confid):

    if props != None and props.strip() != "":
        propList = props.split(",")
        for propNameAndValue in propList:
            name = propNameAndValue.split(":")[0].strip()
            value = propNameAndValue.split(":")[1].strip()
            # print name, value
            addOrModify(server_confid, name, value)

    
    


