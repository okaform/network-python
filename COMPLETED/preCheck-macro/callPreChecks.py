'''This script will only work if there is a precheck folder generated. It will use the precheck scripts in the precheck folder to generate the precheck log'''
import os



def preCheck(con, dir, ipAd, file):
    #check for folder name before attempting to continue
    if file.name != "":#this might not be needed. It's to make sure this doesn't run if a script file wasn't generated        
        if not os.path.exists(dir):
            os.makedirs(dir)  #new dir for files to be moved
            print("\n"+str(dir) +" has been created!\n")
        print("creating logs for "+str(file.name) + " right now" )
        
        #open the script file that we got from the main method
        filename = file.name
        scriptFile = open(file.name, "r")# we open the closed object like this (not really open)
        
        #put the file in a list object
        listObj = scriptFile.readlines()        
        
        preLog_file = open(str(dir)+"\\"+str(filename).split(".txt")[0]+"-preLog.txt", mode="a") #create pre-checklog_file file in .txt for pfcn switches
        
        for i in listObj:#i represents every line expect_string=r'#',
            log = con.send_command(i.strip(), read_timeout = 90) # send the command 
            #this waits for 90 seconds or if it gets the prompt then moves on.
            preLog_file.write("\n"+str(filename.split("-preCheck.txt")[0]) + "#"+ str(i)) #This is the prompt
            preLog_file.write(log)

        #preLog_file.close()
        
        scriptFile.close()

        return
    
    print("preCheck file for "+ str(ipAd) + " was not created.") #this will only run if there is an error up top
    
    
    
    

    
    
        
    