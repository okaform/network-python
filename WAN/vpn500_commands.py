'''This section is for VPN 500. Goodluck!'''
from net_connection import *
from no_net_connection import *
import re, os, sys

conn = r1_conn()

def generate_static_route_list(route_type, prefix_number): 
    #if the file exist,then return that line in the file, if it doesn't then run and return the line in the list
    file_name = "static-next_hop-aggregate.txt"
    if os.path.exists(file_name): #if the file exists, no need to run the others
        try:
            with open(file_name, 'r') as file: #open the file name of the object
                lines = file.readlines() #read the lines of the file 
                return lines[prefix_number - 1] #return the content of the line of the file 
        
        except FileNotFoundError:
            return f"File '{file_name}' not found."
            
    else: #get the actual data from the router and return the first line. This should only be run once
        #create the file

        #Get the static routes
        static_routes = conn.send_command("show running-config | include ip route vrf NA-Guest", read_timeout=180)
        split_static_routes = static_routes.split('\n')
        print(split_static_routes)
        reg = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|Null0)')
        aggregate_list = []
        static_list = []
        next_hop_list = []
        for line in split_static_routes:
            mo = reg.findall(line)
            ip = mo[0] #this is for the ip
            subnet = convert_to_cidr(mo[1]) #convert the subnet mask to cidr notation
            complete_static = str(ip) + "/"+str(subnet) #concatenate the ip to the subnet mask 
            
            gateway = mo[2]
            if gateway == "Null0": #add complete_static IP to aggregate list
                aggregate_list.append(complete_static)
            else:
                static_list.append(complete_static) #add complete_static IP to static list
                next_hop_list.append(gateway) #add gateway to next_hop list

        print("this is static list: " +str(static_list))
        print("this is aggregate list: " +str(aggregate_list))
        print("this is next hop list: " +str(next_hop_list))
        print("This is the prefix_njumber: " +str(prefix_number))
        print("this is the length of one of them: " +str(len(static_list)))
        if route_type == "s" and prefix_number <= len(static_list):
            return static_list[prefix_number - 1] #return the static route
        elif route_type == "n" and prefix_number <= len(next_hop_list):
            return next_hop_list[prefix_number - 1] #return the next hop
        elif route_type == "a" and prefix_number <= len(aggregate_list):
            return aggregate_list[prefix_number - 1] #return the aggregate route
        else:
            return ""

        

def get_vpn500_static_route(route_type, prefix_number):
    static_route = generate_static_route_list(route_type, prefix_number)
    return static_route

def get_vpn500_next_hop(route_type, prefix_number):
    next_hop = generate_static_route_list(route_type, prefix_number)
    return next_hop

def get_vpn500_aggregate(route_type, prefix_number):
    aggregate = generate_static_route_list(route_type, prefix_number)
    return aggregate
    
'''
def get_loopback0():
    raw_output = conn.send_command("show ip interface brief | include Loopback0", read_timeout=180)
    ipv4_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
    find_ipv4 = re.search(ipv4_pattern, raw_output)
    if find_ipv4:
        found_ipv4 = find_ipv4.group()
        print(found_ipv4)
        return found_ipv4
    else:
        print("No loopback found!")
        return("No loopback found!")
    

def get_hostname():
    raw_output = conn.send_command("show running-config | include (hostname )", read_timeout=180)
    hostname = raw_output.split(" ")[1]
    print(hostname)
    return hostname

def get_snmp_location():
    location = conn.send_command("show snmp location", read_timeout=180)
    print(location)
    return location
'''    