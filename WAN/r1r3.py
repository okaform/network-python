import sys, re, os
from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException
from netmiko.ssh_exception import SSHException
from netmiko.ssh_exception import AuthenticationException
from datetime import date, datetime 

import VIPr3, ISRr1 

'''This script aims to help out with the WAN Migration process by simplifying the verification process.
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


''' -----------------------------------
    ------- SITE NAME -----
    ----------------------------------- '''
site_name = input("Enter the site name: ")

''' -----------------------------------
    ------- VIPTELA or ISR -----
    ----------------------------------- '''
#TODO: I need to make this more automated or at least for now, force an option
vip_or_isr = input("\n1. Viptela or 2. ISR ")
#this will determine which directory to use.
if vip_or_isr == '1':
    vip_or_isr = "vip"
    #pr_po_name = "-preLog.txt"
elif vip_or_isr == '2':
    vip_or_isr = "isr"
    #pr_po_name = "-postLog.txt"
else:
    vip_or_isr = "vip"
    #pr_po_name = "-preLog.txt"
''' ---------------------------------------
    ---------- DIRECTORY MOVE -------------
    --------------------------------------- '''
'''dir = "N:\\WAN\\" + str(site_name)+ "\\+Logs-" + str(datetime.now().strftime("%b-%d-%y [%H-%M]"))
#This is for the directory
if os.path.exists(dir):
    os.chdir(dir)
    print("Folder exists")
else:
    os.makedirs(dir)  #new dir for files to be moved
    os.chdir(dir)
    print("\n"+str(dir) +" has been created!\n") '''

''' ---------------------------------------
    ---------- PASTE IP ADDRESSES ---------
    --------------------------------------- '''
#print("\n\nPaste the IP Addresses you want prechecks generated. \n"+
#"When you are done. Hit ENTER, Ctrl + z, and ENTER in that order to end:\n")

#ipAd = sys.stdin.readlines() #This will read multiple lines

#Get the IP Address of either router 1 or router 3. depending on the site. 

r1_r3 = input("Enter the IP Address of either router 1 or router 3: ")


''' ------------------------------------------
    ---------- ACTUAL IMPLEMENTATION ---------
    ------------------------------------------ '''
net_dev = {"host":r1_r3,
           "username":as_id,
           "password":as_pass, 
           "device_type":"cisco_ios",
           "secret":en_secret
           }
try:
    con = ConnectHandler(**net_dev)
except:
    issue_st = "\nThere is a problem with your log in credentials for " +str(r1_r3).strip()+". Please check your username or password.\n"
    print(issue_st)
    #logs_err = open("ZZ-error-logs.txt", mode="a")
    #logs_err.write(issue_st)
#con.enable()

if vip_or_isr == 'vip':
    call_vip = VIPr3.get_r3(con)
else:
    call_vip = ISRr1.r1(con)
    
     
        
           
#print("Successfully Completed. Please the " + str(dir) +" Folder")

elapsed_time = datetime.now() - start_time #to calculate the total elapsed time the script took to run
print("This script took approximately {}".format(elapsed_time))
        
        