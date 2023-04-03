import sys, re, os
from netmiko import ConnectHandler
from datetime import date 

'''This script will install and verify the SMU patches on the macro switch'''

print("\n\nPaste the IP Addresses you want prechecks generated. \n"+
"When you are done. Hit ENTER, Ctrl + z, and ENTER in that order to end:\n")

ipAd = sys.stdin.readlines() #This will read multiple lines


verified_Macros = open("C:\\Users\\as_cz507f\\Desktop\\verified_macros.txt", mode="a")

for i in range(len(ipAd)):
    if len(ipAd[i]) != 1: #this takes care of empty lines so they are not looked at
        #print(str(i) +" -> "+ str(userInput[i]) + " length -> " + str(len(userInput[i])))
        net_dev = {"host":ipAd[i],
                    "username":"as_cz507f",
                    "password":"opf0yeHMcZxELGTJ", #sys.argv[2] this is for the password for as_id
                    "device_type":"cisco_ios",
                    "secret":"opf0yeHMcZxELGTJ"
                    }

        con = ConnectHandler(**net_dev)
        con.enable()
        verify_SMU = "Verify flash:cat9k_lite_iosxe.17.06.04.CSCwd14641.SPA.smu.bin"
        ver = con.send_command_timing(verify_SMU)
        print(ver)
        
        #write the output to the macros
        
        verified_Macros.write(str(ipAd[i]) + " -> " +  str(ver) + "\n\n") 
        print(str(ipAd[i]) + "successfully completed")
        print("Moving on")
        
        
verified_Macros.close()
