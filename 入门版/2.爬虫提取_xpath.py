# xpath解析
# html标签结构是一个树状的结构
# xpath解析原理：实例化一个etree对象，且将即将被解析的数据加载到该对象中
#解析本地存储的html文档：
    #etree.parse('fileName')
#解析网上爬取的html数据：
    #etree.HTML(page_text)
#使用etree对象中的xpath方法结合着不同的xpath表达式实现标签定位和数据提取

# xpath表达式
# 标签定位
    # 最左侧的/:必须要从根标签开始逐层的定位目标标签
    # 非最最侧的/:表示一个层级
    # 最左侧的//：可以从任意位置定义目标标签
    # 非最左侧的//：表示多个层级
# 属性定位：//tagName[@attrName='value']
# 索引定位：//tagName[index],index索引是从1开始
# 模糊匹配：
    # //div[contains(@class, "ng")] 定位到class属性值中包含ng的div标签
    # //div[starts-with(@class, "ta")] 定位到class属性值中是以ta开头的div标签
# 数据提取
# 取标签中的数据
    # /text():直系文本内容
    # //text()：所有的文本内容
# 取属性的数据
    # tagName/@attrName

from lxml import etree

tree = etree.parse('./test.html')#将本地存储的html文档进行解析
tree

tree.xpath('/html/head')#从根标签开始定位head标签
tree.xpath('//head') #将html文档中所有的head标签定位到

tree.xpath('/html//meta')

#定位class为song的div标签
tree.xpath('//div[@class="song"]')

tree.xpath('//li[1]')

tree.xpath('//a[@id="feng"]/text()') # /text():直系文本内容

tree.xpath('//div[@class="song"]//text()') # 所有的文本内容

tree.xpath('//a[@id="feng"]/@href')



import os
import requests
from lxml import etree
headers = {
    "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'
} 
#爬取图片数据和图片名称将其保存到本地
dirName = 'imgLibs'
if not os.path.exists(dirName):
    os.mkdir(dirName)


#第一页：http://pic.netbian.com/4kmeinv/
#非第一页：http://pic.netbian.com/4kmeinv/index_2.html
url = 'http://pic.netbian.com/4kmeinv/index_%d.html'
for page in range(1, 6): # 爬取前五页
    if page == 1:
        new_url = 'http://pic.netbian.com/4kmeinv/'
    else:
        new_url = format(url%page) #表示非第一页的url
    response = requests.get(new_url, headers = headers)
    response.encoding = 'gbk'
    page_text = response.text
    #数据解析：图片地址和图片名称
    tree = etree.HTML(page_text)
    #定位到了所有的li标签
    li_list = tree.xpath('//div[@class = "slist"]/ul/li') #全局数据解析，图片都在li标签下
    for li in li_list:
        img_src = 'http://pic.netbian.com' + li.xpath('./a/img/@src')[0] #局部的数据解析, ./表示的就是xpath调用者li对应的标签
        img_name = li.xpath('./a/img/@alt')[0] + '.jpg'
        img_data = requests.get(img_src, headers = headers).content
        filePath = dirName + '/' + img_name
        with open(filePath, 'wb') as fp:
            fp.write(img_data)
        print(img_name, '下载成功')
