'''This section is for VPN 10. Almost there!'''
from net_connection import *
from no_net_connection import *
import re, os, sys

conn = r3_conn()
#create the List needed globally
aggregate_list = []
static_list = []
next_hop_list = []


def get_m1_next_hop():
    #show ip routes | inc 0.0.0.0 | inc static | inc ge0/1.100
    #show ip routes | inc 0.0.0.0 | inc static | inc ge0/7.50 - tloc inet 1
    #show ip routes | inc 0.0.0.0 | inc static | inc ge0/3 - inet 2
    #show run vpn 0 | inc 0.0.0.0. THere's a list 


'''
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
        print("This should only be seen ONCEEEEE!")
        #Get the static routes
        static_routes = conn.send_command("show running-config | include ip route ", read_timeout=180)
        split_static_routes = static_routes.split('\n')
        print(split_static_routes)
        reg = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|Null0)')
        for line in split_static_routes:
            if "vrf" not in line:
                mo = reg.findall(line)
                ip = mo[0] #this is for the ip
                subnet = convert_to_cidr(mo[1]) #convert the subnet mask to cidr notation
                complete_static = str(ip) + "/"+str(subnet) #concatenate the ip to the subnet mask 
                #Need to work on a way to add the other routes to aggregate like the loopback address
                gateway = mo[2]
                if gateway == "Null0": #add complete_static IP to aggregate list
                    aggregate_list.append(complete_static)
                else:
                    static_list.append(complete_static) #add complete_static IP to static list
                    next_hop_list.append(gateway) #add gateway to next_hop list

        if route_type == "s" and prefix_number <= len(static_list):
            return static_list[prefix_number - 1] #return the static route
        elif route_type == "n" and prefix_number <= len(next_hop_list):
            return next_hop_list[prefix_number - 1] #return the next hop
        elif route_type == "a" and prefix_number <= len(aggregate_list):
            return aggregate_list[prefix_number - 1] #return the aggregate route
        else:
            return ""      

def get_vpn10_static_route(route_type, prefix_number):
    static_route = generate_static_route_list(route_type, prefix_number)
    return static_route

def get_vpn10_next_hop(route_type, prefix_number):
    next_hop = generate_static_route_list(route_type, prefix_number)
    return next_hop

def get_vpn10_aggregate(route_type, prefix_number):
    aggregate = generate_static_route_list(route_type, prefix_number)
    return aggregate

def get_000_658_description():
    int_gi000_658 = conn.send_command("show running-config interface GigabitEthernet 0/0/0.658 | include description", read_timeout=180)
    return int_gi000_658.split("description")[1] #return the second portion of the splitted string which is the actual description 
    
def get_000_658_ip_address():
    int_gi000_658 = conn.send_command("show running-config interface GigabitEthernet 0/0/0.658 | include ip address", read_timeout=180)
    split_line = int_gi000_658.split(" ")#split by the spaces
    ip = split_line[3] #this is for the ip
    subnet = convert_to_cidr(split_line[4]) #convert the subnet mask to cidr notation    
    return str(ip) + "/"+str(subnet) #concatenate the ip to the subnet mask 
        
def get_000_658_shutdown():
    int_gi000_658 = conn.send_command("show running-config interface GigabitEthernet 0/0/0.658 | include shutdown", read_timeout=180)
    if int_gi000_658 == "": #check if keyword shutdown is present, command should return an empty string
        return "FALSE"
    else:
        return "TRUE"

def get_000_658_vrrp():
    int_gi000_658 = conn.send_command("show running-config interface GigabitEthernet 0/0/0.658 | include standby", read_timeout=180)
    reg = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|Null0)') #use regular expression to find the ip. We could also use split but this is more generic
    mo = re.search(reg, int_gi000_658)
    return mo.group()


def get_000_20_ip_address():
    int_gi000_20 = conn.send_command("show running-config interface GigabitEthernet 0/0/0.20 | include ip address", read_timeout=180)
    split_line = int_gi000_20.split(" ")#split by the spaces
    ip = split_line[3] #this is for the ip
    subnet = convert_to_cidr(split_line[4]) #convert the subnet mask to cidr notation    
    return str(ip) + "/"+str(subnet) #concatenate the ip to the subnet mask 

def get_000_20_shutdown(): 
    int_gi000_20 = conn.send_command("show running-config interface GigabitEthernet 0/0/0.20 | include shutdown", read_timeout=180)
    if int_gi000_20 == "": #check if keyword shutdown is present, command should return an empty string
        return "FALSE"
    else:
        return "TRUE"


def get_000_659_description():
    int_gi000_659 = conn.send_command("show running-config interface GigabitEthernet 0/0/0.659 | include description", read_timeout=180)
    return int_gi000_659.split("description")[1] #return the second portion of the splitted string which is the actual description 
    
def get_000_659_ip_address():
    int_gi000_659 = conn.send_command("show running-config interface GigabitEthernet 0/0/0.659 | include ip address", read_timeout=180)
    split_line = int_gi000_659.split(" ")#split by the spaces
    ip = split_line[3] #this is for the ip
    subnet = convert_to_cidr(split_line[4]) #convert the subnet mask to cidr notation    
    return str(ip) + "/"+str(subnet) #concatenate the ip to the subnet mask 
        
def get_000_659_shutdown():
    int_gi000_659 = conn.send_command("show running-config interface GigabitEthernet 0/0/0.659 | include shutdown", read_timeout=180)
    if int_gi000_659 == "": #check if keyword shutdown is present, command should return an empty string
        return "FALSE"
    else:
        return "TRUE"
        
def get_000_202_description():
    int_gi000_202 = conn.send_command("show running-config interface GigabitEthernet 0/0/0.10 | include description", read_timeout=180)#.20 becomes .202
    return int_gi000_202.split("description")[1] #return the second portion of the splitted string which is the actual description 
    
def get_000_202_ip_address():
    int_gi000_202 = conn.send_command("show running-config interface GigabitEthernet 0/0/0.10 | include ip address", read_timeout=180)
    split_line = int_gi000_202.split(" ")#split by the spaces
    ip = split_line[3] #this is for the ip
    subnet = convert_to_cidr(split_line[4]) #convert the subnet mask to cidr notation    
    return str(ip) + "/"+str(subnet) #concatenate the ip to the subnet mask 
        
def get_000_202_shutdown():
    int_gi000_202 = conn.send_command("show running-config interface GigabitEthernet 0/0/0.10 | include shutdown", read_timeout=180)
    if int_gi000_202 == "": #check if keyword shutdown is present, command should return an empty string
        return "FALSE"
    else:
        return "TRUE"

def get_000_202_vrrp():
    int_gi000_202 = conn.send_command("show running-config interface GigabitEthernet 0/0/0.10 | include standby", read_timeout=180)
    reg = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|Null0)') #use regular expression to find the ip. We could also use split but this is more generic
    mo = re.search(reg, int_gi000_202)
    return mo.group()  


def get_vpn10_ospf_id():
    guest_ospf = conn.send_command("show ip ospf 1293 | include Routing Process", read_timeout=180)
    reg = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|Null0)') #use regular expression to find the ip. We could also use split but this is more generic
    mo = re.search(reg, guest_ospf)
    return mo.group()

'''    