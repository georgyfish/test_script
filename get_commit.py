#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup

def get_git_commit_info(repo, branch, begin_time, end_time):
    results = []
    commit_list = []
    data = {
        # http://192.168.114.118/td/code_commit/list
        "repo" : repo,
        "branch" : branch,
        "begin_time" : begin_time,
        "end_time" : end_time
    }
    html = requests.get("http://192.168.114.118/td/code_commit/list", params=data)
    soup = BeautifulSoup(html.text, "html.parser")
    # print(soup.prettify())  #打印soup对象的内容，格式化输出
    for tr in soup.select('tbody tr'):
        commit = {}
        for td in tr.select('td'):
            commit[td['name']] = td.get_text()
        results.insert(0, commit)
    for commit in results:
        # commit_list.append(commit['short_id'])    
        commit_id = commit['short_id']
        # oss_url="https://oss.mthreads.com"
        # if repo == 'gr-umd':
        #     umd_url=f"{oss_url}/release-ci/gr-umd/{branch}/{commit_id}_{arch}-mtgpu_linux-xorg-release-hw{glvnd}.tar.gz"
        commit_list.append(commit['short_id']) 
    return commit_list

if __name__ == "__main__":
    print(get_git_commit_info("gr-kmd", "develop", "2024-02-29 00:00:00", "2024-03-01 00:00:00"))


