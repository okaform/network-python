'''This python script will take the 3 site character code and the IP address for open gear and generate the config needed for the refresh'''
'''Eventually, we should be able to paste all the IP address and site code and generate all the config at once'''

import sys, re, os
from netmiko import ConnectHandler
#from netmiko.ssh_exception import NetMikoTimeoutException
#from netmiko.ssh_exception import SSHException
#from netmiko.ssh_exception import AuthenticationException
from datetime import date, datetime

hostname = input("What is the hostname for the open gear? ").lower()
user_name = input("Insert your as_id: ")
passwd = input("Insert your as_password: ")
router_1 = hostname[:3] + "crwcrt001."+hostname[:3] + ".nam.gm.com"

site_name = hostname[:3]

#log into router and get snmp location

net_dev = {"host": router_1,
           "username": user_name,
           "password": passwd,
           "device_type": "cisco_ios",
           #"secret": en_secret
           }
try:
    con = ConnectHandler(**net_dev)
except:
    issue_st = "\nThere is a problem with your log in credentials for " + str(router_1).strip() + ". Please check your username or password.\n"
    print(issue_st)
try:
    con.enable()
except:
    print("connection doesn't work")

try:
    snmp_loc = con.send_command("sh snmp location", read_timeout=180)
    new_snmp_loc = snmp_loc.replace('"', '')
    print(new_snmp_loc)
except:
    snmp_loc = input("connection issues. Please reach to the device manually and put the snmp location:")
    new_snmp_loc = snmp_loc.replace('"', '')
    print(new_snmp_loc)

'''----------------------------------------
---------------SYSLOG ---------------------
---------------------------------------------'''
# get the 3 char code
three_char_code = hostname[:3]

syslog = f'''
#=================================================
#---------------- OPEN GEAR ----------------------
#=================================================
ogcli merge services/syslog_servers <<'END'
syslogServers[0].address="148.93.115.30"
syslogServers[0].description=""
syslogServers[0].min_severity="info"
syslogServers[0].port=5325
syslogServers[0].port_logging_enabled=true
syslogServers[0].protocol="UDP"
END
ogcli merge services/syslog_servers <<'END'
syslogServers[0].address="130.172.83.30"
syslogServers[0].description=""
syslogServers[0].min_severity="info"
syslogServers[0].port=5325
syslogServers[0].port_logging_enabled=true
syslogServers[0].protocol="UDP"
END
ogcli update system/admin_info 'contact="GM GTSC 855-780-1125"'
ogcli update system/admin_info 'location="{new_snmp_loc}"'
ogcli update system/hostname 'hostname="{three_char_code}crnmts001"'
ogcli create services/snmp_alert_manager 'id="services_snmp_managers-1"' 'address="130.172.129.252"' 'auth_protocol="SHA"' 'msg_type="TRAP"' 'community="Trap41String"' 'version="v2c"' 'protocol="UDP"'
ogcli create services/snmp_alert_manager 'id="services_snmp_managers-1"' 'address="148.93.49.56"' 'auth_protocol="SHA"' 'msg_type="TRAP"' 'community="Trap41String"' 'version="v2c"' 'protocol="UDP"'
ogcli update system/timezone 'timezone="UTC"'
ogcli update services/ntp enabled=true 'servers[0].value="164.56.50.7"' 
ogcli update services/ntp enabled=true 'servers[1].value="130.173.33.162"'
ogcli update services/ntp enabled=true 'servers[2].value="134.46.156.138"'
ogcli replace services/snmpd <<'END'
auth_password="82ndAirborneDivisionParatrooperVeteran"
auth_protocol="SHA"
auth_use_plaintext=true
enable_legacy_versions=false
enable_secure_snmp=true
enabled=true
port=161
priv_password="82ndAirborneDivisionParatrooperVeteran"
priv_protocol="AES"
priv_use_plaintext=true
protocol="UDP"
rocommunity="Delta4123R"
rwcommunity="Zeta2008XT"
security_level="priv"
security_name="snmpv3user"
END
'''
print(syslog)

'''#----------------------------------------
#---------------Port Config  ---------------------
#---------------------------------------------'''
#connect to the open gear router

open_gear = {"host": hostname,
           "username": "root",
           "password": "zXJ-F^Ga35Bk_tkK",
           "device_type": "linux",
           #"secret": en_secret
           }
try:
    con = ConnectHandler(**open_gear)
except:
    issue_st = "\nThere is a problem with your log in credentials for " + str(hostname).strip() + ". Please check your username or password.\n"
    print(issue_st)

ip_address = con.send_command("ifconfig eth0 | grep -oE 'inet addr:[^ ]+' | awk -F ':' '{print $2}'", read_timeout=180)
if ip_address == '':
    ip_address = con.send_command("ifconfig bond0 | grep -oE 'inet addr:[^ ]+' | awk -F ':' '{print $2}'", read_timeout=180)

mask = con.send_command("ifconfig eth0 | grep -oE 'Mask:[^ ]+' | awk -F ':' '{print $2}'", read_timeout=180)
if mask == '':
    mask = con.send_command("ifconfig bond0 | grep -oE 'Mask:[^ ]+' | awk -F ':' '{print $2}'", read_timeout=180)
gateway = con.send_command("ip route | awk '/default via/ {print $3}'", read_timeout=180)

port_config = f'''
#=================================================
#---------- OPEN GEAR PORT CONFIG ----------------
#=================================================
to test open gear/upgrade: NET1: internet, serial port 1: console
#-------------------------------------------------------------------------
ogcli update conn default-conn-1 'ipv4_static_settings.address="10.44.80.50"'
ogcli update conn default-conn-1 'ipv4_static_settings.netmask="255.255.255.224"'
ogcli update conn default-conn-1 'ipv4_static_settings.gateway="10.44.80.48"'


ogcli get conn default-conn-1
#-------------------------------------------------------------------------
ogcli update conn default-conn-1 'ipv4_static_settings.address="{ip_address}"'
ogcli update conn default-conn-1 'ipv4_static_settings.netmask="{mask}"'
ogcli update conn default-conn-1 'ipv4_static_settings.gateway="{gateway}"'


#---------- DELETE IPV4 DHCP for INET1------------
#=================================================
ogcli get conn "default-conn-2"
#------------------------------------------------
ogcli delete conn "default-conn-2"

#---------- DELETE IPV6 DHCP for INET1------------
#=================================================
ogcli get conn "v6-dyn-n1-conn"
#------------------------------------------------
ogcli delete conn "v6-dyn-n1-conn"

#CREATE BOND
#-------------------------------------
ogcli create physif << END
bond_setting.mode="active-backup"
media="bond"
slaves[0]="system_net_physifs-1"
slaves[1]="system_net_physifs-2"
enabled=true
description="BND0 - Aggregate"
primary_slave ="system_net_physifs-1"
END
'''

'''----------------------------------------
--------------- Cellular Enable  ------------
---------------------------------------------'''
cellular_enable = '''
#--------------------------------------------
#--------------- Cellular Enable  ------------
#---------------------------------------------
#to enable the sim
ogcli get conn "default_cellular"
ogcli get physifs
ogcli get physif "wwan0"
#-----------------------------------------------
ogcli update physif wwan0 << 'END'
enabled=true
END
'''

print(port_config)


oob_failover_probe = '''
#--------------------------------------------
#------------OOB Failover Probe  ------------
#---------------------------------------------
#ogcli get failover/settings
#remember that wan0 is cellular right now but it could change in the future
#---------------------------------------------
ogcli update failover/settings <<END
enabled=true
failover_physif="wwan0"
probe_address="10.233.249.68"
probe_physif="bnd0"
probe_address_2="10.233.249.76"
END
'''

'''----------------------------------------
---------------TACACS+  ---------------------
---------------------------------------------'''

tac = '''
#=================================================
#---------- TACACS+ ----------------
#=================================================
ogcli get auth
#-------------------------------------------------------------------------
ogcli update auth 'tacacsAuthenticationServers[0].hostname="148.93.49.176"'
ogcli update auth 'tacacsAuthenticationServers[0].port=49'
ogcli update auth 'tacacsAuthenticationServers[1].hostname="148.93.49.177"'
ogcli update auth 'tacacsAuthenticationServers[1].port=49'
ogcli update auth 'tacacsAuthenticationServers[2].hostname="130.172.129.176"'
ogcli update auth 'tacacsAuthenticationServers[2].port=49'
ogcli update auth 'tacacsAuthenticationServers[3].hostname="130.172.129.177"'
ogcli update auth 'tacacsAuthenticationServers[3].port=49'
ogcli update auth 'tacacsMethod="login"'
ogcli update auth 'tacacsPassword="pR1X1r4nwpFpVlNUV7yFBiKfw2Dr4ohWtzI3kk4CzTickH0VG0DhPD9bntxE6Vy"'
ogcli update auth 'tacacsService="raccess"'
ogcli update auth 'mode="tacacs"'
ogcli update system/cli_session_timeout 'timeout=20'
ogcli update system/webui_session_timeout 'timeout=20'
'''


lighthouse = '''
#==========================================
#---------- LIGHTHOUSE ----------------
#==========================================
#add only the first one it should add the second one. TEST this
#you only add the first one after firewall rules have been added.
#bundle names based on site: DC, Corp, MFG, CCA, Lab, Dev. Not DataCenter
#old token: 7ruwa8ONet7 (this one will be used)
#new token: GM1Lighthouse2Token  (this one will be retired)
#-------------------------------------------------------------------------
ogcli delete lighthouse_enrollment 10.233.249.68
#_------------------------------------------------------------------------
ogcli create lighthouse_enrollment <<'END'
address="10.233.249.68"
bundle="CCA"
port=443
token="7ruwa8ONet7"
END
#-------------------------------------------------------------------------
ogcli get lighthouse_enrollment 10.233.249.68
#-------------------------------------------------------------------------
ogcli delete lighthouse_enrollment 10.233.249.76
--------------------------------------------------------------------------
ogcli create lighthouse_enrollment <<'END'
address="10.233.249.76"
bundle="CCA"
port=443
token="7ruwa8ONet7"
END
#-------------------------------------------------------------------------
ogcli get lighthouse_enrollment 10.233.249.76
#-------------------------------------------------------------------------
'''

cdp_lldp = f'''
#----------------------------------------
#--------------- CDP/LLDP  ---------------------
#---------------------------------------------
#----------------------------------------------------
#on the new device, run ogcli get system/model_name
#---------------------------------------------------
ogcli update services/lldp << 'END'
enabled=true
physifs[0]="system_net_physifs-4"
END

#---------------------------------------------
#---------------CDP/LLDP System FIX  ----------
#----------------------------------------------
#!/bin/bash
platform_name=$(dmidecode -t System | grep "SKU Number" | cut -d ":" -f 2| tr -d '[:space:]')
kernel_info=$(uname -a)

#change the file name
mv /etc/lldpd.conf /etc/lldpd.conf.d
#
config_file="/etc/lldpd.conf"
#
echo configure system description \\'$kernel_info\\'>>"$config_file"
#
echo configure system platform \\'$platform_name\\'>>"$config_file"

#stop the lldp service
systemctl stop lldpd.service

#start the lldp service
systemctl start lldpd.service

#status
systemctl status lldpd.service
#-----------------------------------------------------------------------------------------------------

'''

'''----------------------------------------
---------------PEL  ---------------------
---------------------------------------------'''
serial_number = con.send_command('''setfset | grep "Serial number:" | awk '{print $3}' ''', read_timeout=180)
pel =f'''
=================================================
--------------------- PEL -----------------------
=================================================
with old, go to support report under Status
to get serial number: ogcli get system/serial_number

old opengear = "{serial_number}"
new opengear = 
'''



file = open("N:\\Report\\OG_config\\" +str(hostname[:3]) + " - config.txt", mode="a")

intro = f'''
--------- site name:  {site_name} \n
======================================
address: {hostname} \n
-------------------------------------
hostname: {router_1} \n
======================================\n\n
'''



file.write(intro)
file.write(syslog)
file.write(port_config)
file.write(cellular_enable)
file.write(oob_failover_probe)
file.write(tac)
file.write(lighthouse)
file.write(cdp_lldp)
file.write(pel)

'''
=================================================
---------- OLD SERIAL PORT CONFIG  --------------
================================================='''

port_config_list = []
for i in range(1,9):
    #if i == 1: #this is to change the port to console
    old_port_name = con.send_command("config -g config.ports.port"+str(i)+".label  | awk '{print $NF}' ", read_timeout=180)
    print(old_port_name)
    port_config_list.append(old_port_name)

file.write('''
=================================================
---------- NEW SERIAL PORT CONFIG  --------------
=================================================''')

#Add create a new port config
for i in range(len(port_config_list)):
    if i == 0:
        file.write(f'''
ogcli update port ports-{i+1} <<'END'
	mode="consoleServer"
	escape_char="~"
END
ogcli update port ports-{i+1} baudrate'="9600"' ''')

    if '003' in port_config_list[i] or '004' in port_config_list[i]: #this changes the speed of the device to 115200 to match viptela
        file.write(f'''
ogcli update port ports-{i+1} baudrate'="115200"' ''')
    file.write(f'''
ogcli update port ports-{i+1} label'="{port_config_list[i]}"'
ogcli update port ports-{i+1} logging_level'="eventsOnly"'
#------------------------------------------------------\n''')




file.close()









