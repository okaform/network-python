'''This script Generates the precheck script to be used'''

import sys, os, re

def genPreCheck(con):
    to_send = "sh vlan brief"
    reg = re.compile(r"IECN_VLAN-5[0-4]\d") #for matching IECN vlan ranging from 500 to 549
    #IECN vlan are actually from 495 - 549. .even are pfcn and .odd are IECN on the second octet on IP Address
    mo = reg.findall(con.send_command(to_send)) #find all the IECN vlans from the sh vlan brief command
   
    fileName = con.send_command("sh run | i hostname")
    #print(fileName.split(" ")[1])
    preCheck_file = open(str(fileName.split(" ")[1])+"-preCheck.txt", mode="w") #create precheck_file file in .txt for pfcn switches
    #the config script
    preCheck_file.write('''!
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
''') #add the config to the file
        
    regIP = re.compile(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}")#find regEx for IPs        
        
    for vlans in mo:#this will get all the vlan numbers for the sh ip arp vlan command
        moIps = regIP.findall(con.send_command("sh ip arp vlan" + str((vlans).split("-")[1])))
        for ipS in moIps:
            preCheck_file.write("ping "+str(ipS) + "\n") #write the individual ips to the preCheck file                       
            preCheck_file.write("!\n")
            
    preCheck_file.write('''
!
sh mac address-table
!''')
    preCheck_file.close()
    return preCheck_file


'''tclsh
!
!foreach ip {


!} {ping $ip}
exit
'''