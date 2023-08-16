from special_commands import *
from vpn500_commands import *
from vpn200_commands import *


header_to_function_dict = {
    'csv-deviceIP': get_loopback0
    ,'csv-host-name': get_hostname
    ,'//snmp/contact': "GM GTSC (855)780-1125"
    ,'//snmp/location': get_snmp_location
    #VPN 500 static routes
    ,'/500/vpn-instance/ip/route/vpn500_ipv4_ip_prefix_1/prefix': get_vpn500_static_route("s",1)
    ,'/500/vpn-instance/ip/route/vpn500_ipv4_ip_prefix_2/prefix': get_vpn500_static_route("s",2)
    ,'/500/vpn-instance/ip/route/vpn500_ipv4_ip_prefix_3/prefix': get_vpn500_static_route("s",3)
    ,'/500/vpn-instance/ip/route/vpn500_ipv4_ip_prefix_4/prefix': get_vpn500_static_route("s",4)
    ,'/500/vpn-instance/ip/route/vpn500_ipv4_ip_prefix_5/prefix': get_vpn500_static_route("s",5)
    #VPN 500 next hop
    ,'/500/vpn-instance/ip/route/vpn500_ipv4_ip_prefix_1/next-hop/vpn500_next_hop_ip_address_1/address': get_vpn500_next_hop("n",1)
    ,'/500/vpn-instance/ip/route/vpn500_ipv4_ip_prefix_2/next-hop/vpn500_next_hop_ip_address_2/address': get_vpn500_next_hop("n",2)
    ,'/500/vpn-instance/ip/route/vpn500_ipv4_ip_prefix_3/next-hop/vpn500_next_hop_ip_address_3/address': get_vpn500_next_hop("n",3)
    ,'/500/vpn-instance/ip/route/vpn500_ipv4_ip_prefix_4/next-hop/vpn500_next_hop_ip_address_4/address': get_vpn500_next_hop("n",4)
    ,'/500/vpn-instance/ip/route/vpn500_ipv4_ip_prefix_5/next-hop/vpn500_next_hop_ip_address_5/address': get_vpn500_next_hop("n",5)
    #VPN 500 Aggregate
    ,'/500/vpn-instance/omp/advertise/aggregate/prefix-list/vpn500_aggregate_prefix_1/prefix-entry': get_vpn500_aggregate("a",1)
    ,'/500/vpn-instance/omp/advertise/aggregate/prefix-list/vpn500_aggregate_prefix_2/prefix-entry': get_vpn500_aggregate("a",2)
    ,'/500/vpn-instance/omp/advertise/aggregate/prefix-list/vpn500_aggregate_prefix_3/prefix-entry': get_vpn500_aggregate("a",3)
    ,'/500/vpn-instance/omp/advertise/aggregate/prefix-list/vpn500_aggregate_prefix_4/prefix-entry': get_vpn500_aggregate("a",4)
    ,'/500/vpn-instance/omp/advertise/aggregate/prefix-list/vpn500_aggregate_prefix_5/prefix-entry': get_vpn500_aggregate("a",5)   
    #VPN 500 int gi0/0/0.358
    ,'/500/GigabitEthernet0/0/0.358/interface/ip/address': get_000_358_ip_address
    ,'/500/GigabitEthernet0/0/0.358/interface/dhcp-helper': get_000_358_dhcp_helper
    ,'/500/GigabitEthernet0/0/0.358/interface/shutdown': get_000_358_shutdown
    ,'/500/GigabitEthernet0/0/0.358/interface/vrrp/35/ipv4/address': get_000_358_vrrp
    #VPN 500 int gi0/0/0.25    
    ,'/500/GigabitEthernet0/0/0.25/interface/description': get_000_25_description
    ,'/500/GigabitEthernet0/0/0.25/interface/ip/address': get_000_25_ip_address
    ,'/500/GigabitEthernet0/0/0.25/interface/shutdown': get_000_25_shutdown
    ,'/500/GigabitEthernet0/0/0.25/interface/vrrp/25/ipv4/address': get_000_25_vrrp    
    #VPN 500 router_id
    ,'/500//router/ospf/router-id': get_vpn500_ospf_id    
    #VPN 200 static routes
    ,'/200/vpn-instance/ip/route/vpn200_ipv4_ip_prefix_1/prefix': get_vpn200_static_route("s",1)
    ,'/200/vpn-instance/ip/route/vpn200_ipv4_ip_prefix_2/prefix': get_vpn200_static_route("s",2)
    ,'/200/vpn-instance/ip/route/vpn200_ipv4_ip_prefix_3/prefix': get_vpn200_static_route("s",3)
    ,'/200/vpn-instance/ip/route/vpn200_ipv4_ip_prefix_4/prefix': get_vpn200_static_route("s",4)
    ,'/200/vpn-instance/ip/route/vpn200_ipv4_ip_prefix_5/prefix': get_vpn200_static_route("s",5)
    ,'/200/vpn-instance/ip/route/vpn200_ipv4_ip_prefix_6/prefix': get_vpn200_static_route("s",6)
    ,'/200/vpn-instance/ip/route/vpn200_ipv4_ip_prefix_7/prefix': get_vpn200_static_route("s",7)
    ,'/200/vpn-instance/ip/route/vpn200_ipv4_ip_prefix_8/prefix': get_vpn200_static_route("s",8)
    ,'/200/vpn-instance/ip/route/vpn200_ipv4_ip_prefix_9/prefix': get_vpn200_static_route("s",9)
    ,'/200/vpn-instance/ip/route/vpn200_ipv4_ip_prefix_10/prefix': get_vpn200_static_route("s",10)
    ,'/200/vpn-instance/ip/route/vpn200_ipv4_ip_prefix_11/prefix': get_vpn200_static_route("s",11)
    ,'/200/vpn-instance/ip/route/vpn200_ipv4_ip_prefix_12/prefix': get_vpn200_static_route("s",12)
    ,'/200/vpn-instance/ip/route/vpn200_ipv4_ip_prefix_13/prefix': get_vpn200_static_route("s",13)
    ,'/200/vpn-instance/ip/route/vpn200_ipv4_ip_prefix_14/prefix': get_vpn200_static_route("s",14)
    ,'/200/vpn-instance/ip/route/vpn200_ipv4_ip_prefix_15/prefix': get_vpn200_static_route("s",15)
    #VPN 200 next hop
    ,'/200/vpn-instance/ip/route/vpn200_ipv4_ip_prefix_1/next-hop/vpn200_next_hop_ip_address_1/address': get_vpn200_next_hop("n",1)
    ,'/200/vpn-instance/ip/route/vpn200_ipv4_ip_prefix_2/next-hop/vpn200_next_hop_ip_address_2/address': get_vpn200_next_hop("n",2)
    ,'/200/vpn-instance/ip/route/vpn200_ipv4_ip_prefix_3/next-hop/vpn200_next_hop_ip_address_3/address': get_vpn200_next_hop("n",3)
    ,'/200/vpn-instance/ip/route/vpn200_ipv4_ip_prefix_4/next-hop/vpn200_next_hop_ip_address_4/address': get_vpn200_next_hop("n",4)
    ,'/200/vpn-instance/ip/route/vpn200_ipv4_ip_prefix_5/next-hop/vpn200_next_hop_ip_address_5/address': get_vpn200_next_hop("n",5)
    ,'/200/vpn-instance/ip/route/vpn200_ipv4_ip_prefix_6/next-hop/vpn200_next_hop_ip_address_6/address': get_vpn200_next_hop("n",6)
    ,'/200/vpn-instance/ip/route/vpn200_ipv4_ip_prefix_7/next-hop/vpn200_next_hop_ip_address_7/address': get_vpn200_next_hop("n",7)
    ,'/200/vpn-instance/ip/route/vpn200_ipv4_ip_prefix_8/next-hop/vpn200_next_hop_ip_address_8/address': get_vpn200_next_hop("n",8)
    ,'/200/vpn-instance/ip/route/vpn200_ipv4_ip_prefix_9/next-hop/vpn200_next_hop_ip_address_9/address': get_vpn200_next_hop("n",9)
    ,'/200/vpn-instance/ip/route/vpn200_ipv4_ip_prefix_10/next-hop/vpn200_next_hop_ip_address_10/address': get_vpn200_next_hop("n",10)
    ,'/200/vpn-instance/ip/route/vpn200_ipv4_ip_prefix_11/next-hop/vpn200_next_hop_ip_address_11/address': get_vpn200_next_hop("n",11)
    ,'/200/vpn-instance/ip/route/vpn200_ipv4_ip_prefix_12/next-hop/vpn200_next_hop_ip_address_12/address': get_vpn200_next_hop("n",12)
    ,'/200/vpn-instance/ip/route/vpn200_ipv4_ip_prefix_13/next-hop/vpn200_next_hop_ip_address_13/address': get_vpn200_next_hop("n",13)
    ,'/200/vpn-instance/ip/route/vpn200_ipv4_ip_prefix_14/next-hop/vpn200_next_hop_ip_address_14/address': get_vpn200_next_hop("n",14)
    ,'/200/vpn-instance/ip/route/vpn200_ipv4_ip_prefix_15/next-hop/vpn200_next_hop_ip_address_15/address': get_vpn200_next_hop("n",15)    
    #VPN 200 int gi0/0/0.212
    ,'/200/GigabitEthernet0/0/0.212/interface/description': get_000_212_description
    ,'/200/GigabitEthernet0/0/0.212/interface/ip/address': get_000_212_ip_address
    ,'/200/GigabitEthernet0/0/0.212/interface/shutdown': get_000_212_shutdown
    ,'/200/GigabitEthernet0/0/0.212/interface/vrrp/212/ipv4/address': get_000_212_vrrp
    
    
    
    
    
}

'''










    #VPN 10 static routes
    ,'/10/vpn-instance/ip/route/vpn10_ipv4_ip_route_prefix_1/prefix': (get_vpn10_static_routes, "1")
    ,'/10/vpn-instance/ip/route/vpn10_ipv4_ip_route_prefix_2/prefix': (get_vpn10_static_routes, "2")
    ,'/10/vpn-instance/ip/route/vpn10_ipv4_ip_route_prefix_3/prefix': (get_vpn10_static_routes, "3")
    ,'/10/vpn-instance/ip/route/vpn10_ipv4_ip_route_prefix_4/prefix': (get_vpn10_static_routes, "4")
    ,'/10/vpn-instance/ip/route/vpn10_ipv4_ip_route_prefix_5/prefix': (get_vpn10_static_routes, "5")
    ,'/10/vpn-instance/ip/route/vpn10_ipv4_ip_route_prefix_6/prefix': (get_vpn10_static_routes, "6")
    ,'/10/vpn-instance/ip/route/vpn10_ipv4_ip_route_prefix_7/prefix': (get_vpn10_static_routes, "7")
    ,'/10/vpn-instance/ip/route/vpn10_ipv4_ip_route_prefix_8/prefix': (get_vpn10_static_routes, "8")
    ,'/10/vpn-instance/ip/route/vpn10_ipv4_ip_route_prefix_9/prefix': (get_vpn10_static_routes, "9")
    ,'/10/vpn-instance/ip/route/vpn10_ipv4_ip_route_prefix_10/prefix': (get_vpn10_static_routes, "10")
    ,'/10/vpn-instance/ip/route/vpn10_ipv4_ip_route_prefix_11/prefix': (get_vpn10_static_routes, "11")
    ,'/10/vpn-instance/ip/route/vpn10_ipv4_ip_route_prefix_12/prefix': (get_vpn10_static_routes, "12")
    ,'/10/vpn-instance/ip/route/vpn10_ipv4_ip_route_prefix_13/prefix': (get_vpn10_static_routes, "13")
    ,'/10/vpn-instance/ip/route/vpn10_ipv4_ip_route_prefix_14/prefix': (get_vpn10_static_routes, "14")
    ,'/10/vpn-instance/ip/route/vpn10_ipv4_ip_route_prefix_15/prefix': (get_vpn10_static_routes, "15")
    ,'/10/vpn-instance/ip/route/vpn10_ipv4_ip_route_prefix_16/prefix': (get_vpn10_static_routes, "16")
    ,'/10/vpn-instance/ip/route/vpn10_ipv4_ip_route_prefix_17/prefix': (get_vpn10_static_routes, "17")
    ,'/10/vpn-instance/ip/route/vpn10_ipv4_ip_route_prefix_18/prefix': (get_vpn10_static_routes, "18")
    ,'/10/vpn-instance/ip/route/vpn10_ipv4_ip_route_prefix_19/prefix': (get_vpn10_static_routes, "19")
    ,'/10/vpn-instance/ip/route/vpn10_ipv4_ip_route_prefix_20/prefix': (get_vpn10_static_routes, "20")
    #VPN 10 next hop
    ,'/10/vpn-instance/ip/route/vpn10_ipv4_ip_route_prefix_1/next-hop/vpn_next_hop_ip_address_1/address': (get_vpn10_next_hop, "1")
    ,'/10/vpn-instance/ip/route/vpn10_ipv4_ip_route_prefix_2/next-hop/vpn_next_hop_ip_address_2/address': (get_vpn10_next_hop, "2")
    ,'/10/vpn-instance/ip/route/vpn10_ipv4_ip_route_prefix_3/next-hop/vpn_next_hop_ip_address_3/address': (get_vpn10_next_hop, "3")
    ,'/10/vpn-instance/ip/route/vpn10_ipv4_ip_route_prefix_4/next-hop/vpn_next_hop_ip_address_4/address': (get_vpn10_next_hop, "4")
    ,'/10/vpn-instance/ip/route/vpn10_ipv4_ip_route_prefix_5/next-hop/vpn_next_hop_ip_address_5/address': (get_vpn10_next_hop, "5")
    ,'/10/vpn-instance/ip/route/vpn10_ipv4_ip_route_prefix_6/next-hop/vpn_next_hop_ip_address_6/address': (get_vpn10_next_hop, "6")
    ,'/10/vpn-instance/ip/route/vpn10_ipv4_ip_route_prefix_7/next-hop/vpn_next_hop_ip_address_7/address': (get_vpn10_next_hop, "7")
    ,'/10/vpn-instance/ip/route/vpn10_ipv4_ip_route_prefix_8/next-hop/vpn_next_hop_ip_address_8/address': (get_vpn10_next_hop, "8")
    ,'/10/vpn-instance/ip/route/vpn10_ipv4_ip_route_prefix_9/next-hop/vpn_next_hop_ip_address_9/address': (get_vpn10_next_hop, "9")
    ,'/10/vpn-instance/ip/route/vpn10_ipv4_ip_route_prefix_10/next-hop/vpn_next_hop_ip_address_10/address': (get_vpn10_next_hop, "10")
    ,'/10/vpn-instance/ip/route/vpn10_ipv4_ip_route_prefix_11/next-hop/vpn_next_hop_ip_address_11/address': (get_vpn10_next_hop, "11")
    ,'/10/vpn-instance/ip/route/vpn10_ipv4_ip_route_prefix_12/next-hop/vpn_next_hop_ip_address_12/address': (get_vpn10_next_hop, "12")
    ,'/10/vpn-instance/ip/route/vpn10_ipv4_ip_route_prefix_13/next-hop/vpn_next_hop_ip_address_13/address': (get_vpn10_next_hop, "13")
    ,'/10/vpn-instance/ip/route/vpn10_ipv4_ip_route_prefix_14/next-hop/vpn_next_hop_ip_address_14/address': (get_vpn10_next_hop, "14")
    ,'/10/vpn-instance/ip/route/vpn10_ipv4_ip_route_prefix_15/next-hop/vpn_next_hop_ip_address_15/address': (get_vpn10_next_hop, "15")
    ,'/10/vpn-instance/ip/route/vpn10_ipv4_ip_route_prefix_16/next-hop/vpn_next_hop_ip_address_16/address': (get_vpn10_next_hop, "16")
    ,'/10/vpn-instance/ip/route/vpn10_ipv4_ip_route_prefix_17/next-hop/vpn_next_hop_ip_address_17/address': (get_vpn10_next_hop, "17")
    ,'/10/vpn-instance/ip/route/vpn10_ipv4_ip_route_prefix_18/next-hop/vpn_next_hop_ip_address_18/address': (get_vpn10_next_hop, "18")
    ,'/10/vpn-instance/ip/route/vpn10_ipv4_ip_route_prefix_19/next-hop/vpn_next_hop_ip_address_19/address': (get_vpn10_next_hop, "19")
    ,'/10/vpn-instance/ip/route/vpn10_ipv4_ip_route_prefix_20/next-hop/vpn_next_hop_ip_address_20/address': (get_vpn10_next_hop, "20")
    #VPN 10 Aggregate
    ,'/10/vpn-instance/omp/advertise/aggregate/prefix-list/vpn10_omp_aggregate_aggregate_prefix-1/prefix-entry': (get_vpn10_aggregate, "1")
    ,'/10/vpn-instance/omp/advertise/aggregate/prefix-list/vpn10_omp_aggregate_aggregate_prefix-2/prefix-entry': (get_vpn10_aggregate, "2")
    ,'/10/vpn-instance/omp/advertise/aggregate/prefix-list/vpn10_omp_aggregate_aggregate_prefix-3/prefix-entry': (get_vpn10_aggregate, "3")
    ,'/10/vpn-instance/omp/advertise/aggregate/prefix-list/vpn10_omp_aggregate_aggregate_prefix-4/prefix-entry': (get_vpn10_aggregate, "4")
    ,'/10/vpn-instance/omp/advertise/aggregate/prefix-list/vpn10_omp_aggregate_aggregate_prefix-5/prefix-entry': (get_vpn10_aggregate, "5")
    ,'/10/vpn-instance/omp/advertise/aggregate/prefix-list/vpn10_omp_aggregate_aggregate_prefix-6/prefix-entry': (get_vpn10_aggregate, "6")
    ,'/10/vpn-instance/omp/advertise/aggregate/prefix-list/vpn10_omp_aggregate_aggregate_prefix-7/prefix-entry': (get_vpn10_aggregate, "7")
    ,'/10/vpn-instance/omp/advertise/aggregate/prefix-list/vpn10_omp_aggregate_aggregate_prefix-8/prefix-entry': (get_vpn10_aggregate, "8")
    ,'/10/vpn-instance/omp/advertise/aggregate/prefix-list/vpn10_omp_aggregate_aggregate_prefix-9/prefix-entry': (get_vpn10_aggregate, "9")
    ,'/10/vpn-instance/omp/advertise/aggregate/prefix-list/vpn10_omp_aggregate_aggregate_prefix-10/prefix-entry': (get_vpn10_aggregate, "10")
    ,'/10/vpn-instance/omp/advertise/aggregate/prefix-list/vpn10_omp_aggregate_aggregate_prefix-11/prefix-entry': (get_vpn10_aggregate, "11")
    ,'/10/vpn-instance/omp/advertise/aggregate/prefix-list/vpn10_omp_aggregate_aggregate_prefix-12/prefix-entry': (get_vpn10_aggregate, "12")
    ,'/10/vpn-instance/omp/advertise/aggregate/prefix-list/vpn10_omp_aggregate_aggregate_prefix-13/prefix-entry': (get_vpn10_aggregate, "13")
    ,'/10/vpn-instance/omp/advertise/aggregate/prefix-list/vpn10_omp_aggregate_aggregate_prefix-14/prefix-entry': (get_vpn10_aggregate, "14")
    ,'/10/vpn-instance/omp/advertise/aggregate/prefix-list/vpn10_omp_aggregate_aggregate_prefix-15/prefix-entry': (get_vpn10_aggregate, "15")
    ,'/10/vpn-instance/omp/advertise/aggregate/prefix-list/vpn10_omp_aggregate_aggregate_prefix-16/prefix-entry': (get_vpn10_aggregate, "16")
    ,'/10/vpn-instance/omp/advertise/aggregate/prefix-list/vpn10_omp_aggregate_aggregate_prefix-17/prefix-entry': (get_vpn10_aggregate, "17")
    ,'/10/vpn-instance/omp/advertise/aggregate/prefix-list/vpn10_omp_aggregate_aggregate_prefix-18/prefix-entry': (get_vpn10_aggregate, "18")
    ,'/10/vpn-instance/omp/advertise/aggregate/prefix-list/vpn10_omp_aggregate_aggregate_prefix-19/prefix-entry': (get_vpn10_aggregate, "19")
    ,'/10/vpn-instance/omp/advertise/aggregate/prefix-list/vpn10_omp_aggregate_aggregate_prefix-20/prefix-entry': (get_vpn10_aggregate, "20")
    #VPN 10 int gi0/0/0.658
    ,'/10/GigabitEthernet0/0/0.658/interface/description': get_000_658_description
    ,'/10/GigabitEthernet0/0/0.658/interface/ip/address': get_000_658_ip_address
    ,'/10/GigabitEthernet0/0/0.658/interface/shutdown': get_000_658_shutdown
    ,'/10/GigabitEthernet0/0/0.658/interface/vrrp/58/ipv4/address': get_000_658_vrrp  
    #VPN 10 int gi0/0/0.20
    ,'/10/GigabitEthernet0/0/0.20/interface/ip/address': get_000_20_ip_address
    ,'/10/GigabitEthernet0/0/0.20/interface/shutdown': get_000_20_shutdown
    #VPN 10 int gi0/0/0.659
    ,'/10/GigabitEthernet0/0/0.659/interface/description': get_000_659_description
    ,'/10/GigabitEthernet0/0/0.659/interface/ip/address': get_000_659_ip_address
    ,'/10/GigabitEthernet0/0/0.659/interface/shutdown': get_000_659_shutdown
    #Loopback
    ,'/10/Loopback0/interface/ip/address': get_loopback0
    #VPN 10 int gi0/0/0.202
    ,'/10/GigabitEthernet0/0/0.202/interface/description': get_000_202_description
    ,'/10/GigabitEthernet0/0/0.202/interface/ip/address': get_000_202_ip_address
    ,'/10/GigabitEthernet0/0/0.202/interface/shutdown': get_000_202_shutdown
    ,'/10/GigabitEthernet0/0/0.202/interface/vrrp/58/ipv4/address': get_000_202_vrrp
    #VPN 10 router_id
    ,'/10//router/ospf/router-id' : get_vpn10_ospf_id
    #VPN 0 static route
    ,'/0/vpn-instance/ip/route/m1_ip_prefix_default/prefix': '0.0.0.0/0'
    ,'/0/vpn-instance/ip/route/m2_ip_prefix_default/prefix': '0.0.0.0/0'
    ,'/0/vpn-instance/ip/route/i1_ip_prefix_default/prefix': '0.0.0.0/0'
    ,'/0/vpn-instance/ip/route/i2_ip_prefix_default/prefix': '0.0.0.0/0'
    ,'/0/vpn-instance/ip/route/i3_ip_prefix_default/prefix': '0.0.0.0/0'
    ,'/0/vpn-instance/ip/route/lte_ip_prefix_default/prefix': '0.0.0.0/0'
    #VPN 0 next hop
    ,'/0/vpn-instance/ip/route/m1_ip_prefix_default/next-hop/m1_next_hop_ip_address_0/address': get_m1_next_hop
    ,'/0/vpn-instance/ip/route/m2_ip_prefix_default/next-hop/m2_next_hop_ip_address_0/address': get_m2_next_hop
    ,'/0/vpn-instance/ip/route/i1_ip_prefix_default/next-hop/i1_next_hop_ip_address_0/address': get_i1_next_hop
    ,'/0/vpn-instance/ip/route/i2_ip_prefix_default/next-hop/i2_next_hop_ip_address_0/address': get_i2_next_hop
    ,'/0/vpn-instance/ip/route/i3_ip_prefix_default/next-hop/i3_next_hop_ip_address_0/address': get_i3_next_hop
    ,'/0/vpn-instance/ip/route/lte_ip_prefix_default/next-hop/lte_next_hop_ip_address_0/address': get_lte_next_hop
    #VPN 0 int gi0/0/2
    ,'/0/GigabitEthernet0/0/2/interface/description': get_002_description
    ,'/0/GigabitEthernet0/0/2/interface/ip/address': get_002_ip_address
    ,'/0/GigabitEthernet0/0/2/interface/shutdown': get_002_shutdown
    ,'/0/GigabitEthernet0/0/2/interface/autonegotiate': get_002_autonegotiate
    ,'/0/GigabitEthernet0/0/2/interface/shaping-rate': get_002_shaping_rate
    ,'/0/GigabitEthernet0/0/2/interface/bandwidth-upstream': get_002_bandwidth_upstream
    ,'/0/GigabitEthernet0/0/2/interface/bandwidth-downstream': get_002_bandwidth_downstream
    #VPN 0 int gi0/0/1
    ,'/0/GigabitEthernet0/0/1/interface/shutdown': "FALSE"
    #VPN 0 int te0/0/4
    ,'/0/TenGigabitEthernet0/0/4.100/interface/description': get_004_100_description
    ,'/0/TenGigabitEthernet0/0/4.100/interface/ip/address': get_004_100_ip_address
    ,'/0/TenGigabitEthernet0/0/4.100/interface/shutdown': get_004_100_shutdown
    ,'/0/TenGigabitEthernet0/0/4.100/interface/bandwidth-upstream': get_004_100_bandwidth_upstream
    ,'/0/TenGigabitEthernet0/0/4.100/interface/bandwidth-downstream': get_004_100_bandwidth_downstream
    ,'/0/TenGigabitEthernet0/0/4/interface/description': get_004_description
    ,'/0/TenGigabitEthernet0/0/4/interface/ip/address': get_004_ip_address
    ,'/0/TenGigabitEthernet0/0/4/interface/shutdown': get_004_shutdown
    ,'/0/TenGigabitEthernet0/0/4/interface/autonegotiate': get_004_autonegotiate
    ,'/0/TenGigabitEthernet0/0/4/interface/shaping-rate': get_004_shaping_rate
    ,'/0/TenGigabitEthernet0/0/4/interface/bandwidth-upstream': get_004_bandwidth_upstream
    ,'/0/TenGigabitEthernet0/0/4/interface/bandwidth-downstream': get_004_bandwidth_downstream
    #VPN 0 TLOC interface 
    ,'/0/GigabitEthernet0/0/1.59/interface/ip/address': get_001_59_ip_address
    ,'/0/GigabitEthernet0/0/1.59/interface/shutdown': get_001_59_shutdown
    ,'/0/GigabitEthernet0/0/1.52/interface/ip/address': get_001_52_ip_address
    ,'/0/GigabitEthernet0/0/1.52/interface/shutdown': get_001_52_shutdown
    ,'/0/GigabitEthernet0/0/1.51/interface/ip/address': get_001_51_ip_address
    ,'/0/GigabitEthernet0/0/1.51/interface/shutdown': get_001_51_shutdown
    ,'/0/GigabitEthernet0/0/1.50/interface/ip/address': get_001_50_ip_address
    ,'/0/GigabitEthernet0/0/1.50/interface/shutdown': get_001_50_shutdown
    ,'/0/GigabitEthernet0/0/1.10/interface/ip/address': get_001_10_ip_address
    ,'/0/GigabitEthernet0/0/1.10/interface/shutdown': get_001_10_shutdown
    #VPN 0 gi0/0/0
    ,'/0/GigabitEthernet0/0/0/interface/shutdown': "FALSE"
    #BGP
    ,'/0//router/bgp/as-num': get_bgp_as_num
    ,'/0//router/bgp/shutdown': get_bgp_shutdown
    ,'/0//router/bgp/address-family/ipv4-unicast/network/MPLS_carrier_network_address_prefix/prefix': get_bgp_net_address
    ,'/0//router/bgp/address-family/ipv4-unicast/network/MPLS_TLOC_network_address_prefix/prefix': get_bgp_tloc_address
    ,'/0//router/bgp/neighbor/bgp_neighbor_address_0/address': get_bgp_neighbor_address
    ,'/0//router/bgp/neighbor/bgp_neighbor_address_0/shutdown': get_bgp_neighbor_shutdown
    ,'/0//router/bgp/neighbor/bgp_neighbor_address_0/remote-as': get_bgp_neighbor_remote_as
    #FINAL STUFF
    ,'//system/host-name': get_hostname
    ,'//system/gps-location/latitude': get_latitude
    ,'//system/gps-location/longitude': get_longitude
    ,'//system/system-ip': get_loopback0
    ,'//system/site-id': get_site_id
    
'''