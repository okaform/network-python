'''This file will not have any connection to the routers.'''
subnet_to_cidr = {
    '255.255.255.255': "32",
    '255.255.255.254': "31",
    '255.255.255.252': "30",
    '255.255.255.248': "29",
    '255.255.255.240': "28",
    '255.255.255.224': "27",
    '255.255.255.192': "26",
    '255.255.255.128': "25",
    '255.255.255.0': "24",
    '255.255.254.0': "23",
    '255.255.252.0': "22",
    '255.255.248.0': "21",
    '255.255.240.0': "20",
    '255.255.224.0': "19",
    '255.255.192.0': "18",
    '255.255.128.0': "17",
    '255.255.0.0': "16",
    '255.254.0.0': "15",
    '255.252.0.0': "14",
    '255.248.0.0': "13",
    '255.240.0.0': "12",
    '255.224.0.0': "11",
    '255.192.0.0': "10",
    '255.128.0.0': "9",
    '255.0.0.0': "8",
    '254.0.0.0': "7",
    '252.0.0.0': "6",
    '248.0.0.0': "5",
    '240.0.0.0': "4",
    '224.0.0.0': "3",
    '192.0.0.0': "2",
    '128.0.0.0': "1",
}

#This function returns the corresponding cidr notation from the subnet mask
def convert_to_cidr(subnet_mask): 
    return subnet_to_cidr.get(subnet_mask, "CIDR NOT FOUND")

def subtract_one_from_ipv4(ipv4_address):
    octets = ipv4_address.split('.')
    last_octet = int(octets[-1]) #get the last octet and convert to int
    new_last_octet = max(last_octet - 1, 0) #ensure we don't get a negative number
    octets[-1] = str(new_last_octet)
    new_ipv4_address = '.'.join(octets)
    return new_ipv4_address


def add_one_from_ipv4(ipv4_address):
    octets = ipv4_address.split('.')
    last_octet = int(octets[-1]) #get the last octet and convert to int
    new_last_octet = max(last_octet + 1, 0) #ensure we don't get a negative number
    octets[-1] = str(new_last_octet)
    new_ipv4_address = '.'.join(octets)
    return new_ipv4_address