#!/usr/bin/env python3
import subprocess
import os
import re
import time
import sys
import random,itertools



'''
测试进度可视化----读取接口信息，按照接口信息列出当前接口组合、执行完成接口组合、待完成接口组合、总共所有接口组合；
加入win+P 快捷键切换， pyautogui,控制键盘
before test;
    测试前，初始化，显示模式恢复默认，扩展模式，xrandr --output DP-1 --auto
run test;
    xrandr --output 
after test;
    HWR/dmesg 读取; log
'''

def get_vga_support():
    """
    get_vga_card_info
    S80  --- 4个接口
    """
    result = []
    status = None
    device_name = None
    cmd = "export DISPLAY=:0.0 && xrandr"
    rs = subprocess.Popen(cmd, shell=True, close_fds=True, stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE, preexec_fn = os.setsid)
    for line in rs.stdout.readlines():
        line = line.decode()
        rs = re.search(r"([\w-]+)\s+(connected|disconnected)", line)
        if rs:
            device_name = rs.group(1)
            status = rs.group(2)
            # if status == 'connected':
            #     result[device_name] = {}
            result.append(device_name)
        rs = re.search(r"((\d+)x(\d+))\s+(.*)", line)
        if rs:
            mode = rs.group(1)
            x = rs.group(2)
            y = rs.group(3)
            if int(x) >= 1024 and int(y) >= 768:
                result[device_name][mode] = re.findall(r"\d+\.\d+", rs.group(4))
    return result

def get_display_support():
    result = {}
    status = None
    device_name = None
    cmd = "export DISPLAY=:0.0 && xrandr"
    rs = subprocess.Popen(cmd, shell=True, close_fds=True, stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE, preexec_fn = os.setsid)
    for line in rs.stdout.readlines():
        line = line.decode()
        rs = re.search(r"([\w-]+)\s+(connected|disconnected)", line)
        if rs:
            device_name = rs.group(1)
            status = rs.group(2)
            if status == 'connected':
                result[device_name] = {}
        rs = re.search(r"((\d+)x(\d+))\s+(.*)", line)
        if rs:
            mode = rs.group(1)
            x = rs.group(2)
            y = rs.group(3)
            if int(x) >= 1024 and int(y) >= 768:
                result[device_name][mode] = re.findall(r"\d+\.\d+", rs.group(4))
    return result

def get_current_display():
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
        rs = re.search(r"([\w-]+)\s+(connected|disconnected)", line)
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

def before_test(config):
    '''
    before test set mode max resolution
    '''
    cmd = f"export DISPLAY=:0 "
    modes = list(config.keys())
    for i in range(len(modes)):
        cmd += f"&& xrandr --output {modes[i]} --auto "
    print(cmd)
    rs = subprocess.Popen(cmd, shell=True, close_fds=True, stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE, preexec_fn = os.setsid)
    stdout,stderr = rs.communicate(timeout=10)
    if rs.returncode == 0 :
        # print(f"\"{cmd}\" executed successfully.")
        time.sleep(10)
        if not check_status:
            return False
    else:
        print(f"\"{cmd}\" executed failed.")
        return False

def after_test():
    '''
    check dmesg & HWR
    '''

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

# 
def run_display_mode(config, times):
    modes = list(config.keys())
    if times == None:
        times = 2
    for i in range(times):
        if i %2 == 0:
            rs = subprocess.Popen(f"export DISPLAY=:0.0 && xrandr --output {modes[0]} --same-as {modes[1]}", shell=True)
        else:
            rs = subprocess.Popen(f"export DISPLAY=:0.0 && xrandr --output {modes[0]} --right-of {modes[1]} --auto", shell=True)
        time.sleep(10)
        if not check_status():
            return False

# xrandr扩展、左右屏设置，xrandr主屏及左右屏设置,支持多屏,3屏/4屏
def run_xrandr_extend_mode(config, times):
    print("="*30 + "run_xrandr_extend_mode" + "="*30)
    before_test(config)
    modes = list(config.keys())
    if times == None:
        times = 2
    if len(modes) <= 1:
        print(f"Only support multi monitor! Please check display!")
        return False
    modes_permutations = list(itertools.permutations(modes,len(modes)))
    # 左右屏
    for i in range(times):
        for modes_permutation in modes_permutations:
            print(modes_permutation)
            cmd = f"export DISPLAY=:0.0 && xrandr --output {modes_permutation[0]} --auto "
            n=1
            while n < len(modes_permutation):
                cmd += f"--output {modes_permutation[n]} --right-of {modes_permutation[n-1]} --auto "
                n += 1
            print(cmd)
            # rs = subprocess.Popen(cmd,shell=True)
            rs = subprocess.Popen(cmd, shell=True, close_fds=True, stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE, preexec_fn = os.setsid)
            stdout,stderr = rs.communicate(timeout=10)
            if rs.returncode != 0 :
                print(f"\"{cmd}\" executed failed.")
            else:
                time.sleep(10)
                if not check_status:
                    return False
    
    # 左右屏主屏       
    for i in range(times):
        for modes_permutation in modes_permutations:
            print(modes_permutation)
            cmd = f"export DISPLAY=:0.0 && xrandr --output {modes_permutation[0]} --auto --primary "
            n=1
            while n < len(modes_permutation):
                cmd += f"--output {modes_permutation[n]} --right-of {modes_permutation[n-1]} --auto "
                n += 1
            print(cmd)
            # rs = subprocess.Popen(cmd,shell=True)
            rs = subprocess.Popen(cmd, shell=True, close_fds=True, stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE, preexec_fn = os.setsid)
            stdout,stderr = rs.communicate(timeout=10)
            if rs.returncode != 0 :
                print(f"\"{cmd}\" executed failed.")
            else:
                time.sleep(10)
                if not check_status:
                    return False
    print("="*30 + "xrandr_extend_mode done" + "="*30)

# xrandr复制屏,只设置一次
def run_duplicate_mode(config):
    print("="*30 + "run_duplicate_mode" + "="*30)
    before_test(config)
    modes = list(config.keys())
    resolution = []
    if len(modes) <= 1:
        print(f"Only support multi monitor! Please check display!")
        return False
    for i in range(len(modes)):
        tmp = config[modes[i]]
        if bool(tmp):
            tmp = list(tmp.keys())
            resolution.append(tmp[0])
            # rate[i] = v
    # 先把分辨率设置为相同，高分辨率向下适配，再执行--same-as，就不会出现高分辨率显示器画面溢出；
    resolution_sort = list(set(resolution))
    resolution_sort.sort()
    for i in range(len(modes)):
        if resolution[i] == resolution_sort[0]:
            mode = modes[i]
    cmd = f'export DISPLAY=:0.0 && xrandr --output {mode} --auto '
    for i in range(len(modes)):
        if resolution[i] != resolution_sort[0]:
            cmd += f"&& xrandr --output {modes[i]} --mode {resolution_sort[0]} --auto --same-as {mode}"
            # cmd += f"&& xrandr --output {modes[i]}  --same-as {mode} "
        elif modes[i] != mode:
            cmd += f"&& xrandr --output {modes[i]}  --same-as {mode} "
    print(cmd)
    rs = subprocess.Popen(cmd, shell=True, close_fds=True, stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE, preexec_fn = os.setsid)
    stdout,stderr = rs.communicate(timeout=10)
    if rs.returncode != 0 :
        print(f"\"{cmd}\" executed failed.")
    else:
        time.sleep(10)
        if not check_status:
            return False
    print("="*30 + "duplicate_mode done" + "="*30)

# 复制、扩展模式切换(扩展模式左右、上下)
def run_duplicate_switch_extend_mode(config,times):
    print("="*30 + "run_duplicate_switch_extend_mode" + "="*30)
    before_test(config)
    modes = list(config.keys())
    if len(modes) <= 1:
        print(f"Only support multi monitor! Please check display!")
        return False
    if times == None:
        times = 2
    modes_permutations = list(itertools.permutations(modes,len(modes)))
    for i in range(times):
        for modes_permutation in modes_permutations:
            print(modes_permutation)
            run_duplicate_mode(config)
            cmd = "export DISPLAY=:0.0 && "
            n=0
            while n < len(modes_permutation):
                if n == 0:
                    cmd += f"xrandr --output {modes_permutation[n]} --auto "
                else:
                    if i %2 == 0:
                        cmd += f"--output {modes_permutation[n]} --right-of {modes_permutation[n-1]} --auto "
                    else:
                        cmd += f"--output {modes_permutation[n]} --above {modes_permutation[n-1]} --auto "
                n += 1
            print(cmd)
            rs = subprocess.Popen(cmd, shell=True, close_fds=True, stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE, preexec_fn = os.setsid)
            stdout,stderr = rs.communicate(timeout=10)
            if rs.returncode != 0 :
                print(f"\"{cmd}\" executed failed.")
            else:
                time.sleep(10)
                if not check_status:
                    return False
    print("="*30 + "duplicate_switch_extend_mode done" + "="*30)


# 复制独立模式切换
def run_duplicate_switch_only_mode(config,times):
    print("="*30 + "run_duplicate_switch_only_mode" + "="*30)
    before_test(config)
    modes = list(config.keys())
    if len(modes) <= 1:
        print(f"Only support multi monitor! Please check display!")
        return False
    # str  = "export DISPLAY=:0.0 && "
    # for mode in modes:
    #     str += f"xrandr --output {mode} "
    # rs = subprocess.Popen(str,shell=True)
    # time.sleep(10)
    # if not check_status:
    #     return False
    if times == None:
        times = 2
    modes_permutations = list(itertools.permutations(modes,len(modes)))
    for i in range(times):
        for modes_permutation in modes_permutations:
            run_duplicate_mode(current)
            cmd = "export DISPLAY=:0.0 && "
            # cmd1 = 'export DISPLAY=:0.0 && '
            n = 0
            while n < len(modes_permutation):
                if n == 0:
                    cmd += f"xrandr --output {modes_permutation[n]} --auto "
                else:
                    cmd += f"--output {modes_permutation[n]} --off "
                    # cmd1 += f"xrandr --output {modes_permutation[n]} --auto "
                n += 1
            print(cmd)
            # rs = subprocess.Popen(cmd,shell=True)
            rs = subprocess.Popen(cmd, shell=True, close_fds=True, stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE, preexec_fn = os.setsid)
            stdout,stderr = rs.communicate(timeout=10)
            if rs.returncode != 0 :
                print(f"\"{cmd}\" executed failed.")
            else:
                time.sleep(10)
                if not check_status:
                    return False
    print("="*30 + "duplicate_switch_only_mode done" + "="*30)

def run_primary_switch(config,times):
    """
    monitor_primary_switch 主屏切换，不应改变左右屏的方位
    """
    print("="*30 + "monitor_primary_switch" + "="*30)
    before_test(config)
    modes = list(config.keys())
    if len(modes) <= 1:
        print(f"Only support multi monitor! Please check display!")
        return False
    if times == None:
        times = 2
    # tmp_list = list(itertools.permutations(modes,len(modes)))
    for mode in modes:
        cmd = f"export DISPLAY=:0.0 && xrandr --output {mode} --auto --primary"
        print(f"将执行下列命令切换主屏为{mode}:")
        print(cmd)
        # rs = subprocess.Popen(cmd,shell=True)
        rs = subprocess.Popen(cmd, shell=True, close_fds=True, stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE, preexec_fn = os.setsid)
        stdout,stderr = rs.communicate(timeout=10)
        if rs.returncode != 0 :
            print(f"\"{cmd}\" executed failed.")
        else:
            time.sleep(10)
            if not check_status:
                return False
    # for i in range(times):
    #     if i % 2 == 0:
    #         rs = subprocess.Popen(f"export DISPLAY=:0.0 && xrandr --output {modes[0]} --right-of {modes[1]} --auto --primary", shell=True)
    #     else:
    #         rs = subprocess.Popen(f"export DISPLAY=:0.0 && xrandr --output {modes[1]} --left-of {modes[0]} --auto --primary", shell=True)
    #     time.sleep(10)
    #     if not check_status:
    #         return False   


# 扩展独立模式切换
def run_extend_switch_only_mode(config,times):
    print("="*30 + "run_extend_switch_only_mode" + "="*30)
    before_test(config)    
    modes = list(config.keys())
    if len(modes) <= 1:
        print(f"Only support multi monitor! Please check display!")
        return False
    if times == None:
        times = 2
    modes_permutations = list(itertools.permutations(modes,len(modes)))
    for i in range(times):
        for modes_permutation in modes_permutations:
            cmd = "export DISPLAY=:0.0 && "
            cmd1 = "export DISPLAY=:0.0 && "
            n = 0
            while n < len(modes_permutation):
                if n == 0:
                    cmd += f"xrandr --output {modes_permutation[n]} --auto "
                    cmd1 += f"xrandr --output {modes_permutation[n]} --auto "
                else:
                    if i % 2 == 0:
                        cmd += f"--output {modes_permutation[n]} --right-of {modes_permutation[n-1]} --auto "
                    else:
                        cmd += f"--output {modes_permutation[n]} --above {modes_permutation[n-1]} --auto "
                    cmd1 += f"&& xrandr --output {modes_permutation[n]} --off "
                n += 1
            print(cmd)
            rs = subprocess.Popen(cmd, shell=True, close_fds=True, stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE, preexec_fn = os.setsid)
            stdout,stderr = rs.communicate(timeout=10)
            if rs.returncode != 0 :
                print(f"\"{cmd}\" executed failed.")
            else:
                time.sleep(10)
                if not check_status:
                    return False

            print(cmd1)
            rs = subprocess.Popen(cmd, shell=True, close_fds=True, stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE, preexec_fn = os.setsid)
            stdout,stderr = rs.communicate(timeout=10)
            if rs.returncode != 0 :
                print(f"\"{cmd}\" executed failed.")
            else:
                time.sleep(10)
                if not check_status:
                    return False
    print("="*30 + "extend_switch_only_mode done" + "="*30)

# 独立模式切换
def run_only_mode(config,times):
    print("="*30 + "run_only_mode" + "="*30)
    before_test(config) 
    modes = list(config.keys())
    if len(modes) <= 1:
        print(f"Only support multi monitor! Please check display!")
        return False
    if times == None:
        times = 2
    modes_permutations = list(itertools.permutations(modes,len(modes)))
    for i in range(times):
        for modes_permutation in modes_permutations:
            cmd = "export DISPLAY=:0.0 && "
            n = 0
            while n < len(modes_permutation):
                if n == 0:
                    cmd += f"xrandr --output {modes_permutation[n]} --auto "
                else:
                    cmd += f"--output {modes_permutation[n]} --off "
                n += 1
            print(cmd)
            # rs = subprocess.Popen(cmd,shell=True)
            rs = subprocess.Popen(cmd, shell=True, close_fds=True, stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE, preexec_fn = os.setsid)
            stdout,stderr = rs.communicate(timeout=10)
            if rs.returncode != 0 :
                print(f"\"{cmd}\" executed failed.")
            else:
                time.sleep(10)
                if not check_status:
                    return False
    print("="*30 + "run_only_mode done" + "="*30)

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
    current = get_current_display()
    # 修改分辨率
    #run_display_resolution(config, times, random_flag)
    # 修改显示模式
    # run_display_mode(config, times)

    # config = {'HDMI-1':{'1920x1080':'60.00'},'DP-1':{'2560x1440':'60'},'DP-2':{'2560x1440':'60'}}
    # current = {'HDMI-1':{'1920x1080':'60.00'},'DP-1':{'2560x1440':'60'},'DP-2':{'2560x1440':'60'}}
    modes = list(config.keys())
    if len(modes) <= 1:
        print(f"Only support multi monitor! Please check display!")
        # return False
    # 复制模式使用current
    # run_duplicate_mode(current)
    # run_duplicate_switch_extend_mode(current,times)
    # run_duplicate_switch_only_mode(current, times)

    # 扩展模式、扩展切换独立模式
    # run_xrandr_extend_mode(config, times)
    # run_extend_switch_only_mode(config,times)

    # 独立模式
    # run_only_mode(config,times)

    # 主副屏切换
    # run_primary_switch(config,times)
    before_test(config) 