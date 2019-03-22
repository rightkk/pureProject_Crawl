import datetime
import re

from lxml import etree

from bs4 import BeautifulSoup


class Student:
    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def __str__(self):
        print('执行str()或print时执行__str__()函数')
        return "姓名：{}，年龄：{}，性别：{}".format(self.name, self.age, self.gender)


def readFile(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()
        html_tree = etree.HTML(html)
        result = etree.tostring(html_tree, encoding='utf-8')
        print(type(html_tree))
        print(type(result))
        print(result.decode("utf-8"))


def readHtmlFile(file_path):
    html = etree.parse(file_path, etree.HTMLParser())  # 从本地读取HTML文件，指定解析器HTMLParser，返回lxml.etree._Element对象
    # 房屋信息
    bt = html.xpath("//div[@class='house-title']/h1[1]/text()")[0]
    zj = html.xpath("//span[@class='price strongbox']/text()")[0]
    dj = html.xpath("//span[@class='unit strongbox']/text()")[0]
    hx = html.xpath('//p[@class="room"]/span[1]/text()')[0]
    zx = html.xpath('//p[@class="area"]/span[2]/text()')[0]
    cqmj = html.xpath("//div[@id='generalSituation']/descendant::ul[@class='general-item-left']/descendant::span[last()-2]/text()")[0]
    symj = html.xpath("//p[@class='area']/span[1]/text()")[0]
    cx = html.xpath("//p[@class='toward']/span[1]/text()")[0]
    jznd = html.xpath("//div[@id='generalSituation']/ descendant::ul[@class='general-item-right']/descendant::span[last()]/text()")[0]
    lc = html.xpath("//p[@class='room']/span[2]/text()")[0]
    cqnx = html.xpath("//div[@id='generalSituation']/ descendant::ul[@class='general-item-right']/descendant::span[last()-2]/text()")[0]
    fbrq = html.xpath("//p[@class='house-update-info']/span[2]/text()")[0]
    # 小区信息
    xq = html.xpath("//div[@id='xiaoWrap']/descendant::div[@class='xiaoqu-info']/h3/a/text()")[0]
    szqy = html.xpath("//div[@id='xiaoWrap']/descendant::div[@class='xiaoqu-info']/ul/li[2]/span[@class='c_333']/a[2]/text()")[0]
    xqjj = html.xpath("//div[@id='xiaoWrap']/descendant::div[@class='xiaoqu-info']/ul/li[1]/span[2]/text()")[0]
    wyf = html.xpath("//div[@id='xiaoWrap']/descendant::div[@class='xiaoqu-info']/ul/li[3]/span[2]/text()")[0]
    rjl = html.xpath("//div[@id='xiaoWrap']/descendant::div[@class='xiaoqu-info']/ul/li[4]/span[2]/text()")[0]
    lhl = html.xpath("//div[@id='xiaoWrap']/descendant::div[@class='xiaoqu-info']/ul/li[5]/span[2]/text()")[0]
    # 现场照片urls
    xczp_urls = html.xpath("//div[@class='basic-pic-list pr']/descendant::li/@data-value")

    result = etree.tostring(html)  # 解析成字节
    # result = etree.tostringlist(html)  # 解析成列表
    print(type(html))
    print(bt.strip())
    print(zj.strip())
    print(dj.strip())
    print(hx.strip())
    print(zx.strip())
    print(cqmj.strip())
    print(symj.strip())
    print(cx.strip())
    print(jznd.strip())
    print(lc.strip())
    print(cqnx.strip())
    print(fbrq.strip())
    print(xq.strip())
    print(szqy.strip())
    print(xqjj.strip())
    print(wyf.strip())
    print(rjl.strip())
    print(lhl.strip())
    print(xczp_urls)


if __name__ == '__main__':
    s = "1天前"
    s2 = re.findall("\d+", s)[0]
    print(s2)
    print((datetime.datetime.now() - datetime.timedelta(hours=22)).strftime("%Y-%m-%d %H:%M"))
    print(" ".join(["111", "222"]))
    fp = 'H:\\37325907926563x.shtml'
    try:
        readHtmlFile(fp)
    except FileNotFoundError as fe:
        print(fe.strerror)

