'''This script compares IECN Ports with mac addresses from the macro-validation script'''

import sys, os, re
from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException
from netmiko.ssh_exception import SSHException
from netmiko.ssh_exception import AuthenticationException

#gW5qDNdjY2BfGPxL

def comparePort(pfcn_port_name, mac_address, iecn_port_name, con):
    found_cmd = con.send_command("sh mac address-table | inc " +str(mac_address))
    #find only the port from this information
    regPort = re.compile(r"[A-Z][a-z][0-9]/0/\d+") #for port name  eg. Te3/0/4
    moPo = regPort.search(found_cmd)
    logs_created = open("ports_found.txt", "a")
    if moPo == None:
        logs_created.write("\nPFCN PORT NAME: " +str(pfcn_port_name)+ " | IECN PORT NAME: "+str(iecn_port_name)+ 
          " | MAC ADDRESS FOUND: " +str(mac_address)+ "  | FOUND PORT: NONE\n")
          
    else:      
        #print("\nPFCN PORT NAME: " +str(pfcn_port_name)+ " | IECN PORT NAME: "+str(iecn_port_name)+ 
        # " | MAC ADDRESS FOUND: " +str(mac_address)+ "  | FOUND PORT:" + str(moPo.group()))
        if moPo.group() == iecn_port_name:#for matching Port name 
            logs_created.write("\nPFCN PORT NAME: " +str(pfcn_port_name)+ " | IECN PORT NAME: "+str(iecn_port_name)+ 
            " | MAC ADDRESS FOUND: " +str(mac_address)+ "  | FOUND PORT:" + str(moPo.group())+" | MATCHED\n")
        else: #not matching port names          
            logs_created.write("\nPFCN PORT NAME: " +str(pfcn_port_name)+ " | IECN PORT NAME: "+str(iecn_port_name)+ 
            " | MAC ADDRESS FOUND: " +str(mac_address)+ "  | FOUND PORT:" + str(moPo.group())+" | DOES NOT MATCH \n")
        #print("FOUND PORT:" + str(moPo.group()))
    logs_created.close()
    
    
    

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
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    '''
    
    
    
    to_send = "sh vlan brief"
    reg = re.compile(r"IECN_VLAN-5[0-4]\d") #for matching IECN vlan ranging from 500 to 549
    #IECN vlan are actually from 495 - 549. .even are pfcn and .odd are IECN on the second octet on IP Address
    mo = reg.findall(con.send_command(to_send)) #find all the IECN vlans from the sh vlan brief command
   
    fileName = con.send_command("sh run | i hostname")
    #print(fileName.split(" ")[1])
    preCheck_file = open(str(fileName.split(" ")[1])+"-preCheck.txt", mode="w") #create precheck_file file in .txt for pfcn switches
    #the config script
    preCheck_file.write(''!
terminal length 0
!
sh vlan
!
show interface status
!
sh ip arp
!
sh int trunk
!
sh mac address-table
!
'') #add the config to the file
        
    regIP = re.compile(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}")#find regEx for IPs        
        
    for vlans in mo:#this will get all the vlan numbers for the sh ip arp vlan command
        moIps = regIP.findall(con.send_command("sh ip arp vlan" + str((vlans).split("-")[1])))
        for ipS in moIps:
            preCheck_file.write("ping "+str(ipS) + "\n") #write the individual ips to the preCheck file                       
            preCheck_file.write("!\n")
            
    preCheck_file.write(''
!
sh mac address-table
!'')
    preCheck_file.close()
    return preCheck_file


''tclsh
!
!foreach ip {


!} {ping $ip}
exit
'''