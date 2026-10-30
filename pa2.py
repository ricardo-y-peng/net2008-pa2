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

    def check_owner(self):
        if self.owner is None:
            return "missing_owner"

    def check_interfaces(self):
        down_int = 0
        for interface in self.interfaces:
            if interface["status"] == "down":
                down_int += 1
        return down_int

    

   



    
        



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

#convert root into a dict of Device class
devices = []
skipped_devices = 0
for device in root:
    id = device.get("id")
    if id is None:
        skipped_devices += 1
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

total_devices = len(devices)

#go for audit
audit = {}

site = root.get("site")
audit["site"] = site
audit["total_devices"] = total_devices
audit["skipped_devices"] = skipped_devices

roles = {}
#go loop the list devices of class Device
for device in devices:
    role = device.role
    if role in roles:
        roles[role] += 1
    else:
        roles[role] = 1
print("the roles: ", roles)
audit["roles"] = roles


#interfaces key in audit
int_status = {"up":0, "down":0, "other": 0}
for device in devices:
   for interface in device.interfaces:
       status = interface["status"]
       if status == "up":
           int_status["up"] += 1
       elif status == "down":
           int_status["down"] += 1
       else:
           int_status["other"] += 1
           
print("the interface status: ", int_status)
audit["interfaces"] = int_status


#violations and compliant key
violations = []
for device in devices:

    #check if policy require to check owner first
    if policy["require_owner"] == True:
        #then check the owner
        if device.check_owner() == "missing_owner":
                violation = {}
                violation["device"] = device.id
                violation["type"] = "missing_owner"
                violations.append(violation)

    #check if policy require to check too many down interfaces
    if policy["max_down_interfaces"] is not None:
        down_int = device.check_interfaces()
        if down_int > policy["max_down_interfaces"]:
            violation = {}
            violation["device"] = device.id
            violation["type"] = "too_many_down"
            violation["down"] = down_int
            violations.append(violation)


    

audit["violations"] = violations





    
    




