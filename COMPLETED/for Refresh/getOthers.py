'''This portion will extract the serial number from a switch even if it's just one switch stack or 8 switch stack.'''

import sys
sys.path.append('N:/Python Libraries')  
from tabulate import tabulate


def getSerialNumber(switch_name, con):
    #Get the serial numbers
    serial_numbers = con.send_command("sh ver | inc System Serial Number ", read_timeout=180)
    #Split the serial numbers by the expression and put in a list    
    split_serial_numbers = serial_numbers.split("System Serial Number            : ")
   
    #get the hostname and add to table
    serial_number_table = []
    for j in range(len(split_serial_numbers)):
        if split_serial_numbers[j] != '':
            serial_number_table.append([(str(switch_name) + "-"+str(j)), split_serial_numbers[j]])
    
    #get it in tablulate format
    table = tabulate(serial_number_table, headers=["Switch Stack","Serial Numbers"])       
    print(table)          
    
    return(table)
        
    
    
