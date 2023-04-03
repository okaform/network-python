
import sys, re, os
from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException
from netmiko.ssh_exception import SSHException
from netmiko.ssh_exception import AuthenticationException
from datetime import date, datetime  

'''ip_ad = "10.22.3.5"
as_id = "as_cz507f"
passwd = "eqBHKti48MWSmzr7"
en = "eqBHKti48MWSmzr7"'''

#print("This is sys.argv 0 ->",sys.argv[1])
#date.today())+
#str(datetime.now().strftime("%m-%d-%y-{%H-%M}"))
start_time = datetime.now()

site_name = input("ENTER SITE NAME")

print("\n\nPaste the IP Addresses you want postchecks generated. \n"+
"When you are done. Hit ENTER, Ctrl + z, and ENTER in that order to end:\n")

ipAd = sys.stdin.readlines() #This will read multiple lines

dir = str(site_name)+"-PostCheckLogs-" + str(datetime.now().strftime("%m-%d-%y-{%H-%M}"))

#sys.argv[1] is for the as_is
os.chdir("C:\\Users\\"+sys.argv[1]+"\\Desktop")
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
        try:
            con = ConnectHandler(**net_dev)
        except:
            print("There is a problem with your log in credentials for " +str(ipAd[i])+". Please check your username or password")
            continue #This should break out of the loop
        con.enable()
        
        scriptFile = open("../script.txt", "r")#we're going back a directory because we changed to the postcheck directory
        fileName = con.send_command("sh run | i hostname", read_timeout=180)
        postCheck_file = open(str(fileName.split(" ")[1])+"-postLog.txt", mode="a") #create postcheck_file file in .txt for pfcn switches
        
        listObj = scriptFile.readlines()
        
        
        for j in listObj:
            to_send = j
            log = con.send_command(to_send, read_timeout = 180)#, read_timeout=0, last_read = 8.0)
            postCheck_file.write("\n"+str(fileName.split(" ")[1]) + "#"+ str(to_send)) #postLog file and postCheck_file...
            postCheck_file.write(log)
            #print(to_send)
            #print(log)

        postCheck_file.close()
        
        scriptFile.close()
            
    if i != len(ipAd) - 1: #do not print this on the last switch
        print("\n-----------------------------------------------------------")    
        print("-------------------------NEXT SWITCH ----------------------")
        print("-----------------------------------------------------------\n\n") 
        
print("Successfully Completed. Please check your Desktop for the" + str(dir) +" Folder")

elapsed_time = datetime.now() - start_time #to calculate the total elapsed time the script took to run
print("This script took approximately {}".format(elapsed_time))
        
        