import xml.etree.ElementTree as ET
import paramiko
from .utils import  parseChild,update_xml_file,aliases, get_element, getRes


class Interface:
    def __init__(self, name, parent):
        self.descr = parseChild(parent, "descr")
        self.enable = parseChild(parent, "enable")
        self.ipaddr = parseChild(parent, "ipaddr")
        self.subnet = parseChild(parent, "subnet")
        self.type = parseChild(parent, "type")
        self.virtual = parseChild(parent, "virtual")
        self.spoofmac=parseChild(parent, "spoofmac")
        self.attr=None

class Vlan:
    def __init__(self,name, parent):
        self.parentinterface =parseChild(parent, "if")
        self.tag = parseChild(parent,"tag")
        self.pcp = parseChild(parent,"pcp")
        self.proto = parseChild(parent,"proto")
        self.descr = parseChild(parent,"descr")
        self.vlanif = parseChild(parent,"vlanif")
        self.attr=None

class Dhcpd:
    def __init__(self, name, parent):
        self.enable = parseChild(parent, "enable")
        self.ddnsdomainalgorithm = parseChild(parent, "ddnsdomainalgorithm")
        self.range={
            "_from":"",
            "_to":""
        }
        self.attr=None


class OpennsenseHelper():
    def __init__(self, filepath, method=None, user=None, passw=None,  host=None, api_key=None, api_secret=None):
        self.filepath=filepath
        self.tree = ET.parse(filepath)
        self.root = self.tree.getroot()
        self.objects={
        "vlans":{},
        "dhcpd":{},
        "interfaces":{}
        }

        if(method=="ssh"):
            self.ssh = paramiko.SSHClient()
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh.connect(host, username=user, password=passw)
            self.sftp = self.ssh.open_sftp() 
            #self.ssh .open_sftp
        if(method=="http"):
            self.url = host
            self.api_key = api_key
            self.api_secret = api_secret
            self.host=host

    def initialize(self):
        self.get_all("dhcpd")
        self.get_all("vlans")
        self.get_all("interfaces")
    def save(self,output):
        update_xml_file(self.objects["dhcpd"],self.root,"dhcpd")
        update_xml_file(self.objects["interfaces"],self.root,"interfaces")
        update_xml_file(self.objects["vlans"],self.root,"vlans")
        with open(output, 'w') as f:
            f.write(ET.tostring(self.root, encoding='unicode', method='xml'))
    
    def get_all(self,element):
        print(f'''          -----------------------------
                    {element}''')
        for parent in self.root.findall(element):
            for key in parent:
                if element== "dhcpd":
                        child = Dhcpd(key.tag,parent)
                elif element== "interfaces":
                        child = Interface(key.tag,parent)
                elif element== "vlans":
                        child = Vlan(key.tag,parent)

                child=get_element(parent, key.tag, child)
                if element== "dhcpd":
                    _range={"_from": parent.find(key.tag).find("range/from"),
                    "_to":parent.find(key.tag).find("range/to")}
                    if _range["_from"] is not None:
                        _range["_from"]=_range["_from"].text
                        _range["_to"]=_range["_to"].text
                        child.range =_range
                child.attr=key.attrib if key.attrib is not None else None
                print(child.attr) 
                self.objects[element][key.tag]=child.__dict__
                print(f'''{key.tag} : {child.__dict__}
                -------------------''')

        return(self.objects[element])
    def close_con(self):
        self.sftp.close()
        self.ssh.close()
    def put_file(self, _from,_to):    
        self.sftp.put(_from, _to)
    def get_file(self,_from,_to):
        self.sftp.get(_from,_to)
    def get_backup(self,_from,_to):
        command = 'core/firmware/status'
        timeout = 5
        getRes(self.host, command, self.api_key, self.api_secret, timeout)


