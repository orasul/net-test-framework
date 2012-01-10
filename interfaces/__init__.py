#!/usr/bin/env python

def InterfaceTable(host):
  os=host['os']
  protocol=host['protocol']
  hostname=host['hostname']
  creds=host['credentials']
  import_string="from dev_access_modules."+str(os)+"_"+str(protocol)+" import get_interfaces"
  exec import_string
  return get_interfaces(hostname,creds)

