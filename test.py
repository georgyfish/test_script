#!/usr/bin/python3
from datetime import datetime, timezone, timedelta
import middle_search
from get_deb_version import get_deb_version
import subprocess
"""
1. 根据时间区间拿到deb大致区间，
2. 二分法定位:  执行deb -----> 拿到测试结果------->写入字典--->判断   ------> 继续执行deb安装-----> 拿到测试结果------->写入字典------>
判断   结束  -- 得到deb引入区间；
3. 根据deb 区间，定位到UMD、KMD commit区间；
4. 定位UMD commit引入，
5. UMD定位不到，执行KMD定位；

"""


def get_deb_section(branch, begin_time,end_time):
    result = []
    return result

# 根据deb version拿到umd、kmd区间
def get_commit(list):
    result = []
    return result

branch = 'develop'
driver_dic = {'musa_2024.03.26-D+10129': 'https://oss.mthreads.com/release-ci/repo_tags/20240326.txt', 'musa_2024.03.27-D+10151': 'https://oss.mthreads.com/release-ci/repo_tags/20240326.txt'}
driver_info_dic = get_deb_version('develop','20240325', '20240327') 
# {'20240325': ['musa_2024.03.25-D+10109', 'https://oss.mthreads.com/release-ci/repo_tags/20240325.txt', 'https://oss.mthreads.com/product-release/develop/20240325/musa_2024.03.25-D+10109+dkms+glvnd-Ubuntu_amd64.deb', 'musa_2024.03.25-D+10109+dkms+glvnd-Ubuntu_amd64.deb'], '20240326': ['musa_2024.03.26-D+10129', 'https://oss.mthreads.com/release-ci/repo_tags/20240326.txt', 'https://oss.mthreads.com/product-release/develop/20240326/musa_2024.03.26-D+10129+dkms+glvnd-Ubuntu_amd64.deb', 'musa_2024.03.26-D+10129+dkms+glvnd-Ubuntu_amd64.deb'], '20240327': ['musa_2024.03.27-D+10151', 'https://oss.mthreads.com/release-ci/repo_tags/20240327.txt', 'https://oss.mthreads.com/product-release/develop/20240327/musa_2024.03.27-D+10151+dkms+glvnd-Ubuntu_amd64.deb', 'musa_2024.03.27-D+10151+dkms+glvnd-Ubuntu_amd64.deb']}
repo_tag_list = list(driver_dic.values())
gr_umd_list = []
gr_kmd_list = []
for repo_tag in repo_tag_list:
    rs = subprocess.Popen(f"curl {repo_tag}", shell=True, close_fds=True, stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE).communicate()
    repo_tag = eval(rs[0].decode())
    gr_umd_list.append(repo_tag['gr-umd'][branch])
    gr_kmd_list.append(repo_tag['gr-kmd'][branch])
    

contribute_deb = middle_search.middle_check(get_deb_section("develop","2024-02-29 00:00:00", "2024-03-01 00:00:00"))
umd_list = get_commit("gr-umd","develop",contribute_deb)
middle_search.middle_check(umd_list)

if __name__ == "__main__":
    pass
