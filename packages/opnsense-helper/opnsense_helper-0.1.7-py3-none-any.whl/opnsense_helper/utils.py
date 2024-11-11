import xml.etree.ElementTree as ET
# import libraries
import json
import xml.etree.ElementTree as ET
import requests
import os

aliases={
"parentinterface": "if",
"_from":"from",
"_to":"to",
"interface":"if"
}

#curl -k -u $OPNS_KEY:$OPNS_SECRET https://$IPFW/api/diagnostics/interface/getinterfaceconfig

def parseChild(parent, tag):
    result=parent.find(tag)

    element=result.text if  result is not None else None
    return element

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

def ping(helper):
    response = os.system(f"ping -c 1 {helper.host}")
    if response == 0:
        print(f"IP {helper.host} is reachable")
        return 0
    else: return 1
def api_get(helper, command,params=None):
    #url= "https://192.168.1.103/api/interfaces/vlan_settings/get"
    s="s" if helper.ssl is True else ""
    url = f"http{s}://{helper.host}/api/{command}"
    r = requests.get(url, verify=helper.verify, params=params,  auth=(helper.api_key, helper.api_secret))


    if r.status_code == 200:
        if 'application/json' in r.headers['Content-Type']:
            # Verwenden Sie json.dump
            response = json.loads(r.content)
        else:
            # Verwenden Sie ET.fromstring
            response = ET.fromstring(r.content)
        return (response)
    else:
        print ('Connection / Authentication issue, response received:')
        print (r.text)
def api_post(helper, command, Data):
    def post(Data,url):
        return requests.post(url, verify=helper.verify, allow_redirects=False, headers={'Content-Type': 'application/json'},  auth=(helper.api_key, helper.api_secret), data=Data)
    def fail(error):
        print ('Connection / Authentication issue, response received:')
        print (error)
    def success(response):
        response = json.loads(r.text)
        return (response)
    Data=json.dumps(Data)
    s="s" if helper.ssl is True else ""
    url = f"http{s}://{helper.host}/api/{command}"
    r = post(Data,url)
    if r.status_code == 200:
        return success(r)
    # if we fail because of redirect we start a new request
    # if we allow redirect in the first place, our post request will get turned in a get request
    elif r.status_code == 301:
        new_url = r.headers['Location']
        r = post(Data,new_url)
        if r.status_code == 200:
            return success(r)
        else:
            fail(r.text)
    else:
        fail(r.text)
def get_vlans(helper):
    command="interfaces/vlan_settings/get"
    vlans=api_get(helper,command)
    print(vlans)     

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
        print(objects)
        if(type=="vlans"):
            key="vlan"

        if value["attr"] is not None:
             e = ET.SubElement(el, key,value["attr"])
        else:
            e=ET.SubElement(el,key)
        recoursion(e,value)
