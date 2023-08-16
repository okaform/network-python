from net_connection import *
import re

conn = r1_conn()

def get_loopback0():
    raw_output = conn.send_command("show ip interface brief | include Loopback0", read_timeout=180)
    ipv4_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
    find_ipv4 = re.search(ipv4_pattern, raw_output)
    if find_ipv4:
        found_ipv4 = find_ipv4.group()
        #print(found_ipv4)
        return found_ipv4
    else:
        print("No loopback found!")
        return("No loopback found!")
    

def get_hostname():
    raw_output = conn.send_command("show running-config | include (hostname )", read_timeout=180)
    hostname = raw_output.split(" ")[1]
    #print(hostname)
    return hostname

def get_snmp_location():
    location = conn.send_command("show snmp location", read_timeout=180)
    #print(location)
    return location
    