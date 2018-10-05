import commands
import datetime
import psutil
import subprocess
from datetime import timedelta

def get_cpuload():
    cpuload = psutil.cpu_percent(interval=1, percpu=False)
    return str(cpuload)

def get_ram():
    san = subprocess.check_output(['free','-m'])
    lines = san.split('\n')
    return ( int(lines[1].split()[6]), int(lines[1].split()[1]) )

def get_cpu_temp():
    tempFile = open( "/sys/class/thermal/thermal_zone0/temp" )
    cpu_temp = tempFile.read()
    tempFile.close()
    return float(cpu_temp)/1000

def get_gpu_temp():
    gpu_temp = commands.getoutput( '/opt/vc/bin/vcgencmd measure_temp' ).replace('temp=','').replace('C','')
    return float(gpu_temp)

def get_connections():
    san = subprocess.check_output(['netstat','-tun'])
    return len([x for x in san.split() if x == 'ESTABLISHED'])

def get_ipaddress():
    arg='ip route list'
    ip=subprocess.Popen(arg,shell=True,stdout=subprocess.PIPE)
    data = ip.communicate()
    split_data = data[0].split()
    ipaddr = split_data[split_data.index('src')+1]
    return ipaddr
def get_uptime():
    with open('/proc/uptime', 'r') as f:
     uptime_seconds = float(f.readline().split()[0])
     uptime = (timedelta(seconds = uptime_seconds))
     return str(uptime)

print 'Uso CPU: ' + get_cpuload() + '%'
print 'Mem. Libre: ' + str(get_ram()[0]) + ' Mb de ' + str(get_ram()[1]) + ' Mb'
print 'Temp. CPU: ' + str(get_cpu_temp())
#print 'Temp.GPU ' + str(get_gpu_temp())
#print 'Con.Red. ' + str(get_connections())+ ' Activas'
print 'Direc. IP: ' + str(get_ipaddress())+ ' '
print 'Uptime: ' + get_uptime()
