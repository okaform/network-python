

::@py <directory to the python script> %* forward any command line arguments to the python program
:: change the color of the batch file.(I didn't know I could do that)
color F2 

@echo off
::Rem echo Input your as_id

echo Welcome!
::Get the users as_id, password and python script to run 
set /p as_id="Input your as_id: " 
set py_name="getPreCheckScript.py"
set /p passwd="Input your PASSWORD for your AS_ACCOUNT: "

::print out the working directory
::echo "Your working directory is " 
::dir 

::copy the python script to a working directory 
::This could just be changed to use the python file directly
copy %py_name% "C:\Users\%as_id%\Desktop"
echo "Successfully copied %py_name% to C:\Users\%as_id%\Desktop"

::change directory 
cd "C:\Users\%as_id%\Desktop>"
echo "Successfully changed directory to C:\Users\%as_id%\Desktop"

@python getPreCheckScript.py %as_id% %passwd%

@pause.exe