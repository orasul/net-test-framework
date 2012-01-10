#!/usr/bin/env python

from parser import load_json

tests=load_json("tests.json")
hosts=load_json("hosts.json")

hostnames=[x["hostname"] for x in hosts]

result={}

for test in tests:
  result[test['id']]=True

print

for test in tests:
  # Here should be called simple function from library
  # for example: result[test['id']]=routing_table.max_entries('router1',4)
  test_type=test['type']
  test_name=test[test_type].keys()[0]
  test_params=test[test_type][test_name]
  hostname=test['host']
  host=hosts[hostnames.index(hostname)]
  id_number=test['id']
#  exec('"result[id_number]="+test_type+"."+test_name+"("+hostname+","+test_params+")"')
  import_string = "from %s.%s import test_func" % ( test_type , test_name )
  print import_string
  exec import_string
  print "result["+str(id_number)+"]=test_func("+str(host)+","+str(test_params)+")"
  result[id_number]=test_func(host,test_params)
  print


for test in tests:
  print test['id']
  print result[test['id']]
  print
  print
