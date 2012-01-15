#!/usr/bin/env python

# Json parameter should be integer.
# For example: 6
#
#
#
#


from __init__ import *

def test_func(host,test_params):
  try:
    RT=RouteTable(host)
  except:
    return "Couldn't get data from host"
  num_entries=len(RT)
  try:
    test_params=int(test_params)
  except:
    return "Test parameter should be integer."
  if num_entries < test_params:
    return "Number of entries in routing table is %s" % num_entries
  return True
