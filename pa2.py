import sys
import yaml
import json
import xml.etree.ElementTree as ET
from pathlib import Path

class Device:
    def __init__(self, id, role, os, owner, interfaces):
        self.id = id
        self.role = role
        self.os = os
        self.owner = owner
        self.interfaces = interfaces



data_str = ""

#test if can read the str transfered from the file
try:
    #convert file into string data type
    with open("PA2_sample1.xml", "r") as f:
        data_str = f.read()

    root = ET.fromstring(data_str)
    print(root.tag)
    print(root.attrib)

except FileNotFoundError as e:
    print("file not found", e)


policy_str = ""
#test if can open and transfer the policy file
try:
    with open("PA2_policy.yaml", "r") as f:
        policy_str = f.read()

    policy = yaml.safe_load(policy_str)
    print(policy["min_os"]["switch"])

except FileNotFoundError as e:
    print("file not found", e)

#convert root into dict
devices = []
for device in root:
    id = device.get("id")
    if id is None:
        continue

    os = device.get("os")
    role = device.get("role")
    owner = device.findtext("owner")

    #make a list for interfaces, and append them into the list
    interfaces = []
    #make a dict for each interface
    for interface in device.findall("interface"):
        name = interface.get("name")
        status = interface.get("status")
        an_interface = {"name": name, "status": status}
        interfaces.append(an_interface)

    #test the output, delete later
    print(id, interfaces)
        

    a_device = Device(id, role, os, owner, interfaces)
    devices.append(a_device)

print()
print(len(devices))
print(devices[0].id)
print(devices[1].interfaces)
    
    




