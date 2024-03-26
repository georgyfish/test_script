#!/usr/bin/python3
# import get_commit
# import get_deb_test_result

lis1 = ["commit0","commit1","commit2","commit3","commit4","commit5","commit6","commit7","commit8","commit9","commit10","commit11","commit12"]
dic1 = {"commit0":"true","commit1":"true","commit2":"true","commit3":"true","commit4":"true","commit5":"true","commit6":"true","commit7":"true","commit8":"true","commit9":"true","commit10":"true","commit11":"true","commit12":"true"}


def middle_check(lis1):
    # left、right初始值为列表元素的序号index 最小值和最大值
    left = 0 
    count = 0
    result = []
    right = len(lis1) - 1
    # dic1[lis1[left]] = get_deb_test_result(lis1[left])
    # dic1[lis1[right]] = get_deb_test_result(lis1[right])
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
        if dic1[lis1[middle]] == dic1[lis1[left]]:
                left = middle 
        elif dic1[lis1[middle]] == dic1[lis1[right]]:
                right = middle 
        # print(f"定位到引入范围是 {lis1[left]},{lis1[right]}") 
    else:
        print(f"count={count}")
        print(f"定位到引入范围是 {lis1[left]}(VNP)-{lis1[right]}(VP)之间引入") 
        result = [lis1[left],lis1[right]]
        return result

if __name__ == "__main__":

    print(middle_check(lis1))
