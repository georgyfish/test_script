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
    # print(date_list)
    work_date_list = []
    # begin_time和end_time之间日期的 去除周末的日期
    for i in date_list:
        i = datetime.datetime.strptime(i,"%Y%m%d")
        if i.weekday() < 5 :
            work_date_list.append(i.strftime("%Y%m%d"))
    print(work_date_list)
    return work_date_list

def get_deb_version(branch,begin_date,end_date):
    result = {}
    work_date_list = deal(begin_date, end_date)
    
    for work_date in work_date_list:
        rs = subprocess.Popen(f"curl https://oss.mthreads.com/product-release/{branch}/{work_date}/daily_build.txt", shell=True, close_fds=True, stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE, preexec_fn = os.setsid).communicate()
        # output = subprocess.Popen(f"curl https://oss.mthreads.com/product-release/{branch}/{work_date}/daily_build.txt",stdout=subprocess.PIPE,shell=True).communicate()
        # print(rs[0])
        rs =  rs[0].decode().strip()
        out_list = rs.splitlines()
        result[work_date] = out_list[0]
    print(result)
    return result

#download driver && install 
def install_driver(branch,begin_date,end_date):
    driver_lic = get_deb_version(branch,begin_date,end_date)
    swqa_ssh_login_cmd = "sshpass -p gfx123456 ssh swqa@192.168.114.8 -o StrictHostKeyChecking=no"
    for work_date,driver_version in driver_lic.items():
        driver_name = f"{driver_version}+dkms+glvnd-Ubuntu_amd64.deb"
        driver_url = f"https://oss.mthreads.com/product-release/{branch}/{work_date}/{driver_name}"

        cmd = f'''
            {swqa_ssh_login_cmd} 'cd /home/swqa/ && wget --no-check-certificate -q {driver_url} '
        '''
        os.system(cmd)




if __name__ == '__main__':
    install_driver('develop','20240301', '20240305')