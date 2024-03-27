#!/usr/bin/python3
from datetime import datetime, timezone, timedelta
import middle_search

# 1. 根据时间区间拿到deb大致区间，
# 2. 二分法定位  执行deb，拿到测试结果，得到deb引入区间；
# 3. 根据deb 区间，定位到UMD、KMD commit区间；
# 4. 定位UMD commit引入，
# 5. UMD定位不到，执行KMD定位；

def get_deb_section(branch, begin_time,end_time):
    result = []
    return result

# 根据deb version拿到umd、kmd区间
def get_commit(repo, branch,list):
    result = []
    return result


contribute_deb = middle_search.middle_check(get_deb_section("develop","2024-02-29 00:00:00", "2024-03-01 00:00:00"))
umd_list = get_commit("gr-umd","develop",contribute_deb)
middle_search.middle_check(umd_list)

if __name__ == "__main__":
    pass
