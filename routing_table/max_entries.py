#!/usr/bin/env python

# Json parameter should be integer.
# For example: 6
#
#
#
#


from __init__ import *

def test_func(host,test_params):
  RT=RouteTable(host)
  num_entries=len(RT)
  if num_entries > test_params:
    return "Number of entries in routing table is %s" % num_entries
  return True
