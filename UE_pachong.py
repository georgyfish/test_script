#!/usr/bin/python3
import requests
from bs4 import BeautifulSoup

# 登录URL和数据
login_url = "https://www.unrealengine.com/id/api/login"
login_data = {
    'email': '13056599771@163.com',
    'password': '1078417253yq'
}

# 创建会话对象
session = requests.Session()

# 发送登录请求
session.post(login_url, data=login_data)

# 目标URL
# url = "https://www.unrealengine.com/marketplace/en-US/profile/Epic+Games?compatibleWith=UE_4.27&count=20&platform=Linux&priceRange=%5B0%2C0%5D&sortBy=effectiveDate&sortDir=DESC&start=0"
url = "https://www.unrealengine.com/marketplace/zh-CN/profile/Epic+Games?compatibleWith=UE_4.27&count=20&platform=Linux&priceRange=%5B0%2C0%5D&sortBy=effectiveDate&sortDir=DESC&start=0"

# 获取网页内容
response = session.get(url)
response.raise_for_status()  # 确保请求成功

# 解析网页内容
soup = BeautifulSoup(response.text, 'html.parser')

# 查找所有包含demo名称的<h3><a>标签
demo_names = []
for asset in soup.select('div.asset-list-group div.asset-container.catalog.asset-full div.asset.asset--owned div.info h3 a'):
    demo_names.append(asset.get_text(strip=True))

# 输出demo名称
for name in demo_names:
    print(name)

