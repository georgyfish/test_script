#!/usr/bin/python3
# import get_commit
import os,sys,time
from get_deb_version import get_deb_version
import subprocess
import get_commit
import umd_fallback



# driver_dic = {'20240326': ['musa_2024.03.26-D+10129', 'https://oss.mthreads.com/release-ci/repo_tags/20240326.txt', 'https://oss.mthreads.com/product-release/develop/20240326/musa_2024.03.26-D+10129+dkms+glvnd-Ubuntu_amd64.deb', 'musa_2024.03.26-D+10129+dkms+glvnd-Ubuntu_amd64.deb'], '20240327': ['musa_2024.03.27-D+10151', 'https://oss.mthreads.com/release-ci/repo_tags/20240327.txt', 'https://oss.mthreads.com/product-release/develop/20240327/musa_2024.03.27-D+10151+dkms+glvnd-Ubuntu_amd64.deb', 'musa_2024.03.27-D+10151+dkms+glvnd-Ubuntu_amd64.deb']}
# lis1 = ["commit0","commit1","commit2","commit3","commit4","commit5","commit6","commit7","commit8","commit9","commit10","commit11","commit12"]
# dic1 = {"commit0":"true","commit1":"true","commit2":"true","commit3":"true","commit4":"true","commit5":"true","commit6":"true","commit7":"true","commit8":"true","commit9":"true","commit10":"true","commit11":"true","commit12":"true"}fd

def install_deb(driver_list,driver_url_list,Test_Host_IP,index):
    swqa_ssh_login_cmd = f"sshpass -p gfx123456 ssh swqa@{Test_Host_IP} -o StrictHostKeyChecking=no"
    print('=='*10 + f"Downloading {driver_list[index]}" + '=='*10)
    os.system(f"{swqa_ssh_login_cmd} 'cd /home/swqa/ && wget --no-check-certificate -q {driver_url_list[index]} -O {driver_list[index]}'")
    print('=='*10 +  f"sudo dpkg -i {driver_list[index]} && sudo reboot" + '=='*10)
    os.system(f"{swqa_ssh_login_cmd} 'sudo dpkg -i /home/swqa/{driver_list[index]} && sudo reboot'")
    time.sleep(150)
    try:
        for i in range(3):
            # time.sleep(10)
            ping_rs = os.system(f"timeout 5 ping {Test_Host_IP} -c 1")
            if ping_rs == 0 :
                print(f"ping {Test_Host_IP} pass!")
                break
    except:
        print(f"ping {Test_Host_IP} fail!")
        sys.exit(0)

def install_umd_kmd(repo,driver_list,Test_Host_IP,index):
    swqa_ssh_login_cmd = f"sshpass -p gfx123456 ssh swqa@{Test_Host_IP} -o StrictHostKeyChecking=no"
    print('=='*10 + f"Downloading UMD commit {driver_list[index]}" + '=='*10)
    # os.system(f"{swqa_ssh_login_cmd} 'cd /home/swqa/ && wget --no-check-certificate -q {driver_url_list[index]} -O {driver_list[index]}'")
    repo = repo[-3:]
    # os.system(f"{swqa_ssh_login_cmd} wget http://192.168.114.118/tool/test.sh")
    os.system(f"{swqa_ssh_login_cmd} 'cd yq/ && ./test.sh -c {repo} -b develop -i {driver_list[index]}'")
    if repo == 'kmd':
        time.sleep(150)
        try:
            for i in range(3):
                # time.sleep(10)
                ping_rs = os.system(f"timeout 5 ping {Test_Host_IP} -c 1")
                if ping_rs == 0 :
                    print(f"ping {Test_Host_IP} pass!")
                    break
        except:
            print(f"ping {Test_Host_IP} fail!")
            sys.exit(0)

def install_driver(repo,driver_list,Test_Host_IP,index):
    # swqa_ssh_login_cmd = f"sshpass -p gfx123456 ssh swqa@{Test_Host_IP} -o StrictHostKeyChecking=no"
    if repo == 'deb':
        install_deb(driver_list,download_url,Test_Host_IP,index)
    elif repo == 'gr-umd' or repo == 'gr-kmd':
        install_umd_kmd(repo,driver_list,Test_Host_IP,index)

    # 安装驱动后需手动测试，并输入测试结果：
    rs = input(f"{driver_list[index]}已安装，请执行测试并输入测试结果，或者输入O过滤这笔commit：(Y/N/O)")
    if rs == 'O':
        print(f'过滤{driver_list[index]}这笔commit')
    return rs

# 二分查找，需要一个有序的数据类型，
def middle_search(repo,test_list):
    # left、right初始值为列表元素的序号index 最小值和最大值
    left = 0 
    right = len(driver_list) - 1
    count = 0
    result = []
    # test_list[0]的value用来存储测试结果，再对vaule的结果进行比对
    dic1 = {}
    # 正常来说左边的值应该表示不发生，右边的值表示问题发生；引入区间就在相邻的两个值不相等的元素。
    Test_Host_IP = umd_fallback.Test_Host_IP
    test_list[left][list(test_list[left].keys())[0]] = install_driver(repo,driver_list,Test_Host_IP,left)
    # test_list[list(test_list[left].keys())[0]] = install_driver(repo,driver_list,Test_Host_IP,left)
    test_list[right][list(test_list[right].keys())[0]] = install_driver(repo,driver_list,Test_Host_IP,right)
    if test_list[left][list(test_list[left].keys())[0]] == test_list[right][list(test_list[right].keys())[0]]:
        print("此区间内，第一个元素和最后一个元素的结果相等，请确认区间范围")
        return None               
    while left <= right -2 :
        middle = (left + right )//2 
        count += 1 
        test_list[middle][list(test_list[middle].keys())[0]] = install_driver(repo,driver_list,Test_Host_IP,middle)
        if test_list[middle][list(test_list[middle].keys())[0]] != None and test_list[middle][list(test_list[middle].keys())[0]] == test_list[left][list(test_list[left].keys())[0]]:
            left = middle 
        elif test_list[middle][list(test_list[middle].keys())[0]] != None and test_list[middle][list(test_list[middle].keys())[0]] == test_list[right][list(test_list[right].keys())[0]]:
            right = middle 
    print(f"使用二分法{count}次确认，定位到问题引入范围是 {test_list[left][list(test_list[left].keys())[0]]}(不发生)-{test_list[right][list(test_list[right].keys())[0]]}(发生)之间引入") 
    # return test_list[left:right]
    return [test_list[left][list(test_list[left].keys())[0]],test_list[right][list(test_list[right].keys())[0]]]
# def middle_search(repo,driver_list):
#     # left、right初始值为列表元素的序号index 最小值和最大值
#     left = 0 
#     right = len(driver_list) - 1
#     count = 0
#     result = []
#     # dic1用来存储测试结果
#     dic1 = {}
#     # 正常来说左边的值应该表示不发生，右边的值表示问题发生；引入区间就在相邻的两个值不相等的元素。
#     Test_Host_IP = umd_fallback.Test_Host_IP
#     dic1[driver_list[left]] = install_driver(repo,driver_list,Test_Host_IP,left)
#     dic1[driver_list[right]] = install_driver(repo,driver_list,Test_Host_IP,right)
#     if dic1[driver_list[left]] == dic1[driver_list[right]]:
#         print("此区间内，第一个元素和最后一个元素的结果相等，请确认区间范围")
#         return -1
#     # 当left + 1 =right时，即driver_list[left]、driver_list[right]为相邻元素时，结束循环，right即为引入
#     while left <= right -2:
#         #中间值为 left+right的和除2，取商
#         middle = (left + right)//2 
#         count += 1
#         #后续每次只需要去拿到middle 的值
#         dic1[driver_list[middle]] = install_driver(repo,driver_list,Test_Host_IP,middle)
#         if dic1[driver_list[middle]] == dic1[driver_list[left]]:
#                 left = middle 
#         elif dic1[driver_list[middle]] == dic1[driver_list[right]]:
#                 right = middle 
#         # print(f"count={count}")
#     print(f"使用二分法{count}次确认，定位到问题引入范围是 {driver_list[left]}(不发生)-{driver_list[right]}(发生)之间引入")     
#         # print(f"对应的deb的repo_tag为{driver_repo_tag[left]},{driver_repo_tag[right]}")
#         # result = {driver_list[left]:driver_repo_tag[left],driver_list[right]:driver_repo_tag[left]}
#     # return right
#     return driver_list[left:right]

if __name__ == "__main__":
    Test_Host_IP = "192.168.114.26"
    branch = 'develop'
    arch = 'x86_64'
    glvnd = '-glvnd'
    driver_info_dic = get_deb_version(branch,'20240325', '20240327') 
    driver_url_list = list(driver_info_dic.values())
    #  driver_url_list 是列表嵌入列表的格式
    driver_repo_tag = []
    driver_url_ls = []
    driver_dic = {}
    for i in driver_url_list:
        driver_dic[i[-1]] = i[2]
        driver_repo_tag.append(i[1])

    driver_list = list(driver_dic.keys())
    download_url = list(driver_dic.values())
    right = middle_search('deb',driver_list)
    if right == -1:
        print('此deb区间无法确定到问题引入范围，请往更前找')
        sys.exit(-1)
    repo_tag_list = [driver_repo_tag[right - 1],driver_repo_tag[right]]
    gr_umd_list = []
    gr_kmd_list = []
    for repo_tag in repo_tag_list:
        rs = subprocess.Popen(f"curl {repo_tag}", shell=True, close_fds=True, stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE).communicate()
        repo_tag = eval(rs[0].decode())
        gr_umd_list.append(repo_tag['gr-umd'][branch])
        gr_kmd_list.append(repo_tag['gr-kmd'][branch])
    umd_list = get_commit.get_git_commit_info("gr-umd", "develop", "2024-02-29 00:00:00", "2024-03-01 00:00:00")
    kmd_list = get_commit.get_git_commit_info("gr-kmd", "develop", "2024-02-29 00:00:00", "2024-03-01 00:00:00")
    a,b = 0,0
    for i in umd_list:
        if i == gr_umd_list[0]:
            a = umd_list.index(i)
        if i == gr_umd_list[-1]:
            b = umd_list.index(i)
    umd_list = umd_list[a:b+1]
    for i in kmd_list:
        if i == gr_kmd_list[0]:
            a = kmd_list.index(i)
        if i == gr_kmd_list[-1]:
            b = kmd_list.index(i)
    kmd_list = kmd_list[a:b+1]
    # kmd_url = []
    # for i in umd_list: 
    #     umd_url.append(f"http://oss.mthreads.com/release-ci/gr-umd/{branch}/{i}_{arch}-mtgpu_linux-xorg-release-hw{glvnd}.tar.gz")
    # for i in umd_list: 
    #     umd_url.append(f"http://oss.mthreads.com/release-ci/gr-umd/{branch}/{i}_{arch}-mtgpu_linux-xorg-release-hw{glvnd}.tar.gz")
    # 最后拿到一个umd_comp列表，一个umd_url列表；
    umd_right = middle_search('gr-umd',umd_list)
    if umd_right == -1:
        print('umd此区间不存在问题引入，相同kmd驱动，仅更换umd驱动，结果相同。后续将测试kmd引入')
        kmd_right = middle_search('gr-kmd',kmd_list)
        if kmd_right == -1 :
            print('此deb区间确实有问题引入，但更换kmd、umd无法确认引入；')
            sys.exit(-1)
        else:
            print(f'问题引入为{kmd_list[right]}')
    else:
        print(f'问题引入为{umd_list[right]}')




    driver_full_list = get_deb_version(branch,'20240325', '20240327') 
    driver_list = []
    # driver_tag_list = []
    for driver in driver_full_list:
        driver_version = driver[0]
        driver_tag = driver[1]
        driver_list.append({driver_version:None})
    print(driver_list)
    # [{'musa_2024.03.25-D+10109': None}, {'musa_2024.03.26-D+10129': None}, {'musa_2024.03.27-D+10151': None}]
    deb_rs_list = middle_search('deb',driver_list)
    if deb_rs_list == None:
        print("此deb区间无法确定到问题引入范围")
        sys.exit(-1)

    gr_umd_start_end = []
    gr_kmd_start_end = []
    for deb in deb_rs_list:
        index_of_deb = driver_full_list.index(deb)
        repo_tag_url = driver_full_list[index_of_deb][1]
        rs = subprocess.Popen(f"curl {repo_tag_url}", shell=True, close_fds=True, stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE).communicate()
        repo_tag_dict = eval(rs[0].decode())
        # {'mthreads-gmi': {'develop': '775306fcc', 'master': 'b55a66c9d'}, 'mt-media-driver': {'develop': '2a48bb594'}, 'mt-pes': {'master': 'ff3b990ba'}, 'gr-kmd': {'develop': 'cfb671a2d',\
        #  'release-2.5.0-OEM': '6e65e6285'}, 'graphics-compiler': {'master': '6bfb47527'}, 'm3d': {'master': 'fad16f82a'}, 'vbios': {'master': '79c044773'}, 'ogl': {'master': '757a3724b'}, \
        # 'd3dtests': {'master': 'a88614bcc'}, 'gr-umd': {'develop': 'da0c850b8', 'release-2.5.0-OEM': '3d2e327ca'}, 'wddm': {'develop': '11ba5447c'}}
        gr_umd_start_end.append(repo_tag_dict['gr-umd'][branch])
        gr_kmd_start_end.append(repo_tag_dict['gr-kmd'][branch])
    print(gr_umd_start_end,gr_kmd_start_end)
    umd_list = get_commit.get_git_commit_info("gr-umd", "develop", "2024-02-29 00:00:00", "2024-03-01 00:00:00")
    kmd_list = get_commit.get_git_commit_info("gr-kmd", "develop", "2024-02-29 00:00:00", "2024-03-01 00:00:00")
    index_start, index_end= 0,0
    for i in umd_list:
        if i == gr_umd_list[0]:
            index_start = umd_list.index(i)
        if i == gr_umd_list[-1]:
            index_end = umd_list.index(i)
    umd_list = umd_list[index_start:index_end+1]
    for i in kmd_list:
        if i == gr_kmd_list[0]:
            index_start = kmd_list.index(i)
        if i == gr_kmd_list[-1]:
            index_end = kmd_list.index(i)
    kmd_list = kmd_list[index_start:index_end+1]
