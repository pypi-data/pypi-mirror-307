import opnsense_helper.opnsense_helper 
opnsensehelper=opnsense_helper.opnsense_helper
def test():
    filepath = '/home/ji/confignew.xml'
    output="/home/ji/.ansible/collections/ansible_collections/ji_podhead/podnet/plugins/x.xml"
    conf_path="/conf/config.xml"
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