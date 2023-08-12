import sys, re, os
import sys, re, os
import xlsxwriter
import openpyxl
import csv
from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException
from netmiko.ssh_exception import SSHException
from netmiko.ssh_exception import AuthenticationException



''' ---------------------------------------
    ---------- OPEN EXCEL FILE -------------
    --------------------------------------- '''
r1_template = "N:\\Report\\vEdge-to-cEdge\\MFG-NA-8300-R1-M1-I2-I3-I1-LTE-T4-v5.csv"
updated_data = []
try:
    with open(r1_template, 'r') as read_r1_template:
        csv_reader = csv.reader(read_r1_template)
    
        header = next(csv_reader)#Read the first row as the header
        data = next(csv_reader)#Read the next/second row as the value/data
        
        #header_to_index = {col: i for i, col in enumerate(header)}
        
        for i in range(len(header)):
            if header[i] == "//system/host-name":
                data[i] = "ashkdfhlkdsjfha;sdf;f"
                updated_data.append(data)
     
except FileNotFoundError:
    print("File not found:", r1_template)
except openpyxl.utils.exceptions.InvalidFileException:
    print("Invalid Excel file format:", r1_template)
    
with open(r1_template, 'w') as csv_file:
    csv_writer = csv.writer(csv_file)
    
    for row in updated_data:
        csv_writer.writerow(row)