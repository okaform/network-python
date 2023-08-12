from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException
from netmiko.ssh_exception import SSHException
from netmiko.ssh_exception import AuthenticationException


#This file does the connection
''' -------------------------------------
    --------- CREDENTIAL OPTIONS --------
    ------------------------------------- '''
as_id = "as_cz507f" #input("Insert your as_id: ")
as_pass = "7Bn5wrWgdf6T8jSU" #input("\nInsert your as_password: ")
r1_ip_address = "10.193.8.158" #input("\nInsert router 1's IP Address: ")
r3_ip_address = "10.193.8.184" #input("\nInsert router 3's IP Address: ")



def r1_conn():
    net_dev_1 = {"host":r1_ip_address,
                "username":as_id,
                "password":as_pass, 
                "device_type":"cisco_ios",
             }
    try:
        con = ConnectHandler(**net_dev_1)
    except:
        issue_st = "\nThere is a problem with your log in credentials for " +str(r1_ip_address).strip()+". Please check your username or password.\n"
        print(issue_st)
    con.enable()
    print("r1 is connected")
    
    return con

def r3_conn():
    net_dev_3 = {"host":r3_ip_address,
                "username":as_id,
                "password":as_pass, 
                "device_type":"cisco_ios",
             }
    try:
        con = ConnectHandler(**net_dev_3)
    except:
        issue_st = "\nThere is a problem with your log in credentials for " +str(r1_ip_address).strip()+". Please check your username or password.\n"
        print(issue_st)
    print("r3 is connected")
    
    return con
