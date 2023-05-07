
import sys, re, os
from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException
from netmiko.ssh_exception import SSHException
from netmiko.ssh_exception import AuthenticationException
from datetime import date, datetime 
import compare_IECN_port
sys.path.append('N:/Python Libraries')  
from tabulate import tabulate

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

start_time = datetime.now()

''' -------------------------------------
    --------- CREDENTIAL OPTIONS --------
    ------------------------------------- '''
as_id = input("Insert your as_id: ")
as_pass = input("\nInsert your as_password: ")
en_secret = input("\nInsert your secret password:")
#This is useful for switches without management template. It will use the enable secret
if en_secret == '':
    en_secret = as_pass

''' -------------------------------------------------
    ---------- Get IP ADDRESS OF MACRO SWITCH -------
    ------------------------------------------------- '''
macro_switch = input("What's the IP Address of the MACRO SWITCH to validate?\n")


compare_port_list = []

#Make sure you paste the log you want to use in the logs_to_read file 
logs = open("logs_to_read.txt", "r").read()
pfcn_port_names = open("pfcn_port_names.txt", "r").readlines()
iecn_port_names = open("iecn_port_names.txt", "r").readlines()

#we need to concatenate the pfcn port names to be read in the log file
for i in range(len(pfcn_port_names)):
    if "TenGigabitEthernet" in pfcn_port_names[i]:
        pfcn_port_names[i]= pfcn_port_names[i].replace("TenGigabitEthernet","Te")
    elif "TwoGigabitEthernet" in pfcn_port_names[i]:
        pfcn_port_names[i] = pfcn_port_names[i].replace("TwoGigabitEthernet","Tw")
    elif "GigabitEthernet" in pfcn_port_names[i]:
        pfcn_port_names[i] = pfcn_port_names[i].replace("GigabitEthernet","Gi")  
        
#we need to concatenate the iecn port names to be read in the log file
for i in range(len(iecn_port_names)):
    if "TenGigabitEthernet" in iecn_port_names[i]:
        iecn_port_names[i]= iecn_port_names[i].replace("TenGigabitEthernet","Te")
    elif "TwoGigabitEthernet" in iecn_port_names[i]:
        iecn_port_names[i] = iecn_port_names[i].replace("TwoGigabitEthernet","Tw")
    elif "GigabitEthernet" in iecn_port_names[i]:
        iecn_port_names[i] = iecn_port_names[i].replace("GigabitEthernet","Gi")
         

#print("No of lines in the log file")
#print(len(logs))
#print(type(logs))

#connect to the switch with the username, password, and ip Address
conn = compare_IECN_port.connecttoSwitch(as_id, as_pass, macro_switch)

for i in range(len(pfcn_port_names)):
    #regex for mac-address -> \w{4}\.\w{4}.\w{4} 
    #This regex will find the mac address based on the port names
    reg = re.compile(r"\w{4}\.\w{4}.\w{4}\s+DYNAMIC+\s+"+str(pfcn_port_names[i].strip())+"\s")
    mo = reg.findall(logs)
    if len(mo) == 0: #if no match object found then the Port is probably not connected
        #print("This port: " +str(pfcn_port_names[i].strip())+" was probably not connected on the PFCN Switch. It is not on the mac-address table.")
        
        #logs_created = open("ports_found.txt", "a")
        #logs_created.write("\nPFCN PORT NAME: " +str(pfcn_port_names[i].strip())+" NOT in MAC TABLE. NOT CONNECTTED\n")
        #logs_created.close()
        
        #append to the compare_port_list
        compare_IECN_port.theAppender(compare_port_list, pfcn_port_names[i].strip(), iecn_port_names[i].strip(), "NOT in MAC TABLE", "NONE", "NOT CONNECTED")
    
    else:
        regMac = re.compile(r"\w{4}\.\w{4}.\w{4}")
        for mac in mo:#This will take the matched object and extract the mac-address we will use to verify
            moAD = regMac.search(mac)
            #print(moAD.group()) #This will give us the mac address
            compare_IECN_port.comparePort(compare_port_list, pfcn_port_names[i].strip(), moAD.group(), iecn_port_names[i].strip(), conn)


''' ---------------------------------------
    ---------- DIRECTORY COPY -------------
    --------------------------------------- '''   
dir = "N:\\Report\\macro-validation"
#This is for the directory
if os.path.exists(dir):
    print("Folder exists")
else:
    os.makedirs(dir)  #new dir for files to be moved
    print("\n"+str(dir) +" has been created!\n")

''' -------------------------------------------------
    ---------- TABULATE THE LIST AND SAVE TO FILE  -------
    ------------------------------------------------- '''
tabulated_table = tabulate(compare_port_list, headers=["PFCN PORT NAME","IECN PORT NAME","MAC ADDRESS FOUND","FOUND PORT", "STATUS"])       
print(tabulated_table)  
logs_created = open("N:\\Report\\macro-validation\\ports_found.txt", "a")
logs_created.write(tabulated_table)
logs_created.close()
 
elapsed_time = datetime.now() - start_time #to calculate the total elapsed time the script took to run
print("This script took approximately {}".format(elapsed_time))
    
