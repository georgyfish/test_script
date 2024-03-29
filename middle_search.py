#!/usr/bin/python3
# import get_commit
import os,sys,time
from get_deb_version import get_deb_version



# driver_dic = {'20240326': ['musa_2024.03.26-D+10129', 'https://oss.mthreads.com/release-ci/repo_tags/20240326.txt', 'https://oss.mthreads.com/product-release/develop/20240326/musa_2024.03.26-D+10129+dkms+glvnd-Ubuntu_amd64.deb', 'musa_2024.03.26-D+10129+dkms+glvnd-Ubuntu_amd64.deb'], '20240327': ['musa_2024.03.27-D+10151', 'https://oss.mthreads.com/release-ci/repo_tags/20240327.txt', 'https://oss.mthreads.com/product-release/develop/20240327/musa_2024.03.27-D+10151+dkms+glvnd-Ubuntu_amd64.deb', 'musa_2024.03.27-D+10151+dkms+glvnd-Ubuntu_amd64.deb']}
# lis1 = ["commit0","commit1","commit2","commit3","commit4","commit5","commit6","commit7","commit8","commit9","commit10","commit11","commit12"]
# dic1 = {"commit0":"true","commit1":"true","commit2":"true","commit3":"true","commit4":"true","commit5":"true","commit6":"true","commit7":"true","commit8":"true","commit9":"true","commit10":"true","commit11":"true","commit12":"true"}
# lis1 = []
# for i in driver_info_dic.values():
#     lis1.append(i[0]) 

def install_driver(driver_info_dic,Test_Host_IP,index):
    driver_url_list = list(driver_info_dic.values()) 
    swqa_ssh_login_cmd = f"sshpass -p gfx123456 ssh swqa@{Test_Host_IP} -o StrictHostKeyChecking=no"
    print('=='*10 + f"Download {driver_url_list[index][-1]}" + '=='*10)
    os.system(f"{swqa_ssh_login_cmd} 'cd /home/swqa/ && wget --no-check-certificate -q {driver_url_list[index][2]} -O {driver_url_list[index][-1]}'")
    print('=='*10 +  f"sudo dpkg -i {driver_url_list[index][-1]} && sudo reboot" + '=='*10)
    # os.system(f"{swqa_ssh_login_cmd} 'sudo dpkg -i /home/swqa/{driver_url_list[index][-1]} && sudo reboot'")
    # time.sleep(150)
    try:
        for i in range(3):
            # time.sleep(10)
            ping_rs = os.system(f"timeout 5 ping {Test_Host_IP} -c 1")
            if ping_rs == 0 :
                print(f"ping {Test_Host_IP} pass!")
                break
    except:
        print(f"ping {Test_Host_IP} fail!")
        exit()
    # 安装驱动后需手动测试，并输入测试结果：
    rs = input(f"{driver_url_list[index][-1]}已安装，请执行测试并输入测试结果：")
    return rs



# 二分法查找
def middle_check(driver_info_dic):
    # left、right初始值为列表元素的序号index 最小值和最大值
    left = 0 
    count = 0
    result = []
    lis1 = []
    dic1 = {}
    for i in driver_info_dic.values():
        lis1.append(i[0]) 
    # lis1 = list(dic1.keys())
    right = len(lis1) - 1
    dic1[lis1[left]] = install_driver(driver_info_dic,Test_Host_IP,left)
    dic1[lis1[right]] = install_driver(driver_info_dic,Test_Host_IP,right)

    if dic1[lis1[left]] == dic1[lis1[right]]:
        print("此区间内，第一个元素和最后一个元素的结果相等，请确认")
        return -1
    while left <= right -2:
        #中间值为 left+right的和除2，取商
        middle = (left + right)//2 
        count += 1
        # print(f"left={left},right={right}")
        # print(f"middle={middle}")
        # print(f"dic1[lis1[middle]]={dic1[lis1[middle]]}") #这里写交互或者执行测试得到结果
        # print(f"dic1[lis1[left]]={dic1[lis1[left]]},dic1[lis1[right]]={dic1[lis1[right]]}")
        #循环结束条件：
        #后续每次只需要去拿到middle 的值
        dic1[lis1[middle]] = install_driver(driver_info_dic,Test_Host_IP,middle)
        if dic1[lis1[middle]] == dic1[lis1[left]]:
                left = middle 
        elif dic1[lis1[middle]] == dic1[lis1[right]]:
                right = middle 
        # print(f"定位到引入范围是 {lis1[left]},{lis1[right]}") 
    else:
        # print(f"count={count}")
        print(f"使用二分法{count}次确认，定位到问题引入范围是 {lis1[left]}(不发生)-{lis1[right]}(发生)之间引入") 
        result = [lis1[left],lis1[right]]
        return result

if __name__ == "__main__":
    Test_Host_IP = "192.168.114.26"
    driver_info_dic = get_deb_version('develop','20240325', '20240327') 
    print(middle_check(driver_info_dic))
