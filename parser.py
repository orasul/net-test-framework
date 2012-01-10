#!/usr/bin/env python

import json

def load_json(filename):
  f=file(filename,"r")
  dat=f.read()
  f.close()
  js=json.loads(dat)
  return js


