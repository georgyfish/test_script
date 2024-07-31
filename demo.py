from tabulate import tabulate
from time import sleep
# 示例数据
deb_list = [
    'musa_2024.07.11-D+375',
    'musa_2024.07.12-D+378',
    'musa_2024.07.13-D+379',
    'musa_2024.07.14-D+392',
    'musa_2024.07.15-D+418']

# data = [
#     ["deb", '1.1', ""],
#     ["deb", '1.2', ""],
#     ["deb", '1.3', ""],
#     ["deb", '1.4', ""],
#     ["deb", '1.5', ""],
#     ["deb", '1.5', ""],
#     ["deb", '1.5', ""],
#     ["deb", '1.5', ""],
#     ["deb", '1.5', ""],
#     ["deb", '1.5', ""],
#     ["deb", '1.5', ""],
#     ["deb", '1.5', ""],
#     ["deb", '1.5', ""],
#     ["deb", '1.5', ""],
# ]

# 定义表头
def testcase(driver):
    
    rs = input(f"{driver}测试结果：pass/fail\n")
    return rs

def func(repo,data):
    # left = 0 
    # right = len(data) - 1
    # middle = (left + right )//2 
    # data[middle][-1] = '1'
    headers = [repo, "Version/Commit", "result"]
    table = tabulate(data, headers=headers, tablefmt="grid")
    print(table)
    sleep(2)
    return table

def middle_search(repo,middle_search_list):
    data  = []
    for driver in middle_search_list:
        data.append([driver,''])
    # left、right初始值为列表元素的序号index 最小值和最大值
    left = 0 
    right = len(middle_search_list) - 1
    count = 1
    # right_value = "fail"
    if repo == 'deb':
        right_value =  "fail"
        data[right][-1] = right_value
        func(repo,data)
        left_value = testcase(middle_search_list[left])
        data[left][-1] = left_value
        func(repo,data)
    else:
        func(repo,data)
        left_value = testcase(middle_search_list[left])
        data[left][-1] = left_value
        func(repo,data)

        right_value = testcase(middle_search_list[right])
        data[right][-1] = right_value
        func(repo,data)
        sleep(2)
    #     if pc_list:
    #         left_value = install_driver(repo,middle_search_list[left],Pc,Pc_info,branch,pc_list[left])
    #     else:
    #         left_value = install_driver(repo,middle_search_list[left],Pc,Pc_info,branch)
    # else:
    #     left_value = install_driver(repo,middle_search_list[left],Pc,Pc_info,branch)
    #     right_value = install_driver(repo,middle_search_list[right],Pc,Pc_info,branch)
    if left_value == right_value:
        print(f"{middle_search_list}区间内第一个元素和最后一个的结果相同，请确认区间范围")
        return None               
    while left <= right -2 :
        middle = (left + right )//2 
        count += 1 
        func(repo,data)
        mid_value = input(f"{middle_search_list[middle]}\tinput pass or fail\n")
        data[middle][-1] = mid_value
        func(repo,data)
        if mid_value != None and mid_value == left_value:
            left = middle 
        elif mid_value != None and mid_value == right_value:
            right = middle 
    print(f"总共{count}次查找\n\n定位到问题引入范围是：\"{middle_search_list[left]}\"(不发生)-\"{middle_search_list[right]}\"(发生)之间引入") 
    return middle_search_list[left:right+1]

# 输出表格到命令行
# UMD_table = tabulate(data, headers=headers, tablefmt="grid")
# print(UMD_table)

# data[0][-1] = 'pass'
# UMD_table = tabulate(data, headers=headers, tablefmt="grid")
# print(UMD_table)

# data[-1][-1] = 'fail'
# UMD_table = tabulate(data, headers=headers, tablefmt="grid")
# print(UMD_table)

middle_search('deb',deb_list)