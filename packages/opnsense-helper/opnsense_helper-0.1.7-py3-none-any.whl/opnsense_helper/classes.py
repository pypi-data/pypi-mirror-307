
import paramiko
import xml.etree.ElementTree as ET
import logging

from opnsense_helper.utils import parseChild, update_xml_file,  get_element, api_get, api_post, aliases
class Interface:
    def __init__(self, name, parent):
        self.descr = parseChild(parent, "descr")
        self.enable = parseChild(parent, "enable")
        self.ipaddr = parseChild(parent, "ipaddr")
        self.subnet = parseChild(parent, "subnet")
        self.type = parseChild(parent, "type")
        self.virtual = parseChild(parent, "virtual")
        self.spoofmac=parseChild(parent, "spoofmac")
        self.attr={}

class Vlan:
    def __init__(self,name, parent):
        self.parentinterface =parseChild(parent, "if")
        self.tag = parseChild(parent,"tag")
        self.pcp = parseChild(parent,"pcp")
        self.proto = parseChild(parent,"proto")
        self.descr = parseChild(parent,"descr")
        self.vlanif = parseChild(parent,"vlanif")
        self.attr={}

class Dhcpd:
    def __init__(self, name, parent):
        self.enable = parseChild(parent, "enable")
        self.ddnsdomainalgorithm = parseChild(parent, "ddnsdomainalgorithm")
        self.range={
            "_from":"",
            "_to":""
        }
        self.attr={}
class Opnsense_Helper():
    def __init__(self, host=None, ssh_auth=None, api_auth=None, filepath="./config.xml", verbose=False):
        if(verbose):
            self.logging=logging.basicConfig(level=logging.DEBUG)
        self.objects={
        "vlans":{},
        "dhcpd":{},
        "interfaces":{}
        }
        self.filepath= filepath
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(host, username=ssh_auth["user"], password=ssh_auth["passw"])
        if("api_key" in api_auth):
            self.sftp = self.ssh.open_sftp() 
            self.url = host
            self.api_key = api_auth["api_key"]
            self.api_secret = api_auth["api_secret"]
            self.ssl=api_auth["ssl"]
            self.verify=api_auth["verify"]
            self.host=host

    def initialize(self):
        """
        Initialize the configuration.

        This method reads the configuration from the in-memory configuration. 
        The configuration is read from the
        remote host via the SSH protocol or the opnsense API.
        Either run get_backup() or get_conf() before calling this method.
        This method is not called automatically when the class is instantiated, so you need to get the conf file before and then call this method.

        """
        self.get_all("dhcpd")
        self.get_all("vlans")
        self.get_all("interfaces")
    def save(self,output):
        """
        Save the current configuration to a file.

        This method takes the current in-memory configuration and saves it to a
        file specified by the output parameter. The file is written in XML
        format.

        Parameters
        ----------
        output : str
            The path to the file to which the configuration should be written.
        """
        update_xml_file(self.objects["dhcpd"],self.root,"dhcpd")
        update_xml_file(self.objects["interfaces"],self.root,"interfaces")
        #update_xml_file(self.objects["vlans"],self.root,"vlans")
        with open(output, 'w') as f:
            f.write(ET.tostring(self.root, encoding='unicode', method='xml'))
    def get_all(self,element):
        """
        Get all objects of a given type from the in-memory xml data.

        This method returns a dictionary containing all objects of this type. The dictionary keys are the tags
        of the elements, and the values are dictionaries containing the
        attributes and subelements of the elements.

        Parameters
        ----------
        element : str
            The type of the objects to retrieve. Can be "dhcpd", "interfaces",
            or "vlans".

        Returns
        -------
        dict
            A dictionary containing all objects of the given type.
        """
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
                if element != "vlans": 
                    name = key.tag
                else:
                     name = child.descr
                self.objects[element][name]=child.__dict__
                print(f'''{key.tag} : {child.__dict__}
                -------------------''')
        return(self.objects[element])
    def close_con(self):
        self.sftp.close()
        self.ssh.close()
    def put_file(self, _from,_to):    
        """
        Apply the configuration.
        Transfer a file from the local host to the remote host.

        Parameters
        ----------
        _from : str
            The path to the file on the local host.
        _to : str
            The destination path on the remote host where the file should be stored.
        """
        self.sftp.put(_from, _to)
    def add_Items(self,type, data):
        """
        Add objects of a given type to the in-memory xml data.

        This method adds all objects given in the data parameter to the in-memory
        xml data. The objects are stored in the self.objects dictionary.

        Parameters
        ----------
        type : str
            The type of the objects to add. Can be "dhcpd", "interfaces",
            or "vlans".

        data : dict
            A dictionary containing the objects to add. The keys are the tags of
            the elements, and the values are dictionaries containing the
            attributes and subelements of the elements.

        Returns
        -------
        None
        """
        def replace(item):
            Data = {}
            #data='{"vlan": {"descr": "example2", "if": "vtnet1", "tag": 110, "pcp": 0, "vlanif": "vlan0.110"}}'
            for key, value in item.items():
                if key in aliases.keys():
                    Data[aliases[key]] = value
                else:
                    Data[key] = value 
            return Data
        print(type)
        print(data)
        print(self.objects)
        # if( type== "vlans"):
        #     vlans= api_get(self,"interfaces/vlan_settings/get")
        for name, value in data.items():
            value["attr"]={}
            self.objects[type][name] = value
    def set_vlans(self,vlans):
        for value in vlans:
                    print("---------set vlan-----------------")
                    payload={"vlan":value}
                    r=api_post(self,"interfaces/vlan_settings/set",payload)
                    print(r)
    def add_vlans(self,vlans):
        for value in vlans:
            print("---------add vlan-----------------")
            print(value)
            payload={"vlan":value}
            r=api_post(self,"interfaces/vlan_settings/addItem",payload)
            print(r)
            r=api_post(self,"interfaces/vlan_settings/reconfigure",{})
            print(r)
    # please use the get_backup function to avoid losing data
    
    def get_conf(self,_from,_to=None):
        """
        Get the config file from the remote host and save it to a file.

        Parameters
        ----------
        _from : str
            The path to the file on the remote host.
        _to : str
            The path to the file on the local host. If None, the file is saved
            to the location specified in self.filepath.
        """
        if _to == None:
            _to=self.filepath
        self.sftp.get(_from,_to)
        self.tree = ET.parse(_to)
        self.root = self.tree.getroot()
    def get_backup(self,output=None):
        """
        this function is currently deprecated
        it was used to get the config file using the api
        i left it in however if someone wants to fetch a certain backup 
        i need to implement the backup selection though
        """
        command = 'core/backup/download/this'
        backup=api_get(self,command)
        self.root=backup
        print(ET.tostring(backup, encoding='unicode'))
        # if output != None:
        #     path=output
        # else:
        #     path = self.filepath
        # with open(path, 'w') as f:
        #     f.write(ET.tostring(backup, encoding='unicode', method='xml'))

     #   getRes(self.host, command, self.api_key, self.api_secret, timeout)


