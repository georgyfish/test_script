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
            print(f"rs.group(1) = {rs.group(1)},rs.group(2) = {rs.group(2)},rs.group(3) = {rs.group(3)},rs.group(4) = {rs.group(4)}")
            x = rs.group(2)
            y = rs.group(3)
            if int(x) >= 1024 and int(y) >= 768:
                result[device_name][mode] = re.findall("\d+\.\d+", rs.group(4))
    return result

def get_current_display_mode():
    """
    get current display_mode
    """
    # rs = subprocess.Popen(cmd, shell=True, close_fds=True, stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE, preexec_fn = os.setsid).communicate()
    # rs =  rs[0].decode().strip().splitlines()
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
        rs = re.search(r"((\d+)x(\d+)).*\s([\d\.]+)\*",line)
        if rs:
            mode = rs.group(1)
            x = rs.group(2)
            y = rs.group(3)
            if int(x) >= 1024 and int(y) >= 768:
                result[device_name][mode] = rs.group(4)
    return result



def get_best_display_mode():
    '''
    get best resolution
    '''

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

# xrandr左右屏设置，xrandr主屏及左右屏设置
def run_extend_mode(config, times):
    modes = list(config.keys())
    if time == None:
        times = 2
    for i in range(times):
        if i % 2 == 0:
            rs = subprocess.Popen(f"export DISPLAY=:0.0 && xrandr --output {modes[0]} --right-of {modes[1]} --auto", shell=True)
        else:
            rs = subprocess.Popen(f"export DISPLAY=:0.0 && xrandr --output {modes[1]} --right-of {modes[0]} --auto", shell=True)
        time.sleep(10)
        if not check_status:
            return False
    for i in range(times):
        if i % 2 == 0:
            rs = subprocess.Popen(f"export DISPLAY=:0.0 && xrandr --output {modes[0]} --right-of {modes[1]} --auto --primary", shell=True)
        else:
            rs = subprocess.Popen(f"export DISPLAY=:0.0 && xrandr --output {modes[1]} --right-of {modes[0]} --auto --primary", shell=True)
        time.sleep(10)
        if not check_status:
            return False    

# xrandr复制屏
def run_duplicate_mode(config,times):
    modes = list(config.keys())
    if time == None:
        times = 2
    # 先把分辨率设置为相同，高分辨率向下适配，再执行--same-as，就不会出现高分辨率显示器画面溢出的现象；(2 monitors)
    resolution0 = config[modes[0]].keys()[0]
    resolution1 = config[modes[1]].keys()[0]
    if resolution0 == resolution1:
        rs = subprocess.Popen(f"export DISPLAY=:0.0 && xrandr --output {modes[0]} --same-as {modes[1]} --auto", shell=True) 
    elif resolution0 > resolution1:
        rs = subprocess.Popen(f"export DISPLAY=:0.0 && xrandr --output {modes[0]} --mode {resolution1} ; xrandr --output {modes[0]} --same-as {modes[1]} --auto", shell=True)
    else:
        rs = subprocess.Popen(f"export DISPLAY=:0.0 && xrandr --output {modes[1]} --mode {resolution0} ; xrandr --output {modes[1]} --same-as {modes[0]} --auto", shell=True)
    time.sleep(10)
    if not check_status:
        return False

# 复制、扩展模式切换
def run_duplicate_switch_extend_mode():
    """
    duplicate_switch_extend
    """

def run_duplicate_switch_only_mode():
    """
    duplicate_switch_only
    """
def run_primary_switch():
    """
    monitor_primary_switch
    """
    modes = list(config.keys())
    if time == None:
        times = 2
    for i in range(times):
        if i % 2 == 0:
            rs = subprocess.Popen(f"export DISPLAY=:0.0 && xrandr --output {modes[0]} --right-of {modes[1]} --auto --primary", shell=True)
        else:
            rs = subprocess.Popen(f"export DISPLAY=:0.0 && xrandr --output {modes[1]} --left-of {modes[0]} --auto --primary", shell=True)
        time.sleep(10)
        if not check_status:
            return False   

# 扩展独立模式切换
def run_extend_switch_only_mode(config,times):
    modes = list(config.keys())
    if time == None:
        times = 2
    for i in range(times):
        if i % 2 == 0:
            rs = subprocess.Popen(f"export DISPLAY=:0.0 && xrandr --output {modes[0]} --right-of --output {modes[1]} --auto", shell=True)
            time.sleep(10)
            if not check_status:
                return False
            rs = subprocess.Popen(f"export DISPLAY=:0.0 && xrandr --output {modes[0]} --auto --output {modes[1]} --off", shell=True)
            time.sleep(10)
            if not check_status:
                return False
        else:
            rs = subprocess.Popen(f"export DISPLAY=:0.0 && xrandr --output {modes[0]} --left-of --output {modes[1]} --auto", shell=True)
            time.sleep(10)
            if not check_status:
                return False
            rs = subprocess.Popen(f"export DISPLAY=:0.0 && xrandr --output {modes[1]} --auto --output {modes[0]} --off", shell=True)
            time.sleep(10)
            if not check_status:
                return False

# 独立模式切换
def run_only_mode(config,times):
    modes = list(config.keys())
    if time == None:
        times = 2
    for i in range(times):
        if i % 2 == 0:
            rs = subprocess.Popen(f"export DISPLAY=:0.0 && xrandr --output {modes[0]} --auto --output {modes[1]} --off", shell=True)
        else:
            rs = subprocess.Popen(f"export DISPLAY=:0.0 && xrandr --output {modes[1]} --auto --output {modes[0]} --off", shell=True)
        time.sleep(10)
        if not check_status:
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
    # config = get_display_support()
    # 修改分辨率
    #run_display_resolution(config, times, random_flag)
    # 修改显示模式
    # run_display_mode(config, times)
    current_display_config = get_current_display_mode()
    run_duplicate_mode(current_display_config)