import xml.etree.ElementTree as ET
import re
import paramiko
# import libraries
import json
import requests
import os
aliases={
"parentinterface": "if",
"_from":"from",
"_to":"to"
}

def getRes(host, command, api_key, api_secret, timeout = 5):
    host = '192.168.1.103'
    response = os.system(f"ping -c 1 {host}")
    if response == 0:
        print(f"IP {host} is reachable")
        url = f"https://{host}/api/{command}"
        r = requests.get(url, verify=False,  auth=(api_key, api_secret))
        # verify='OPNsense.pem',
        if r.status_code == 200:
            response = json.loads(r.text)
            with open('/home/ji/.ansible/collections/ansible_collections/ji_podhead/podnet/plugins/data.json', 'w') as f:
                json.dump(response, f)
            print (response)
        else:
            print ('Connection / Authentication issue, response received:')
            print (r.text)
    else:
        print(f"IP {host} is not reachable")
def get_child(root,element, id, keys):
    elements=[]
    for parent in root.findall(element):
        child= {}
        for y in keys:
            child[y]=None
        for x in parent.findall(id):
            for key in keys:
                child[key]=parseChild(x, key)
        elements.append(child)
    return elements
def parseChild(parent, tag):
    result=parent.find(tag)

    element=result.text if  result is not None else None
    return element

def get_element(root,id, obj):
    for x in root.findall(id):
        for key in obj.__dict__.keys():
#            if isinstance(obj.__dict__[key], dict):
            if(key!="_to"and key!="_from"):
                
                if key in aliases.keys():
                    key2 = aliases[key] 
                    y=parseChild(x, key2)
                else:
                    y=parseChild(x, key)
                setattr(obj, key, y)
    return obj

def recoursion(e, value):
    for key2, value2 in value.items():
        if(key2!="attr"):
            if key2 in aliases.keys():
                key2 = aliases[key2] 
            x=ET.SubElement(e, key2)
            if isinstance(value2, dict):
                recoursion(x,value2)
            else:
                x.text = value2

def update_xml_file(objects,root,type):
    el = root.find(type)
    el.clear()
    for key, value in objects.items():
        if value["attr"] is not None:
             e = ET.SubElement(el, key,value["attr"])
        else:
            e=ET.SubElement(el,key)
        recoursion(e,value)
