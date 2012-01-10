#!/usr/bin/env python

from parser import load_json
import routing_table
import interfaces
#from classes import host

tests=load_json("tests.json")

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
  id_number=test['id']
#  exec('"result[id_number]="+test_type+"."+test_name+"("+hostname+","+test_params+")"')
  print hostname
  print test_params
  if test_type=='routing_table' and test_name=='max_entries': result[id_number]=routing_table.max_entries(hostname,test_params)
  if test_type=='routing_table' and test_name=='min_entries': result[id_number]=routing_table.min_entries(hostname,test_params)
  if test_type=='routing_table' and test_name=='route_to_ip': result[id_number]=routing_table.route_to_ip(hostname,test_params)
  if test_type=='interfaces' and test_name=='parameters': result[id_number]=interfaces.parameters(hostname,test_params)
  if not 'condition' in test.keys():
    cond=True
  else:
    cond=test['condition']
  print result[id_number]
  print
  print
#  result[id_number] = result[id_number] ^ cond ^ True

print result
