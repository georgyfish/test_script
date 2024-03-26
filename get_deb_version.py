#!/usr/bin/python3
import os,sys,time
import datetime
import pandas as pd
import subprocess


def deal(begin_date, end_date):
    date_list = []
    begin_date = datetime.datetime.strptime(begin_date, "%Y%m%d")
    end_date = datetime.datetime.strptime(end_date, "%Y%m%d")
    while begin_date <= end_date:
        date_str = begin_date.strftime("%Y%m%d")
        date_list.append(date_str)
        begin_date += datetime.timedelta(days=1)
    print(date_list)
    return date_list

def get_deb_version(branch,begin_date,end_date):
    result = []
    date_list = deal(begin_date, end_date)
    work_date_list = []
    # begin_time和end_time之间日期的 去除周末的日期
    for i in date_list:
        i = datetime.datetime.strptime(i,"%Y%m%d")
        if i.weekday() < 5 :
            work_date_list.append(i.strftime("%Y%m%d"))
    swqa_ssh_login_cmd = "sshpass -p gfx123456 ssh swqa@192.168.114.8 -o StrictHostKeyChecking=no"
    for work_date in work_date_list:
        rs = subprocess.Popen(f"curl https://oss.mthreads.com/product-release/{branch}/{work_date}/daily_build.txt", shell=True, close_fds=True, stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE, preexec_fn = os.setsid)
        for line in rs.stdout.readlines():
            line = line.decode().strip()
            line_list = []
            line_list.append(line)
        result.append(line_list[0])
    print(result)
#         cmd = f'''
#         {swqa_ssh_login_cmd} "cd /home/swqa/xc_tool/ &&  ./download_driver.py -b {branch} -v {work_date}"
#         {swqa_ssh_login_cmd} "sudo dpkg -i /home/swqa/xc_tool/driver/"

# '''
#         os.system(cmd)

    print(work_date_list)

if __name__ == '__main__':
    # deal('20180221', '20180305')
    get_deb_version('develop','20240301', '20240305')