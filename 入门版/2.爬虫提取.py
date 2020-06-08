# pip install beautifulsoup4

import requests
r = requests.get("https://python123.io/ws/demo.html")
demo = r.text

# 让<html>内容更加“友好”的显示
# 用prettify添加换行符
from bs4 import BeautifulSoup
soup = BeautifulSoup(demo, "html.parser")
# html.parser 解析器
print(soup.prettify())

#lxml的html解析器 BeautifulSoup(demo, "lxml")
#pip install lxml
#
#lxml的xml解析器 BeautifulSoup(demo, "xml")
#pip install lxml
#
#html5lib的解析器 BeautifulSoup(demo, "html5lib")
#pip install html5lib

# BeautifulSoup类的基本元素
# Tag 标签 用<>和</>标明开头和结尾
# Name 标签的名字 <p>...</p>的名字是p，<tag>.name
# Attributes 标签的属性 字典形式 <tag>.attrs
# NavigableString 标签内非属性字符串<>...</> <tag>.string
# Comment 标签内字符串的注释部分

from bs4 import BeautifulSoup
soup = BeautifulSoup(demo, "html.parser")
soup.title # 获取标题
tag = soup.a # 返回第一个a标签
soup.a.name
soup.a.parent.name # 包含a标签的上一层标签
soup.a.parent.parent.name

tag.attrs
tag.attrs['class'] # class属性的值
tag.attrs['href']
type(tag.attrs)
type(tag)

soup.a
soup.a.string
soup.p
soup.p.string
type(soup.p.string)

###

import requests
r = requests.get("https://python123.io/ws/demo.html")
demo = r.text
demo

# 标签树的下行遍历
# .contents 子节点的列表，将<tag>所有儿子节点存入列表
# .children 子节点的迭代类型，用于循环遍历儿子节点
# .descendants 子孙节点的迭代类型，包含所有子孙节点，用于循环遍历

soup = BeautifulSoup(demo, "html.parser")
soup.head
soup.head.contents # 显示head标签之内的内容
soup.body.contents
len(soup.body.contents) # 获取儿子节点的数量
soup.body.contents[1]

# 遍历儿子节点
for child in soup.body.children:
    print(child)

# 标签树的上行遍历
# .parent 节点的父亲标签
# .parents 节点先辈标签的迭代类型，用于循环遍历先辈节点
soup = BeautifulSoup(demo, "html.parser")
soup.title.parent
soup.html.parent

for parent in soup.a.parents:
    if parent is None: # 上行遍历会遍历到soup本身的parent，但soup的parent不存在
        print(parent)
    else:
        print(parent.name)

# 标签树的平行遍历
# .next_sibling 返回按照HTML文本顺序的下一个平行节点标签
# .previous_sibling 返回按照HTML文本顺序的上一个平行节点标签
# .next_siblings 迭代类型，返回按照HTML文本顺序的后续所有平行节点标签
# .previous_sibings 迭代类型，返回按照HTML文本顺序的前续所有平行节点标签
# 平行遍历发生在【同一个父节点下】的各节点之间

soup = BeautifulSoup(demo, "html.parser")
soup.a.next_sibling
soup.a.next_sibling.next_sibling
soup.a.previous_sibling
soup.a.previous_sibling.previous_sibling # 没有返回信息，说明前前平行节点为空
soup.a.parent

# 遍历后续节点
for sibling in soup.a.next_siblings:
    print(sibling)
# 遍历前续节点
for sibling in soup.a.previous_siblings:
    print(sibling)


from bs4 import BeautifulSoup
soup = BeautifulSoup(demo, "html.parser")
print(soup.prettify())


# 信息的标记
# XML JSON YAML
# XML
    # <name>...</name>
    # <name  />
    # <!--  -->
# JSON
    # "key" : "value"
    # "key" : ["value1", "value2"]
    # "key" : {"subkey" : "subvalue"}
# YAML
    # key : value
    """ key : #Comment
        -value1
        -value2 """
    """ key :
        subkey : subvalue """

# 提取HTML中所有URL链接
# 搜到所有<a>标签
# 解析<a>标签格式，提取href后的链接
from bs4 import BeautifulSoup
soup = BeautifulSoup(demo, "html.parser")
for link in soup.find_all('a'):
    print(link.get('href'))

# find_all 返回一个列表类型，存储查找的结果
# name 对标签名称的检索字符串
soup.find_all('a')
soup.find_all(['a','b'])
# 打印所有的标签
for tag in soup.find_all(True):
    print(tag.name)
# 用正则表达式库辅助打印所有b开头的标签    
import re
for tag in soup.find_all(re.compile('b')): # 以b开头的所有的信息作为查找的要素，打印出标签的名称
    print(tag.name)

# attrs 对标签属性值得检索字符串，可标注属性检索
# 找带有course属性值的p标签
soup.find_all('p','course')
soup.find_all(id = 'link1')
# 找link开头的
import re
soup.find_all(id = re.compile('link')) 

# recursive 是否对子孙全部检索，默认True
soup.find_all('a')
soup.find_all('a', recursive = False)
# string <>...</>中字符串区域的检索字符串
soup
soup.find_all(string = "Basic Python")
# 找所有含python的字符串
import re
soup.find_all(string = re.compile("python"))


# 爬取大学排名
# 定向爬取：仅针对输入的URL爬取，而不扩展爬取
# http://www.zuihaodaxue.com/zuihaodaxuepaiming-zongbang-2020.html
# 右键-查看源代码-搜索清华大学-找出与大学相对应的代码信息，判断爬虫是否可实现
# 查看网站的robots协议

# 格式化打印
#tplt = ''  格式化模板
#print(tplt.format(....)) 填充内容

#tplt = '{0}-{1}+{2}={3}'

#{}表示了一个槽，槽里面的内容使用key:value表示，key取值为自然数，表示序号，与后面format()的参数列表对应，value设置槽的格式，可由以下属性组合：

# 字符    用于填充单个字符
# <       左对齐
# >       右对齐
# ^       居中对齐
# 数字    槽的宽度
# ,       数字的千位分隔符
# .数字   浮点小数的精度或字符串的最大输出长度
# 类型    整型b,c,d,o,x,X，浮点型e,E,f,%

# format('a', 'b','c','d'),'a'填充到槽1内，'b'填充到槽2内，'c'填充到槽3内，'d'填充到槽4内

import requests
from bs4 import BeautifulSoup
import bs4

def getHTMLText(url): # 获取网页内容
    try:
        r = requests.get(url, timeout = 30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ""

def fillUnivList(ulist, html): # 将网页内容提取到合适的数据结构
    soup = BeautifulSoup(html, "html.parser")
    # 手动查看发现表头信息在tr标签中
    for tr in soup.find('tbody').children:
        if isinstance(tr, bs4.element.Tag): # 检测tr标签类型，如果不是bs4中的类型，则过滤掉           
            tds = tr('td')
            ulist.append([tds[0].string, tds[1].string, tds[2].string])

def printUnivList(ulist, num): # 利用数据结构展示并输出结果，num为输出前多少条结果
    print("{:^10}\t{:^6}\t{:^10}".format("排名", "校名", "位置"))
    for i in range(num):
        u = ulist[i]
        print("{:^10}\t{:^6}\t{:^10}".format(u[0], u[1], u[2]))
# {0:^10}中的0是一个序号，表示格式化输出的第0个字符，依次累加；
# {0:^10}中的10表示输出宽度约束为10个字符；
# {0:^10}中的^表示输出时居中对齐，若宽度小于字符串的实际宽度，以实际宽度输出；


def main():
    ulist = []
    url = 'http://www.zuihaodaxue.com/zuihaodaxuepaiming-zongbang-2020.html'
    html = getHTMLText(url)
    fillUnivList(ulist, html)
    printUnivList(ulist, 20)

main()

# 中文对齐问题
# 采用中文字符的空格填充chr(12288)
import requests
from bs4 import BeautifulSoup
import bs4

def getHTMLText(url): # 获取网页内容
    try:
        r = requests.get(url, timeout = 30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ""
# raise_for_status 在连接失败时会返回一个异常，此时将直接跳转到except

def fillUnivList(ulist, html): # 将网页内容提取到合适的数据结构
    soup = BeautifulSoup(html, "html.parser")
    for tr in soup.find('tbody').children: # find返回soup对象的第一个标签
        if isinstance(tr, bs4.element.Tag): # 检测tr标签类型，如果不是bs4中的类型，则过滤掉
            tds = tr('td')
            ulist.append([tds[0].string, tds[1].string, tds[2].string])

def printUnivList(ulist, num): # 利用数据结构展示并输出结果
    tplt = "{0:^10}\t{1:{3}^10}\t{2:^10}" 
    # {1:{3}^10} 1表示位置，{3}表示用第3个参数(即format里的chr(12288))来填充，^表示居中，10表示占10个位置
    print(tplt.format("排名", "校名", "位置", chr(12288)))
    for i in range(num):
        u = ulist[i]
        print(tplt.format(u[0], u[1], u[2], chr(12288)))

def main():
    ulist = []
    url = 'http://www.zuihaodaxue.com/zuihaodaxuepaiming-zongbang-2020.html'
    html = getHTMLText(url)
    fillUnivList(ulist, html)
    printUnivList(ulist, 20)

main()
