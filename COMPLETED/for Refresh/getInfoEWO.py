import sys, re, os
from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException
from netmiko.ssh_exception import SSHException
from netmiko.ssh_exception import AuthenticationException
from datetime import date, datetime
sys.path.append('N:/Python Libraries')  
from tabulate import tabulate
import docx


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


''' ---------------------------------------
    ---------- Get IP ADDRESS ---------
    --------------------------------------- '''
ipAd = input("\n\nPaste the IP Address you want to generate some EWO Info: ")

''' ------------------------------------------
    ---------- Open the Word Docx ---------
    ------------------------------------------ '''
'''doc_path = input("Enter the path to the EWO Document: ")

doc = docx.Document(doc_path)

target_paragrapgh = None

search_string = "Badge Access Switch Connection"
for paragraph in doc.paragraphs:
    if search_string in paragraph.text:
        #find the target paragraph
        target_paragrapgh = paragraph
        print(paragraph.text)
        
if target_paragrapgh:
    new_table = 
'''           
        
        
        


''' ------------------------------------------
    ---------- CONNECTION ---------
    ------------------------------------------ '''
net_dev = {"host":ipAd,
           "username":as_id,
           "password":as_pass, 
           "device_type":"cisco_ios",
           "secret":en_secret }
try:
    con = ConnectHandler(**net_dev)
except:
    issue_st = "\nThere is a problem with your log in credentials for " +str(ipAd).strip()+". Please check your username or password.\n"
    print(issue_st)
    #logs_err = open("ZZ-error-logs.txt", mode="a")
    #logs_err.write(issue_st)

try:
    con.enable()
except:
    print("\nThere is an issue with enable password")
    


''' -----------------------------------
    ------- EWO -----
    ----------------------------------- '''
EWO = input("\n1. EWO Name? ")

''' ---------------------------------------
    ---------- DIRECTORY MOVE -------------
    --------------------------------------- '''   
dir = "N:\\Report\\" + str(EWO)+ "-" + str(datetime.now().strftime("%b-%d-%y [%H-%M]"))
#This is for the directory
if os.path.exists(dir):
    os.chdir(dir)
    print("Folder exists")
else:
    os.makedirs(dir)  #new dir for files to be moved
    os.chdir(dir)
    print("\n"+str(dir) +" has been created!\n")

    
    
''' ------------------------------------------
    ---------- FILENAME ---------
    ------------------------------------------ '''    
#filename
fileName = con.send_command("sh run | i (hostname )", read_timeout=180)
host_dev_table = open(str(fileName.split(" ")[1]) +"-Table 2.txt", mode="a") 
port_config = open("port_config.txt", mode="a")    

#Get Mac Address Dynamic
mac_add = con.send_command("sh mac address-table dynamic", read_timeout=180)
#print(mac_add)   


''' ------------------------------------------
    ---------- PATTERNS ---------
    ------------------------------------------ '''
vlan_pattern = re.compile(r'^.*\b\d{3}\b.*$', re.MULTILINE)

matches = re.findall(vlan_pattern, mac_add)

mac_pattern = re.compile(r"([0-9a-fA-F]{4}\.){2}[0-9a-fA-F]{4}")

port_pattern = re.compile(r"[a-zA-Z]{2}\d+\/\d+\/\d+")

table_info = []

patch_cord_type = "Cat5e"

#The matches object is in a list and would be used to get the description
for vlan_match in matches:      
    #For the Mac Address
    mac_found = re.search(mac_pattern, vlan_match)
    if mac_found:
        #print(mac_found.group())
        mac_found = mac_found.group()
        
    #For the Ports
    port_found = re.search(port_pattern, vlan_match)
    if port_found:
        #print(port_found.group(0))
        int_desc = con.send_command("sh int " +str(port_found.group()) + " | inc Description", read_timeout=180)
        #for interface description
        int_desc = int_desc.split(":")[1]
        #For the intface type. if vlan 300, assign tenGig ports, else assign two gig ports
        if '300' in vlan_match:
            port_found_str = str(port_found.group()).replace("Gi", "Te")
            #create another file and write the configuration to it.
            #port_config.write("\n")
            port_config.write("\ninterface " + str(port_found_str))
            port_config.write("\n description " + str(int_desc))
            port_config.write("\n no shutdown")
            port_config.write("\nexit")
            port_config.write("\n!\n!")
            
        else:
            port_found_str = str(port_found.group()).replace("Gi", "Two")
            
    #The intface change process    
    int_change = str(port_found.group()) +" - " +str(port_found_str)
    table_info.append([int_desc, int_change, patch_cord_type, mac_found])
        

tabulated_table = tabulate(table_info, headers=["Device Name","Interface (Old - New)","Patch Cord Type","Length"])       
print(tabulated_table)          
    
    
host_dev_table.write(tabulated_table)
        
host_dev_table.close()   
port_config.close()     
        
     
print("Successfully Completed. Please the " + str(dir) +" Folder")

elapsed_time = datetime.now() - start_time #to calculate the total elapsed time the script took to run
print("This script took approximately {}".format(elapsed_time))
        
        