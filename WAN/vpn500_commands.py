'''This section is for VPN 500. Goodluck!'''
from net_connection import *
from no_net_connection import *
import re, os, sys

conn = r1_conn()
#create the List needed globally
aggregate_list = []
static_list = []
next_hop_list = []

#print("This is aggregate_list:" +str(aggregate_list))
#print("This is static_list:" +str(static_list))
#print("This is next_hop_list:" +str(next_hop_list))

def generate_static_route_list(route_type, prefix_number): 
    #if the file exist,then return that line in the file, if it doesn't then run and return the line in the list
    #if static_list is not empty and aggregate_list is also not empty and next_hop_list is also not empty, then we return the list item based on the route type or an empty string
    if (len(static_list) != 0 and len(next_hop_list) != 0) or len(aggregate_list) != 0:
        if route_type == "s" and prefix_number <= len(static_list):
            return static_list[prefix_number - 1] #return the static route
        elif route_type == "n" and prefix_number <= len(next_hop_list):
            return next_hop_list[prefix_number - 1] #return the next hop
        elif route_type == "a" and prefix_number <= len(aggregate_list):
            return aggregate_list[prefix_number - 1] #return the aggregate route
        else:
            return ""        
 
    else: #get the actual data from the router and return the first line. This should only be run once
        ##print("This should only be seen ONCEEEEE!")
        #Get the static routes
        static_routes = conn.send_command("show running-config | include ip route vrf NA-Guest", read_timeout=180)
        split_static_routes = static_routes.split('\n')
        ##print(split_static_routes)
        reg = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|Null0)')
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
        #print("this is static list: " +str(static_list))
        #print("this is aggregate list: " +str(aggregate_list))
        #print("this is next hop list: " +str(next_hop_list))
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


def get_000_358_ip_address():
    int_gi000_26 = conn.send_command("show running-config interface GigabitEthernet 0/0/0.26 | include ip address", read_timeout=180)#.26 becomes .358
    split_line = int_gi000_26.split(" ")#split by the spaces
    ip = split_line[3] #this is for the ip
    subnet = convert_to_cidr(split_line[4]) #convert the subnet mask to cidr notation    
    return str(ip) + "/"+str(subnet) #concatenate the ip to the subnet mask 

def get_000_358_dhcp_helper():
    helpers = []
    int_gi000_26 = conn.send_command("show running-config interface GigabitEthernet 0/0/0.26 | include helper-address", read_timeout=180)#.26 becomes .358
    split_int = int_gi000_26.split('\n')
    for helper_address in split_int:
        ip_helper = helper_address.strip("ip helper-address ") #split the string to get only the ip helper address
        helpers.append(ip_helper) #add the helper address to the helpers list
    
    helpers_as_string = ', '.join(helpers)
    return helpers_as_string
        
def get_000_358_shutdown():
    int_gi000_26 = conn.send_command("show running-config interface GigabitEthernet 0/0/0.26 | include shutdown", read_timeout=180)#.26 becomes .358
    if int_gi000_26 == "": #check if keyword shutdown is present, command should return an empty string
        return "FALSE"
    else:
        return "TRUE"

def get_000_358_vrrp():
    int_gi000_26 = conn.send_command("show running-config interface GigabitEthernet 0/0/0.26 | include standby", read_timeout=180)#.26 becomes .358
    reg = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|Null0)') #use regular expression to find the ip. We could also use split but this is more generic
    mo = re.search(reg, int_gi000_26)
    return mo.group()


def get_000_25_description():
    int_gi000_25 = conn.send_command("show running-config interface GigabitEthernet 0/0/0.25 | include description", read_timeout=180)
    return int_gi000_25.split("description")[1] #return the second portion of the splitted string which is the actual description 

def get_000_25_ip_address():
    int_gi000_25 = conn.send_command("show running-config interface GigabitEthernet 0/0/0.25 | include ip address", read_timeout=180)
    split_line = int_gi000_25.split(" ")#split by the spaces
    ip = split_line[3] #this is for the ip
    subnet = convert_to_cidr(split_line[4]) #convert the subnet mask to cidr notation    
    return str(ip) + "/"+str(subnet) #concatenate the ip to the subnet mask 

def get_000_25_shutdown(): 
    int_gi000_25 = conn.send_command("show running-config interface GigabitEthernet 0/0/0.25 | include shutdown", read_timeout=180)
    if int_gi000_25 == "": #check if keyword shutdown is present, command should return an empty string
        return "FALSE"
    else:
        return "TRUE"

def get_000_25_vrrp():
    int_gi000_25 = conn.send_command("show running-config interface GigabitEthernet 0/0/0.25 | include standby", read_timeout=180)
    reg = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|Null0)') #use regular expression to find the ip. We could also use split but this is more generic
    mo = re.search(reg, int_gi000_25)
    return mo.group()


def get_vpn500_ospf_id():
    guest_ospf = conn.send_command("sh ip ospf 900 | include Routing Process", read_timeout=180)
    reg = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|Null0)') #use regular expression to find the ip. We could also use split but this is more generic
    mo = re.search(reg, guest_ospf)
    return mo.group()
    conn.disconnect()
    