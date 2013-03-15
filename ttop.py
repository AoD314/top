#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import subprocess
import time

def main():
    cmd = "cat /proc/cpuinfo | grep 'model name' | wc -l"
    cpu_cout = subprocess.getoutput(cmd)

    cmd = "cat /proc/cpuinfo | grep 'model name' | uniq"
    cpu_name = subprocess.getoutput(cmd)    
    cpu_name = cpu_name[cpu_name.find(":") + 1:]
    for i in range(len(cpu_name)):
        cpu_name = cpu_name.replace("  ", " ")

    cmd = "nvidia-smi -a | grep 'Product Name'"
    gpu_name = str(subprocess.getoutput(cmd).replace("\n", " "))
    gpu_name = gpu_name[gpu_name.find(':')+1:]

    sys.stdout.write("[" + cpu_cout.rjust(len(cpu_cout) + 1) + " x" + cpu_name.rjust(len(cpu_name)) + " ]" + "   [" + gpu_name.rjust(len(gpu_name)) + " ]\n")

    while True:
        cmd = "sensors | grep 'CPU Temperature' | awk '{print $3}'"
        temp_cpu = subprocess.getoutput(cmd)
        if (temp_cpu == ""):
            cmd = "sensors | grep 'Core 0' | awk '{print $3}'"
            temp_cpu = subprocess.getoutput(cmd)

        degr = temp_cpu[-2:]

        cmd = "nvidia-smi -q -d TEMPERATURE -i 0 | grep 'Gpu' | awk '{print $3}'"
        temp_gpu = subprocess.getoutput(cmd)
        temp_gpu = "+" + temp_gpu + ".0" + degr

        mess = temp_cpu + " " + temp_gpu
        sys.stdout.write("\r" + repr(temp_cpu).rjust(len(cpu_name) + 6 + len(cpu_cout)) + repr(temp_gpu).rjust(len(gpu_name) + 6))
        sys.stdout.flush()
        time.sleep(1)

if __name__ == '__main__':
    main()

