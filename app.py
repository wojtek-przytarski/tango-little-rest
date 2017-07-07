#!/usr/bin/python
from flask import Flask, Response, jsonify

import PyTango, json

app = Flask(__name__)

#get device status, state, dev_info and description
#route to reach tangotest device is /devices/sys/tg_test/1
@app.route('/devices/<domain>/<family>/<member>')
def get_device(domain, family, member):
	device = (domain+'/'+family+'/'+member)
	proxy = PyTango.DeviceProxy(device)

	state, status = proxy.read_attributes(["state", "status"])
	dev_info = proxy.info()

	devinfo = dict(
		classname = dev_info.dev_class,
		devtype = dev_info.dev_type,
		docurl = dev_info.doc_url,
		serverhost = dev_info.server_host,
		serverid = dev_info.server_id,
		serverversion = dev_info.server_version
	)
	db_info = proxy.get_db_host()

	dbinfo = dict(
		host = proxy.get_db_host(),
		port = proxy.get_db_port()
	)

	attributes = list(proxy.get_attribute_list())
	data = json.dumps(dict(state = (state.value),
                           status = status.value,
                           devinfo = devinfo,
                           description = proxy.description(),
                           dbinfo = dbinfo,
                           logginglevel = proxy.get_logging_level()))
	return Response(data, mimetype="application/json")

#-------------------Attribute section----------------------------------
#get attribute list
@app.route('/devices/<domain>/<family>/<member>/attributes')
def get_device_attributes(domain, family, member):
    device = (domain+'/'+family+'/'+member)
    proxy = PyTango.DeviceProxy(device)

    attributes = list(proxy.get_attribute_list())
    data = json.dumps(dict(attributes=attributes))
    return Response(data, mimetype="application/json")

#get specific attribute and its value 
@app.route('/devices/<domain>/<family>/<member>/attributes/<attribute>')
def get_device_attribute(domain, family, member, attribute):
    device = (domain+'/'+family+'/'+member)
    proxy = PyTango.DeviceProxy(device)

    device_attribute = proxy.read_attribute(attribute)
    value = str(device_attribute.value)
    data = json.dumps(dict(name=device_attribute.name,
                           value=value))
    return Response(data, mimetype="application/json")

#-------------------Command section----------------------------------

#get list of last n commands
@app.route('/devices/<domain>/<family>/<member>/commands/<int:n>')
def get_device_commands(domain, family, member, n):	
	device = (domain+'/'+family+'/'+member)
	proxy = PyTango.DeviceProxy(device)
	commands = list(proxy.black_box(n))
	data = json.dumps(dict(commands=commands))
	return Response(data, mimetype="application/json")

#get last used command
@app.route('/devices/<domain>/<family>/<member>/commands/last')
def get_device_commands_default(domain, family, member):	
	device = (domain+'/'+family+'/'+member)
	proxy = PyTango.DeviceProxy(device
)
	command = list(proxy.black_box(1))[0]
	data = json.dumps(dict(command=command))
	return Response(data, mimetype="application/json")



if __name__ == '__main__':
    app.run()


