#Requests库
# pip install requests

import requests
r = requests.get("https://www.baidu.com")
r.status_code # 状态码是200说明访问成功，404失败
r.apparent_encoding # 猜测可用的网页的编码
r.encoding # 查看网页的编码
r.encoding = 'utf-8' # 设定编码方式
r.text # 打印网页字符串形式内容
r.content
# r.content 网页内容二进制形式

#r = requests.get(url,params = None, **kwargs)

# 六种连接异常
#request.ConnectionError 网络连接错误，如DNS查询失败、拒绝连接
#request.HTTPError HTTP错误异常
#request.URLRequired URL缺失异常
#request.TooManyRedirects 超过最大重定向次数，产生重定向异常
#request.ConnectTimeout 连接远程服务器超时异常
#request.Timeout 请求URL超时，产生超时异常

# r.raise_for_status() 如果不是200，引发request.HTTPError
# 应用r.raise_for_status()
# 爬取网页通用框架
def getHTMLText(url):
    try:
        r = requests.get(url, timeout = 30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return "产生异常"

if __name__ == "__main__":
    url = "https://www.baidu.com"
    print(getHTMLText(url))


#requests.request() 构造一个请求，支撑以下各方法
    # r = requests.request('GET'/'HEAD'/'POST'等等, url, **kwargs)
#requests.get() 获取HML网页 对应HTTP的GET
#requests.head() 获取网页头信息 对应HTTP的HEAD
    # r = request.head('url')
    # r.headers
#requests.post() 向网页提交POST请求(附加新的数据) 对应HTPP的POST
    # payload = {'key1':'value1', 'key2':'value2'}
    # r = requests.post('url', data = payload)
    # r.text
#requests.put() 向网页提交PUT请求（存储一个资源覆盖原资源） 对应...
    # 同上,区别在于post变put
#requests.patch() 向网页提交局部修改请求 对应...
#requests.delete() 向网页提交删除请求 对应...

# **kwargs 控制访问参数
    # params：字典或字节序列
    # data 作为request的内容
    # json json格式的数据，作为request的内容
    # headers 字典，http定制头 hd = {'user-agent':'Chrome/10'}用CHROME的UA
    # cookies 某些反爬措施需要登录才能爬取
    # auth HTTP认证
    # files 传输文件 fs = {'file':open('data.xls','rb')}
    # timeout 设定超时时间，秒为单位
    # proxies 设定访问代理服务器 pxs = {'https':'https://8.8.8.8:1234'} 用来隐藏用户自己的IP
    # allow_redirects True/False 默认True，重定向开关
    # stream True/False 默认True，获取内容立即下载
    # varify True/False 默认True，SSL证书
    # cert 本地SSL证书路径


# 盗亦有道
    # 爬网页：小规模，数据量小，爬取速度不敏感 用Requests库 最常用
    # 爬网站：中规模，数据量大，对速度敏感（跟上网站更新的速度），Scrapy库
    # 爬全网：大规模，搜索引擎，爬取速度关键，定制开发

    # 服务器和自身资源消耗问题、产权问题、隐私问题
    
    # 爬虫规范
        #来源审查，判读User-agent，只响应特定浏览器
        #发布公告，Robots协议，要求遵守特定的爬取策略，哪些可以爬哪些不可以
            # Robots Exclusion Standard 网络爬虫排除标准，在网站根目录下放robots.txt文件
            # User-agent: * 表示针对所有
            # Disallow: / 表示根目录，即所有内容都不允许爬，如果Disallow为空表示允许爬取所有内容
        # Robots协议遵守方式 建议遵守但非约束性


# 实例1：京东商品页面的爬取
import requests
url = "https://item.jd.com/100010343850.html"
try: 
    r = requests.get(url)
    r.raise_for_status()
    r.encoding = r.apparent_encoding
    print(r.text)
except:
    print("爬取失败")

# 此时输出结果为：window.location.href='https://passport.jd.com/uc/login
# 虽然status_code是200但是爬取失败，需要添加headers伪装解决这个问题
import requests
url = "https://item.jd.com/100010343850.html"
try: 
    hd = {'user-agent':'Mozilla/5.0'}
    r = requests.get(url, headers = hd)
    r.raise_for_status()
    r.encoding = r.apparent_encoding
    print(r.text)
except:
    print("爬取失败")

# 实例2：爬取亚马逊的商品信息
import requests
url = "https://www.amazon.cn/dp/B07YDBYZZT/ref=sr_1_1?__mk_zh_CN=%E4%BA%9A%E9%A9%AC%E9%80%8A%E7%BD%91%E7%AB%99&keywords=%E7%88%AC%E8%99%AB&qid=1591462328&sr=8-1"
r = requests.get(url)
r.encoding
# 返回ISO-8859-1
r.encoding = r.apparent_encoding
r.status_code
# 返回错误代码503
r.text
# 抱歉，我们只是想确认一下当前访问者并非自动程序。为了达到最佳效果，请确保您浏览器上的 Cookie 已启用
# 同样需要设置User-agent
import requests
url = "https://www.amazon.cn/dp/B07YDBYZZT/ref=sr_1_1?__mk_zh_CN=%E4%BA%9A%E9%A9%AC%E9%80%8A%E7%BD%91%E7%AB%99&keywords=%E7%88%AC%E8%99%AB&qid=1591462328&sr=8-1"
try: 
    hd = {'user-agent':'Mozilla/5.0'}
    r = requests.get(url, headers = hd)
    r.raise_for_status()
    r.encoding = r.apparent_encoding
    print(r.text)
except:
    print("爬取失败")
    
# 实例3：百度/360搜索关键词提交
# 搜索引擎关键词提交接口
    # 百度：https://www.baidu.com/s?wd=keyword
    # 360：http://www.so.com/s?q=keyword
import requests
keyword = "python"
try:
    kv = {'wd':keyword}  
    r = requests.get("https://www.baidu.com/s", params = kv)
    print(r.request.url) # 返回'https://www.baidu.com/s?wd=python'则正确
    r.raise_for_status()
    print(len(r.text))
except:
    print("爬取失败")
# 返回https://wappass.baidu.com/，爬取失败

# 360搜索
import requests
keyword = "python"
try:
    kv = {'q':keyword}  
    r = requests.get("https://www.so.com/s", params = kv)
    print(r.request.url) # 返回'https://www.so.com/s?q=python'则正确
    r.raise_for_status()
    print(len(r.text))
except:
    print("爬取失败")

# 实例4：网络图片的爬取和存储
import requests
path = "D:/abc.jpg"
url = "https://www.nationalgeographic.com/travel/where-the-locals-go/asia/china/city-local-travel-tips-xian-china/#/big-wild-goose-pagoda-xian-china.jpg"
r = requests.get(url)
r.status_code
with open(path, "wb") as f:
    f.write(r.content)
# 存在版权，下载后打不开

import requests
import os
url = "http://imgsrc.baidu.com/forum/pic/item/16a1b8ca7bcb0a46b664d7d86563f6246a60af5b.jpg"
root = "D://pics//"
path = root + url.split('/')[-1] # 通过链接截取文件名
try:
    if not os.path.exists(root):
        os.mkdir(root)
    if not os.path.exists(path):
        r = requests.get(url)
        with open(path, 'wb') as f:
            f.write(r.content)
            f.close()
            print("文件保存成功")
    else:
        print("文件已存在")
except:
    print("爬取失败")

# 实例5：IP归属地的自动查询
import requests
url = 'https://m.ip138.com/iplookup.asp?ip='
try:
    hd = {'user-agent':'Mozilla/5.0'}
    r = requests.get(url + '14.215.177.39', headers = hd)
    r.raise_for_status()
    r.encoding = r.apparent_encoding
    print(r.text)	# 输出后500个字符
except:
    print('爬取失败')

##################
    
import requests

# with open('./sogou.html', 'w', encoding = 'utf-8') as f:
#     f.write(page_text)

word = input('关键词：')
url = 'https://www.sogou.com/web'
params = {'query':word, 'user-agent':'Mozilla/5.0'}
response = requests.get(url = url, params = params)
response.encoding = response.apparent_encoding
page_text = response.text
fileName = word + '.html'
with open(fileName, 'w', encoding = 'utf-8') as f:
    f.write(page_text)
print(word, '下载成功')

# 爬取豆瓣网中的电影详情数据
# 当滚轮滑动到底部的时候，页面会发起ajax请求，且请求到一组电影详情数据
# 当滚轮不滑动的时候，页面显示的电影数据，通过对浏览器地址栏的url发起请求是请求不到的

url = 'https://movie.douban.com/j/chart/top_list'
# 参数动态化 通过浏览器-控制台-网络捕获到如下参数
# 控制台-网络-响应中的内容复制到JSON在线解析https://www.sojson.com/
# 原网页地址为https://movie.douban.com/typerank?type_name=%E7%A7%91%E5%B9%BB&type=17&interval_id=100:90&action=
params = {
    "type": "17",
    "interval_id": "100:90",
    "action": "",
    "start": "40",
    "limit": "20",
} 
# type电影类型，start是从第40个开始取limit 20个
headers = {
    "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'
} # 这里请求头如果写入params里，执行response会报错
response = requests.get(url=url, headers=headers, params=params)
page_text = response.json()
#将电影名称和评分进行解析 title和score来自于json源码
for dic in page_text:
    name = dic['title']
    score = dic['score']
    print(name+':'+score)


# 肯德基餐厅查询：http://www.kfc.com.cn/kfccda/storelist/index.aspx
# 通过点击查询才出来数据，是动态数据
# 通过F12找到getstorelist-响应，解析json，在标头中提取请求URL，在标头-表单数据中提取字典
url = 'http://www.kfc.com.cn/kfccda/ashx/GetStoreList.ashx?op=keyword'
# 获取所有页的信息
# 点击下一页时，控制台-网络-响应，发现标头的参数发生变化，即便pageIndex，因此for循环
for pageNum in range(1,8):
    data = {
        "cname": "",
        "pid": "",
        "keyword": "北京",
        "pageIndex": str(pageNum),
        "pageSize": "10",
    }
# 使用post提交
# 参数：data是用来实现参数动态化，等同于get方法中的params参数的作用
    response = requests.post(url=url,headers=headers,data=data)
    page_text = response.json()
    for dic in page_text['Table1']:
        pos = dic['addressDetail']
        print(pos)

####################
        
# 爬取药监总局中的企业详情数据 http://125.35.6.84:81/xk/
# 打开一个公司的详情页，F12控制台-网络-刷新页面-找到地址栏对应的文件-响应-搜不到网页中的关键词-所以是动态数据
# 用抓包工具进行全局搜索，单击地址栏对应的文件，ctrl+f进去全局搜索，搜索关键词比如粤妆20200022
# 将搜到的信息复制到json解析中，另外将搜到的信息查看标头，提取url和表单数据中的ID
# http://125.35.6.84:81/xk/itownet/portalAction.do?method=getXkzsById
# id: ff83aff95c5541cdab5ca6e847514f88
# 换另一家企业，重复上述步骤，发现http一样而id不一样
# 每一家企业详情数据对应的请求url和请求方式是一样的，只有请求id不一样
# 要爬取所有企业信息，则需要捕获每家企业的id，id很可能与名称在一起

# 在首页即http://125.35.6.84:81/xk/中，控制台-网络-刷新页面-全局搜索企业名称-解析json
# 请求url：http://125.35.6.84:81/xk/itownet/portalAction.do?method=getXkzsList
# 请求参数（位于表单数据）：
# on: true
# page: 1
# pageSize: 15
# productName: 
# conditionType: 1
# applyname: 
# applysn:

url = 'http://125.35.6.84:81/xk/itownet/portalAction.do?method=getXkzsList'
data = {
    'on': 'true',
    'page': '1',
    'pageSize': '15',
    'productName': '',
    'conditionType': '1',
    'applyname': '',
    'applysn': '',
}

response = requests.post(url = url, headers = headers, data = data)
all_company_list = response.json()['list'] # 原json中，list字典包含了企业基本信息
for dic in all_company_list:
    _id = dic['ID']
    detail_url = 'http://125.35.6.84:81/xk/itownet/portalAction.do?method=getXkzsById'
    data = {
        'id':_id
    }
    response = requests.post(url = detail_url, headers = headers, data = data)
    company_detail_dic = response.json()
    person_name = company_detail_dic['businessPerson'] # 法定代表人
    addr = company_detail_dic['epsProductAddress'] # 地址
    print(person_name, addr)

# 分析如何捕获多页数据


# 爬取图片数据
# 方式1：requests
# 方式2：urllib
#requests见前文
#urllib
from urllib import request
url = 'http://pics.sc.chinaz.com/files/pic/pic9/201908/zzpic19447.jpg'
request.urlretrieve(url = url,filename='./456.png')

# requests的方式可以实现UA伪装，而urlib无法实现UA伪装

# 站长素材图片数据的爬取
# 反爬机制：图片懒加载。只有当图片数据被显示在可视化范围之内，则图片才会被加载出来。
# 伪属性：src2，阻止图片加载的。只有当伪属性被变成真正的src属性值图片才会被加载出来。
# 分析：
# 图片数据是否为动态加载的数据
# 除了可以在控制台-网络-响应选项卡中进行局部搜索发现存在jpg，已加载的图片在src标签中，未加载的在src2
# 发现控制台-网络-预览中只显示了图片的名称，并没有显示图片数据
import requests
import re
headers = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'
}
url = 'http://sc.chinaz.com/tag_tupian/YaZhouMeiNv.html'
page_text = requests.get(url, headers = headers).text #获取字符串形式的响应数据
#通过正则进行图片地址的解析
#<a target="_blank" href="http://sc.chinaz.com/tupian/200609013165.htm" alt="气质清新日本美女图片">
#<img src2="http://pic.sc.chinaz.com/Files/pic/pic9/202006/apic25718_s.jpg" alt="气质清新日本美女图片">
#</a>
ex = '<a.*?<img src2="(.*?)" alt.*?</a>' # 这里的alt，是源码中到alt截止
img_src_list = re.findall(ex, page_text, re.S) # re.S处理回车，不加这个回获取到空列表

# 爬取的是https://m.vmall.com/help/hnrstoreaddr.htm中门店的详情数据
# 如果可以捕获到一家门店的详情数据，可以保证捕获到所有门店的详情数据
# 检测门店的详情数据是否为动态加载的数据，发现为动态加载，因为需要全局搜索
# 请求道的URL：https://openapi.vmall.com/mcp/offlineshop/getShopById?portal=2&version=10&country=CN&shopId=108302&lang=zh-CN
# 将问号及其后的参数去掉：https://openapi.vmall.com/mcp/offlineshop/getShopById
# 在标头中发现字符串参数为下，shopId便是每家店的识别依据
# portal: 2
# version: 10
# country: CN
# shopId: 108302
# lang: zh-CN

# 捕获每一家店面的id值，首先返回https://m.vmall.com/help/hnrstoreaddr.htm
# 全局搜索任意地址关键词，找到关键页面，提取标头中的URL：https://openapi.vmall.com/mcp/offlineshop/getShopList
# 发现请求方式为：POST，关键词如下：
# {"portal":2,"lang":"zh-CN","country":"CN","brand":1,"province":"广东省","city":"深圳市","pageNo":1,"pageSize":20}: 
# 可以看出这里的参数为JSON键值对

#捕获店面的id值
#import json

url = 'https://openapi.vmall.com/mcp/offlineshop/getShopList'
data = {
    "portal":2,
    "lang":"zh-CN",
    "country":"CN",
    "brand":1,
    "province":"河北",
    "city":"邯郸",
    "pageNo":1,
    "pageSize":20
}
#json_data_ids = requests.post(url = url, headers = headers, data=json.dumps(data)).json()
json_data_ids = requests.post(url = url, headers = headers, json = data).json()

for dic in json_data_ids['shopInfos']:
    _id = dic['id']#捕获到门店的id
    detail_url = 'https://openapi.vmall.com/mcp/offlineshop/getShopById'
    params = {
          "portal": "2",
          "version": "10",
          "country": "CN",
          "shopId": _id,
          "lang": "zh-CN",
    }
    shop_detail = requests.get(url = detail_url, headers = headers, params = params).json()
    print(shop_detail)
