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
        result[work_date][0]= out_list[0]
        result[work_date][1]= out_list[1]
    for work_date,driver_version in result.items():
        driver_name = f"{driver_version[0]}+dkms+glvnd-Ubuntu_amd64.deb"
        driver_url = f"https://oss.mthreads.com/product-release/{branch}/{work_date}/{driver_name}"
        result[work_date][2] = driver_url
        result[work_date][3] = driver_name
    print(result)
    return result

#download driver && install 
def install_driver(branch,begin_date,end_date):
    result = {}
    driver_dic = get_deb_version(branch,begin_date,end_date)
    date_list = list(get_deb_version(branch,begin_date,end_date).keys())
    driver_url_list = list(get_deb_version(branch,begin_date,end_date).values())
    left = 0
    right = len(driver_url_list) - 1
    Test_Host_IP = "192.168.114.8"
    for i in [left,right]:
        swqa_ssh_login_cmd = f"sshpass -p gfx123456 ssh swqa@{Test_Host_IP} -o StrictHostKeyChecking=no"
        os.system(f"{swqa_ssh_login_cmd} 'cd /home/swqa/ && wget --no-check-certificate -q {driver_url_list[i][2]} -O {driver_url_list[i][-1]}' && sudo dpkg -i {driver_url_list[i][-1]} && sudo reboot")
        time.sleep(150)
        try:
            for i in range(3):
                # time.sleep(10)
                ping_rs = os.system(f"timeout 5 ping {Test_Host_IP} -c 1")
                if ping_rs == 0 :
                    break
        except:
            print(f"ping {Test_Host_IP} fail!")
            exit()

        rs = input(f"{driver_url_list[i][-1]}已安装，请执行测试并输入测试结果：")
        result[date_list[i]] = rs





if __name__ == '__main__':
    install_driver('develop','20240301', '20240305')