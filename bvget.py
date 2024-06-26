import requests
import os
import json
from lxml import etree

bv = input("input the bv number >> ")

url = f"https://www.bilibili.com/video/{bv}"

headers = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36", 
    "referer":  f"https://www.bilibili.com/video/{bv}"
}

print("==>正获取网页源代码...")
res = requests.get(url, headers = headers)

print("==>正解析网页源代码...")
html = etree.HTML(res.text)
src = str(html.xpath('/html/head/script[4]/text()')[0])
src = src[20:]
src_dict = json.loads(src)

print("==>正获取视频地址...")
v_url = src_dict['data']['dash']['video'][0]['backup_url'][0]
print("==>正获取音频地址...")
a_url = src_dict['data']['dash']['audio'][0]['backup_url'][0]

res = requests.get(a_url, headers = headers)
with open("a.mp3", "wb") as f:
    print("==>正写入音频...")
    f.write(res.content)

res = requests.get(v_url, headers = headers)
with open("v.mp4", "wb") as f:
    print("==>正写入视频...")
    f.write(res.content)

UserName = os.environ['USER']
path = f"/home/{UserName}/Desktop"
s = input("input absolute path for the outputfile >> ")
if s != "":
    path = s
path = path + f"/{bv}.mp4"

print("==>正写入合成的视频文件...")
os.system(f"ffmpeg -i v.mp4 -i a.mp3 -c:v copy -c:a aac -strict experimental {path}")

print("==>正删除临时文件...")
os.system("rm a.mp3 v.mp4")
