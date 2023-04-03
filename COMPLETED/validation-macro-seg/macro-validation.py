
import sys, re, os
from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException
from netmiko.ssh_exception import SSHException
from netmiko.ssh_exception import AuthenticationException
from datetime import date, datetime 
import compare_IECN_port, callPreChecks


'''
This script does the port validation for macro. 
1. Make sure you have the ip address of the switch you want. Then open the logs_to_read file and add the logs from the precheck logs.
2. Open the Pfcn_port_names file and paste the port names from the cut sheet. 
3. Open the iecn_port_names and paste the port names from the cut sheet. 
4. Run the script. -> double click on VDI-macro-validation
5. It will prompt you for your as_id, as_password, and the macro switch to use. 
6. Sit back and relax for a minute. Cheers!
Author: Marvel Okafor
Date Completed: 12/07/2022
Time: 5:31 PM CST
Signature: no-one
'''

#gW5qDNdjY2BfGPxL

start_time = datetime.now()

#get the ip address of the MACRO SWITCH
macro_switch = input("What's the IP Address of the MACRO SWITCH to validate?\n")

#Make sure you paste the log you want to use in the logs_to_read file 
logs = open("logs_to_read.txt", "r").read()
pfcn_port_names = open("pfcn_port_names.txt", "r").readlines()
iecn_port_names = open("iecn_port_names.txt", "r").readlines()

#we need to concatenate the pfcn port names to be read in the log file
for i in range(len(pfcn_port_names)):
    if "TenGigabitEthernet" in pfcn_port_names[i]:
        pfcn_port_names[i]= pfcn_port_names[i].replace("TenGigabitEthernet","Te")
        #print(pfcn_port_names[i])
    elif "TwoGigabitEthernet" in pfcn_port_names[i]:
        pfcn_port_names[i] = pfcn_port_names[i].replace("TwoGigabitEthernet","Tw")
        #print(pfcn_port_names[i])
    elif "GigabitEthernet" in pfcn_port_names[i]:
        pfcn_port_names[i] = pfcn_port_names[i].replace("GigabitEthernet","Gi")
        #print(pfcn_port_names[i])    
        
#we need to concatenate the iecn port names to be read in the log file
for i in range(len(iecn_port_names)):
    if "TenGigabitEthernet" in iecn_port_names[i]:
        iecn_port_names[i]= iecn_port_names[i].replace("TenGigabitEthernet","Te")
        #print(iecn_port_names[i])
    elif "TwoGigabitEthernet" in iecn_port_names[i]:
        iecn_port_names[i] = iecn_port_names[i].replace("TwoGigabitEthernet","Tw")
        #print(iecn_port_names[i])
    elif "GigabitEthernet" in iecn_port_names[i]:
        iecn_port_names[i] = iecn_port_names[i].replace("GigabitEthernet","Gi")
        #print(iecn_port_names[i])  

#print("No of lines in the log file")
#print(len(logs))
#print(type(logs))

#connect to the switch with the username, password, and ip Address
conn = compare_IECN_port.connecttoSwitch(sys.argv[1], sys.argv[2], macro_switch)

for i in range(len(pfcn_port_names)):
    #print(str(pfcn_port_names[i]).strip() + "\t" + str(iecn_port_names[i]).strip())
    #regex for mac-address -> \w{4}\.\w{4}.\w{4} 
    #This regex will find the mac address based on the port names
    reg = re.compile(r"\w{4}\.\w{4}.\w{4}\s+DYNAMIC+\s+"+str(pfcn_port_names[i].strip())+"\s")
    mo = reg.findall(logs)
    if len(mo) == 0: #if no match object found then the Port is probably not connected
        #print("This port: " +str(pfcn_port_names[i].strip())+" was probably not connected on the PFCN Switch. It is not on the mac-address table.")
        logs_created = open("ports_found.txt", "a")
        logs_created.write("\nPFCN PORT NAME: " +str(pfcn_port_names[i].strip())+" NOT in MAC TABLE. NOT CONNECTTED\n")
        logs_created.close()
    
    else:
        regMac = re.compile(r"\w{4}\.\w{4}.\w{4}")
        for mac in mo:#This will take the matched object and extract the mac-address we will use to verify
            moAD = regMac.search(mac)
            #print(moAD.group()) #This will give us the mac address
            compare_IECN_port.comparePort(pfcn_port_names[i].strip(), moAD.group(), iecn_port_names[i].strip(), conn)
    
elapsed_time = datetime.now() - start_time #to calculate the total elapsed time the script took to run
print("This script took approximately {}".format(elapsed_time))
    
