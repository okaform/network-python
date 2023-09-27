import sys, re, os
from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException
from netmiko.ssh_exception import SSHException
from netmiko.ssh_exception import AuthenticationException
from datetime import date, datetime  



#print("This is sys.argv 0 ->",sys.argv[1])
#date.today())+
#str(datetime.now().strftime("%m-%d-%y-[%H-%M]"))
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

#print(en_secret)
''' -----------------------------------
    ------- PRECECK or POST CHECK -----
    ----------------------------------- '''
pre_or_post = input("\n1. Pre Check or 2. Post Check? ")
#this will determine which directory to use.
if pre_or_post == '1':
    pre_or_post = "pre-check-report"
    pr_po_name = "-preLog.txt"
elif pre_or_post == '2':
    pre_or_post = "post-check-report"
    pr_po_name = "-postLog.txt"
else:
    pre_or_post = "pre-check-report"
    pr_po_name = "-preLog.txt"

''' -----------------------------------
    ---------- SCRIPT CHOICES ---------
    ----------------------------------- '''
#give the user an option on which script to use
ch_script = input("\nWhich Script are you using?"
"\n1. Refresh/MFG Script"+
"\n2. WTC/Corp Script"+
"\n3. Short Script"+
"\n4. Long Script" +
"\n5. SDWAN Script" +
"\nInput: ")

script_to_use = ""
if ch_script == '1':
    script_to_use = "mfg-script.txt"
elif ch_script == '2':
    script_to_use = "corp-script.txt"
elif ch_script == '3':
    script_to_use = "short-script.txt"
elif ch_script == '4':
    script_to_use = "long-script.txt"
elif ch_script == '5':
    script_to_use = "sdwan.txt"
else:
    script_to_use = "mfg-script.txt"
    

''' ---------------------------------------
    ---------- DIRECTORY MOVE -------------
    --------------------------------------- '''
dir = "N:\\Report\\" + str(pre_or_post)+ "\\+Logs-" + str(datetime.now().strftime("%b-%d-%y [%H-%M]"))
#This is for the directory
if os.path.exists(dir):
    os.chdir(dir)
    print("Folder exists")
else:
    os.makedirs(dir)  #new dir for files to be moved
    os.chdir(dir)
    print("\n"+str(dir) +" has been created!\n")

''' ---------------------------------------
    ---------- PASTE IP ADDRESSES ---------
    --------------------------------------- '''
print("\n\nPaste the IP Addresses you want prechecks generated. \n"+
"When you are done. Hit ENTER, Ctrl + z, and ENTER in that order to end:\n")

ipAd = sys.stdin.readlines() #This will read multiple lines



''' ------------------------------------------
    ---------- ACTUAL IMPLEMENTATION ---------
    ------------------------------------------ '''
for i in range(len(ipAd)):
    if len(ipAd[i]) != 1: #this takes care of empty lines so they are not looked at
        #print(str(i) +" -> "+ str(userInput[i]) + " length -> " + str(len(userInput[i])))
        net_dev = {"host":ipAd[i],
                    "username":as_id,
                    "password":as_pass, 
                    "device_type":"cisco_ios",
                    "secret":en_secret
                    }
        try:
            con = ConnectHandler(**net_dev)
        except:
            issue_st = "\nThere is a problem with your log in credentials for " +str(ipAd[i]).strip()+". Please check your username or password.\n"
            print(issue_st)
            logs_err = open("ZZ-error-logs.txt", mode="a")
            logs_err.write(issue_st)
            continue #This should break out of the loop
        #con.enable()
        
        scriptFile = open("N:\\Scripts\\COMPLETED\\preCheckLogGenerator\\scripts\\"+str(script_to_use), "r")#we're going back a directory because we changed to the precheck directory
        
        #for others
        fileName = con.send_command("sh run | i (hostname )", read_timeout=180)
        #for VIPTELA
        #fileName = con.send_command("sh run | i host-name", read_timeout=180)
        
        preCheck_file = open(str(fileName.split(" ")[1])+ pr_po_name, mode="a") #create precheck_file file in .txt for pfcn switches
        
        listObj = scriptFile.readlines()
        
        
        for j in listObj:
            to_send = j
            log = con.send_command(to_send, read_timeout = 180)#, read_timeout=0, last_read = 8.0)
            preCheck_file.write("\n"+str(fileName.split(" ")[1]) + "#"+ str(to_send)) #preLog file and preCheck_file...
            preCheck_file.write(log)
            #print(to_send)
            #print(log)

        preCheck_file.close()
        
        scriptFile.close()
            
    if i != len(ipAd) - 1: #do not print this on the last switch
        print("\n--------------------------------------------------------------------------")    
        print("----------------------- Moving on to " +str(ipAd[i + 1]).strip() + " -------------------------")
        print("--------------------------------------------------------------------------\n\n") 
        
print("Successfully Completed. Please the " + str(dir) +" Folder")

elapsed_time = datetime.now() - start_time #to calculate the total elapsed time the script took to run
print("This script took approximately {}".format(elapsed_time))
        
        