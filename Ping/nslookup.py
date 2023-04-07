'''This takes a string and does an nslookup, returning a list object with its ip address and hostname'''

import subprocess

def nslookup(ip_or_hostname): 
    data=[]
    #take the ip or hostname
    output = subprocess.run(["nslookup", ip_or_hostname],stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    #std_out and std_err are not going to be seen with this DEVNULL statement
    try:
        hostname = str(output.stdout.splitlines()[3]).replace("b'Name:   ", '').replace('\'', '')
    except:
        hostname = "Not found"
            
    try:
        ipAdd = str(output.stdout.splitlines()[4]).replace("b'Address: ", '').replace('\'', '')
    except:
        ipAdd = ("not found")   
            
            
    data= [ipAdd, hostname]
    
    return data