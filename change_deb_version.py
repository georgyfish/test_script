#!/usr/bin/env python3
import sys, os
import argparse
import shutil

# https://oss.mthreads.com/product-release/release-2.1.0/20230614/musa_2.1.0-0Kylin_loongarch64.deb
def func1(deb_url, new_version, new_deb_name):
    deb_name = deb_url.spilt("/")[-1]
    oss_url = deb_url.spilt('oss.mthreads.com')[1].split(deb_name)[0]
    arch = deb_name.split('_')[-1].split('.')[0]
    #cmd = "wget -P ./tmp/ %s"%deb_url
    work_path = os.path.realpath("tmp")
    if os.path.exists(work_path):
        shutil.rmtree(work_path) #删除tmp
    # if not os.path.exists():
    #     os.mkdir(work_path)
    os.system(f"wget -P ./tmp/ {deb_url}")
    print(f"wget -P ./tmp/ {deb_url}")
    os.system(f"dpkg-deb -R {deb_name} ./tmp/")
    os.system(f'sed -i "/^Version/cVersion: {new_version}" ./tmp/DEBIAN/control')
    os.system('chmod 775 ./tmp/DEBIAN/*')
    os.system(f'dpkg-deb -b ./tmp/ {new_deb_name}')
    mc_path = os.path.realpath("/usr/local/bin/mc")
    if not os.path.exists(work_path):
        os.system('sudo wget --no-check-certificate -q http://oss.mthreads.com/installation-files/minio/2021-04-22/mc -O /usr/local/bin/mc; sudo chmod 755 /usr/local/bin/mc')
    os.system("mc alias set oss https://oss.mthreads.com product-release  product-release123")
    os.system(f"mc cp {new_deb_name} oss/{oss_url}")



func1(sys.argv[1],sys.argv[2],sys.argv[3])