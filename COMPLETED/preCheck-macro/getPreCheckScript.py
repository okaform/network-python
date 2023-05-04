
import sys, re, os
from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException
from netmiko.ssh_exception import SSHException
from netmiko.ssh_exception import AuthenticationException
from datetime import date, datetime 
import genPreCheckScripts, callPreChecks


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
    ---------- GET THE IP ADDRESSES ---------
    --------------------------------------- '''

print("\n\nPaste the IP Addresses you want prechecks generated. \n"+
"When you are done. Hit ENTER, Ctrl + z, and ENTER in that order to end:\n")

ipAd = sys.stdin.readlines() #This will read multiple lines

''' ---------------------------------------
    ---------- DIRECTORY MOVE -------------
    --------------------------------------- '''   
dir = "N:\\Report\\macro-preCheck-" + str(datetime.now().strftime("%b-%d-%y [%H-%M]"))
#This is for the directory
if os.path.exists(dir):
    os.chdir(dir)
    print("Folder exists")
else:
    os.makedirs(dir)  #new dir for files to be moved
    os.chdir(dir)
    print("\n"+str(dir) +" has been created!\n")





for i in range(len(ipAd)):
    if len(ipAd[i]) != 1: #this takes care of empty lines so they are not looked at
        #print(str(i) +" -> "+ str(userInput[i]) + " length -> " + str(len(userInput[i])))
        net_dev = {"host":ipAd[i],
                    "username":as_id,
                    "password": as_pass, 
                    "device_type":"cisco_ios",
                    "secret": en_secret
                    }
        #This try catch block makes sure that if we hit a bad switch it doesn't crash the program but keeps going
        try:
            con = ConnectHandler(**net_dev)
        except:
            print("There is a problem with your log in credentials for " +str(ipAd[i])+". Please check your username or password")
            continue
        try:
            con.enable()
        except:
            print("There is a problem with your log in credentials for " +str(ipAd[i])+". Please check your username or password")
            continue
        
        #call the genPreCheckScript
        script_directory = str(dir) + "\\scripts"
        file_host_data = genPreCheckScripts.genPreCheck(con, script_directory) # filename it created in the function needs to be returned to be used for logs
        
        #call the callPreChecks
        send_report = str(dir) +"\\Logs"
        #file_host_data[0] and [1] are the precheck file object and the hostname respectively
        callPreChecks.preCheck(con, send_report, ipAd[i], file_host_data[0], file_host_data[1])
        
        
        
        if i != len(ipAd) - 1: #do not print this on the last switch
            print("\n------------------------------------------------------------------------------------------")    
            print("----------------------- Moving on to " +str(ipAd[i + 1]).strip() + " -------------------------")
            print("----------------------------------------------------------------------------------------------\n\n") 
        
print("Successfully Completed. Please check your Reports Folder for the PreCheck Information. ")

elapsed_time = datetime.now() - start_time #to calculate the total elapsed time the script took to run
print("This script took approximately {}".format(elapsed_time))
        
        