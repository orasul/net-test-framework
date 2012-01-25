#!/usr/bin/env python

# Parameter should be dictionary
# 'protocol': default is 'tcp', if it is tcp you can ignore it or you can set 'udp'
# 'port': (should be integer) or you can use its name (IANA) 'service' (should be string)
# ex: {'port':'22'}
# ex: {'protocol':'tcp', 'service':'http'}
# ex: {'protocol':'udp', 'port':'123'}

import socket, sys, re
service_dict={
"echo":7,
"discard":9,
"systat":11,
"daytime":13,
"quoteoftheday":17,
"chargen":19,
#"ftp":20,
"ftp":21,
"ssh":22,
"telnet":23,
"smtpmailtransfer":25,
"smtp":25,
"timeserver":37,
"nameserver":42,
"nicnamewhois":43,
"dommainleinnameserver":53,
"dns":53,
"tftptrivialfiletransfer":69,
"tftp":69,
"gopher":70,
"finger":79,
"http":80,
"www":80,
"kerberos":88,
"hostnamenic":101,
"rtelnet":107,
"pop2":109,
"pop3":110,
"sunrpc":111,
"identificationprotocol":113,
"uucp":117,
"nntp":119,
"ntp":123,
"epmap":135,
"netbios(nameservice)":137,
"netbios(dgm)":138,
"netbios(ssn)":139,
"imap":143,
"snmp":161,
"snmptrap":162,
"print":170,
"bgp":179,
"irc":194,
"ipx":213,
"ldap":389,
"https(ssl)":443,
"https":443,
"ssl":443,
"microsoft(ds)":445,
"kpasswd":464,
"isakmpkeyexchange":500,
"remoteexecute":512,
"login/who":513,
"shellcmd/syslog":514,
"printerspooler":515,
"talk":517,
"ntalk":518,
"router/efs":520,
"timeserver":525,
"tempo":526,
"rpc":530,
"conferencechat":531,
"netnewsnewsreader":532,
"netwall":533,
"uucp":540,
"klogin":543,
"kshell":544,
"rwho":550,
"remotefs":556,
"rmonitor":560,
"monitor":561,
"kerberosadministration":749,
"kerberosversioniv":750,
"kpop":1109,
"phone":1167,
"ovpn":1194,
#"ms":1433,
"ms":1434,
"xwins":1512,
"ingreslock":1524,
"pptp(pointtopoint)":1723,
"pptp":1723,
"radiusauthentication":1812,
"radiusaccounting":1813,
"nfsserver":2049,
"manremoteserver":9535
}

def test_func(host,test_params):
  proto='tcp'
  if test_params.has_key('protocol'):
    proto=test_params['protocol']
  hostname=host['hostname']
  if test_params.has_key('port'):
    try:
      port=int(test_params['port'])
    except:
      return "port should be integer"
  elif test_params.has_key('service'):
    serv=test_params['service']
    if service_dict.has_key(serv):
      port=service_dict[serv]
    else:
      return "Unknown service name. Please, specify port number."
  if proto=='tcp':
    return tcp_test(hostname,port)
  elif proto=='udp':
    return udp_test(hostname,port)
  else:
    return "Unknown protocol, choose tcp or udp."
    


def tcp_test(hostname,port):
  s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
  s.settimeout(5)
  flag=False
  port=int(port)
  try:
    s.connect((hostname, port))
    flag=True
  except:
    return "Service is down"
  if flag:
    data = "HELO"
    try:
      s.sendall(data)
      s.shutdown(1)
      buf=s.recv(1024)
      buf=str(buf)
      buf=re.sub('\n','',buf)
      buf=re.sub('\r\n','',buf)
      return "It's UP! Received: %s" % buf
    except:
      return "Service is up but it is silent"


def udp_test(hostname,port):
  s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  s.settimeout(5)
  try:
    s.connect((hostname, port))
  except:
    return "Hostname or port is unknown."
  data = "testing"
  try:
    s.sendall(data)
    s.shutdown(1)
    buf=s.recv(1024)
    buf=str(buf)
    buf=re.sub('\n','',buf)
    buf=re.sub('\r\n','',buf)
    return "It's UP! Received: %s" % buf
  except:
    return "Cannot determine service availability."

if __name__=='__main__':
  print test_func({"hostname":"localhost"},{"port":22})
  print test_func({"hostname":"192.168.102.11"},{"protocol":"udp","port":53})
  print test_func({"hostname":"yandex.ru"},{"protocol":"tcp","port":80})
  print test_func({"hostname":"vpn.orwik.org"},{"protocol":"udp","port":1194})
