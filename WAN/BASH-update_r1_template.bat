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

@python update_r1_template.py 
::%as_id% %passwd%

@pause.exe