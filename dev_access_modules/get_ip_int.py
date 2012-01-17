import re,fcntl,socket,struct,math

ifaces_file=open('/proc/net/dev','r')
ifaces=[]
for i in ifaces_file:
	iface=re.search('([a-zA-Z0-9]*):',i)
	if iface:
		ifaces.append(iface.group(1))

def get_netmask(ifname):
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		mask=socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x891b, struct.pack('256s',ifname))[20:24])
	except(IOError):
		return 'None'
	else:
		pref=0
		for i in mask.split('.'):
    			if i != '255':
        			prefx=int(8-math.log(int(256-int(i)),2))
        			pref=pref+prefx
    			else:
        			pref=pref+8
	return pref

def getifip(ifn):
	try:
    	 s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    	 return socket.inet_ntoa(fcntl.ioctl(s.fileno(),0x8915,struct.pack('256s', ifn[:15]))[20:24])
	except(IOError):
		 return "None"
ips=[]
ifs=[]
netmasks=[]

for i in ifaces:
	ifs.append(i),ips.append(getifip(i)),netmasks.append(get_netmask(i))

slov={'int':[ifs],'ip':ips,'mask':netmasks}
print slov
