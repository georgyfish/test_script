#!/usr/bin/python3

lis1 = ["commit0","commit1","commit2","commit3","commit4","commit5","commit6","commit7","commit8","commit9","commit10","commit11"]
dic1 = {"commit0":"true","commit1":"true","commit2":"true","commit3":"true","commit4":"true","commit5":"true","commit6":"true","commit7":"true","commit8":"true","commit9":"true","commit10":"true","commit11":"false","commit12":"false"}

def middle_check(lis1,dic1):
    # left、right初始值为列表元素的序号index 最小值和最大值
    left = 0 
    count = 0
    right = len(lis1) - 1
    while left <= right -2:
        #中间值为 left+right的和除2，取商
        middle = (left + right)//2 
        count += 1
        # print(f"left={left},right={right}")
        # print(f"middle={middle}")
        # print(f"dic1[lis1[middle]]={dic1[lis1[middle]]}") #这里写交互或者执行测试得到结果
        # print(f"dic1[lis1[left]]={dic1[lis1[left]]},dic1[lis1[right]]={dic1[lis1[right]]}")
        #循环结束条件：
        # if   right - left == 2:
        #     print(f"循环结束")
        #     if dic1[lis1[middle]] == dic1[lis1[left]]:
        #         left = middle 
        #     elif dic1[lis1[middle]] == dic1[lis1[right]]:
        #         right = middle 
        #     print(f"定位到引入范围是 {lis1[left]},{lis1[right]}")               
        #     break
        # elif dic1[lis1[middle]] == dic1[lis1[left]]:
        #     left = middle 
        # elif dic1[lis1[middle]]  == dic1[lis1[right]]:
        #     right = middle 
        # else:
        #     print("pass")
        if dic1[lis1[middle]] == dic1[lis1[left]]:
                left = middle 
        elif dic1[lis1[middle]] == dic1[lis1[right]]:
                right = middle 
        # print(f"定位到引入范围是 {lis1[left]},{lis1[right]}") 
    else:
        print(f"count={count}")
        print(f"定位到引入范围是 {lis1[left]},{lis1[right]}") 

if __name__ == "__main__":
    middle_check(lis1,dic1)
