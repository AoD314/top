#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import subprocess
import time


class CPU:
    def __init__(self):
        self.count = int(subprocess.getoutput("cat /proc/cpuinfo | grep 'model name' | wc -l"))

        cpu_name = subprocess.getoutput("cat /proc/cpuinfo | grep 'model name' | uniq")
        self.name = cpu_name[cpu_name.find(":") + 1:].replace('  ', ' ').replace('  ', ' ').replace('  ', ' ')

    def name(self):
        return str(self.name)

    def count(self):
        return self.count

    def temperature(self):
        cmd = "sensors | grep 'CPU Temperature' | awk '{print $3}'"
        temp_cpu = subprocess.getoutput(cmd)
        i = self.count - 1
        while temp_cpu == "":
            temp_cpu = subprocess.getoutput("sensors | grep 'Core " + str(i) + "' | awk '{print $3}'")
            i -= 1
            if i < 0:
                break
        return float(temp_cpu[:-2])


class GPU:
    def __init__(self):
        gpu_name = str(subprocess.getoutput("nvidia-smi -a | grep 'Product Name'").replace("\n", " "))
        self.name = gpu_name[gpu_name.find(':') + 1:]

    def name(self):
        return str(self.name)

    def temperature(self):
        return float(subprocess.getoutput("nvidia-smi -q -d TEMPERATURE -i 0 | grep 'Gpu' | awk '{print $3}'") + ".0")


class Printer:
    def __init__(self, cpu_count, cpu_name, gpu_name):
        self.cpu_len = 6 + len(cpu_name) + len(str(cpu_count))
        self.gpu_len = 6 + len(gpu_name)
        sys.stdout.write("[" + str(cpu_count).rjust(len(str(cpu_count)) + 1) + " x"
                         + cpu_name.rjust(len(cpu_name)) + " ]"
                         + "   [" + gpu_name.rjust(len(gpu_name))
                         + " ]\n")

    def status(self, cpu_temp, gpu_temp):
        cpu = str(cpu_temp) + '°C'
        gpu = str(gpu_temp) + '°C'
        sys.stdout.write("\r" + repr(cpu).rjust(self.cpu_len) + repr(gpu).rjust(self.gpu_len))


def main():
    cpu = CPU()
    gpu = GPU()
    printer = Printer(cpu.count, cpu.name, gpu.name)

    while True:
        printer.status(cpu.temperature(), gpu.temperature())
        time.sleep(1)
        if input() == 'q':
            break


if __name__ == '__main__':
    main()
