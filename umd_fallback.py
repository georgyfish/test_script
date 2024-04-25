#!/usr/bin/python3
import os,sys,time
import subprocess
import get_commit
import middle_search,bs4

#提供一个入口，手动添加umd_list

def umd_fallback(repo,umd_list):
    umd_result = middle_search.middle_search(repo,umd_list)
    if umd_result == -1:
        print('umd此区间不存在问题引入，相同kmd驱动，仅更换umd驱动，结果相同。后续将测试kmd引入')      
    else:
        print(f'问题引入为{umd_result}')
    return umd_result

Test_Host_IP = "192.168.114.8"
if __name__ == "__main__":
    
    repo = 'gr-umd'
    branch = 'develop'
    begin_time = "2024-04-23 00:00:00"
    end_time = "2024-04-24 00:00:00"
    umd_list = get_commit.get_git_commit_info(repo, branch, begin_time, end_time)
    if len(sys.argv) != 1 and len(sys.argv) != 2:
        commit_begin = sys.argv[1]
        commit_end = sys.argv[2]
        a,b = 0,0
        for i in umd_list:
            if i == commit_begin:
                a = umd_list.index(i)
            if i == commit_end:
                b = umd_list.index(i)
        umd_list = umd_list[a:b+1]
    print(umd_list)
    umd_fallback(repo,umd_list)