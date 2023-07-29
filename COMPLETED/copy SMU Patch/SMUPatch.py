import sys, re, os
from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException
from netmiko.ssh_exception import SSHException
from netmiko.ssh_exception import AuthenticationException
from datetime import date, datetime 
import logging 


logging.basicConfig(filename='netmiko_global.log', level=logging.DEBUG)
logger = logging.getLogger("netmiko")

#print("This is sys.argv 0 ->",sys.argv[1])
#date.today())+
#str(datetime.now().strftime("%m-%d-%y-[%H-%M]"))
start_time = datetime.now()

''' ---------------------------------------
    ---------- DIRECTORY MOVE -------------
    --------------------------------------- '''
dir = "N:\\Report\\blockpoint\\" 
#This is for the directory
if os.path.exists(dir):
    os.chdir(dir)
    print("Folder exists")
else:
    os.makedirs(dir)  #new dir for files to be moved
    os.chdir(dir)
    print("\n"+str(dir) +" has been created!\n")
    
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
    ---------- SMU PATCH CHOICES ---------
    ----------------------------------- '''
#smu pathces

smu_1 = "copy tftp://10.9.1.250/cat9k_iosxe.17.06.04.CSCwd17488.SPA.smu.bin flash:"
smu_2 = "copy tftp://10.9.1.252/cat9k_iosxe.17.06.04.CSCwa34390.SPA.smu.bin flash:"
smu_3 = "copy tftp://10.9.1.250/cat9k_iosxe.17.06.04.CSCwb51963.SPA.smu.bin flash:"

verify_1 = "Verify flash:cat9k_iosxe.17.06.04.CSCwd17488.SPA.smu.bin"
verify_2 = "Verify flash:cat9k_iosxe.17.06.04.CSCwa34390.SPA.smu.bin"
verify_3 = "Verify flash:cat9k_iosxe.17.06.04.CSCwb51963.SPA.smu.bin"
verify_4 = "Verify flash:cat9k_iosxe.17.06.04.SPA.bin"
    

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
        con.enable()
        

        #Hostname
        fileName = con.send_command("sh run | i (hostname )", read_timeout=180)
        fileName = fileName.split(" ")[1]
        #DO the verify of Main Code
        main_code = con.send_command("dir | include cat9k_iosxe.17.06.04.SPA.bin ")
        #if main code is present, continue, if not, break out of current iteration by continue 
        if main_code == "":
            print("The main version 17.06.04 code is not present. Please download.")
            continue
        else:
            print(main_code)
            #con.send_command("Verify flash:cat9k_iosxe.17.06.04.SPA.bin", read_timeout=360)
            
        #COPY SMU Patch
        #SMU 1
        copy_smu_1 = con.send_command_timing(smu_1, read_timeout= 0)
        #This is to verify the overwrite command
        if "over write" in copy_smu_1:
            con.send_command("n", read_timeout=120)
            con.send_command("", read_timeout=120)
            print(con.send_command("!", read_timeout=120))
        else:
            con.send_command_timing("", read_timeout=0)
        
        #SMU 2
        copy_smu_2 = con.send_command_timing(smu_2, read_timeout= 0)
        print(copy_smu_2)
        #This is to verify the overwrite command
        if "over write" in copy_smu_2:
            print(con.send_command("n", read_timeout=120))
            print(con.send_command("", read_timeout=120))
            con.send_command("!", read_timeout=120)
        else:
            con.send_command_timing("", read_timeout=0)


        #SMU 3
        copy_smu_3 = con.send_command_timing(smu_3, read_timeout= 0)
        #This is to verify the overwrite command
        if "over write" in copy_smu_3:
            con.send_command("n", read_timeout=120)
            con.send_command("", read_timeout=120)
            con.send_command("!", read_timeout=120)
        else:
            con.send_command_timing("", read_timeout=0)
            con.send_command("!", read_timeout=120)            


        #VERIFY
        v1 = con.send_command_timing(verify_1, read_timeout=0)
        v2 = con.send_command_timing(verify_2, read_timeout=0)
        v3 = con.send_command_timing(verify_3, read_timeout=0)
        print(con.send_command_timing(verify_4, read_timeout=0))
        con.send_command("", read_timeout=120)
        
        dir_output = con.send_command("dir | inc 17.06.04", read_timeout=120)
        print(dir_output)
        
        dir_log_file = open("N:\\Report\\blockpoint\\test.txt", "a")

        dir_log_file.write(fileName)
        dir_log_file.write("\n")
        dir_log_file.write(v1)
        dir_log_file.write(v2)
        dir_log_file.write(v3)
        dir_log_file.write(dir_output)
        dir_log_file.write("\n=========================================================================\n")

            
    if i != len(ipAd) - 1: #do not print this on the last switch
        print("\n--------------------------------------------------------------------------")    
        print("----------------------- Moving on to " +str(ipAd[i + 1]).strip() + " -------------------------")
        print("--------------------------------------------------------------------------\n\n") 
        
print("Successfully Completed. Please the " + str(dir) +" Folder")

elapsed_time = datetime.now() - start_time #to calculate the total elapsed time the script took to run
print("This script took approximately {}".format(elapsed_time))
        
        