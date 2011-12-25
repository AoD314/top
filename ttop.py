#!/usr/bin/python
import sys
import subprocess
import time

cmd = "cat /proc/cpuinfo | grep 'model name' | wc -l"
p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, close_fds=True)
cpu_cout = p.stdout.read()
cpu_cout = cpu_cout[:cpu_cout.find("\n")]
 

cmd = "cat /proc/cpuinfo | grep 'model name' | uniq"
p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, close_fds=True)
cpu_name = p.stdout.read()
cpu_name = cpu_name[cpu_name.find(":") + 1:cpu_name.find("\n")]
for i in range(len(cpu_name)):
    cpu_name = cpu_name.replace("  ", " ")
    
cmd = "nvidia-smi -a | grep 'Product Name'"
#cmd = "nvidia-smi -L | awk '{print $3; print $4; print $5}'"
p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, close_fds=True)
gpu_name = str(p.stdout.read().replace("\n", " "))
gpu_name = gpu_name[gpu_name.find(':')+1:-1]

sys.stdout.write("[" + cpu_cout.rjust(len(cpu_cout) + 1) + " x" + cpu_name.rjust(len(cpu_name)) + " ]" + "   [" + gpu_name.rjust(len(gpu_name)) + " ]\n")

while True:
	cmd = "sensors | grep 'CPU Temperature' | awk '{print $3}'"
	p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, close_fds=True)
	temp_cpu = p.stdout.read()
	temp_cpu = temp_cpu[:temp_cpu.find("\n")-3]
	
	cmd = "nvidia-smi -q -d TEMPERATURE -i 0 | grep 'Gpu' | awk '{print $3}'"
	p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, close_fds=True)
	temp_gpu = p.stdout.read()
	temp_gpu = "+" + temp_gpu[:temp_gpu.find("\n")] + ".0"
	
	mess = temp_cpu + " " + temp_gpu
	sys.stdout.write("\r" + repr(temp_cpu).rjust(len(cpu_name) + 6 + len(cpu_cout)) + repr(temp_gpu).rjust(len(gpu_name) + 6))
	sys.stdout.flush()
	time.sleep(1)
