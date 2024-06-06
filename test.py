#!/usr/bin/python3
from datetime import datetime, timezone, timedelta
import middle_search
from get_deb_version import get_deb_version
import subprocess,os,sys,get_commit
"""
确定发生一个回退问题----》大致版本区间---》根据
1. 根据时间区间拿到deb大致区间   给定一个时间区间参数，分支参数；
    test.py develop 20240501(不发生) 2023040520(发生)
    根据时间参数--找到中间的工作日期  
    根据工作日期对应的daily_deb   
        curl --insecure https://oss.mthreads.com/product-release/develop/20240527/daily_build.txt
        f"curl --insecure https://oss.mthreads.com/product-release/{branch}/{daily_tag}/daily_build.txt"
        result = get_deb_version.get_deb_version(branch,begin_date,end_date)
        [['musa_2024.03.26-D+10129', 'https://oss.mthreads.com/release-ci/repo_tags/20240326.txt'],
          ['musa_2024.03.27-D+10151', 'https://oss.mthreads.com/release-ci/repo_tags/20240327.txt']]

2. 二分法定位:  执行deb -----> 拿到测试结果------->写入字典--->判断   ------> 继续执行deb安装-----> 拿到测试结果------->写入字典------>
判断   结束  -- 得到deb引入区间
    二分查找法，根据嵌套列表的index次序 
        每次去安装查找的那个包 得到结果 写入result 列表
        middle_search 返回一个列表[left.right], left为不发生的index , right为发生的index
    远程控制， 安装驱动deb 
    install_deb()

3. 根据deb 区间  定位到UMD、KMD commit区间 
    result[left][1] = 'https://oss.mthreads.com/release-ci/repo_tags/20240326.txt'
    result[left][2] = 'https://oss.mthreads.com/release-ci/repo_tags/20240327.txt'
    curl 'https://oss.mthreads.com/release-ci/repo_tags/20240326.txt'  ---》 {"mthreads-gmi":{"develop":"15d1e9380","master":"8ee556f92"},"mt-pes":{"master":"7202a31dc"},"mt-management":\
        {"develop":"dad852321","master":"6c374091d"},"mt-media-driver":{"develop":"7e4ecb1cc"},"DirectStream":{"develop":"208e5240d"},"gr-kmd":{"develop":"69d7e3104",\
            "release-2.5.0-OEM":"8c51763a1"},"graphics-compiler":{"master":"545ffa3a9"},"m3d":{"master":"a9567d601"},"mtdxum":{"master":"9cac086dd"},"d3dtests":{"master":"bd0358ed2"},\
                "ogl":{"master":"44be1b68a"},"gr-umd":{"develop":"6dd19a265","release-2.5.0-OEM":"27a85ebf5"},"wddm":{"develop":"d23c6060d"}}
    字典嵌套字典  
        dict['gr-umd']["develop"]  ---> UMD commitID


4. 定位UMD commit引入
    获取UMD commitID 列表
    方法一：
        爬取commit网页，修改begin时间和end时间，筛选出一个umd_commit list，再根据第3步获取的区间，截取、切片找到需要的umd_commit_list；
    方法二：
        使用get_lib.get_git_commit_info() 获取所有的git commit信息，再写一个根据第3步获取的区间得到需要的umd_commit_list的方法；
    

5. UMD定位不到  执行KMD定位

定位umd_commit:
1. get_commit   commit_begin  commit_end
2. middle_search()----> 区间

"""


def get_deb_section(branch, begin_time,end_time):
    result = []
    return result

# 根据deb version拿到umd、kmd区间
# def get_commit(list):
#     result = []
#     return result

# branch = 'develop'
# driver_dic = {'musa_2024.03.26-D+10129': 'https://oss.mthreads.com/release-ci/repo_tags/20240326.txt', 'musa_2024.03.27-D+10151': 'https://oss.mthreads.com/release-ci/repo_tags/20240326.txt'}
# driver_info_dic = get_deb_version('develop','20240325', '20240327') 
# # {'20240325': ['musa_2024.03.25-D+10109', 'https://oss.mthreads.com/release-ci/repo_tags/20240325.txt', 'https://oss.mthreads.com/product-release/develop/20240325/musa_2024.03.25-D+10109+dkms+glvnd-Ubuntu_amd64.deb', 'musa_2024.03.25-D+10109+dkms+glvnd-Ubuntu_amd64.deb'], '20240326': ['musa_2024.03.26-D+10129', 'https://oss.mthreads.com/release-ci/repo_tags/20240326.txt', 'https://oss.mthreads.com/product-release/develop/20240326/musa_2024.03.26-D+10129+dkms+glvnd-Ubuntu_amd64.deb', 'musa_2024.03.26-D+10129+dkms+glvnd-Ubuntu_amd64.deb'], '20240327': ['musa_2024.03.27-D+10151', 'https://oss.mthreads.com/release-ci/repo_tags/20240327.txt', 'https://oss.mthreads.com/product-release/develop/20240327/musa_2024.03.27-D+10151+dkms+glvnd-Ubuntu_amd64.deb', 'musa_2024.03.27-D+10151+dkms+glvnd-Ubuntu_amd64.deb']}
# repo_tag_list = list(driver_dic.values())
# gr_umd_list = []
# gr_kmd_list = []
# for repo_tag in repo_tag_list:
#     rs = subprocess.Popen(f"curl {repo_tag}", shell=True, close_fds=True, stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE).communicate()
#     repo_tag = eval(rs[0].decode())
#     gr_umd_list.append(repo_tag['gr-umd'][branch])
#     gr_kmd_list.append(repo_tag['gr-kmd'][branch])
    

# contribute_deb = middle_search.middle_check(get_deb_section("develop","2024-02-29 00:00:00", "2024-03-01 00:00:00"))
# umd_list = get_commit("gr-umd","develop",contribute_deb)
# middle_search.middle_check(umd_list)

def slice_full_list(start_end_list, full_list):
    if start_end_list[0] in full_list:
        index_start = full_list.index(start_end_list[0])
    else:
        print("input error!")
        sys.exit(-1)
    if start_end_list[1] in full_list:
        index_end = full_list.index(start_end_list[1])
    else:
        print("input error!")
        sys.exit(-1)        
    return full_list[index_start:index_end+1]

begin_date = '20240527'
end_date = '20240529'
branch = 'develop'

if __name__ == "__main__":
    # begin_date = '20240527'
    # end_date = '20240529'
    # branch = 'develop'
    driver_full_list = get_deb_version(branch,begin_date, end_date) 
    driver_list = []
    # driver_tag_list = []
    for driver in driver_full_list:
        driver_version = driver[0]
        driver_tag = driver[1]
        driver_list.append(driver_version)
    print(driver_list)
    # deb_rs_list = middle_search('deb',driver_list)
    deb_rs_list = ['musa_2024.05.28-D+11235', 'musa_2024.05.29-D+11244']
    if not deb_rs_list:
        print("此deb区间无法确定到问题引入范围")
        sys.exit(-1)

    gr_umd_start_end = []
    gr_kmd_start_end = []
    for deb in deb_rs_list:
        index_of_deb = driver_list.index(deb)
        repo_tag_url = driver_full_list[index_of_deb][1]
        rs = subprocess.Popen(f"curl {repo_tag_url}", shell=True, close_fds=True, stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE).communicate()
        repo_tag_dict = eval(rs[0].decode())
        # {'mthreads-gmi': {'develop': '775306fcc', 'master': 'b55a66c9d'}, 'mt-media-driver': {'develop': '2a48bb594'}, 'mt-pes': {'master': 'ff3b990ba'}, 'gr-kmd': {'develop': 'cfb671a2d',\
        #  'release-2.5.0-OEM': '6e65e6285'}, 'graphics-compiler': {'master': '6bfb47527'}, 'm3d': {'master': 'fad16f82a'}, 'vbios': {'master': '79c044773'}, 'ogl': {'master': '757a3724b'}, \
        # 'd3dtests': {'master': 'a88614bcc'}, 'gr-umd': {'develop': 'da0c850b8', 'release-2.5.0-OEM': '3d2e327ca'}, 'wddm': {'develop': '11ba5447c'}}
        gr_umd_start_end.append(repo_tag_dict['gr-umd'][branch])
        gr_kmd_start_end.append(repo_tag_dict['gr-kmd'][branch])
    print(f"umd区间为{gr_umd_start_end}\nkmd区间为{gr_kmd_start_end}")
    begin_date_datetime = datetime.strptime(begin_date,"%Y%m%d")
    end_date_datetime = datetime.strptime(end_date,"%Y%m%d")
    previous_day = begin_date_datetime - timedelta(days=1)
    # 设置时间为12:00
    previous_day_at_noon = previous_day.replace(hour=12, minute=0, second=0)
    end_date = end_date_datetime.replace(hour=23,minute=0,second=0)
    # 格式化输出
    commit_begin_date = previous_day_at_noon.strftime("%Y-%m-%d %H:%M:%S")
    commit_end_date = end_date.strftime("%Y-%m-%d %H:%M:%S")
    print(f"查询开始时间：{commit_begin_date}\n查询结束时间：{commit_end_date}")    

    umd_list = get_commit.get_git_commit_info("gr-umd", branch, commit_begin_date , commit_end_date)
    kmd_list = get_commit.get_git_commit_info("gr-kmd", branch, commit_begin_date , commit_end_date)
    # index_start, index_end= 0,0
    umd_search_list = slice_full_list(gr_umd_start_end,umd_list)
    kmd_search_list = slice_full_list(gr_kmd_start_end,kmd_list)
    # for umd in umd_list:
    #     if umd_list.index(umd) >= umd_list.index(gr_umd_start_end[0]) and umd_list.index(umd) <= umd_list.index(gr_umd_start_end[1]):
    #         umd_search_list.append({umd:None})
    # for kmd in kmd_list:
    #     if kmd_list.index(kmd) >= kmd_list.index(gr_kmd_start_end[0]) and kmd_list.index(kmd) <= kmd_list.index(gr_kmd_start_end[1]):
    #         kmd_search_list.append({umd:None})

    print(f"umd_list：{umd_search_list}\nkmd_list：{kmd_search_list}")



