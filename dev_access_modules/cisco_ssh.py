#!/usr/bin/env python

import paramiko
import re

def ipconvert(IPaddress):  #converts string to digit
    a=IPaddress.split('.')
    try:
        a=[int(a[i]) for i in range(4)]
        if (len(a)==4) and (max(a)<256) and (min(a)>=0):
            return (a[0]*256*256*256+a[1]*256*256+a[2]*256+a[3])
        else:
            raise ValueError
    except ValueError:
       # print 'Can not understand IP adress: '+IPaddress
        return -1

def uniq(inlist):
    uniques = []
    for item in inlist:
        if item not in uniques:
            uniques.append(item)
    return uniques


def getoutput(hostname,creds,cmd):
  ssh=paramiko.SSHClient()
  ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
  login = creds["login"]
  password = creds["password"]
  print "%s === %s" % (login, password)
  print len(login)
  print len(password)
  ssh.connect(hostname, username=login, password=password, timeout =  30)
  #terminal length 0 ; to disable paging 
  #ssh.exec_command("terminal length 0")
  stdin, stdout, stderr = ssh.exec_command(cmd)
  output=stdout.read()
  ssh.close()
  return output

r_prefixes={"C ":"C","S ":"S","R ":"R","M ":"M","B ":"B","D ":"E","D EX":"E","O ":"O","O IA":"O","O N1":"O","O N2":"O","O E1":"O","O E2":"O"}
ip_regexp='(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})'

def parsse(string,prfx,mask):
  route=[]
  route.append(r_prefixes[prfx])
  ips=re.findall(ip_regexp,string)
  route.append(ips[0])
  if string.split(ips[0])[1][0]=="/":
    mask=string.split(ips[0])[1][1:3]
  mask=mask.rstrip()
  route.append(mask)
  if len(ips)>1:
    route.append(ips[1])
  else:
    route.append("self")
  #if r_prefixes[prfx]=="S":
  #  route.append("STATIC")
  #else:
  route.append(string.split()[-1])
  return route

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

def get_routing_table(hostname,creds):
  mask=""
  r_table=[]
  a=getoutput(hostname,creds,"show ip route")
  table=a.splitlines()[11:]
  for line in table:
    if "subnetted" in line:
      mask=line.split(re.findall(ip_regexp,line)[0])[1][1:3]
    for prfx in r_prefixes.keys():
      if line.startswith(prfx) or line.startswith(prfx[0]+"*"+prfx[2:]):
        route=parsse(line,prfx,mask)
        r_table.append(route)
  #* routes appear twice in routing table
  r_table=uniq(r_table)
  c_r_table=[x for x in r_table if x[0]=='C']
  s_r_table=[x for x in r_table if x[0]=='S']
  for route in r_table:
    if route[0]=='S' and route[3]!='self':
      next_hop_ip=route[3]
      for croute in c_r_table:
        if addr_in_net(ipconvert(next_hop_ip),ipconvert(croute[1]),maskif(croute[2])):
          route[4]=croute[4]
  return r_table


def get_interfaces(hostname,creds):
  interfaces=[]
  a=getoutput(hostname,creds,"show ip interface brief")
  table=a.splitlines()[2:]
  for line in table:
    lst=line.split()
    if ipconvert(lst[1])==-1:
      interfaces.append(lst[0:2]+["-"]+lst[3:4]+lst[-1:])
    else:
      # getting netmask with another cmd
      b=getoutput(hostname,creds,"show ip interface "+lst[0]).splitlines()
      i=0
      addr_line=""
      while addr_line=="":
        if "Internet address is" in b[i]:
          addr_line=b[i]
        i=i+1
      mask=addr_line.split("/")[1]
      interfaces.append(lst[0:2]+[mask]+lst[3:4]+lst[-1:])
  return interfaces

def ping_test(hostname,creds,host):
  a=getoutput(hostname,creds,"ping ip "+host)
  ping_result=a.splitlines()[-1]
  #print ping_result
  if ping_result.split()[0]=="Success":
    if int(ping_result.split()[3])>0:
      return 0
    else:
      return 1
  else:
    return 2

