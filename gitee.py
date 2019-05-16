import requests
from bs4 import BeautifulSoup
import tesserocr



# def geturl(url):
#     r = requests.get(url)
#     soup = BeautifulSoup(r.text,"lxml")
#     result = soup.select("div.item-header > div.title > a")
#     url = []
#     for i in result:
#         url.append("https://gitee.com"+i.get("href"))
#     return url

# url = "https://gitee.com/search?language=Python&page={}&q=python&type="
# urllist = []
# for i in range(1,101):
#     print("正在爬取第{}页".format(i))
#     urllist.append(geturl(url.format(i)))
# print(urllist)
# print("总共{}条数据".format(len(urllist)))


def getimage(url):
    r= requests.get("https://gitee.com/fasiondog/hikyuu/repository/archive/master.zip")
    soup = BeautifulSoup(r.text,'lxml')
    

# image_to_text()方法将图片内容转化为文本
result = tesserocr.image_to_text(image)
# 打印转化结果
print(result)