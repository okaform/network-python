import nslookup
import sys
'''I am IMPORTING LIKE This because of the nature of the VDI not ening persistent. 
I am adding this directory to the python path so that python can find the library.'''
sys.path.append('N:/Python Libraries')
from pythonping import ping


def hostname(ip_ad):
    hostname = nslookup.nslookup(ip_ad)  
    return hostname[1]
    
    
    
def will_ping(ip_Ad):
      status = 0
      #we add the strip() because the user input takes data with a lot of space and causes issues.
      ping_req = ping(ip_Ad.strip(), verbose=False, count=1) #change this to the number of times you want to ping.
      # check the response..
      if ping_req.packets_lost == 0:
            status = "Up"
      else:
            status = "Down"
      return status