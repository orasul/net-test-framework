import json
import os
import sys
from paste.httpserver import serve
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.renderers import render_to_response

# hosts actions
def index(request):
  ht = [x[:-5] for x in os.listdir(os.getcwd() + '/hosts/') if x[-5:] == ".json"]
  tt = [x[:-5] for x in os.listdir(os.getcwd() + '/tests/') if x[-5:] == ".json"]
  return render_to_response(os.getcwd() + '/web/index.pt', {'host_table':ht,'test_table':tt}, request=request)

def add_host_form(request):
  return render_to_response(os.getcwd() + '/web/add_host.pt', {}, request=request)

def delete_host(request):
  os.remove(os.getcwd() + '/hosts/' + request.params['hostname'] + '.json')
  return Response("OK")

def add_host_apply_delete(request):
  os.remove(os.getcwd() + '/hosts/' + request.params['oldname'] + '.json')
  return add_host_apply(request)

def add_host_apply(request):
  dic = dict(request.params)

  try:
    del dic["oldname"]
  except:
    True

  json_str = json.dumps(dic, indent=2) 
  
  f = file(os.getcwd() + '/hosts/' + request.params['hostname'] + '.json', "w")
  f.write(json_str)
  f.close()

  return render_to_response(os.getcwd() + '/web/add_host_apply.pt', { 'created' : json_str, 'cwd' : os.getcwd() }, request=request)

def edit_host(request):
  f = file(os.getcwd() + '/hosts/' + request.params['hostname'] + '.json', "r")
  json_dict = json.loads(f.read())
  f.close()

  return render_to_response(os.getcwd() + '/web/edit_host.pt', json_dict, request=request)

#tests actions
def add_test_form(request):
  l = [x[:-5] for x in os.listdir(os.getcwd() + '/hosts/') if x[-5:] == ".json"]
  code = '{"route_to_ip":"hello world","max_entries":"xxx"}'

  routing_table_tests = list_tests("routing_table");
  interfaces_tests = list_tests("interfaces");
  service_tests = list_tests("service");


  d = dict([("routing_table_" + key, get_comment("routing_table",key)) for key in routing_table_tests] + 
           [("interfaces_" + key, get_comment("interfaces",key)) for key in interfaces_tests] + 
           [("service_" + key, get_comment("service",key)) for key in service_tests])

  return render_to_response(os.getcwd() + '/web/add_test.pt', {'hosts': l, "routing_table_tests": routing_table_tests, "interfaces_tests": interfaces_tests, "service_tests": service_tests, "code": json.dumps(d)}, request=request)

def list_tests(t):
  return [x[:-3] for x in os.listdir(os.getcwd() + "/" + t) if x[-3:] == ".py" and x != "__init__.py" ] 

def get_comment(test_type, test_name):
  f = file(os.getcwd() + "/" + test_type + "/" + test_name + ".py", "r")
  f.readline() 
  f.readline() 
  result = ""
  for x in range(5):
    result += f.readline()
  f.close()
  return result

def delete_test(request):
  os.remove(os.getcwd() + '/tests/' + request.params['id'] + '.json')
  return Response("OK")

def add_test_apply_delete(request):
  os.remove(os.getcwd() + '/tests/' + request.params['oldname'] + '.json')
  return add_test_apply(request)

def add_test_apply(request):
  dic = dict(request.params)

  try:
    del dic["oldname"]
  except:
    True

  json_str = json.dumps(dic, indent=2) 
  
  f = file(os.getcwd() + '/tests/' + request.params['id'] + '.json', "w")
  f.write(json_str)
  f.close()

  return render_to_response(os.getcwd() + '/web/add_test_apply.pt', { 'created' : json_str, 'cwd' : os.getcwd() }, request=request)

def edit_test(request):
  f = file(os.getcwd() + '/tests/' + request.params['id'] + '.json', "r")
  json_dict = json.loads(f.read())
  f.close()

  return render_to_response(os.getcwd() + '/web/edit_test.pt', json_dict, request=request)

def run_tests(request):
  from head import test_results,hosts,tests
  test_res=test_results(hosts,tests)
  l=""
  for key in test_res.keys():
    l=l+str(key)+"  :  "+str(test_res[key])+"\n"

  del(test_results,hosts,tests)
  return render_to_response(os.getcwd() + '/web/run_tests.pt', { 'tests' : l }, request=request)

if __name__ == '__main__':
   config = Configurator()

   config.add_route('index', '/')
   config.add_view(index, route_name='index')

   config.add_route('add_host_form', '/add_host')
   config.add_view(add_host_form, route_name='add_host_form')

   config.add_route('add_host_apply', '/add_host_apply')
   config.add_view(add_host_apply, route_name='add_host_apply')

   config.add_route('add_host_apply_delete', '/add_host_apply_delete')
   config.add_view(add_host_apply_delete, route_name='add_host_apply_delete')

   config.add_route('delete_host', '/delete_host')
   config.add_view(delete_host, route_name='delete_host')

   config.add_route('edit_host', '/edit_host')
   config.add_view(edit_host, route_name='edit_host')

   config.add_route('add_test_form', '/add_test')
   config.add_view(add_test_form, route_name='add_test_form')

   config.add_route('add_test_apply', '/add_test_apply')
   config.add_view(add_test_apply, route_name='add_test_apply')

   config.add_route('add_test_apply_delete', '/add_test_apply_delete')
   config.add_view(add_test_apply_delete, route_name='add_test_apply_delete')

   config.add_route('delete_test', '/delete_test')
   config.add_view(delete_test, route_name='delete_test')

   config.add_route('edit_test', '/edit_test')
   config.add_view(edit_test, route_name='edit_test')

   config.add_route('run_tests', '/run_tests')
   config.add_view(run_tests, route_name='run_tests')

   config.add_static_view(name='static', path=os.getcwd() + '/static')

   app = config.make_wsgi_app()
   serve(app, host='0.0.0.0')
