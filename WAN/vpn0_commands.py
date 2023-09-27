'''This section is for VPN 10. Almost there!'''
from net_connection import *
from no_net_connection import *
import re, os, sys

#conn = r3_conn()
#create the List needed globally
bgp_list = []

reg = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')

#FIX the logic error here for router 2. 
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
        if "ip " not in mpls_ip:
            return "7.7.7.2/28"
        else:
            ip_ad = mpls_ip.split('\n')[0].split()[-1].split('/')[0]#This split by newline then by spaces and then by the / to get the ip address
            new_ip_ad = subtract_one_from_ipv4(ip_ad)
            return new_ip_ad
    else:
        found_next_hop = reg.findall(mpls_static)[1] #The 0 will be the 0.0.0.0 and the 1 will be the ip address that we need.
        return found_next_hop

#FIX the logic error here for router 2. 
def get_m2_next_hop():
    mpls2_tloc = ''
    found_next_hop = ''
    try:#we expect the timeout to fail so we catch it.
        conn = r3_conn()
        mpls2_tloc = conn.send_command_timing("show ip routes | include 0.0.0.0 | inc ge0/7.11", strip_prompt=True, strip_command=True, read_timeout=5)#we use send_command_timing so it doesn't take so much time    
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

#FIX the logic error here for router 2. 
def get_i1_next_hop():
    inet1_tloc = ''
    found_next_hop = ''
    try:#we expect the timeout to fail so we catch it.
        conn = r3_conn()
        inet1_tloc = conn.send_command_timing("show ip routes | include 0.0.0.0 | inc ge0/7.50", strip_prompt=True, strip_command=True, read_timeout=5)#we use send_command_timing so it doesn't take so much time    
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
        new_ip_ad = add_one_from_ipv4(ip_ad)
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
        inet2_tloc = conn.send_command_timing("show ip routes | include 0.0.0.0 | inc ge0/3", strip_prompt=True, strip_command=True, read_timeout=15)#we use send_command_timing so it doesn't take so much time    
        conn.disconnect()#trying to disconnect to see if it fixes the timing issue
        print("R3 is disconnected")
    except Exception as e:
        print(f"An error occurred: {e}")
        found_next_hop = ''
    if inet2_tloc == '' or 'show ip routes' in inet2_tloc: #we are adding the command as a way to show that the string is empty since the strip command and prompt still shows
        #Get the IP Address from MPLS 1 and subtract 1 from the ip 
        new_conn = r3_conn()#connect back
        mpls_ip = new_conn.send_command("show running-config vpn 0 interface ge0/3 | inc address", strip_prompt=True, strip_command=True, read_timeout=120)
        if "ip " not in mpls_ip:
            return "7.7.7.3/28"
        else:
            ip_ad = mpls_ip.split('\n')[0].split()[-1].split('/')[0]#This split by spaces and then by the / to get the ip address
            new_ip_ad = subtract_one_from_ipv4(ip_ad)
            return new_ip_ad       
    else:
        print("Did you get here for inet2?")
        found_next_hop = reg.findall(inet2_tloc)[1] #The 0 will be the 0.0.0.0 and the 1 will be the ip address that we need.
        return found_next_hop

#FIX the logic error here for router 2.         
def get_i3_next_hop():
    inet3_tloc = ''
    found_next_hop = ''
    try:#we expect the timeout to fail so we catch it.
        conn = r3_conn()
        inet3_tloc = conn.send_command_timing("show ip routes | include 0.0.0.0 | inc ge0/0", strip_prompt=True, strip_command=True, read_timeout=5)#we use send_command_timing so it doesn't take so much time    
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
        lte_tloc = conn.send_command_timing("show ip routes | include 0.0.0.0 | inc ge0/7.59", strip_prompt=True, strip_command=True, read_timeout=5)#we use send_command_timing so it doesn't take so much time    
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


#VPN0 GI0/0/2        
def get_002_description():
    conn = r3_conn()
    ge0_3_desc = conn.send_command("show running-config vpn 0 interface ge0/3 description | exclude vpn | exclude interface", read_timeout=120)
    strip_str = ge0_3_desc.split('\n')[0].replace('description', '').strip().strip('"')
    conn.disconnect()
    return strip_str

def get_002_ip_address():
    conn = r3_conn()
    ge0_3_ip = conn.send_command("show running-config vpn 0 interface ge0/3 ip | exclude vpn | exclude interface", read_timeout=120)
    ge0_3_ip_strip = ge0_3_ip.split('\n')[0].split(" ")[-1]
    conn.disconnect()
    return ge0_3_ip_strip

def get_002_shutdown():
    conn = r3_conn()
    ge0_3_shutdown = conn.send_command("show running-config vpn 0 interface ge0/3 shutdown | exclude vpn | exclude interface", read_timeout=120)
    conn.disconnect()
    if "no shutdown" in ge0_3_shutdown:
        return "FALSE"
    else:
        return "TRUE"

#Work on this
def get_002_autonegotiate():
    conn = r3_conn()
    ge0_3_auto = conn.send_command("show int detail ge0/3 | inc auto", read_timeout=120)
    conn.disconnect()
    if "false" in ge0_3_auto.split(" ")[-1]:
        return "FALSE"
    else:
        return "TRUE"
    
def get_002_shaping_rate():
    conn = r3_conn()
    ge0_3_shape = conn.send_command("show running-config vpn 0 interface ge0/3 shaping-rate | exclude vpn | exclude interface", read_timeout=120)
    ge0_3_shape_strip = ge0_3_shape.split('\n')[0].split(" ")[-1]
    conn.disconnect()
    return ge0_3_shape_strip

def get_002_bandwidth_upstream():
    conn = r3_conn()
    ge0_3_up = conn.send_command("show running-config vpn 0 interface ge0/3 bandwidth-upstream | exclude vpn | exclude interface", read_timeout=120)
    ge0_3_up_strip = ge0_3_up.split('\n')[0].split(" ")[-1]
    conn.disconnect()
    return ge0_3_up_strip

def get_002_bandwidth_downstream():
    conn = r3_conn()
    ge0_3_down = conn.send_command("show running-config vpn 0 interface ge0/3 bandwidth-downstream | exclude vpn | exclude interface", read_timeout=120)
    ge0_3_down_strip = ge0_3_down.split('\n')[0].split(" ")[-1]
    conn.disconnect()
    return ge0_3_down_strip



#VPN 0 te0/0/4.100
def get_004_100_description():
    conn = r3_conn()
    ge0_3_desc = conn.send_command("show running-config vpn 0 interface ge0/1.100 description | exclude vpn | exclude interface", read_timeout=120)
    strip_str = ge0_3_desc.split('\n')[0].replace('description', '').strip().strip('"')
    conn.disconnect()
    return strip_str
    
def get_004_100_ip_address():
    conn = r3_conn()
    ge0_3_ip = conn.send_command("show running-config vpn 0 interface ge0/1.100 ip | exclude vpn | exclude interface", read_timeout=120)
    ge0_3_ip_strip = ge0_3_ip.split('\n')[0].split(" ")[-1]
    conn.disconnect()
    return ge0_3_ip_strip
    
def get_004_100_shutdown():
    conn = r3_conn()
    ge0_3_shutdown = conn.send_command("show running-config vpn 0 interface ge0/1.100 shutdown | exclude vpn | exclude interface", read_timeout=120)
    conn.disconnect()
    if "no shutdown" in ge0_3_shutdown:
        return "FALSE"
    else:
        return "TRUE"
        
def get_004_100_bandwidth_upstream():
    conn = r3_conn()
    ge0_3_up = conn.send_command("show running-config vpn 0 interface ge0/1.100 bandwidth-upstream | exclude vpn | exclude interface", read_timeout=120)
    ge0_3_up_strip = ge0_3_up.split('\n')[0].split(" ")[-1]
    conn.disconnect()
    return ge0_3_up_strip
    
def get_004_100_bandwidth_downstream():
    conn = r3_conn()
    ge0_3_down = conn.send_command("show running-config vpn 0 interface ge0/1.100 bandwidth-downstream | exclude vpn | exclude interface", read_timeout=120)
    ge0_3_down_strip = ge0_3_down.split('\n')[0].split(" ")[-1]
    conn.disconnect()
    return ge0_3_down_strip


#VPN 0 te0/0/4   
def get_004_description():
    conn = r3_conn()
    ge0_3_desc = conn.send_command("show running-config vpn 0 interface ge0/1 description | exclude vpn | exclude interface", read_timeout=120)
    strip_str = ge0_3_desc.split('\n')[0].replace('description', '').strip().strip('"')
    conn.disconnect()
    return strip_str
    
def get_004_ip_address():
    conn = r3_conn()
    ge0_3_ip = conn.send_command("show running-config vpn 0 interface ge0/1 ip | exclude vpn | exclude interface", read_timeout=120)
    conn.disconnect()
    if "No entries found" in ge0_3_ip:
        return "7.7.7.2/30"
    else:
        ge0_3_ip_strip = ge0_3_ip.split('\n')[0].split(" ")[-1]
        return ge0_3_ip_strip
    
def get_004_shutdown():
    conn = r3_conn()
    ge0_3_shutdown = conn.send_command("show running-config vpn 0 interface ge0/1 shutdown | exclude vpn | exclude interface", read_timeout=120)
    conn.disconnect()
    if "no shutdown" in ge0_3_shutdown:
        return "FALSE"
    else:
        return "TRUE"

def get_004_autonegotiate():
    conn = r3_conn()
    ge0_3_auto = conn.send_command("show int detail ge0/1 | inc auto", read_timeout=120)
    conn.disconnect()
    if "false" in ge0_3_auto.split(" ")[-1]:
        return "FALSE"
    else:
        return "TRUE"
        
def get_004_shaping_rate():
    conn = r3_conn()
    ge0_3_shape = conn.send_command("show running-config vpn 0 interface ge0/1 shaping-rate | exclude vpn | exclude interface", read_timeout=120)
    ge0_3_shape_strip = ge0_3_shape.split('\n')[0].split(" ")[-1]
    conn.disconnect()
    return ge0_3_shape_strip
    
def get_004_bandwidth_upstream():
    conn = r3_conn()
    ge0_3_up = conn.send_command("show running-config vpn 0 interface ge0/1 bandwidth-upstream | exclude vpn | exclude interface", read_timeout=120)
    ge0_3_up_strip = ge0_3_up.split('\n')[0].split(" ")[-1]
    conn.disconnect()
    return ge0_3_up_strip
    
def get_004_bandwidth_downstream():
    conn = r3_conn()
    ge0_3_down = conn.send_command("show running-config vpn 0 interface ge0/1 bandwidth-downstream | exclude vpn | exclude interface", read_timeout=120)
    ge0_3_down_strip = ge0_3_down.split('\n')[0].split(" ")[-1]
    conn.disconnect()
    return ge0_3_down_strip

#VPN 0 Gi0/0/3
def get_003_description():
    conn = r3_conn()
    ge0_3_desc = conn.send_command("show running-config vpn 0 interface ge0/0 description | exclude vpn | exclude interface", read_timeout=120)
    strip_str = ge0_3_desc.split('\n')[0].replace('description', '').strip().strip('"')
    conn.disconnect()
    return strip_str
    
def get_003_ip_address():
    conn = r3_conn()
    ge0_3_ip = conn.send_command("show running-config vpn 0 interface ge0/0 ip | exclude vpn | exclude interface", read_timeout=120)
    ge0_3_ip_strip = ge0_3_ip.split('\n')[0].split(" ")[-1]
    conn.disconnect()
    return ge0_3_ip_strip
    
def get_003_shutdown():
    conn = r3_conn()
    ge0_3_shutdown = conn.send_command("show running-config vpn 0 interface ge0/0 shutdown | exclude vpn | exclude interface", read_timeout=120)
    conn.disconnect()
    if "no shutdown" in ge0_3_shutdown:
        return "FALSE"
    else:
        return "TRUE"

def get_003_shaping_rate():
    conn = r3_conn()
    ge0_3_shape = conn.send_command("show running-config vpn 0 interface ge0/0 shaping-rate | exclude vpn | exclude interface", read_timeout=120)
    ge0_3_shape_strip = ge0_3_shape.split('\n')[0].split(" ")[-1]
    conn.disconnect()
    return ge0_3_shape_strip
    
def get_003_bandwidth_upstream():
    conn = r3_conn()
    ge0_3_up = conn.send_command("show running-config vpn 0 interface ge0/0 bandwidth-upstream | exclude vpn | exclude interface", read_timeout=120)
    ge0_3_up_strip = ge0_3_up.split('\n')[0].split(" ")[-1]
    conn.disconnect()
    return ge0_3_up_strip
    
def get_003_bandwidth_downstream():
    conn = r3_conn()
    ge0_3_down = conn.send_command("show running-config vpn 0 interface ge0/0 bandwidth-downstream | exclude vpn | exclude interface", read_timeout=120)
    ge0_3_down_strip = ge0_3_down.split('\n')[0].split(" ")[-1]
    conn.disconnect()
    return ge0_3_down_strip
    
    

#VPN 0 TLOC Interface
def get_001_59_ip_address():
    conn = r3_conn()
    ge0_3_ip = conn.send_command("show running-config vpn 0 interface ge0/7.59 ip | exclude vpn | exclude interface", read_timeout=120)
    ge0_3_ip_strip = ge0_3_ip.split('\n')[0].split(" ")[-1]
    conn.disconnect()
    return ge0_3_ip_strip

def get_001_59_shutdown():
    conn = r3_conn()
    ge0_3_shutdown = conn.send_command("show running-config vpn 0 interface ge0/7.59 shutdown | exclude vpn | exclude interface", read_timeout=120)
    conn.disconnect()
    if "no shutdown" in ge0_3_shutdown:
        return "FALSE"
    else:
        return "TRUE"

def get_001_52_ip_address():
    conn = r3_conn()
    ge0_3_ip = conn.send_command("show running-config vpn 0 interface ge0/7.52 ip | exclude vpn | exclude interface", read_timeout=120)
    ge0_3_ip_strip = ge0_3_ip.split('\n')[0].split(" ")[-1]
    conn.disconnect()
    return ge0_3_ip_strip

def get_001_52_shutdown():
    conn = r3_conn()
    ge0_3_shutdown = conn.send_command("show running-config vpn 0 interface ge0/7.52 shutdown | exclude vpn | exclude interface", read_timeout=120)
    conn.disconnect()
    if "no shutdown" in ge0_3_shutdown:
        return "FALSE"
    else:
        return "TRUE"    

def get_001_51_ip_address():
    conn = r3_conn()
    ge0_3_ip = conn.send_command("show running-config vpn 0 interface ge0/7.51 ip | exclude vpn | exclude interface", read_timeout=120)
    ge0_3_ip_strip = ge0_3_ip.split('\n')[0].split(" ")[-1]
    conn.disconnect()
    return ge0_3_ip_strip

def get_001_51_shutdown():
    conn = r3_conn()
    ge0_3_shutdown = conn.send_command("show running-config vpn 0 interface ge0/7.51 shutdown | exclude vpn | exclude interface", read_timeout=120)
    conn.disconnect()
    if "no shutdown" in ge0_3_shutdown:
        return "FALSE"
    else:
        return "TRUE"  


def get_001_50_ip_address():
    conn = r3_conn()
    ge0_3_ip = conn.send_command("show running-config vpn 0 interface ge0/7.50 ip | exclude vpn | exclude interface", read_timeout=120)
    ge0_3_ip_strip = ge0_3_ip.split('\n')[0].split(" ")[-1]
    conn.disconnect()
    return ge0_3_ip_strip

def get_001_50_shutdown():
    conn = r3_conn()
    ge0_3_shutdown = conn.send_command("show running-config vpn 0 interface ge0/7.50 shutdown | exclude vpn | exclude interface", read_timeout=120)
    conn.disconnect()
    if "no shutdown" in ge0_3_shutdown:
        return "FALSE"
    else:
        return "TRUE"  

def get_001_10_ip_address():
    conn = r3_conn()
    ge0_3_ip = conn.send_command("show running-config vpn 0 interface ge0/7.10 ip | exclude vpn | exclude interface", read_timeout=120)
    ge0_3_ip_strip = ge0_3_ip.split('\n')[0].split(" ")[-1]
    conn.disconnect()
    return ge0_3_ip_strip

def get_001_10_shutdown():
    conn = r3_conn()
    ge0_3_shutdown = conn.send_command("show running-config vpn 0 interface ge0/7.10 shutdown | exclude vpn | exclude interface", read_timeout=120)
    conn.disconnect()
    if "no" in ge0_3_shutdown:
        return "FALSE"
    else:
        return "TRUE"  


#BGP
def get_all_bgp_info():
    conn = r3_conn()
    #bgp AS_num
    bgp_as_num = conn.send_command("show running-config vpn 0 router bgp | inc bgp", read_timeout=120)
    bgp_as_num = bgp_as_num.split('\n')[0].split(" ")[-1]
    #Add the bgp as_num to the bgp list
    bgp_list.append(bgp_as_num)
    
    #BGP Shutdown
    bgp_shut = conn.send_command("show running-config vpn 0 router bgp | until ! | inc shut", read_timeout=120)
    if 'shutdown' in bgp_shut:
        bgp_shut = "TRUE"
    else:
        bgp_shut = "FALSE"
    bgp_list.append(bgp_shut)
    
    #BGP Net Address
    bgp_net_add_1 = conn.send_command("show running-config vpn 0 router bgp | inc network", read_timeout=120)
    bgp_list.append(bgp_net_add_1.split("\n")[0].split(" ")[-1])#bgp network  
    bgp_list.append(bgp_net_add_1.split("\n")[1].split(" ")[-1]) #bgp tloc
    
    #BGP Neighbor
    bgp_neighbor = conn.send_command("show running-config vpn 0 router bgp | inc neighbor", read_timeout=120)
    bgp_neighbor = bgp_neighbor.split('\n')[0].split(" ")[-1]
    bgp_list.append(bgp_neighbor)
    
    
    #BGP Nieghbor Shutdown
    bgp_nei_shut = conn.send_command("show running-config vpn 0 router bgp | inc shut", read_timeout=120)
    if "no" in bgp_nei_shut:
        bgp_nei_shut = "FALSE"
    else:
        bgp_nei_shut = "TRUE"   
    bgp_list.append(bgp_nei_shut)
    
    #BGP Remote AS_num
    bgp_remote = conn.send_command("show running-config vpn 0 router bgp | inc remote", read_timeout=120)
    bgp_remote = bgp_remote.split('\n')[0].split(" ")[-1]
    bgp_list.append(bgp_remote)
    
    #NOT BGP but SITE ID
    site_id = conn.send_command("show running-config system | inc site", read_timeout=120)
    site_id = site_id.split('\n')[0].split(" ")[-1]
    bgp_list.append(site_id)    
    print(bgp_list)
    

get_all_bgp_info()

def get_bgp_as_num():
    return bgp_list[0]

def get_bgp_shutdown():
    return bgp_list[1]

def get_bgp_net_address():
    return bgp_list[2]
    
def get_bgp_tloc_address():
    return bgp_list[3]

def get_bgp_neighbor_address():
    return bgp_list[4]
    
def get_bgp_neighbor_shutdown():
    return bgp_list[5]
    
def get_bgp_neighbor_remote_as():
    return bgp_list[6]    


#SITE ID
def get_site_id():
   return bgp_list[7]
