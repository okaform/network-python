import sys, re, os
import xlsxwriter
import openpyxl
import csv
from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException
from netmiko.ssh_exception import SSHException
from netmiko.ssh_exception import AuthenticationException
from datetime import date, datetime  
#import special_commands
from header_to_function import header_to_function_dict


''' ---------------------------------------
    ---------- OPEN EXCEL FILE -------------
    --------------------------------------- '''
r1_template = "N:\\Report\\vEdge-to-cEdge\\MFG-NA-8300-R1-M1-I2-I3-I1-LTE-T4-v5.csv"
try:
    with open(r1_template, 'r') as read_r1_template:
        csv_reader = csv.reader(read_r1_template)
    
        header = next(csv_reader)#Read the first row as the header
        data = next(csv_reader)#Read the next/second row as the value/data
        
        #for item in header:
        #    if item in header_to_function:
                
        
        header_to_index = {col: i for i, col in enumerate(header)}
        
        for header_name, new_value in header_to_function_dict.items():
            if header_name in header_to_index: #if header name in dictionary is in the header index from the csv file, then
                index_to_update = header_to_index[header_name] #find the  index of the header 
                data_value = data[index_to_update] #match it to the index of the data
                #update the data and then update the csv file
                print(data_value)
                print(type(data_value))
                new_value(data_value)
            else:
                print(f"Header '{header_name}' not found.")
            
        print("Updated Header:", header)
        print("Updated Data:", data)
            
except FileNotFoundError:
    print("File not found:", r1_template)
except openpyxl.utils.exceptions.InvalidFileException:
    print("Invalid Excel file format:", r1_template)