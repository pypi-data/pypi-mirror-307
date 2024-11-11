import xml.etree.ElementTree as ET
import re
import paramiko
# import libraries
import json
import requests
import os
from . import utils

class Interface:
    def __init__(self, name, parent):
        self.descr = utils.parseChild(parent, "descr")
        self.enable = utils.parseChild(parent, "enable")
        self.ipaddr = utils.parseChild(parent, "ipaddr")
        self.subnet = utils.parseChild(parent, "subnet")
        self.type = utils.parseChild(parent, "type")
        self.virtual = utils.parseChild(parent, "virtual")
        self.spoofmac=utils.parseChild(parent, "spoofmac")
        self.attr=None

class Vlan:
    def __init__(self,name, parent):
        self.parentinterface =utils.parseChild(parent, "if")
        self.tag = utils.parseChild(parent,"tag")
        self.pcp = utils.parseChild(parent,"pcp")
        self.proto = utils.parseChild(parent,"proto")
        self.descr = utils.parseChild(parent,"descr")
        self.vlanif = utils.parseChild(parent,"vlanif")
        self.attr=None

class Dhcpd:
    def __init__(self, name, parent):
        self.enable = utils.parseChild(parent, "enable")
        self.ddnsdomainalgorithm = utils.parseChild(parent, "ddnsdomainalgorithm")
        self.range={
            "_from":"",
            "_to":""
        }
        self.attr=None


class opnsensehelper():
    def __init__(self, filepath, ssh=None, user=None, passw=None, remote_address=None):
        self.filepath=filepath
        self.tree = ET.parse(filepath)
        self.root = self.tree.getroot()
        self.objects={
        "vlans":{},
        "dhcpd":{},
        "interfaces":{}
        }

        if(ssh!=None):
            self.ssh = paramiko.SSHClient()
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh.connect(remote_address, username=user, password=passw)
            self.sftp = self.ssh.open_sftp() 
            #self.ssh .open_sftp
    def initialize(self):
        self.get_all("dhcpd")
        self.get_all("vlans")
        self.get_all("interfaces")
    def save(self,output):
        utils.update_xml_file(self.objects["dhcpd"],self.root,"dhcpd")
        utils.update_xml_file(self.objects["interfaces"],self.root,"interfaces")
        utils.update_xml_file(self.objects["vlans"],self.root,"vlans")
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

                child=utils.get_element(parent, key.tag, child)
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




def test():
    filepath = '/home/ji/confignew.xml'
    output="/home/ji/.ansible/collections/ansible_collections/ji_podhead/podnet/plugins/x.xml"
    conf_path="/conf/config.xml"
    #curl -k -u $OPNS_KEY:$OPNS_SECRET https://$IPFW/api/diagnostics/interface/getinterfaceconfig
    api_key = 'oNRfkFFndCAaD8yRo/kImZEKZ80uHKWuPoCHWUQkgjlwbrCAnWzH82D9byFJRJyL8/qNeEUHhCKUo3PI'
    api_secret = '2ypsTRzKQIq8yS0uK2tl47qj50w29ExvUBSYoBuX6FyQKbfaOfMUo5pSNOmrFx8ZDtrQaJWZTv8hNQ9I'
    host="192.168.1.103"
    command = 'core/firmware/status'
    command2= 'diagnostics/interface/getinterfaceconfig'
    command3 = 'core/interfaces/gif_settings/get'
    timeout = 5

    utils.getRes(host, command2, api_key, api_secret, timeout)
    vlan3 ={'parentinterface': 'vtnet1', 'tag': '3', 'pcp': '0', 'proto': None, 'descr': 'vlan3', 'vlanif': 'vlan0.3',"attr":{"uuid":"cb503df8-821d-4acd-86ba-66b35e4df17n"}}
    vlan4 ={'parentinterface': 'vtnet1', 'tag': '4', 'pcp': '0', 'proto': None, 'descr': 'vlan4', 'vlanif': 'vlan0.4',"attr":{"uuid":"cb503df8-821d-4acd-86ba-66b35e4s7c"}}
    opt3_dhcp= {'enable': '1', 'ddnsdomainalgorithm': 'hmac-md', "range":{'from': '200.0.3.10', '_to': '200.0.3.100'},"attr":None}
    opt4_dhcp= {'enable': '1', 'ddnsdomainalgorithm': 'hmac-md', "range":{'from': '200.0.4.10', '_to': '200.0.4.100'},"attr":None}
    opt3_interface= {'descr': 'vlan3', 'enable': '1', 'ipaddr': '200.0.3.1', 'subnet': '24', 'type': None, 'virtual': None, 'spoofmac': '00:00:00:00:00:03', 'attr': {}}
    opt4_interface= {'descr': 'vlan4', 'enable': '1', 'ipaddr': '200.0.3.1', 'subnet': '24', 'type': None, 'virtual': None, 'spoofmac': '00:00:00:00:00:04', 'attr': {}}
    helper=opnsensehelper(filepath,True,"root","opnsense","192.168.1.103")
    helper.get_file(conf_path, output)
    helper.initialize()
    helper.objects["dhcpd"]["opt3"]=opt3_dhcp
    helper.objects["dhcpd"]["opt4"]=opt4_dhcp
    helper.objects["vlans"]["vlan3"]=vlan3
    helper.objects["vlans"]["vlan4"]=vlan4
    helper.objects["interfaces"]["opt3"]=opt3_interface
    helper.objects["interfaces"]["opt4"]=opt4_interface
    helper.save(output)
    helper.put_file(output,conf_path)
    helper.close_con()
if __name__ == "__main__":
    test()