'''This section is for VPN 10. Almost there!'''
from net_connection import *
from no_net_connection import *
import re, os, sys

conn = r3_conn()
#create the List needed globally
aggregate_list = []
static_list = []
next_hop_list = []
reg = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
#show ip routes | inc 0.0.0.0 | inc static | inc ge0/1.100 - mpls 1
#show ip routes | inc 0.0.0.0 | inc static | inc ge0/7.50 - tloc inet 1
#show ip routes | inc 0.0.0.0 | inc static | inc ge0/7.11 - tloc mpls 2 
#show ip routes | inc 0.0.0.0 | inc static | inc ge0/3 - inet 2
#show ip routes | inc 0.0.0.0 | inc static | inc ge0/0 inet 3
#show ip routes | inc 0.0.0.0 | inc static | inc ge0/7.59 - tloc lte
#show run vpn 0 | inc 0.0.0.0. THere's a list 


def get_m1_next_hop():
    found_next_hop = ''
    mpls_static = ''
    try:
        mpls_static = conn.send_command_timing("show ip routes static | include 0.0.0.0 | inc ge0/1.100", strip_prompt=True, strip_command=True, read_timeout=5)#we use send_command_timing so it doesn't take so much time
        conn.disconnect()
        print("R3 is disconnected")
        found_next_hop = reg.findall(mpls_static)[1] #The 0 will be the 0.0.0.0 and the 1 will be the ip address that we need.
    except Exception as e:
        print(f"An error occurred: {e}")
        found_next_hop = ''
    if found_next_hop == "": #if no static IP Address is found, find it from the ip address configuration
        #Get the IP Address from MPLS 1 and subtract 1 from the ip 
        new_conn = r3_conn()
        #new_conn.send_command("")
        mpls_ip = new_conn.send_command("show running-config vpn 0 interface ge0/1.100 | inc address", strip_prompt=True, strip_command=True, read_timeout=120)
        ip_ad = mpls_ip.split('\n')[0].split()[-1].split('/')[0]#This split by newline then by spaces and then by the / to get the ip address
        new_ip_ad = subtract_one_from_ipv4(ip_ad)
        return new_ip_ad
    else:
        found_next_hop = reg.findall(mpls_static)[1] #The 0 will be the 0.0.0.0 and the 1 will be the ip address that we need.
        return found_next_hop


def get_m2_next_hop():
    mpls2_tloc = ''
    found_next_hop = ''
    try:#we expect the timeout to fail so we catch it.
        conn = r3_conn()
        mpls2_tloc = conn.send_command_timing("show ip routes | include 0.0.0.0 | inc ge0/7.11", strip_prompt=True, strip_command=True, read_timeout=1)#we use send_command_timing so it doesn't take so much time    
        conn.disconnect()#trying to disconnect to see if it fixes the timing issue
        print("R3 is disconnected")
    except Exception as e:
        print(f"An error occurred: {e}")
        found_next_hop = ''
    if mpls2_tloc == '' or 'show ip routes' in mpls2_tloc: #we are adding the command as a way to show that the string is empty since the strip command and prompt still shows
        #Get the IP Address from MPLS 1 and subtract 1 from the ip 
        new_conn = r3_conn()#connect back
        mpls_ip = new_conn.send_command("show running-config vpn 0 interface ge0/7.11 | inc address", strip_prompt=True, strip_command=True, read_timeout=120)
        ip_ad = mpls_ip.split('\n')[0].split()[-1].split('/')[0]#This split by spaces and then by the / to get the ip address
        new_ip_ad = subtract_one_from_ipv4(ip_ad)
        return new_ip_ad       
    else:
        print("did you get here for mpls2?")
        found_next_hop = reg.findall(mpls2_tloc)[1] #The 0 will be the 0.0.0.0 and the 1 will be the ip address that we need.
        return found_next_hop


def get_i1_next_hop():
    inet1_tloc = ''
    found_next_hop = ''
    try:#we expect the timeout to fail so we catch it.
        conn = r3_conn()
        inet1_tloc = conn.send_command_timing("show ip routes | include 0.0.0.0 | inc ge0/7.50", strip_prompt=True, strip_command=True, read_timeout=1)#we use send_command_timing so it doesn't take so much time    
        conn.disconnect()#trying to disconnect to see if it fixes the timing issue
        print("R3 is disconnected")
    except Exception as e:
        print(f"An error occurred: {e}")
        found_next_hop = ''
    if inet1_tloc == '' or 'show ip routes' in inet1_tloc: #we are adding the command as a way to show that the string is empty since the strip command and prompt still shows
        #Get the IP Address from MPLS 1 and subtract 1 from the ip 
        new_conn = r3_conn()#connect back
        mpls_ip = new_conn.send_command("show running-config vpn 0 interface ge0/7.50 | inc address", strip_prompt=True, strip_command=True, read_timeout=120)
        ip_ad = mpls_ip.split('\n')[0].split()[-1].split('/')[0]#This split by spaces and then by the / to get the ip address
        new_ip_ad = subtract_one_from_ipv4(ip_ad)
        return new_ip_ad       
    else:
        print("Did you get here for inet1?")
        found_next_hop = reg.findall(inet1_tloc)[1] #The 0 will be the 0.0.0.0 and the 1 will be the ip address that we need.
        return found_next_hop

def get_i2_next_hop():
    inet2_tloc = ''
    found_next_hop = ''
    try:#we expect the timeout to fail so we catch it.
        conn = r3_conn()
        inet2_tloc = conn.send_command_timing("show ip routes | include 0.0.0.0 | inc ge0/3", strip_prompt=True, strip_command=True, read_timeout=1)#we use send_command_timing so it doesn't take so much time    
        conn.disconnect()#trying to disconnect to see if it fixes the timing issue
        print("R3 is disconnected")
    except Exception as e:
        print(f"An error occurred: {e}")
        found_next_hop = ''
    if inet2_tloc == '' or 'show ip routes' in inet2_tloc: #we are adding the command as a way to show that the string is empty since the strip command and prompt still shows
        #Get the IP Address from MPLS 1 and subtract 1 from the ip 
        new_conn = r3_conn()#connect back
        mpls_ip = new_conn.send_command("show running-config vpn 0 interface ge0/3 | inc address", strip_prompt=True, strip_command=True, read_timeout=120)
        ip_ad = mpls_ip.split('\n')[0].split()[-1].split('/')[0]#This split by spaces and then by the / to get the ip address
        new_ip_ad = subtract_one_from_ipv4(ip_ad)
        return new_ip_ad       
    else:
        print("Did you get here for inet2?")
        found_next_hop = reg.findall(inet2_tloc)[1] #The 0 will be the 0.0.0.0 and the 1 will be the ip address that we need.
        return found_next_hop
        
def get_i3_next_hop():
    inet3_tloc = ''
    found_next_hop = ''
    try:#we expect the timeout to fail so we catch it.
        conn = r3_conn()
        inet3_tloc = conn.send_command_timing("show ip routes | include 0.0.0.0 | inc ge0/0", strip_prompt=True, strip_command=True, read_timeout=1)#we use send_command_timing so it doesn't take so much time    
        conn.disconnect()#trying to disconnect to see if it fixes the timing issue
        print("R3 is disconnected")
    except Exception as e:
        print(f"An error occurred: {e}")
        found_next_hop = ''
    if inet3_tloc == '' or 'show ip routes' in inet3_tloc: #we are adding the command as a way to show that the string is empty since the strip command and prompt still shows
        #Get the IP Address from MPLS 1 and subtract 1 from the ip 
        new_conn = r3_conn()#connect back
        mpls_ip = new_conn.send_command("show running-config vpn 0 interface ge0/0 | inc address", strip_prompt=True, strip_command=True, read_timeout=120)
        ip_ad = mpls_ip.split('\n')[0].split()[-1].split('/')[0]#This split by spaces and then by the / to get the ip address
        new_ip_ad = subtract_one_from_ipv4(ip_ad)
        return new_ip_ad       
    else:
        print("Did you get here for inet3?")
        found_next_hop = reg.findall(inet3_tloc)[1] #The 0 will be the 0.0.0.0 and the 1 will be the ip address that we need.
        return found_next_hop
        
#The TLOC might be messed up. Check diagram and subnet calculation
def get_lte_next_hop():
    lte_tloc = ''
    found_next_hop = ''
    try:#we expect the timeout to fail so we catch it.
        conn = r3_conn()
        lte_tloc = conn.send_command_timing("show ip routes | include 0.0.0.0 | inc ge0/7.59", strip_prompt=True, strip_command=True, read_timeout=1)#we use send_command_timing so it doesn't take so much time    
        conn.disconnect()#trying to disconnect to see if it fixes the timing issue
        print("R3 is disconnected")
    except Exception as e:
        print(f"An error occurred: {e}")
        found_next_hop = ''
    if lte_tloc == '' or 'show ip routes' in lte_tloc: #we are adding the command as a way to show that the string is empty since the strip command and prompt still shows
        #Get the IP Address from MPLS 1 and subtract 1 from the ip 
        new_conn = r3_conn()#connect back
        mpls_ip = new_conn.send_command("show running-config vpn 0 interface ge0/7.59 | inc address", strip_prompt=True, strip_command=True, read_timeout=120)
        ip_ad = mpls_ip.split('\n')[0].split()[-1].split('/')[0]#This split by spaces and then by the / to get the ip address
        new_ip_ad = subtract_one_from_ipv4(ip_ad)
        return new_ip_ad       
    else:
        print("Did you get here for lte?")
        found_next_hop = reg.findall(lte_tloc)[1] #The 0 will be the 0.0.0.0 and the 1 will be the ip address that we need.
        return found_next_hop

        
def get_002_description():
    conn = r3_conn()
    ge0_3_desc = conn.send_command("show running-config vpn 0 interface ge0/3 description | exclude vpn | exclude interface", read_timeout=120)
    strip_str = ge0_3_desc.replace('description', '').strip().strip('"')
    return strip_str

def get_002_ip_address():
    ge0_3_ip = conn.send_command("show running-config vpn 0 interface ge0/3 ip | exclude vpn | exclude interface", read_timeout=120)
    ge0_3_ip_strip = ge0_3_ip.split(" ")[-1]
    return ge0_3_ip_strip

def get_002_shutdown():
    ge0_3_shutdown = conn.send_command("show running-config vpn 0 interface ge0/3 shutdown | exclude vpn | exclude interface", read_timeout=120)
    if "no shutdown" in ge0_3_shutdown:
        return "FALSE"
    else:
        return "TRUE"

def get_002_autonegotiate():
    ge0_3_auto = conn.send_command("show int detail ge0/3 | inc auto", read_timeout=120)
    if ge0_3_auto == "false":
        return "FALSE"
    else:
        return "TRUE"

    
def get_002_shaping_rate():
    ge0_3_shape = conn.send_command("show running-config vpn 0 interface ge0/3 shaping-rate | exclude vpn | exclude interface", read_timeout=120)
    ge0_3_shape_strip = ge0_3_shape.split(" ")[-1]
    return ge0_3_shape_strip


def get_002_bandwidth_upstream():
    ge0_3_up = conn.send_command("show running-config vpn 0 interface ge0/3 bandwidth-upstream | exclude vpn | exclude interface", read_timeout=120)
    ge0_3_up_strip = ge0_3_up.split(" ")[-1]
    return ge0_3_up_strip

def get_002_bandwidth_downstream():
    ge0_3_down = conn.send_command("show running-config vpn 0 interface ge0/3 bandwidth-downstream | exclude vpn | exclude interface", read_timeout=120)
    ge0_3_down_strip = ge0_3_down.split(" ")[-1]
    return ge0_3_down_strip









        
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