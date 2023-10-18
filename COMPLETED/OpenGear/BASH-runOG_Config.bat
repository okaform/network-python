::@py <directory to the python script> %* forward any command line arguments to the python program
:: change the color of the batch file.(I didn't know I could do that)

::Color attributes are specified by TWO hex digits -- the first
::corresponds to the background; the second the foreground.  Each digit
::can be any of the following values:
::    0 = Black       8 = Gray
::    1 = Blue        9 = Light Blue
::    2 = Green       A = Light Green
::    3 = Aqua        B = Light Aqua
::    4 = Red         C = Light Red
::    5 = Purple      D = Light Purple
::    6 = Yellow      E = Light Yellow
::    7 = White       F = Bright White

::@py <directory to the python script> %* forward any command line arguments to the python program
:: change the color of the batch file.(I didn't know I could do that)
color 30 

@echo off
::Rem echo Input your as_id

echo Welcome!
::Get the users as_id, password and python script to run 
:: set /p as_id="Input your as_id: " 
::set py_name="getPCLog.py"
::set /p passwd="Input your PASSWORD for your AS_ACCOUNT: "

::print out the working directory
:: echo "Your working directory is " 
::dir 

::copy the python script to a working directory 
::This could just be changed to use the python file directly
::copy %py_name% "C:\Users\%as_id%\Desktop"
::copy script.txt "C:\Users\%as_id%\Desktop"
::echo "Successfully copied %py_name% to C:\Users\%as_id%\Desktop"
::echo "Successfully copied script.txt to C:\Users\%as_id%\Desktop"

::change directory 
::cd "C:\Users\%as_id%\Desktop>"
::echo "Successfully changed directory to C:\Users\%as_id%\Desktop"

@python getOG_Config.py 
::%as_id% %passwd%

@pause.exe