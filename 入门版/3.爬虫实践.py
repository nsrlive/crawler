# Re(正则表达式)库入门Regular Expression
# 正则表达式是用来简洁表达一组字符串的表达式

#'PN'
#'PYN'
#'PYTN'
#'PYTHN'
#'PYTHON'
#正则表达式：P(Y|YT|YTH|YTHO)?N

#'PY'
#'PYY'
#'PYYY'
#...
#'PYYYY...'
#正则表达式：PY+

#'PY'开头
#后续存在不多于10个字符
#后续字符不能是'P'或'Y'
#'PYABC'可以
#'PYXYZ'不可以
# 正则表达式：PY[^PY]{0,10}

# 编译
# regex = '正则表达式'
# p=re.compile(regex)

# 正则表达式的常用操作符
# .表示任何单个字符
# []字符集，对单个字符给出取值范围，[abc]表示a,b,c，[a-z]表示a到z单个字符
# [^ ] 非字符集，对单个字符给出排除范围，[^abc]表示非a或b或c的单个字符
# * 星号前一个字符0次或无限次扩展，abc*表示ab,abc,abcc,abccc等
# + 加号前一个字符1次或无限次扩展，abc+表示abc,abvv,abccc等
# ? 问号前一个字符0次或1次扩展，abc?表示ab,abc
# | 左右表达式任意一个，abc|def表示abc,def
# {m} 扩展前一个字符m次，ab{2}c表示abbc
# {m,n} 扩展前一个字符m至n次（包括n），ab{1,2}c表示abc,abbc
# ^ 匹配字符串开头，^abc表示abc且在一个字符串的开头
# $ 匹配字符串结尾，abc$表示abc且在一个字符串的结尾
# () 分组标记，内部只能使用| （即“或”）操作符，(abc)表示abc，(abc|def)表示abc、def
# \d 数字，等价于[0-9]
# \w 单词字符，等价于[A-Za-z0-9_]

# P(Y|YT|YTH|YTHO)?N
# 'PN','PYN','PYTN','PYTHN','PYTHON'

# PYTHON+
# 'PYTHON','PYTHONN','PYTHONNN'...

# PY[TH]ON 
# 'PYTON','PYHON'

# PY[^TH]?ON
# 'PYON','PTaON','PYbON','PYcON'... 只要不是T H

# PY{:3}N  扩展Y 0到3次
# 'PN','PYN','PYYN','PYYYN'

# ^[A-Za-z]+$  由26个字母组成的字符串
# ^[A-Za-z0-9]+$  由26个字母和数字组成的字符串
# ^-?\d+$  整数形式的字符串
# ^[0-9]*[1-9][0-9]*$  正整数形式的字符串
# [1-9]\d{5}  中国境内邮政编码6位
# [\u4e00-\u9fa5]  匹配中文字符
# \d{3}-\d{8}|\d{4}-\d{7}  国内电话号码 010-68913536

# 匹配ID地址的正则表达式
# \d+.\d+.\d+.\d+
# /d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}
# 不够精确，取值需要0-255
# 0-99  [1-9]?\d
# 100-199  1\d{2}
# 200-249  2[0-4]\d
# 250-255  25[0-5]
# (([1-9]?\d|1\d{2}|2[0-4]\d|25[0-5]).){3}([1-9]?\d|1\d{2}|2[0-4]\d|25[0-5])

# /Chapter [1-9][0-9]*/  表示任意章节数
# /Chapter [0-9]{1,2}/   表示0-99章节，包括chapter 0
# /Chapter [1-9][0-9]?/  表示1-99章节，不包括chapter 0。该表达式也可以使用/Chapter [1-9][0-9]{0,1}/ 表示


# Re库的基本使用
# import re
# r'正则表达式'

# Re库主要功能函数
# re.search() 在一个字符串中搜索匹配正则表达式的第一个位置，返回match对象
    # re.search(pattern, string, flags=0)
    # re.search(正则或原生字符串, 待匹配字符串, 控制标记)
    # 控制标记 re.I re.IGNORECASE 忽略大小写
    # re.M re.MULTILINE 正则表达式中^能够将给定字符串的每行当作匹配开始
    # re.S re.DOTALL 正则表达式中的.能够匹配所有字符，默认匹配除换行外所有字符
import re
match = re.search(r'[1-9]\d{5}', 'BIT 100081')
if match:
    print(match.group(0))
# [1-9]:表示1到9任意一个数字，邮编没有0开头的
# \d{5}:表示0-9任意5个数字组合 ({5}表示匹配连续的五个\d)
# [1-9]占了一位，\d{5}占了5位    
# group(0)匹配正则表达式整体结果

# re.match() 从一个字符串的开始位置起匹配正则表达式，返回match对象
    # re.match(pattern, string, flags=0)
    # re.match(正则或原生字符串, 待匹配字符串, 控制标记)
import re
match = re.match(r'[1-9]\d{5}', '100081 BIT')
if match:
    print(match.group(0))

# re.findall() 搜索字符串，以列表形式返回全部匹配的子串
    # re.findall(pattern, string, flags=0)
    # re.findall(正则或原生字符串, 待匹配字符串, 控制标记)
import re
ls = re.findall(r'[1-9]\d{5}', 'BIT100081 TSU100084')
ls

# re.split() 将一个字符串按照正则表达式匹配结果进行分割，返回列表类型
    # re.split(pattern, string, maxsplit = 0, flags=0)
    # re.split(正则或原生字符串, 待匹配字符串, 最大分割数(剩余部分作为最后一个元素输出), 控制标记)
import re
re.split(r'[1-9]\d{5}', 'BIT100081 TSU100084')
# 将匹配的部分去掉
re.split(r'[1-9]\d{5}', 'BIT100081 TSU100084', maxsplit = 1)
# 观察区别

# re.finditer() 搜索字符串，返回一个匹配结果的迭代类型，每个迭代元素是match对象
    # re.finditer(pattern, string, flags=0)
    # re.finditer(正则或原生字符串, 待匹配字符串, 控制标记)
import re
for m in re.finditer(r'[1-9]\d{5}', 'BIT100081 TSU100084'):
    if m:
        print(m.group(0))

# re.sub 在一个字符串中替换所有匹配正则表达式的子串，返回替换后的字符串
    # re.sub(pattern, repl, string, count = 0, flags=0)
    # re.sub(正则或原生字符串, 用于替换的字符串, 待匹配字符串, 匹配的最大替换次数, 控制标记)
import re
re.sub(r'[1-9]\d{5}', ':zipcode', 'BIT100081 TSU100084')

# Re库的另一种等价用法
# 一次性操作
rst = re.search(r'[1-9]\d{5}', 'BIT100081')
# 编译后多次操作
pat = re.compile(r'[1-9]\d{5}')
rst = pat.search('BIT100081')

# regex = re.compile(pattern, flags = 0)
# re.compile(正则或原生字符串, 控制标记)

# Re库的match对象
match = re.search(r'[1-9]\d{5}', 'BIT100081')
# 判断match是否成立
if match:
    print(match.group(0))
type(match)

# match对象的属性
# .string 待匹配的文本
# .re 匹配时使用的正则表达式
# .pos 正则表达式搜索文本的开始位置
# .endpos 正则表达式搜索文本的结束位置

# match对象的方法
# .group(0) 获得匹配后的字符串
# .start() 匹配字符串在原始字符串的开始位置
# .end() 匹配字符串在原始字符串的结束位置
# .span() 返回(.start(), .end())

import re
m = re.search(r'[1-9]\d{5}', 'BIT100081 TSU100084')
# 分别执行
m.string
m.re
m.pos
m.endpos

m.group(0)
m.start()
m.end()
m.span()

# Re库的贪婪匹配和最小匹配
match = re.search(r'PY.*N', 'PYANBNCNDN')
match.group(0)
# Re库默认采用贪婪匹配，即输出匹配最长的字符串

# 如何输出最短的字符串——加问号
match = re.search(r'PY.*?N', 'PYANBNCNDN')
match.group(0)

# 最小匹配操作符
# *? 前一个字符0次或无限次扩展，最小匹配
# +? 前一个字符1次或无限次扩展，最小匹配
# ?? 前一个字符0次或1次扩展，最小匹配
# {m,n}? 扩展前一个字符m至n次（含n），最小匹配


# 实例：淘宝商品比价定向爬虫
# 获取淘宝搜索页面的信息，提取其中的商品名称和价格
# 搜索接口和翻页的处理

# 起始页
# https://s.taobao.com/search?q=switch&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20200608&ie=utf8
# 第二页 s=44
# https://s.taobao.com/search?q=switch&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20200608&ie=utf8&bcoffset=1&ntoffset=1&p4ppushleft=2%2C48&s=44
# 第三页 s=88
# https://s.taobao.com/search?q=switch&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20200608&ie=utf8&bcoffset=-2&ntoffset=-2&p4ppushleft=2%2C48&s=88
# 猜测，44 88是当前页起始商品的编号

# 提交商品搜索请求，循环获取页面
# 对于每个页面，提取商品名称和价格信息 善用查看源代码，找价格名字的键值对
# 将信息输出到屏幕上

# 淘宝的反爬虫机制，会使得未登录则不可访问，所以我们得先登录，并获取cookie
# header中需要有cookie和user-agent字段，cookie是为了模拟登录

import requests
import re

def getHTMLText(url):
    try:
        coo = 'cna=n9MKFpFgyn0CAYP7/N31lPeL; hng=GLOBAL%7Czh-CN%7CUSD%7C999; t=69c32f86035fd98e3ef377cfd702a278; tracknick=niusiruilive; enc=QmSp9WEsuCjFJLlfk2h%2FwEoGbN7YNiGtK0D5Q22yBYg9WEovEVhKPfxXGyHpLYweAihnrIf2BU71CaDHceIt0Q%3D%3D; _m_h5_tk=cf42d562873ebe151b8b014afd135872_1591559847063; _m_h5_tk_enc=04ec4cd6baf56c1af42b6e3a407bd31b; cookie2=1a4b54a201400ee59bc0918946862c78; _tb_token_=f8e11aafeee83; alitrackid=world.taobao.com; _samesite_flag_=true; sgcookie=ELORYyxFTDwNgbO8bZOUn; unb=740672566; uc3=id2=VAXb2dp%2Fhrw9&lg2=VT5L2FSpMGV7TQ%3D%3D&vt3=F8dBxGDe2IHHVQ8FfX4%3D&nk2=De68obbZ8%2BRbCuzi; csg=2c5d06dc; lgc=niusiruilive; cookie17=VAXb2dp%2Fhrw9; dnk=niusiruilive; skt=f9bd5c19a6298297; existShop=MTU5MTU2MTg5Nw%3D%3D; uc4=id4=0%40Vhz5su5fSLb74Qo9yfk08cnr0w0%3D&nk4=0%40Dzurn%2F74JgvhPFDj1aqjepQBoYkSwMA%3D; publishItemObj=Ng%3D%3D; _cc_=VT5L2FSpdA%3D%3D; _l_g_=Ug%3D%3D; sg=e6c; _nk_=niusiruilive; cookie1=BYbypMxvkPZ7HGMYvwIzOyGsQm%2BI%2BuzzqKwzokufPx8%3D; JSESSIONID=4EE63E17ED02F6AC4ABECA553DFE1C39; lastalitrackid=login.taobao.com; tfstk=ci_hBPbE4M-QoMtGcyTCZuzLatqAZ5weLa7d7wahfBeldsQNiIiZ0kGLsdPks01..; mt=ci=4_1; uc1=cookie15=URm48syIIVrSKA%3D%3D&cookie14=UoTV7X%2BwyghtrA%3D%3D&pas=0&cookie21=UIHiLt3xTIkz&existShop=false&cookie16=UIHiLt3xCS3yM2h4eKHS9lpEOw%3D%3D; l=eBrOB2tlQphV7qM9KO5Z-urza779yIdfGsPzaNbMiInca1-hTFGwWNQDd66k7dtj3t5nMety9_1AhRn2-kaLRx15WMfpRs5mpL968e1..; isg=BHNzIrVJKcfhduXb9hkJHPSMAnedqAdqcHUk4CURexLJJJfGrXnKulr23kTKhF9i'
        cookies = {}
        for line in coo.split(';'): # 模拟登录
            name, value = line.strip().split('=', 1)
            cookies[name] = value
        hd = {'user-agent':'Mozilla/5.0'}
        r = requests.get(url, cookies=cookies, headers = hd, timeout = 30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return "该网页请求连接失败"

def parsePage(ilt, html):
    try:
        plt = re.findall(r'\"view_price\"\:\"[\d\.]*\"', html)
        tlt = re.findall(r'\"raw_title\"\:\".*?\"', html)
        sal = re.findall(r'\"view_sales\"\:\"[\d\.]*[\u4e00-\u9fa5]?\+?人付款\"', html)
        # [\u4e00-\u9fa5]表示中文字符
        for i in range(len(plt)):
            price = eval(plt[i].split(':')[1])
            title = eval(tlt[i].split(':')[1])
            sales = eval(sal[i].split(':')[1])
            ilt.append([price, title, sales])
    except:
        print("解析网页出现异常")
# "view_price\" 点进任一商品页面，右键查看源代码，商品价格的html属性为view_price
# "raw_title\" 商品名称的的html属性为raw_title，‘\"’匹配双引号，‘view_price’匹配view_price
# ‘\:’匹配冒号，‘\d\.’匹配一个整数加一个小数点，‘[]*’*号匹配中括号内的正则表达式，商品名称同理，其中‘.*?’用于匹配前面频繁或重复出现符号的非贪婪版本，这里用于匹配最短数目的同性质字符，如下图。


def printGoodsList(ilt):
    tplt = "{:4}\t{:8}\t{:16}\t{:8}"
    print(tplt.format("序号", "价格", "商品名称", "商品销量"))
    count = 0
    for g in ilt:
        count = count + 1
        print(tplt.format(count, g[0], g[1], g[2]))

def main():
    goods = 'switch'
    depth = 2
    start_url = 'https://s.taobao.com/search?q=' +goods
    infoList = []
    for i in range(depth):
        try:
            url = start_url + '&s=' +str(44*i)
            html = getHTMLText(url)
            parsePage(infoList, html)
        except:
            continue #如果某一个页面出现了问题，则会跳过该页面的解析，而不会影响程序的整体运行
    printGoodsList(infoList)

main()


############################################

# "^\\d+$"　　//非负整数（正整数 + 0） 
# "^[0-9]*[1-9][0-9]*$"　　//正整数 
# "^((-\\d+)|(0+))$"　　//非正整数（负整数 + 0） 
# "^-[0-9]*[1-9][0-9]*$"　　//负整数 
# "^-?\\d+$"　　　　//整数 
# "^\\d+(\\.\\d+)?$"　　//非负浮点数（正浮点数 + 0） 
# "^(([0-9]+\\.[0-9]*[1-9][0-9]*)|([0-9]*[1-9][0-9]*\\.[0-9]+)|([0-9]*[1-9][0-9]*))$"　　//正浮点数 
# "^((-\\d+(\\.\\d+)?)|(0+(\\.0+)?))$"　　//非正浮点数（负浮点数 + 0） 
# "^(-(([0-9]+\\.[0-9]*[1-9][0-9]*)|([0-9]*[1-9][0-9]*\\.[0-9]+)|([0-9]*[1-9][0-9]*)))$"　　//负浮点数 
# "^(-?\\d+)(\\.\\d+)?$"　　//浮点数 
# "^[A-Za-z]+$"　　//由26个英文字母组成的字符串 
# "^[A-Z]+$"　　//由26个英文字母的大写组成的字符串 
# "^[a-z]+$"　　//由26个英文字母的小写组成的字符串 
# "^[A-Za-z0-9]+$"　　//由数字和26个英文字母组成的字符串 
# "^\\w+$"　　//由数字、26个英文字母或者下划线组成的字符串 
# "^[\\w-]+(\\.[\\w-]+)*@[\\w-]+(\\.[\\w-]+)+$"　　　　//email地址 
#"^[a-zA-z]+://(\\w+(-\\w+)*)(\\.(\\w+(-\\w+)*))*(\\?\\S*)?$"　　//url

############################################

# 获取上交所和深交所所有股票的名称和交易信息，并保存到文件中
# 股票信息需要静态存在于html中，而不是在js脚本文件中

# 从东方财富网获取股票列表
# 根据股票列表逐个到百度股票获取个股信息
# 将结果存储到文件

import requests
import re
import traceback
from bs4 import BeautifulSoup

def getHTMLText(url, code='utf-8'):
   try:
       r = requests.get(url)
       r.raise_for_status()
       r.encoding = code
       return r.text
   except:
       print('爬取失败')
    
def getStockList(lst, stockURL):
    html = getHTMLText(stockURL, 'GB2312')
    soup = BeautifulSoup(html, 'html.parser')
    a = soup.find_all('a') # 通过查看源代码知道股票名称和代码位于a标签中
    for i in a:
        try:
            href = i.attrs['href'] # 提取网址
            lst.append(re.findall(r"[s][hz]\d{6}", href)[0]) # [0]
            # s开头，第二个字母是h或z，\d是[0-9]，{6}扩展前一个字符6次，为股票代码
        except:
            continue

def getStockInfo(lst, stockURL, fpath):
    # list可以使用set()去重，set() 函数创建一个无序不重复元素集
    lst = list(set(lst))
    count = 0 # 显示进度用
    for stock in lst:
        url = stockURL + stock[-6:] # 后六位，去掉了SH SZ，根据所爬取的网页决定。该代码用于访问个股页面
        html = getHTMLText(url)
        try:
            if html == '': # 判断是否空页面
                continue
            infoDict = {} # 定义一个字典，存储股票信息
            soup = BeautifulSoup(html, 'html.parser')
            stockInfo = soup.find('div', attrs={'class':'stock-info'})
                        # 股票信息在该网页的div标签下
            name = stockInfo.find_all(attrs={'class':'name'})[0] # 股票名称位于<h1 class="name">
            price = stockInfo.find_all(attrs={'class': 'latest'})[0] # <span class="latest">
            infoDict.update({'股票名称':name.text.split()[0], '最新行情':price.text.split()[0]})
            keyList = stockInfo.find_all('dt') # 键域 如成交量 成交额
            valueList = stockInfo.find_all('dd') # 值域 如897万 3901万
            for i in range(len(keyList)):
                key = keyList[i].text
                val = valueList[i].text
                infoDict[key] = val # 为字典添加新的键值对——直接给不存在的key赋值即可
            with open(fpath, 'a', encoding = 'utf-8') as f:
                # with open 中的'a'：打开一个文件用于追加
                f.write(str(infoDict) + '\n') # \n换行
                count = count + 1
                ## 增加动态进度显示
                print('\r当前进度：{:.2f}%'.format(count * 100/len(lst)), end = '')
        except:
             traceback.print_exc()
             count = count + 1
             print("\r当前进度: {:.2f}%".format(count * 100 / len(lst)), end="")
             continue

def main():
    stock_list_url = 'http://app.finance.ifeng.com/list/stock.php?t=ha'
    stock_info_url = 'https://www.laohu8.com/stock/'
    output_file = 'D:/StockInfo.txt'
    slist = [] # 股票列表
    getStockList(slist, stock_list_url)
    getStockInfo(slist, stock_info_url, output_file)

main()
