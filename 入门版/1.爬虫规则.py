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
