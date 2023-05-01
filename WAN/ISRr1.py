#this is for ISR


def r1(con):
    print("this is for ISR")
    command1 = con.send_command("show ip int brief", read_timeout = 180)
    print(command1)