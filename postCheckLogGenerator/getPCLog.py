
import sys, re, os
from netmiko import ConnectHandler
from datetime import date 

'''ip_ad = "10.22.3.5"
as_id = "as_cz507f"
passwd = "eqBHKti48MWSmzr7"
en = "eqBHKti48MWSmzr7"'''

#print("This is sys.argv 0 ->",sys.argv[1])



print("\n\nPaste the IP Addresses you want prechecks generated. \n"+
"When you are done. Hit ENTER, Ctrl + z, and ENTER in that order to end:\n")

ipAd = sys.stdin.readlines() #This will read multiple lines

dir = "PostCheckLogs-" + str(date.today())

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

        con = ConnectHandler(**net_dev)
        con.enable()
        
        scriptFile = open("../script.txt", "r")#we're going back a directory because we changed to the precheck directory
        fileName = con.send_command("sh run | i hostname")
        postCheck_file = open(str(fileName.split(" ")[1])+"-postLog.txt", mode="a") #create postCheck_file file in .txt for pfcn switches
        while True:
            to_send = scriptFile.readline()
            
            log = con.send_command_timing(to_send)#, read_timeout=0, last_read = 8.0)
            postCheck_file.write("\n"+str(fileName.split(" ")[1]) + "#"+ str(to_send))
            postCheck_file.write(log)
            #print(log)
            
            if scriptFile.readline() == '': break

        postCheck_file.close()
        
        scriptFile.close()
            
        print("\n\nNext Switch")
print("Successfully Completed. Please check your Desktop for the PostCheckLogs Folder")
        
        