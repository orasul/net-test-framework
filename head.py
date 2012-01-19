#!/usr/bin/env python

from parser import load_json
import os
import ast
import re

def get_tests(directory):
  tests=[]
  for test_file in os.listdir(directory):
    tests.append(load_json(directory+test_file))
  for test in tests:
    tes_type=test['type']
    tes_name=test['test_name']
    tes_params=ast.literal_eval(re.sub('\r\n','',test['test_params']))
    tes_params=ast.literal_eval(re.sub('#','',test['test_params']))
    test[tes_type]={tes_name:tes_params}
    del(test['test_name'])
    del(test['test_params'])
  return tests


def get_hosts(directory):
  hosts=[]
  for host_file in os.listdir(directory):
    hosts.append(load_json(directory+host_file))
  for host in hosts:
    hos_login=host['login']
    hos_password=host['password']
    host['credentials']={'login':hos_login,'password':hos_password}
    del(host['login'])
    del(host['password'])
  return hosts

if __name__=='__main__':
  tests=load_json("tests.json")
  hosts=load_json("hosts.json")
else:
  tests=get_tests("tests/")
  hosts=get_hosts("hosts/")


result={}
  
for test in tests:
  result[test['id']]=True

def test_results(hosts,tests):
  hostnames=[x["hostname"] for x in hosts]
  
  result={}
  
  for test in tests:
    result[test['id']]=True
  
  
  for test in tests:
    # Here should be called simple function from library
    # for example: result[test['id']]=routing_table.max_entries('router1',4)
    test_type=test['type']
    test_name=test[test_type].keys()[0]
    test_params=test[test_type][test_name]
    hostname=test['host']
    host=hosts[hostnames.index(hostname)]
    id_number=test['id']
    if not test.has_key('condition'):
      test['condition']=True
  #  exec('"result[id_number]="+test_type+"."+test_name+"("+hostname+","+test_params+")"')
    import_string = "from %s.%s import test_func" % ( test_type , test_name )
    try:
      exec import_string
    except:
      result[id_number]="Specified test missing."
    try:
      result[id_number]=test_func(host,test_params)
    except:
      result[id_number]="Test parameters are bad or test is improperly designed"
  return result

if __name__=='__main__':
  result=test_results(hosts,tests)
  for test in tests:
    print test['id']
    print result[test['id']]
    print
    print
