#!/usr/bin/env python

from pysnmp.entity.rfc3413.oneliner import cmdgen  

snmp_dict=dict([("ipAdEntAddr","1.3.6.1.2.1.4.20.1.1"),
 ("ipAdEntIfIndex","1.3.6.1.2.1.4.20.1.2"),
 ("ipAdEntNetMask","1.3.6.1.2.1.4.20.1.3"),
 ("ipAdEntBcastAddr","1.3.6.1.2.1.4.20.1.4"),
 ("ipAdEntReasmMaxSize","1.3.6.1.2.1.4.20.1.5"),
 ("ipRouteDest","1.3.6.1.2.1.4.21.1.1"),
 ("ipRouteAge","1.3.6.1.2.1.4.21.1.10"),
 ("ipRouteMask","1.3.6.1.2.1.4.21.1.11"),
 ("ipRouteMetric5","1.3.6.1.2.1.4.21.1.12"),
 ("ipRouteInfo","1.3.6.1.2.1.4.21.1.13"),
 ("ipRouteIfIndex","1.3.6.1.2.1.4.21.1.2"),
 ("ipRouteMetric1","1.3.6.1.2.1.4.21.1.3"),
 ("ipRouteMetric2","1.3.6.1.2.1.4.21.1.4"),
 ("ipRouteMetric3","1.3.6.1.2.1.4.21.1.5"),
 ("ipRouteMetric4","1.3.6.1.2.1.4.21.1.6"),
 ("ipRouteNextHop","1.3.6.1.2.1.4.21.1.7"),
 ("ipRouteType","1.3.6.1.2.1.4.21.1.8"),
 ("ipRouteProto","1.3.6.1.2.1.4.21.1.9"),
 ("ifIndex","1.3.6.1.2.1.2.2.1.1"),
 ("ifInOctets","1.3.6.1.2.1.2.2.1.10"),
 ("ifInUcastPkts","1.3.6.1.2.1.2.2.1.11"),
 ("ifInNUcastPkts","1.3.6.1.2.1.2.2.1.12"),
 ("ifInDiscards","1.3.6.1.2.1.2.2.1.13"),
 ("ifInErrors","1.3.6.1.2.1.2.2.1.14"),
 ("ifInUnknownProtos","1.3.6.1.2.1.2.2.1.15"),
 ("ifOutOctets","1.3.6.1.2.1.2.2.1.16"),
 ("ifOutUcastPkts","1.3.6.1.2.1.2.2.1.17"),
 ("ifOutNUcastPkts","1.3.6.1.2.1.2.2.1.18"),
 ("ifOutDiscards","1.3.6.1.2.1.2.2.1.19"),
 ("ifDescr","1.3.6.1.2.1.2.2.1.2"),
 ("ifOutErrors","1.3.6.1.2.1.2.2.1.20"),
 ("ifOutQLen","1.3.6.1.2.1.2.2.1.21"),
 ("ifSpecific","1.3.6.1.2.1.2.2.1.22"),
 ("ifType","1.3.6.1.2.1.2.2.1.3"),
 ("ifMtu","1.3.6.1.2.1.2.2.1.4"),
 ("ifSpeed","1.3.6.1.2.1.2.2.1.5"),
 ("ifPhysAddress","1.3.6.1.2.1.2.2.1.6"),
 ("ifAdminStatus","1.3.6.1.2.1.2.2.1.7"),
 ("ifOperStatus","1.3.6.1.2.1.2.2.1.8"),
 ("ifLastChange","1.3.6.1.2.1.2.2.1.9")
])

snmp_dict=dict((v+".",k) for k, v in snmp_dict.iteritems())

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

def ifmask(netmask):
  import math
  mask=ipconvert(netmask)
  return bin(mask).count('1')

def to_man(string):
  for key in snmp_dict.keys():
    if key in string:
      return snmp_dict[key]+" - "+string[len(key):]
  return string

def get_snmp_output(hostname,creds):
  snmp_result={}
  errorIndication, errorStatus, errorIndex, \
  varBindTable = cmdgen.CommandGenerator().bulkCmd(
            cmdgen.CommunityData('test-agent', 'public'),
            cmdgen.UdpTransportTarget((hostname, 161)),
            0,
            25,
            (1,3,6,1,2,1,4,20), # ipAddrTable OID . This works fine.
            (1,3,6,1,2,1,4,21), # ipRouteTable
#            (1,3,6,1,2,1,4,22), # ipNetToMediaTable
            (1,3,6,1,2,1,2,2),  # ifTable
        )
  if errorIndication:
    print errorIndication
  else:
    if errorStatus:
      print '%s at %s\n' % (
            errorStatus.prettyPrint(),
            errorIndex and varBindTable[-1][int(errorIndex)-1] or '?'
            )
    else:
      for varBindTableRow in varBindTable:
        for name, val in varBindTableRow:
          if not "ifPhysAddress" in to_man(name.prettyPrint()):
            snmp_result[to_man(name.prettyPrint())]=str(val.prettyPrint())
  return snmp_result

def get_interfaces(hostname,creds):
  snmp_result=get_snmp_output(hostname,creds)
  result=[]
  max_number_interfaces=0
  pairs={}
  admin_status={1:"UP",2:"DOWN",3:"DOWN"}
  for i in snmp_result.keys():
    if i[:7]=="ifDescr":
      if int(i[10:])>max_number_interfaces:
        max_number_interfaces=int(i[10:])
  result=[[] for i in range(max_number_interfaces+1)]
  for i in snmp_result.keys():
    if i[:7]=="ifDescr":
      result[int(i[10:])].append(snmp_result[i])
  for i in snmp_result.keys():
    if i[:14]=="ipAdEntIfIndex":
      result[int(snmp_result[i])].append(i[17:])
      pairs[i[17:]]=int(snmp_result[i])
  for i in snmp_result.keys():
    if i[:14]=="ipAdEntNetMask":
      result[pairs[i[17:]]].append(ifmask(snmp_result[i]))
  for i in snmp_result.keys():
    if i[:13]=="ifAdminStatus":
      result[int(i[16:])].append(admin_status[int(snmp_result[i])])
    # Also we should guess how ip address was assigned to the interface
  result2=[i for i in result if len(i)==4]
  for res in result2:
    res.append("-")
  return result2

def get_routing_table(hostname,creds):
  snmp_result=get_snmp_output(hostname,creds)
  result=[]
  number_routes=0
  routing_protocols={2:"L",11:"E",13:"O",14:"B",8:"R",9:"I"}
  routing_protocols2={3:"C",4:"S"}
  pairs={}
  ss=0
  interfaces={0:""}
  for i in snmp_result.keys():
    if i[:7]=="ifDescr":
      interfaces[int(i[10:])]=snmp_result[i]
  for i in snmp_result.keys():
    if i[:11]=="ipRouteInfo":
      result.append(["","",i[14:]])
      pairs[i[14:]]=ss
      ss=ss+1
  for i in snmp_result.keys():
    if i[:12]=="ipRouteProto":
      result[pairs[i[15:]]][0]=routing_protocols[int(snmp_result[i])]
  for i in snmp_result.keys():
    if i[:11]=="ipRouteType":
      result[pairs[i[14:]]][1]=routing_protocols2[int(snmp_result[i])]
  for i in snmp_result.keys():
    if i[:11]=="ipRouteMask":
      result[pairs[i[14:]]].append(ifmask(snmp_result[i]))
  for i in snmp_result.keys():
    if i[:14]=="ipRouteNextHop":
      result[pairs[i[17:]]].append(snmp_result[i])
  for i in snmp_result.keys():
    if i[:14]=="ipRouteIfIndex":
      result[pairs[i[17:]]].append(interfaces[int(snmp_result[i])])
  for ent in result:
    if ent[0]=="L":
      ent[0]=ent[1]
    del(ent[1])
  for ent in result:
    if ent[0]=="C":
      ent[3]="self"
  r_table=result
  c_r_table=[x for x in r_table if x[0]=='C']
  s_r_table=[x for x in r_table if x[0]=='S']
  for route in r_table:
    if route[0]=='S' and route[3]!='self':
      next_hop_ip=route[3]
      for croute in c_r_table:
        if addr_in_net(ipconvert(next_hop_ip),ipconvert(croute[1]),maskif(croute[2])):
          route[4]=croute[4]
  return r_table

print get_routing_table("router1",222)
