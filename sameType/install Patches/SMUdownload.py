import sys, re, os
from netmiko import ConnectHandler
from datetime import date 

'''This script will install and verify the SMU patches on the macro switch'''

print("\n\nPaste the IP Addresses you want prechecks generated. \n"+
"When you are done. Hit ENTER, Ctrl + z, and ENTER in that order to end:\n")

ipAd = sys.stdin.readlines() #This will read multiple lines


for i in range(len(ipAd)):
    if len(ipAd[i]) != 1: #this takes care of empty lines so they are not looked at
        #print(str(i) +" -> "+ str(userInput[i]) + " length -> " + str(len(userInput[i])))
        net_dev = {"host":ipAd[i],
                    "username":"as_cz507f",
                    "password":"dClHXbGriLsp7w4Y", #sys.argv[2] this is for the password for as_id
                    "device_type":"cisco_ios",
                    "secret":"dClHXbGriLsp7w4Y"
                    }

        con = ConnectHandler(**net_dev)
        con.enable()
        download_SMU = "copy tftp://10.59.254.7/ios/current/cat9k_lite_iosxe.17.06.04.CSCwd14641.SPA.smu.bin flash:"
        con.send_command_timing(download_SMU)
        con.send_command_timing("")
        
        print("looking for the file with the dir command")
        reg = re.compile(r"cat9k_lite_iosxe.17.06.04.CSCwd14641.SPA.smu.bin")
        dirs = con.send_command_timing(" dir")
        print(reg.search(dirs).group())
       
        
        print(str(ipAd[i]) + "successfully completed")
        print("Moving on")
