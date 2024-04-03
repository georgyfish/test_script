#!/usr/bin/env python3
import subprocess
import os
import re
import time
import sys
import random

def get_display_support():
    result = {}
    status = None
    device_name = None
    cmd = "export DISPLAY=:0.0 && xrandr"
    rs = subprocess.Popen(cmd, shell=True, close_fds=True, stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE, preexec_fn = os.setsid)
    for line in rs.stdout.readlines():
        line = line.decode()
        rs = re.search("([\w-]+)\s+(connected|disconnected)", line)
        if rs:
            device_name = rs.group(1)
            status = rs.group(2)
            if status == 'connected':
                result[device_name] = {}
        rs = re.search("((\d+)x(\d+))\s+(.*)", line)
        if rs:
            mode = rs.group(1)
            x = rs.group(2)
            y = rs.group(3)
            if int(x) >= 1024 and int(y) >= 768:
                result[device_name][mode] = re.findall("\d+\.\d+", rs.group(4))
    return result

def set_display_config(device_name, mode, rate):
    cmd = f"export DISPLAY=:0.0 && xrandr --output {device_name} --mode {mode} --rate {rate}"
    print(cmd)
    rs = subprocess.Popen(cmd, shell=True, close_fds=True, stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE, preexec_fn = os.setsid)
    stdout,stderr = rs.communicate(timeout=10)

def check_status():
    rs = subprocess.Popen("export DISPLAY=:0.0 xgles3test1", shell=True, close_fds=True, stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE, preexec_fn = os.setsid)
    stdout,stderr = rs.communicate(timeout=10)
    if rs.returncode != 0:
        print("display error")
        return False
    else:
        return True

def run_display_resolution(config, times, random_flag):
    para_list = []
    for device_name in config.keys():
        for mode in config[device_name].keys():
            for rate in config[device_name][mode]:
                para_list.append([device_name, mode, rate])
    para_list_size = len(para_list)
    if times == None:
        times = para_list_size
    for i in range(times):
        index = i % para_list_size
        if random_flag == 'true':
            random.shuffle(para_list)
        device_name, mode, rate = para_list[index]
        set_display_config(device_name, mode, rate)
        time.sleep(10)
        if not check_status():
            return False

def run_display_mode(config, times):
    modes = list(config.keys())

    if times == None:
        times = 2
    for i in range(times):
        if i %2 == 0:
            rs = subprocess.Popen(f"export DISPLAY=:0.0 && xrandr --output {modes[0]} --same-as {modes[1]} --auto", shell=True)
        else:
            rs = subprocess.Popen(f"export DISPLAY=:0.0 && xrandr --output {modes[0]} --right-of {modes[1]} --auto", shell=True)
        time.sleep(10)
        if not check_status():
            return False

def run_primary_display(config,times):
    modes = list(config.keys())
    if times == None:
        times = 2
    for i in range(times):
        if i %2 == 0:
            rs = subprocess.Popen(f"export DISPLAY=:0.0 && xrandr --output {modes[0]} --right-of {modes[1]} --auto --primary", shell=True)
        else:
            rs = subprocess.Popen(f"export DISPLAY=:0.0 && xrandr --output {modes[1]} --left-of {modes[0]} --auto --primary", shell=True)
        time.sleep(5)
        if not check_status():
            return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        times = int(sys.argv[1])
    else:
        times = None
    if len(sys.argv) > 2:
        random_flag = sys.argv[2]
    else:
        random_flag = None
    config = get_display_support()
    #run_display_resolution(config, times, random_flag)
    # run_display_mode(config, times)
    # run_primary_display(config,times)
    print(get_display_support())