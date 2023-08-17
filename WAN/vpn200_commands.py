'''This section is for VPN 200. We Got This!'''
from net_connection import *
from no_net_connection import *
import re, os, sys

conn = r1_conn()
#create the List needed globally
static_list = []
next_hop_list = []


def generate_static_route_list(route_type, prefix_number): 
    #if static_list is not empty and aggregate_list is also not empty and next_hop_list is also not empty, then we return the list item based on the route type or an empty string
    if len(static_list) != 0 or len(next_hop_list) != 0:
        if route_type == "s" and prefix_number <= len(static_list):
            return static_list[prefix_number - 1] #return the static route
        elif route_type == "n" and prefix_number <= len(next_hop_list):
            return next_hop_list[prefix_number - 1] #return the next hop
        else:
            return ""        
 
    else: #get the actual data from the router and return the first line. This should only be run once
        ##print("This should only be seen ONCEEEEE!")
        #Get the static routes
        static_routes = conn.send_command("show running-config | include ip route vrf IECN", read_timeout=180)
        split_static_routes = static_routes.split('\n')
        ##print(split_static_routes)
        reg = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|Null0)')
        for line in split_static_routes:
            mo = reg.findall(line)
            ip = mo[0] #this is for the ip
            subnet = convert_to_cidr(mo[1]) #convert the subnet mask to cidr notation
            complete_static = str(ip) + "/"+str(subnet) #concatenate the ip to the subnet mask
            gateway = mo[2]
            static_list.append(complete_static) #add complete_static IP to static list
            next_hop_list.append(gateway) #add gateway to next_hop list
        
        if route_type == "s" and prefix_number <= len(static_list):
            return static_list[prefix_number - 1] #return the static route
        elif route_type == "n" and prefix_number <= len(next_hop_list):
            return next_hop_list[prefix_number - 1] #return the next hop
        else:
            return ""      

def get_vpn200_static_route(route_type, prefix_number):
    static_route = generate_static_route_list(route_type, prefix_number)
    return static_route

def get_vpn200_next_hop(route_type, prefix_number):
    next_hop = generate_static_route_list(route_type, prefix_number)
    return next_hop

def get_000_212_description():
    int_gi000_25 = conn.send_command("show running-config interface GigabitEthernet 0/0/0.212 | include description", read_timeout=180)
    return int_gi000_25.split("description")[1] #return the second portion of the splitted string which is the actual description 

def get_000_212_ip_address():
    int_gi000_25 = conn.send_command("show running-config interface GigabitEthernet 0/0/0.212 | include ip address", read_timeout=180)
    split_line = int_gi000_25.split(" ")#split by the spaces
    ip = split_line[3] #this is for the ip
    subnet = convert_to_cidr(split_line[4]) #convert the subnet mask to cidr notation    
    return str(ip) + "/"+str(subnet) #concatenate the ip to the subnet mask 

def get_000_212_shutdown(): 
    int_gi000_25 = conn.send_command("show running-config interface GigabitEthernet 0/0/0.212 | include shutdown", read_timeout=180)
    if int_gi000_25 == "": #check if keyword shutdown is present, command should return an empty string
        return "FALSE"
    else:
        return "TRUE"

def get_000_212_vrrp():
    int_gi000_25 = conn.send_command("show running-config interface GigabitEthernet 0/0/0.212 | include standby", read_timeout=180)
    reg = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|Null0)') #use regular expression to find the ip. We could also use split but this is more generic
    mo = re.search(reg, int_gi000_25)
    return mo.group()