# cookie的处理
# 代理操作
# 验证码识别
# 模拟登录

# cookie
# cookie是存储在客户端的一组键值对
# cookie是由服务器端创建
# cookie应用的简单示例：免密登录（指定时长之内）

# 在爬虫中处理cookie的两种方式
# 手动处理：将cookie封装到headers字典中，将该字典作用到get/post方法的headers参数中
# 自动处理
    # Session对象。
    # Session对象的创建：requests.Session()
    # 对象的作用：
    # 可以跟requests一样调用get/post进行请求的发送
    # 在使用session进行请求发送的过程中，如果产生了cookie，则cookie会被自动存储到session对象中
    # 在爬虫中使用session处理cookie时，session对象至少需要被用两次
    # 第一次是为了捕获和存储cookie到session对象中，第二次就是用携带cookie的session进行请求发送，这次请求发送就是携带cookie发起的请求

import requests
headers = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'
}

# https://xueqiu.com/，将雪球网中的新闻资讯进行数据爬取
# 通过控制台-网络-预览发现：首页第一屏的数据不是动态加载，但是后面的新闻无法加载，网页中滚轮滑动到底部后才会动态加载出更多新闻数据
# 打开控制台-网络，向下滑动网页，等加载出新内容后，全局搜索新内容的关键词，找到如下url和四个参数
# since_id: -1
# max_id: 64222
# size: 15

url = 'https://xueqiu.com/statuses/hot/listV2.json?since_id=-1&max_id=64222&size=15'
json_data = requests.get(url = url, headers = headers).json()
json_data
# 没有捕获到正确的数据，原因在于我们进行请求发送的时候没有在请求头中携带cookie

# 基于session自动处理cookie
sess = requests.Session()

# 该次请求只是为了捕获cookie存储到sess中
sess.get(url = 'https://xueqiu.com/', headers = headers)

url = 'https://xueqiu.com/statuses/hot/listV2.json?since_id=-1&max_id=64222&size=15'
json_data = sess.get(url = url, headers = headers).json()
json_data


# 代理操作
# 爬虫程序可能会在短时间内对指定的服务器发起高频的请求，服务器端会将该高频请求的ip禁掉

from lxml import etree
url = 'https://www.xicidaili.com/nn/%d' #%d页码
all_data = []
for page in range(1,30):
    new_url = format(url%page)
    page_text = requests.get( url = new_url, headers = headers).text
    tree = etree.HTML(page_text)
    # ip地址位于tr标签下
    # 在xpath表达式中不可以出现tbody标签，否则会出问题，即不可'//*[@id="ip_list"]/tbody/tr'
    tr_list = tree.xpath('//*[@id="ip_list"]//tr')[1:] # 因为第一个tr是列索引，不是我们要的，所以[1:]
    for tr in tr_list:
        ip_addr = tr.xpath('./td[2]/text()')[0] # tr下第二个td是ip地址
        all_data.append(ip_addr)
print(len(all_data))
# IP被禁后，即便使用浏览器也无法打开被爬取的网站

# 使用代理机制解除ip被禁的情况
# 1.构建一个代理池
ips_list = []
url = 'http://t.11jsq.com/index.php/api/entry?method=proxyServer.generate_api_url&packid=1&fa=0&fetch_key=&groupid=0&qty=52&time=1&pro=&city=&port=1&format=html&ss=5&css=&dt=1&specialTxt=3&specialJson=&usertype=2'
page_text = requests.get(url = url, headers = headers).text
tree = etree.HTML(page_text)
ip_list = tree.xpath('//body//text()')
for ip in ip_list:
    dic = {'https':ip}
    ips_list.append(dic)
ips_list

import random
# 使用代理池操作
url = 'https://www.xicidaili.com/nn/%d'
all_data = []
for page in range(1, 30):
    new_url = format(url%page)
    # proxies={'http':'ip:port'}
    page_text = requests.get(url = new_url, headers = headers, proxies = random.choice(ips_list)).text
    tree = etree.HTML(page_text)
    #在xpath表达式中不可以出现tbody标签，否则会出问题
    tr_list = tree.xpath('//*[@id="ip_list"]//tr')[1:]
    for tr in tr_list:
        ip_addr = tr.xpath('./td[2]/text()')[0]
        all_data.append(ip_addr)
print(len(all_data))



# 验证码识别和模拟登录

# 往往在进行大量请求发送的时候，经常会报出这一样的一个错误：HTTPConnectionPool（host:XX）Max retries exceeded with url。
#原因：
    #1.每次数据传输前客户端要和服务器建立TCP连接，为节省传输消耗，默认为keep-alive，即连接一次，传输多次。
       #然而如果连接迟迟不断开的话，则连接池满后则无法产生新的链接对象，导致请求无法发送。
    #2.ip被封  #3.请求频率太频繁
#解决：如果下列解决未生效，则可以尝试再次执行程序
    #1.设置请求头中的Connection的值为close，表示每次请求成功后断开连接
        # headers = {'Connection':'close'}
    #2.更换请求ip  #3.每次请求之间使用sleep进行等待间隔

import requests
headers = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'
}

#验证码识别
#线上的打码平台进行验证码识别
#云打码：http://www.yundama.com/about.html
#超级鹰（使用）：http://www.chaojiying.com/about.html
#打码兔
# 注册超级鹰并生成一个软件ID (ID:   905860)
# 下载Python示例代码

#!/usr/bin/env python
# coding:utf-8

import requests
from hashlib import md5

class Chaojiying_Client(object):

    def __init__(self, username, password, soft_id):
        self.username = username
        password =  password.encode('utf8')
        self.password = md5(password).hexdigest()
        self.soft_id = soft_id
        self.base_params = {
            'user': self.username,
            'pass2': self.password,
            'softid': self.soft_id,
        }
        self.headers = {
            'Connection': 'Keep-Alive',
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)',
        }

    def PostPic(self, im, codetype):
        """
        im: 图片字节
        codetype: 题目类型 参考 http://www.chaojiying.com/price.html
        """
        params = {
            'codetype': codetype,
        }
        params.update(self.base_params)
        files = {'userfile': ('ccc.jpg', im)}
        r = requests.post('http://upload.chaojiying.net/Upload/Processing.php', data=params, files=files, headers=self.headers)
        return r.json()

    def ReportError(self, im_id):
        """
        im_id:报错题目的图片ID
        """
        params = {
            'id': im_id,
        }
        params.update(self.base_params)
        r = requests.post('http://upload.chaojiying.net/Upload/ReportError.php', data=params, headers=self.headers)
        return r.json()


#自己封装的一个识别验证码图片的函数   
def transform_code_img(imgPath, imgType):
    # 验证码类型参考 https://www.chaojiying.com/price.html
    chaojiying = Chaojiying_Client('nsrlive', 'm65324y', '905860')  #用户中心>>软件ID 生成一个替换 96001
    im = open(imgPath, 'rb').read() #本地图片文件路径 来替换 a.jpg 有时WIN系统须要//
    return chaojiying.PostPic(im, imgType)['pic_str'] #1902 验证码类型  官方网站>>价格体系 3.4+版 print 后要加() 

#调用识别验证码的函数对验证码进行识别
transform_code_img('./a.jpg', 4004)


# 将古诗文网中的验证码图片进行识别
from lxml import etree

# 解析出本次登录页面对应的验证码图片地址
login_url = 'https://so.gushiwen.org/user/login.aspx?from=http://so.gushiwen.org/user/collect.aspx'
page_text = requests.get(url = login_url, headers = headers).text
tree = etree.HTML(page_text)
# 解析出了验证码图片的地址
# 点击浏览器控制台左上角箭头，再点击验证码，可以直接定位到验证码在源码中的位置
# 定位到了以后，右键复制xpath //*[@id="imgCode"]
# 页面中右键验证码复制图像链接 https://so.gushiwen.org/RandCode.ashx
img_path = 'https://so.gushiwen.org' + tree.xpath('//*[@id="imgCode"]/@src')[0]
img_data = requests.get(url = img_path, headers = headers).content #请求到了图片数据

# 将图片保存到本地存储
with open('./code.jpg', 'wb') as fp:
    fp.write(img_data)
    
# 识别验证码
code_result = transform_code_img('./code.jpg', 1004)
print(code_result)


# 模拟登录
# 模拟登录时，要找对应请求方法为POST的URL，这需要先打开控制台并在网页登陆账号
# 观察表单数据
# 观察表单数据

# __VIEWSTATE: rfuTYRdObYsyG/eH311eoaWVFCX5wbTFjE6rcxhjmHCobZunutthfN9x0n5ZzggudwErwdFaBE33Xmvod/ivTCRhT+GG95eUw/FULfm7/jwZ7UEzVLdPqDvund8=
# __VIEWSTATEGENERATOR: C93BE1AE
# from: http://so.gushiwen.org/user/collect.aspx
# email: niusirui@live.cn
# pwd: m65324y
# code: vy58
# denglu: 登录

# 请求参数：__VIEWSTATE和__VIEWSTATEGENERATOR
# 是否加密？是否为动态变化？
# 一般情况下动态变化的请求参数都会被隐藏在前台页面的源码中
# 需要在抓包工具中对动态变化的请求参数的名称进行全局搜索
# 复制其中一个请求参数的名称，在控制台-元素中进行搜索

# 对于需要cookie的登陆，说明cookie在登陆前就已经产生，需要使用Session

sess = requests.Session() #创建好session对象
#处理动态变化的请求参数
login_url = 'https://so.gushiwen.org/user/login.aspx?from=http://so.gushiwen.org/user/collect.aspx'
page_text = sess.get(url = login_url, headers = headers).text
tree = etree.HTML(page_text)

img_path = 'https://so.gushiwen.org' + tree.xpath('//*[@id="imgCode"]/@src')[0]
img_data = sess.get(url = img_path, headers = headers).content #请求到了图片数据

with open('./code.jpg','wb') as fp:
    fp.write(img_data)

# 将动态变化的请求参数从页面源码中解析出来
# 这两个参数每次在登陆页面都不一样，但是我们已经提取了登陆页面的源码
# 退出登录，回到登陆页面，在控制台-元素中进行搜索参数关键词，右键复制xpath

__VIEWSTATE = tree.xpath('//*[@id="__VIEWSTATE"]/@value')[0]
__VIEWSTATEGENERATOR = tree.xpath('//*[@id="__VIEWSTATEGENERATOR"]/@value')[0]

#识别验证码
code_result = transform_code_img('./code.jpg',1004)
print(code_result)

# 对应请求方法为POST的URL
post_url = 'https://so.gushiwen.org/user/login.aspx?from=http%3a%2f%2fso.gushiwen.org%2fuser%2fcollect.aspx'
data = {
    "__VIEWSTATE":__VIEWSTATE,
    "__VIEWSTATEGENERATOR":__VIEWSTATEGENERATOR,
    "from": "http://so.gushiwen.org/user/collect.aspx",
    "email": "niusirui@live.cn",
    "pwd": "m65324y",
    "code": code_result,
    "denglu": "登录",
}
#模拟登录的请求
response = sess.post(url = post_url, headers = headers, data = data)
page_text = response.text #登录成功后页面的源码数据
with open('gushiwen.html', 'w', encoding='utf-8') as fp:
    fp.write(page_text)
    
# 模拟登录中涉及的反爬：
# 验证码
# 动态变化的请求参数
# cookie
# UA
# robots
# 动态加载的数据
# 图片懒加载
# 代理
# js加密
# js混淆