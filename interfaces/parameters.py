#!/usr/bin/env python

# Parameter should be a dictionary
# Availible options are:
# {"interface_name","ip_address","netmask","assigned","state"}
# Ex: {"interface_name":"FastEthernet0/0","ip_address":"192.168.1.21",
# "netmask":"255.255.255.0","assigned":"DHCP","state":"UP"}

from __init__ import *

def test_func(host,test_params):
  IT=InterfaceTable(host)
  params={"interface_name":0,"ip_address":1,"netmask":2,"assigned":3,"state":4}
  for i in test_params.keys():
    if i not in params.keys():
      return "Unknown parameter %s" % i
  if not is_number(test_params["netmask"]):
    test_params["netmask"]=int(str(ifmask(ipconvert(test_params["netmask"]))))
  diff_len=100
  for line in IT:
    real_params=dict([(param,element) for param in params.keys() for element in line if params[param]==line.index(element)])
    difference=dict_diff(test_params,real_params)
    if difference=={} :
      return True
    elif len(difference)<diff_len:
      diff_len=len(difference)
      best_fit=difference
  return "Specified parameters differ from real: "+str(best_fit)

def dict_diff(first, second):
    diff = {}
    # Check all keys in first dict
    for key in first.keys():
        if second.has_key(key):
          if first[key] != second[key]:
            diff[key] = (first[key], second[key])
    return diff

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
    return "Invalid specified mask"

def ipconvert(IPaddress):  #converts string to digit
  a=IPaddress.split('.')
  try:
    a=[int(a[i]) for i in range(4)]
    if (len(a)==4) and (max(a)<256) and (min(a)>=0):
      return (a[0]*256*256*256+a[1]*256*256+a[2]*256+a[3])
    else:
      raise ValueError
  except ValueError:
    return 'Invalid mask '+IPaddress

def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
