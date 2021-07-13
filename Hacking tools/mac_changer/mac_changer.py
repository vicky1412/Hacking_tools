#!/usr/bin/env python

import subprocess
import optparse
import re
import sys

def get_arg():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="interface to change mac address")
    parser.add_option("-m", "--mac", dest="new_mac", help="new mac address to change")
    (option,arguments) = parser.parse_args()
    if not option.interface:
        parser.error("Enter the correct interface or use --help to know how to use macchanger")
    elif not option.new_mac:
        parser.error("Enter the correct mac or use --help to know how to use macchanger")
    return option

def change_mac(interface,new_mac):
    x = subprocess.call(["ifconfig", interface, "down"])
    y = subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    z = subprocess.call(["ifconfig", interface, "up"])

    if x == y == z == 0:
        return
    else:
        print("[-] Check that you put a valid interface and mac address")
        sys.exit()






def permanent_mac(interface):
    per_mac = subprocess.call(["ethtool","-P",interface])

def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac_address = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)
    if mac_address:
        return mac_address.group(0)
    else:
        print("Could not find mac address")

option = get_arg()

current_mac = get_current_mac(option.interface)
print("Current mac =" + str(current_mac))

permanent_mac(option.interface)

change_mac(option.interface, option.new_mac)

new_mac = get_current_mac(option.interface)
if new_mac == option.new_mac:
    print("New mac =" + str(new_mac))
else:
    print("Mac address did not get changed")
