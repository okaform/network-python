from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException
from netmiko.ssh_exception import SSHException
from netmiko.ssh_exception import AuthenticationException


#This file does the connection
''' -------------------------------------
    --------- CREDENTIAL OPTIONS --------
    ------------------------------------- '''
as_id = "as_cz507f" #input("Insert your as_id: ")
as_pass = "S6ZWYK423BdfbPjC" #input("\nInsert your as_password: ")
r1_ip_address = "10.193.17.159" #input("\nInsert router 1's IP Address: ")
r2_ip_address = "10.193.19.223" #input("\nInsert router 2's IP Address: ")
r3_ip_address = "10.193.17.185" #input("\nInsert router 3's IP Address: ")
r4_ip_address = "10.193.19.249" #input("\nInsert router 4's IP Address: ")



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

#Router 2 connection
def r2_conn():
    net_dev_2 = {"host":r2_ip_address,
                "username":as_id,
                "password":as_pass, 
                "device_type":"cisco_ios",
             }
    try:
        con = ConnectHandler(**net_dev_2)
    except:
        issue_st = "\nThere is a problem with your log in credentials for " +str(r1_ip_address).strip()+". Please check your username or password.\n"
        print(issue_st)
    con.enable()
    print("r2 is connected")
    
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

#router 4
def r4_conn():
    net_dev_4 = {"host":r4_ip_address,
                "username":as_id,
                "password":as_pass, 
                "device_type":"cisco_ios",
             }
    try:
        con = ConnectHandler(**net_dev_4)
    except:
        issue_st = "\nThere is a problem with your log in credentials for " +str(r1_ip_address).strip()+". Please check your username or password.\n"
        print(issue_st)
    con.enable()
    print("r4 is connected")
    
    return con