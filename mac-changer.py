#!/usr/bin/python3

import subprocess
import optparse
import re

def search_mac_address(string):
    return re.search(r'([0-9A-Fa-f]{2}[:]){5}([0-9A-Fa-f]{2})', str(string)).group(0)

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC address")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify an interface, use -h or --help for more information.")
    elif not options.new_mac:
        parser.error("[-] Please specify new mac address, use -h or --help for more information")
    return options
    

def set_new_mac_address(interface, new_mac) :
    print("[+] Changing MAC address for " + interface + " to " + new_mac)
    subprocess.call("sudo ifconfig " + interface + " down", shell=True)
    print("[+] " + interface + " down")
    subprocess.call("sudo ifconfig " + interface + " hw ether " + new_mac, shell=True)
    subprocess.call("sudo ifconfig " + interface + " up", shell=True)
    print("[+] " + interface + " up")

def get_mac_address_from_interface(interface):
    ifconfig_result = subprocess.check_output(["sudo", "ifconfig", interface])
    mac_address_search_result = search_mac_address(ifconfig_result)
    if mac_address_search_result:
        return mac_address_search_result
    else:
        print("[-] Could not read MAC address")
        

options = get_arguments()
current_mac_address = get_mac_address_from_interface(options.interface)
print("Current MAC address for interface " + options.interface + " is " + current_mac_address)

set_new_mac_address(options.interface, options.new_mac)

new_mac = get_mac_address_from_interface(options.interface)
if new_mac == options.new_mac:
    print("[+] MAC address was successfully changed to " + new_mac + ".")
else:
    print("[-] MAC address dit not get changed.")