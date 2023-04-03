import sys, re, os
from netmiko import ConnectHandler
from datetime import date 
import stepOne

'''This script will download all the IOS code for the switches'''

print("\n\nPaste the IP Addresses you want prechecks generated. \n"+
"When you are done. Hit ENTER, Ctrl + z, and ENTER in that order to end:\n")

ipAd = sys.stdin.readlines() #This will read multiple lines


for i in range(len(ipAd)):
    if len(ipAd[i]) != 1: #this takes care of empty lines so they are not looked at
        #print(str(i) +" -> "+ str(userInput[i]) + " length -> " + str(len(userInput[i])))
        net_dev = {"host":ipAd[i],
                    "username":"as_cz507f", #sys.argv[1],
                    "password": "7EnJUgVK0DAWpZzS", #sys.argv[2], #sys.argv[2] this is for the password for as_id
                    "device_type":"cisco_ios",
                    "secret":"7EnJUgVK0DAWpZzS" #sys.argv[2]
                    }
        
        try:
            con = ConnectHandler(**net_dev)
        except:
            print("There is a problem with your log in credentials for " +str(ipAd[i])+". Please check your username or password")
            continue #This should break out of the loop
        con.enable()
        ''''STEP ONE: '''
        #stepOne.remove(con)
        
        
        ''''STEP TWO: '''
        #Ask the user if they want to continue with step 2. Reason for this is if they already downloaded the image to the switch
        user_input = input("Do you want to continue with downloading the image to "+str(ipAd[i])+"? y/n\n")
        if user_input.lower() == "y".lower(): get_version_name = stepOne.copy_new_image(con) 
        #The get_version_name will return the version name and also download the code to the switches 
        print("The version for "+str(ipAd[i]).strip()+" is ->" +get_version_name)
        
       
       
        
        print(str(ipAd[i]).strip() + " completed successfully ")
        print("Moving on")
