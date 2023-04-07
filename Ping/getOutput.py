import nslookup

def hostname(con_from_main, ip_ad):
    hostname = nslookup.nslookup(ip_ad)
    #hostname = con_from_main.send_command("sh run | i (hostname )", read_timeout=180)
    #return hostname.split()[1]
    print(hostname)
    
    return hostname[1]
    
    
    
def switch_model(con_from_main):
    model = con_from_main.send_command("sh ver | inc Model Number", read_timeout=120)
    try:
        split_model = model.strip().split(" : ")[1]
        return split_model
    except:
        return "Command does not work"
    
    
    
def show_install_committed(con_from_main):
    sh_install_committed = con_from_main.send_command("sh install committed | inc IMG", read_timeout=120)    
    #split_commit = sh_install_committed.split("IMG ")
    
    try:
        split_commit = sh_install_committed.split("IMG ")[1]
        return split_commit
    except IndexError:
        return "Image not committed"