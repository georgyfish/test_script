#!/usr/bin/env python3

import os 
import time
import subprocess
import sys

path = "/home/georgy/VulkanDemos/build/examples"

def get_file(path):
    l1 = []
    cmd = f"ls -l {path}|grep -v -i make|" + "awk '{print $9}' "
    # file_lists = os.system(cmd)
    rs = subprocess.Popen(cmd, shell=True, close_fds=True, stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE, preexec_fn = os.setsid)
    for line in rs.stdout.readlines():
        line = line.decode()
        print(line)
        str = "".join(line)
        if str != ' ' :
            l1.append(str.split('\n')[0])
    return l1
    # file_lists = file_lists.split()
    # return file_lists


def run(file_lis):
    for file_li in file_lis:
        try:
            os.chdir(path)
        
            cmd = f"./{file_li}"
            with open('~/record.log','a+') as f:
                f.write(f'开始执行{file_li}'+'\n')
            os.system(cmd)
            time.sleep(1)
            user_input = input("输入y继续：")
            if user_input == 'y' :
                pass
            else:
                quit()
        except Exception as e:
            with open('~/fail.log','a+') as f:
                f.write(file_li+'\n')

if __name__ == "__main__":
    file_lis = get_file(path)
    if len(sys.argv) > 1:
        run(file_lis)
    else:
        if sys.argv[2] in file_lis:
            id = file_lis.index(sys.argv[2])
            run(file_lis[id:])
        else:
            exit()
        