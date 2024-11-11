import xml.etree.ElementTree as ET
# import libraries
import json
import xml.etree.ElementTree as ET
import requests
import os

aliases={
"parent": "if",
"_from":"from",
"_to":"to",
"interface":"if"
}

def parseChild(child, tag):
        result=child.find(tag)
        element=result.text if  result is not None else None
        return element

def ping(helper):
    response = os.system(f"ping -c 1 {helper.host}")
    if response == 0:
        print(f"IP {helper.host} is reachable")
        return 0
    else: return 1

def reconfigure_vlans(helper):
    stdin, stdout, stderr = helper.ssh.exec_command('/usr/local/opnsense/scripts/interfaces/reconfigure_vlans.php')
    output = stdout.read().decode('utf-8')
    print(output)
    error = stderr.read().decode('utf-8')
    if error:
        print(f"Fehler: {error}")


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
        if(type=="vlans"):
            key="vlan"

        if value["attr"] is not None:
             e = ET.SubElement(el, key,value["attr"])
        else:
            e=ET.SubElement(el,key)
        recoursion(e,value)

# deprecated due to a logic fail
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

def replace(item):
    Data = {}
    #data='{"vlan": {"descr": "example2", "if": "vtnet1", "tag": 110, "pcp": 0, "vlanif": "vlan0.110"}}'
    for key, value in item.items():
        if key in aliases.keys():
            Data[aliases[key]] = value
        else:
            Data[key] = value 
    return Data
