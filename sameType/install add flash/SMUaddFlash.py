import sys, re, os
from netmiko import ConnectHandler
from datetime import date 

'''This script will install add flash'''

print("\n\nPaste the IP Addresses you want prechecks generated. \n"+
"When you are done. Hit ENTER, Ctrl + z, and ENTER in that order to end:\n")

ipAd = sys.stdin.readlines() #This will read multiple lines


installed_Patches = open("C:\\Users\\as_cz507f\\Desktop\\add_flash.txt", mode="a")

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
        install_SMU = "install add file flash:cat9k_lite_iosxe.17.06.04.CSCwd14641.SPA.smu.bin activate commit"
        iSM = con.send_command_timing(install_SMU, read_timeout=0, last_read = 12.0) #this last_read option gives it more time to read the output
        print(iSM)
        con.send_command_timing("y")
        
        #write the output to the macros
        
        installed_Patches.write(str(ipAd[i]) + " -> " +  str(iSM) + "\n\n") 
        print(str(ipAd[i]) + "successfully completed")
        print("Moving on")
        
        
installed_Patches.close()
