#!/usr/bin/env python

# Parameter should be dictionary
# ip_address - is mandatory, others are optional
# Posiible parameters are: ip_address, interface, existence, type, next_hop
# Example:
# {'ip_address':'123.51.51.51','type':'connected','interface':'FastEthernet0/0'}

from __init__ import *

def test_func(host,conditions_dict):
  type_dict={"S":"static","C":"connected","R":"rip","O":"ospf","I":"igrp","E":"eigrp"}
  if conditions_dict.has_key("type"):
    conditions_dict["type"]=conditions_dict["type"][0].upper()
  if conditions_dict.has_key("existence"):
    conditions_dict["existence"]=conditions_dict["existence"].lower()
  RT=RouteTable(host)
  real_dict=route_to_ip_all_parametres(RT,conditions_dict['ip_address'])
  if real_dict['existence']=='false':
    if conditions_dict.has_key('existence'):
      if conditions_dict['existence']=="false":
        return True
      else:
        return "Route to specified address doesn't exist"
    else:
      return "Route to specified address doesn't exist"
  if conditions_dict.has_key('existence'):
    if real_dict['existence'] != conditions_dict['existence']:
      if real_dict['existence']:
        return "Route to "+str(conditions_dict['ip_address'])+" exists."
      else:
        return "Route to "+str(conditions_dict['ip_address'])+" doesn't exist."
  for key in conditions_dict.keys():
    if conditions_dict[key] != real_dict[key]:
      if key=="type":
        return "The specified type is "+type_dict[str(conditions_dict[key])]+", but real is "+type_dict[str(real_dict[key])]+"."
      else:
        return "The specified "+str(key)+" is "+str(conditions_dict[key])+", but real is "+str(real_dict[key])+"."
  return True



# Sorting routing table by netmask from narrow to wide
def rt_sort(RT):
  from operator import itemgetter, attrgetter
  return sorted(RT, key=itemgetter(2), reverse=True)
  
def ipconvert(IPaddress):  #converts string to digit
  a=IPaddress.split('.')
  try:
    a=[int(a[i]) for i in range(4)]
    if (len(a)==4) and (max(a)<256) and (min(a)>=0):
      return (a[0]*256*256*256+a[1]*256*256+a[2]*256+a[3])
    else:
      raise ValueError
  except ValueError:
    print 'Can not understand IP adress: '+IPaddress
    return -1

def unconvertip(intip):  #converts digit to string
  x=intip
  a=[1,2,3,4]
  for i in range(4):
    a[3-i]=(x%256)
    x=x/256
  return str(a[0])+'.'+str(a[1])+'.'+str(a[2])+'.'+str(a[3])

def ifmask(maskaddress): #Checks if mask is valid, returns prefix
  if maskaddress==0:
    return 0
  m=maskaddress
  i=0
  while not(m%2):
    m=m/2
    i+=1
  if m==(2**(32-i))-1:
    return 32-i
  else:
    return None

def maskif(prefix):
  prefix=int(prefix)
  return 2**33-2**(32-prefix)

def netaddress(ipaddress, maskaddress):
  return ipaddress & maskaddress

def addr_in_net(ip_addr,net_addr,netmask):
  if netaddress(ip_addr, netmask) == net_addr:
    return True
  else:
    return False

# Retrieving all parametres of route to specified address
def route_to_ip_all_parametres(RT,ip_addr):
  rt=rt_sort(RT)
  for route in rt:
    ip=ipconvert(ip_addr)
    net_addr=ipconvert(route[1])
    netmask=maskif(route[2])
    if addr_in_net(ip,net_addr,netmask):
      return {'ip_address':ip_addr,'interface':route[4],'type':route[0],'next-hop':route[3],'existence':'true'}
  return {'existence':'false'}

