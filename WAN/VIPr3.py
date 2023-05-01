#This is for viptela


def get_r3(conn):
    print("this is for r3")
    command1 = conn.send_command("show interface detail ge0/1.100 | nomore | display xml", read_timeout = 180)
    print(command1)
