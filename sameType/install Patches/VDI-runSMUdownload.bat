

::@py <directory to the python script> %* forward any command line arguments to the python program
:: change the color of the batch file.(I didn't know I could do that)
color F2 

@echo off
::Rem echo Input your as_id

echo Welcome!

@python SMUdownload.py %as_id% %passwd%

@pause.exe