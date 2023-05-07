'''This script compares IECN Ports with mac addresses from the macro-validation script'''

import sys, os, re
from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException
from netmiko.ssh_exception import SSHException
from netmiko.ssh_exception import AuthenticationException


def comparePort(compare_port_list, pfcn_port_name, mac_address, iecn_port_name, con):
    found_cmd = con.send_command("sh mac address-table | inc " +str(mac_address))
    #find only the port from this information
    regPort = re.compile(r"[A-Z][a-z][0-9]/0/\d+") #for port name  eg. Te3/0/4
    moPo = regPort.search(found_cmd)
    if moPo == None:
        #Not all macs will be "on". so this will catch that.
        theAppender(compare_port_list, pfcn_port_name, iecn_port_name, mac_address, "NONE", " ")
        
        #logs_created.write("\nPFCN PORT NAME: " +str(pfcn_port_name)+ " | IECN PORT NAME: "+str(iecn_port_name)+ 
        # " | MAC ADDRESS FOUND: " +str(mac_address)+ "  | FOUND PORT: NONE\n")
          
    else:      
        if moPo.group() == iecn_port_name:#for matching Port name 
            #logs_created.write("\nPFCN PORT NAME: " +str(pfcn_port_name)+ " | IECN PORT NAME: "+str(iecn_port_name)+ 
            #" | MAC ADDRESS FOUND: " +str(mac_address)+ "  | FOUND PORT:" + str(moPo.group())+" | MATCHED\n")
            theAppender(compare_port_list, pfcn_port_name, iecn_port_name, mac_address, moPo.group(), "MATCHED")
            
        else: #not matching port names          
            #logs_created.write("\nPFCN PORT NAME: " +str(pfcn_port_name)+ " | IECN PORT NAME: "+str(iecn_port_name)+ 
            #" | MAC ADDRESS FOUND: " +str(mac_address)+ "  | FOUND PORT:" + str(moPo.group())+" | DOES NOT MATCH \n")
            
            theAppender(compare_port_list, pfcn_port_name, iecn_port_name, mac_address, moPo.group(), "DOES NOT MATCH")
            
    #logs_created.close()
    
    
    

def connecttoSwitch(username, passwd, macro_switch):
    net_dev = {"host":macro_switch,
                "username":username,
                "password":passwd,
                "device_type":"cisco_ios",
                "secret":passwd
                }
    #This try catch block makes sure that if we hit a bad switch it doesn't crash the program but keeps going
    try:
        con = ConnectHandler(**net_dev)
    except:
        print("There is a problem with your log in credentials for " +str(macro_switch)+". Please check your username or password")
        return
    vitaminamulch = con.enable()
    print("Successfully connected to " + str(macro_switch))
    return con
        
    
    
'''This function essentially appends the items to the compare_port_list'''    
def theAppender(compare_port_list, pfcn_port, iecn_port, mac_address, found_port, status):
    compare_port_list.append([pfcn_port, iecn_port, mac_address, found_port, status])
    
    
    