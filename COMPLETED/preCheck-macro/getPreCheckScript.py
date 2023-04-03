
import sys, re, os
from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException
from netmiko.ssh_exception import SSHException
from netmiko.ssh_exception import AuthenticationException
from datetime import date, datetime 
import genPreCheckScripts, callPreChecks

'''ip_ad = "10.22.3.5"
as_id = "as_cz507f"
passwd = "eqBHKti48MWSmzr7"
en = "eqBHKti48MWSmzr7"'''

start_time = datetime.now()

#print("This is sys.argv 0 ->",sys.argv[1])

print("\n\nPaste the IP Addresses you want prechecks generated. \n"+
"When you are done. Hit ENTER, Ctrl + z, and ENTER in that order to end:\n")

ipAd = sys.stdin.readlines() #This will read multiple lines

dir = "PreCheck-" + str(datetime.now().strftime("%m-%d-%y-{%H-%M}"))

#sys.argv[1] is for the as_is
os.chdir("C:\\Users\\"+sys.argv[1]+"\\Desktop")

desktop = os.getcwd()

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
                    "username":sys.argv[1],
                    "password":sys.argv[2], #sys.argv[2] this is for the password for as_id
                    "device_type":"cisco_ios",
                    "secret":sys.argv[2]
                    }
        #This try catch block makes sure that if we hit a bad switch it doesn't crash the program but keeps going
        try:
            con = ConnectHandler(**net_dev)
        except:
            print("There is a problem with your log in credentials for " +str(ipAd[i])+". Please check your username or password")
            continue
        con.enable()
        
        #call the genPreCheckScript
        filename = genPreCheckScripts.genPreCheck(con) # filename it created in the function needs to be returned to be used for logs
        
        #call the callPreChecks
        send_desktop = str(desktop)+"\\Logs-"+ str(dir)
        callPreChecks.preCheck(con, send_desktop, ipAd[i], filename)
        
        
        
        if i != len(ipAd) - 1: #do not print this on the last switch
            print("\n-----------------------------------------------------------")    
            print("-------------------------NEXT SWITCH ----------------------")
            print("-----------------------------------------------------------\n\n") 
        
print("Successfully Completed. Please check your Desktop for the PreCheck Folder")

elapsed_time = datetime.now() - start_time #to calculate the total elapsed time the script took to run
print("This script took approximately {}".format(elapsed_time))
        
        