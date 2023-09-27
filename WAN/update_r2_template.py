

print("DONE with ROUTER ONE! MOVING ON to ROUTER TWO!!")

''' ------------------------------------------------------------
    ---------- CONVERT ROUTER TWO FROM CSV TO XLSX -------------
    ------------------------------------------------------------ '''
csv2_filename = "N:\\Report\\vEdge-to-cEdge\\MFG-8300-R2-I1-LTE-M1-I2-I3-G3-v1.csv"
r2_excel = "N:\\Report\\vEdge-to-cEdge\\r2-temp.xlsx"
data = pd.read_csv(csv2_filename) #Load CSV file using pandas
data.to_excel(r2_excel, index=False)


''' ---------------------------------------------------
    ---------- OPEN ROUTER TWO EXCEL FILE -------------
    --------------------------------------------------- '''
try:
    workbook = openpyxl.load_workbook("N:\\Report\\vEdge-to-cEdge\\r2-temp.xlsx") #Open the newly converted excel file
    sheet1 = workbook.active
    col = 1
  
    #print(sheet1.max_column) #to get the size of the column
    for i in range(sheet1.max_column): #loop through the list of header cells
        header = sheet1.cell(row = 1, column = col + i).value #Get the value of the header
        #print(sheet1.cell(row = 1, column = col + i).value)
        if header in header_to_function_dict: #if header value is in the dictionary
            if type(header_to_function_dict[header]) is str: #check if dictionary value is function or string
                value_to_set = header_to_function_dict[header]
                print(value_to_set)
                sheet1.cell(row = 2, column = col + i, value=value_to_set) #Update the coresponding column 
            else:
                value_to_set = header_to_function_dict[header]()
                print(value_to_set)
                sheet1.cell(row = 2, column = col + i, value=value_to_set) #Update the coresponding column 
    
    workbook.save("N:\\Report\\vEdge-to-cEdge\\r2-temp.xlsx")
    
except FileNotFoundError:
    print("File not found:", r2_template)
except openpyxl.utils.exceptions.InvalidFileException:
    print("Invalid Excel file format:", r2_template)

''' -------------------------------------------------
    ---------- CONVERT R1 FROM XLSX TO CSV -------------
    -------------------------------------------------- '''
    
excel_filename = "N:\\Report\\vEdge-to-cEdge\\r2-temp.xlsx"
r2_csv = "N:\\Report\\vEdge-to-cEdge\\r2-temp.csv"
data = pd.read_excel(excel_filename) #Load CSV file using pandas
data.to_csv(r2_csv, index=False)


elapsed_time = datetime.now() - start_time #to calculate the total elapsed time the script took to run
print("This script took approximately {}".format(elapsed_time))    


'''