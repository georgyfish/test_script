#!/usr/bin/python3

# 1. 根据时间区间拿到deb区间，
# 2. 二分法定位  执行deb，拿到测试结果，得到deb引入区间；
# 3. 根据deb 区间，定位到UMD、KMD commit区间；
# 4. 定位UMD commit引入，
# 5. UMD定位不到，执行KMD定位；
