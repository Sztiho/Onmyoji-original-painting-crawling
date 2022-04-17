import requests
from bs4 import BeautifulSoup
import re
import os
import time

url = "https://yys.163.com/media/picture.html"  # 阴阳师视听站
response = requests.get(url).content.decode('utf-8')
# print(response)  # 200为成功访问
soup = BeautifulSoup(response, 'lxml')
wallpaper = soup.find_all('div', {'class': 'tab-cont'})  # 横板加竖版
# print(wallpaper)
pc = wallpaper[0].find_all('div', {'class': 'mask'})  # 横版图片
mo = wallpaper[1].find_all('div', {'class': 'mask'})  # 竖版图片

pc_list = []  # 新建一个空列表存放横版1920*1080的图片
for i in range(len(pc)):
    a = pc[i].find_all('a')
    if len(a) == 6:
        url = re.findall('href="(.*?)" target', str(a[2]))[0]  # 提取1920*1080的图片地址
                                                               # 6种分辨率  a[0]是1366x768 a[5]是2732x2048
        pc_list.append(url)
# print(pc_list) # 筛选结果

if not os.path.exists('./yys原画'):  # 文件夹是否存在
    os.mkdir('./yys原画')
os.chdir('./yys原画')

for i in range(len(pc_list)):
    time.sleep(0.8)  # 爬取延时，不加延时会出现两种情况：被网站发现，然后断开连接；或者网站被爬崩，面向监狱编程。
    img = requests.get(pc_list[i])
    if img.status_code == 200:
        open(f'{i}.jpg', 'wb').write(img.content)
        print(f'{i} 下载成功')
    else:
        print(f'{i} 下载失败  原因：{img.status_code}')
