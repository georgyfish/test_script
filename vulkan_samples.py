#!/usr/bin/env python3

import os 
import time
import subprocess
import sys
import argparse

# remove 'vulkan-basic-samples', use "/vulkan-basic-samples/build/API-Samples/run_all_samples.sh"
valid_app_list=[
    'VulkanDemos-BoblChen',
    'Khronos-Vulkan-Samples',
    'Vulkan-glTF-PBR',
    'SaschaWillems-Vulkan'
    ]
# base_path = subprocess.run(['pwd'], capture_output=True, text=True, check=True).stdout
# print(base_path)
glTF_Asset_path = f"/home/swqa/xc_tool/tool/glTF-Sample-Assets/Models"
def download_glTF_Assets():
    os.chdir("/home/swqa/xc_tool/tool")
    if not os.path.exists(glTF_Asset_path):
        os.system("wget http://192.168.114.118/tool/UE/sample/glTF_Sample.tgz -O glTF_Sample.tgz \
            && tar -xvf glTF_Sample.tgz")

def get_filelist(app,path):
    result= []
    if app == 'SaschaWillems-Vulkan':
        bin_paths = ["SaschaWillems-Vulkan/build/bin"]
    elif app == "VulkanDemos-BoblChen":
        bin_paths = ["VulkanDemos-BoblChen/build/examples"]
    elif app == "Khronos-Vulkan-Samples":
        Khrons_path =  "Khronos-Vulkan-Samples/samples"
        bin_paths =  [f"{Khrons_path}/api",f"{Khrons_path}/extensions",f"{Khrons_path}/performance"]
    else:
        # Vulkan-glTF-PBR 需下载Assets
        download_glTF_Assets()
        bin_paths = [f"{glTF_Asset_path}"]
        pass
    # cmd = f"find {base_path}/{bin_path} -type f -executable -print0 | xargs -0 ls"
    
    for bin_path in bin_paths:
        cmd = f"find {path}/{bin_path} -type f -executable -print0 | xargs -0 ls | xargs -I {{}} basename {{}} |sort"
        if app == "Khronos-Vulkan-Samples":
            cmd = f"find {path}/{bin_path} -maxdepth 1 -type d ! -path {path}/{bin_path} | xargs -I {{}} basename {{}} |sort"
        elif app == "Vulkan-glTF-PBR":
            cmd = f"find {bin_path} -maxdepth 1 -type d ! -path {bin_path} | xargs -I {{}} basename {{}} |sort"

        rs = subprocess.Popen(
            cmd, 
            shell=True,
            close_fds=True,
            stdin = subprocess.PIPE,
            stdout = subprocess.PIPE, 
            stderr = subprocess.PIPE, 
            preexec_fn = os.setsid)
        for line in rs.stdout.readlines():
            line = line.decode()
            # print(line)
            str = "".join(line)
            if str != ' ' :
                result.append(str.split('\n')[0])
    return result

def Run(app,base_path,filelist):
    # filelist = get_filelist(app,base_path)
    for file in filelist:
        try:
            if app == 'SaschaWillems-Vulkan':
                work_path = f"{base_path}/SaschaWillems-Vulkan/build/bin"
            elif app == "VulkanDemos-BoblChen":
                work_path = f"{base_path}/VulkanDemos-BoblChen/build/examples"
            elif app == "Khronos-Vulkan-Samples":
                work_path = f"{base_path}/Khronos-Vulkan-Samples"
            else:
                # Vulkan-glTF-PBR
                work_path = f"{base_path}/Vulkan-glTF-PBR/bin"
            os.chdir(work_path)
        
            command = f"./{file}"
            if app == "Khronos-Vulkan-Samples":
                structure = Get_Structure()
                command = f"./build/linux/app/bin/Release/{structure}/vulkan_samples sample {file}"  
            elif app == "Vulkan-glTF-PBR":
                command = f"./Vulkan-glTF-PBR {glTF_Asset_path}/{file}/glTF/{file}.glTF"
            with open('/home/swqa/record.log','a+') as f:
                f.write(f'开始执行{file}'+'\n')
            print(command)
            os.system(command)
            time.sleep(1)
            user_input = input("输入y继续：")
            if user_input == 'y' or user_input == '':
                pass
            else:
                quit()
        except Exception as e:
            with open('/home/swqa/fail.log','a+') as f:
                f.write(file+'\n')

def Get_Structure():
    rs = subprocess.run(['uname','-m'], capture_output=True, text=True, check=True)
    structure = rs.stdout.split("\n")[0]
    return structure

def args():
    help_info = "Vulkan Samples test, use \"tail -f /home/swqa/record.log\" to record \n'vulkan-basic-samples' use '/vulkan-basic-samples/build/API-Samples/run_all_samples.sh' "
    parser = argparse.ArgumentParser(description=help_info)
    parser.add_argument('--app', type=str, choices=valid_app_list, help=f'Use vaild app in {valid_app_list}',required=True)
    parser.add_argument('--demo',type=str,help="Use --demo_name to start with demo_name")
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    structure = Get_Structure()
    base_path =  "/home/swqa/VulkanSample/VulkanSample"
    args = args()
    app = args.app
    filelist = get_filelist(app,base_path)
    print(f"{filelist}")
    if args.demo:
        demo_name = args.demo
        if demo_name in filelist:
            id = filelist.index(demo_name)
            Run(app,base_path,filelist[id:])
        else:
            print(f"{demo_name} not in {app} execute demo list")
            sys.exit(0)
    else:
        Run(app,base_path,filelist)