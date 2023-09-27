
import sys, re, os
from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException
from netmiko.ssh_exception import SSHException
from netmiko.ssh_exception import AuthenticationException
from datetime import date, datetime  


#print("This is sys.argv 0 ->",sys.argv[1])
#date.today())+
#str(datetime.now().strftime("%m-%d-%y-{%H-%M}"))
start_time = datetime.now()

print("\n\nPaste the IP Addresses you want prechecks generated. \n"+
"When you are done. Hit ENTER, Ctrl + z, and ENTER in that order to end:\n")

ipAd = sys.stdin.readlines() #This will read multiple lines

dir = "QuickSCript-" + str(datetime.now().strftime("%m-%d-%y-{%H-%M}"))

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
    

logName = open("logName.txt", "a")
for i in range(len(ipAd)):
    if len(ipAd[i]) != 1: #this takes care of empty lines so they are not looked at
        #print(str(i) +" -> "+ str(userInput[i]) + " length -> " + str(len(userInput[i])))
        net_dev = {"host":ipAd[i],
                    "username":sys.argv[1],
                    "password":sys.argv[2], #sys.argv[2] this is for the password for as_id
                    "device_type":"cisco_ios",
                    #"secret":sys.argv[2]
                    }
        try:
            con = ConnectHandler(**net_dev)
        except:
            issue = "There is a problem with your log in credentials for " +str(ipAd[i])+". Please check your username or password"
            print(issue)
            logName.write("\n\n"+str(issue)+"\n\n")
            continue #This should break out of the loop
        #con.enable()
        
        #Get the cdp and lldp neigh of switches
        fileName = con.send_command("sh run | inc (hostname )", read_timeout=180) #host-name is for viptela


        #Get CDP NEIGHBORS
        logName.write(str(fileName.split(" ")[1]) + "#") #get the switch name
        quick_com = con.send_command("sh cdp neigh", read_timeout=180)
        logName.write("sh cdp neigh\n")
        logName.write(quick_com)
        logName.write("\n")
        logName.write(str(fileName.split(" ")[1]) + "#") #get the switch name
        #logName.write("sh lldp neigh\n")
        #logName.write(str(con.send_command("sh lldp neigh", read_timeout=180)))
        logName.write("sh int description\n")
        logName.write(str(con.send_command("sh int description", read_timeout=180)))
        logName.write("\n------------------------------------------------------------------------------------\n\n")
        
        

        
        
      
        

        
        logName.write("\n\n")
  

            
    if i != len(ipAd) - 1: #do not print this on the last switch
        print("\n-----------------------------------------------------------")    
        print("-------------------------NEXT SWITCH ----------------------")
        print("-----------------------------------------------------------\n\n") 

logName.close()        
print("Successfully Completed. Please check your Desktop for the" + str(dir) +" Folder")

elapsed_time = datetime.now() - start_time #to calculate the total elapsed time the script took to run
print("This script took approximately {}".format(elapsed_time))
        


''' GET int DESCRIPTION SWEET#
        #create a list
        port_file = open("N:\\Scripts\\COMPLETED\\quick_check\\file_to_read.txt", "r")
        listObj = port_file.readlines()
        logName.write(str(fileName.split(" ")[1])+"#\n") #get the switch name
        for j in listObj:
            quick_com = con.send_command("sh int desc | inc (" + str(j).strip()+ " )", read_timeout=180)
            #print("sh int descr | inc " + str(j))
            print(quick_com)
            logName.write(quick_com)
            logName.write("\n")
        ''' 
            


        
        
''' THis for getting version number
        logName.write(" |   "+str(ipAd[i]).strip() +"   |   ") #get the IP 
        quick_com = con.send_command("sh ver | sec Version", read_timeout=180) #send the command
        
        regPort = re.compile(r"Version \d\d\.\d\d\.\d\d") #for version name
        moPo = regPort.search(quick_com)
        
        if moPo is None: #for the version that is empty
            logName.write("Can't find version")
        else:
            logName.write(str(moPo.group().strip()) +"  |   ")
            
        #for the type 
        quick_com2 = con.send_command("sh ver | sec cisco", read_timeout=180) #send the command
        regPort2 = re.compile(r"cisco C9300-48UXM") #for version name
        moPo2 = regPort2.search(quick_com2)
        
        if moPo2 is None: #for the version that is empty
            logName.write("Can't find version")
        else:
            logName.write(moPo2.group().strip())
        '''
         
         
'''Get CDP NEIGHBORS
        logName.write(str(fileName.split(" ")[1])) #get the switch name
        quick_com = con.send_command("sh cdp neigh", read_timeout=180)
        logName.write("sh cdp neigh")
        logName.write(quick_com)
        logName.write("\n")
        logName.write("sh lldp neigh")
        logName.write(str(con.send_command("sh lldp neigh", read_timeout=180)))
        logName.write("\n") '''
        
        
        
        
        
        
  
'''commands = commands.split("\n")
        #hs = str(fileName.split("host-name              ")[1]) +'#'
        #sys.stdin.readlines() #This will read multiple lines
        for command in commands:
            #logName.write(str(hs) + str(command)) #get the switch name
            quick_com = con.send_command(command, read_timeout=180)
            print(quick_com)
            logName.write("\n") 
            logName.write(quick_com)
            logName.write("\n")         '''  
        
'''Check to see if version 17 is in the dir'''
'''
        logName.write(str(fileName.split(" ")[1]) +'#') #get the switch name
        quick_com = con.send_command("dir | inc sxe.17.06.04.SPA.bin", read_timeout=180)
        logName.write("dir | inc sxe.17.06.04.SPA.bin")
        logName.write("\n")
        logName.write(quick_com)
        logName.write("\n")
        
        
        quick_com2 = con.send_command("dir | inc smu.bin", read_timeout=180)
        logName.write("dir | inc sxe.17.06.04.SPA.bin")
        logName.write("\n")
        logName.write(quick_com2)
        logName.write("\n")
        '''