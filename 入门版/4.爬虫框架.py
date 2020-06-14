# 5+2结构
# ENGINE 控制所有模块之间的数据流，根据条件触发事件
# SCHEDULER 对所有的爬取请求进行调度管理
# DOWNLOADER 根据请求下载网页
# SPIDERS 解析DOWNLOADER返回的响应RESPONSE，产生爬取项SCRAPED ITEM和额外的爬取请求REQUESTS
# ITEM PIPELINES 处理爬取项，由一组操作顺序组成，类似流水线，清理检验查重存储

# ENGINE和SPIDERS、ENGINE和DOWNLOADER之间分别存在MIDDLEWARE模块
# DOWNLOADER MIDDLEWARE 实施ENGINE SCHEDULER和DOWNLOADER之间进行用户可配置的控制（修改丢弃新增请求或响应）
# SPIDER MIDDLEWARE 对请求和爬取项的再处理，修改、丢弃、新增请求或爬取项

# 三大数据路径

# ENGINE从SPIDERS获取REQUESTS转发给SCHEDULER

# ENGINE从SCHEDULER获取下一个爬取网络的REQUESTS，
  #通过中间键发送给DOWNLOADER， DOWNLOADER爬取网页后将内容形成RESPONSE，
    #通过中间键和ENGINE发送给SPIDERS

# SPIDER处理从DOWNLOARER获取的RESPONSE，
 # 产生爬取项ITEM和新的REQUESTS，发送给ENGINE，ENGINE将ITEMS发送给ITEM PIPELINES，
  # 将新的REQUESTS发给SCHEDULER

# ENGINE SCHEDULER DOWNLOADER 三个模块不需要用户编写
# 用户需要编写SPIDERS和ITEM PIPELINES
  
# REQUESTS与SCRAPY
# 都没有处理js、提交表单、应对验证码等功能

# REQUESTS页面级爬虫，SCRAPY网站级爬虫
# REQUESTS是功能库，SCRAPY是框架
# REQUESTS并发性考虑不足、性能差，SCRAPY并发性好、性能高
# REQUESTS重点在于页面下载，SCRAPY重点在于爬虫结构
# REQUESTS定制灵活，SCRAPY一般情况灵活，但深度定制困难
# REQUESTS上手简单，SCRAPY入门较难

# 在cmd中输入scrapy -h启动scrapy命令行
# 常用命令
# startproject 创建一个新工程 scrapy startproject <name> [dir]
# genspider 创建一个爬虫 scrapy genspider [options] <name> <domain>
# settings 获取爬虫配置信息 scrapy settings [options]
# crawl 运行一个爬虫 scrapy crawl <spider>
# list 列出工程中所有爬虫 scrapy list
# shell 启动URL调试命令行 scrapy shell [url]

# Scrapy实践

# 步骤1：建立一个Scrapy爬虫工程

# 打开cmd，cd到想要的目录下，输入scrapy startproject name
# 假如name为Linshi，放置在D盘根目录
# linshi 外层目录
# linshi/scrapy.cfg 部署scrapy爬虫的配置文件
# linshi/linshi/ scrapy框架的用户自定义Python代码
# __init__.py 初始化脚本 不需要编写
# items.py 一般不需要编写
# middlewares.py 需要扩展middlewares功能时编写
# pipelines.py 
# settings.py 爬虫配置文件
# spiders/

# spiders/__init__.py 初始文件，无需修改
# spiders/__pycache__/ 缓存目录，无需修改

# 
# 步骤2：在工程中产生一个Scrapy爬虫
# 在cmd中cd到linshi文件夹下
# scrapy genspider name python123.io # python123.io是要爬取的页面
# D:\linshi\linshi\spiders增加了一个name.py文件，内容如下，需要配置

import scrapy
class NameSpider(scrapy.Spider):
    name = 'name'
    allowed_domains = ['python123.io']
    start_urls = ['http://python123.io/']

    def parse(self, response): # parse()用于处理响应，解析内容形成字典，发现新的URL爬取请求
        pass

# 步骤3：配置产生的Spider爬虫
# 修改name.py
import scrapy
class NameSpider(scrapy.Spider):
    name = 'name'
    # allowed_domains = ['python123.io'] # 不需要
    start_urls = ['https://python123.io/ws/demo.html']

    def parse(self, response): # parse()用于处理响应，解析内容形成字典，发现新的URL爬取请求
        fname = response.url.split('/')[-1]
        with open(fname, 'wb') as f:
            f.write(response.body)
        self.log = ('saved file %s.'% fname)

# 步骤4：运行爬虫，获取网页
# cmd切换到linshi根目录下下执行scrapy crawl name
# D:\linshi文件夹下多出demo.html文件

# yield关键字
# 包含yield语句的函数是一个生成器
# 生成器每次产生一个值(yield语句)，函数被冻结，唤醒后再产生一个值，再执行遍历
def gen(n):
    for i in range(n):
        yield i**2

for i in gen(5):
    print(i, " ", end = "")
# 产生小于n的所有整数的平方值
# for循环执行到yield时会被冻结，并返回当前产生的值

# 如果采用常规的写法:
def square(n):
    ls = [i**2 for i in range(n)]
    return ls

for i in square(5):
    print(i, " ", end = "")

# 生成器优势：节省存储空间、响应更迅速、使用更灵活

# Request类
# class scrapy.http.Request()
# Request对象表示一个HTTP请求
# 由Spider生成，由Downloader执行
# .url 对应的请求URL地址
# .method 对应的请求方法，"GET" "POST"等
# .headers 字典类型风格的请求头
# .body 请求内容主体，字符串类型
# .meta 用户添加的扩展信息，在Scrapy内部模块间传递信息使用
# .copy() 复制该请求

# Response类
# class scrapy.http.Response()
# Response对象表示一个HTTP响应
# 由Downloader生成，由Spider处理
# .url 对应的URL地址
# .status 状态码，默认是200
# .headers 对应的头部信息
# .body 对应的内容信息，字符串类型
# .flags 一组标记
# .request 产生Response类型对应的Request对象
# .copy() 复制该响应

# Item类
# class scrapy.item.Item()
# Item对象表示一个从HTML页面中提取的信息内容
# 由Spider生成，由Item Pipeline处理
# Item类似字典类型，可以按照字典类型操作

# CSS Selector的使用
# <HTML>.css('a::attr(href)').extract()

# Scrpay实现股票爬虫
# 步骤1：建立工程和Spider模板
# scrapy startproject XueqiuStocks
# cd XueqiuStocks
# scrapy genspider stocks xueqiu.com
# 修改spiders/stocks.py文件

# 步骤2：编写Spider
# 修改对返回页面的处理
# 修改对新增URL爬取请求的处理
import scrapy
import re

class StocksSpider(scrapy.Spider):
    name = 'stocks'
    start_urls = ['http://quote.eastmoney.com/stock_list.html']

    def parse(self, response):
        for href in response.css('a::attr(href)').extract(): # 提取a标签中的链接
        	try:
        		stock = re.findall(r"[s][hz]\d{6}", href)[0]
        		url = 'https://xueqiu.com/S/' + stock
        		yield scrapy.Request(url, callback = self.parse_stock) # callback给出处理URL对应响应的函数
        	except: # 对于错误的链接用except处理，保证程序继续运行
        		continue

    def parse_stock(self, response): # 该函数返回提取的信息给ITEM PIPELINES
        infoDict = {} # ITEM是字典类型，所以首先对每个页面生成一个空字典
        name = response.css('.stock-name').extract()[0] # 雪球财经中，股票名字位于源代码<div class="stock-name">后
        stockInfo = response.css('.quote-info') # 股票数据位于<table class="quote-info">后，和前一行一样要注意小数点
        keyList = stockInfo.css('td').extract()
        valueList = stockInfo.css('span').extract()
        for i in range(len(keyList)): # 将提取的信息保存至字典
        	key = re.findall(r'>.*?<', keyList[i])[0][1:-2]
        	try:
        		val = re.findall(r'>\d+\.?.*</span>', valueList[i])[0][1:-7]
        		# \d+表示多次（1次和1次以上）数字
        		# \.表示小数点，因为.表示任意字符，所以加\将.转义表示只是点的意思
        		# \.?表示这个点（小数点）最多只能出现一次，即要么不出现，要么只出现一次。?表示出现0次或1次
        		# .*就是单个字符连续匹配直到最后一个，即贪婪匹配。 .*?是满足条件的情况只匹配一次，即最小匹配
        	except:
        		val = "--"
        	infoDict[key] = val # 添加新内容

        infoDict.update(
        	#<div class="stock-name">白云机场(SH:600004)</div>
        	{'股票名称': re.findall(r'>.*<', name)[0][1:-1]})
        yield infoDict

# 步骤3：编写ITEM Pipelines
# 配置pipelines.py文件
class XueqiustocksPipeline(object):
    def process_item(self, item, spider):
        return item

class XueqiustocksInfoPipeline(object): # 每个PIPELINE中有三个方法
	"""docstring for XueqiustocksInfoPipeline"""
	def open_spider(self, spider): # 当一个爬虫被调用时，对应的PIPELINE启动的方法
		self.f = open('XueqiuStockInfo.txt','w')

	def close_spider(self, spider): # 一个爬虫结束时，PIPELINE对应的方法
		self.f.close()

	def process_item(self, item, spider): # 对每个ITEM处理时，对应的方法
		try: # 将字典信息写入文件
			line = str(dict(item)) + '\n' # 换行
			self.f.write(line)
		except:
			pass
		return item

# 修改settings.py文件
# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'XueqiuStocks.pipelines.XueqiustocksInfoPipeline': 300,
}
# 这里是XueqiustocksInfoPipeline，是自己定义的那个，不是默认生成的

# 步骤3：执行爬虫
# scrapy crawl stocks # Spider下name = 'stocks'


# 配置并发连接选项
# settings.py文件
# CONCURRENT_REQUESTS  DOWNLOADER最大并发请求下载数量，默认32，即同时下载32个网站
# CONCURRENT_ITEMS  ITEM POPELINE最大并发ITEM处理数量，默认100
# CONCURRENT_REQUESTS_PRE_DOMAIN  每个目标域名最大的并发请求数量，默认8
# CONCURRENT_REQUESTS_PRE_IP  每个目标IP最大的并发请求数量，默认0，非0有效
# 后两个参数最多只有一个发挥作用

## Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.6788.400 QQBrowser/10.3.2864.400'
#}




# 其他案例

# scrapy startproject xicidailiSpider # 项目名
# cd xicidailiSpider
# scrapy genspider xicidaili xicidaili.com # 爬虫名不要和项目名一样 域名为了限定爬取的网址

import scrapy

class XicidailiSpider(scrapy.Spider):
    name = 'xicidaili' # 爬虫名字，必须唯一
    allowed_domains = ['xicidaili.com'] # 允许采集的域名
    start_urls = ['https://www.xicidaili.com/nn/'] # 第一次采集的网站
    # start_urls = [f'https://www.xicidaili.com/nn/{page}' for page in range(1, 3685)]

    # 解析相应的数据 提取数据或者网址等 response就是网页源码
    def parse(self, response):
        # 提取数据
        # response.xpath('表达式')  百度xpath w3
        # 要得到title标签内的内容，xpath表达式应该写成//title/text()
        # 浏览器安装xpath helper插件可以辅助爬虫
        selectors = response.xpath('//tr')
        # 循环遍历tr标签下的td标签
        # //tr/td[2]是页面中的IP地址，//tr/td[3]是端口port
        for selector in selectors:
        	ip = selector.xpath('./td[2]/text()').get() # .点在当前节点下继续选择
        	port = selector.xpath('./td[3]/text()').get()
        	# 或者替换.get为.extract_first()，等价，如果每次有多个IP要获取用getall
        	# print(ip, port)
        	
        	items = {'ip':ip, 'port':port}
        	yield items

        # 翻页 //a[@class="next_page"]/@href
        next_page = response.xpath('//a[@class="next_page"]/@href').get()
        if next_page:
        	print(next_page)
        	# 拼接网址
        	next_url = response.urljoin(next_page)
        	# 用Request发出请求，callback是回调函数，将请求得到的响应交给自己处理
        	yield scrapy.Request(next_url, callback = self.parse) # 之前def了parse

# settings.py
# 修改请求头
DEFAULT_REQUEST_HEADERS = {
   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
   'Accept-Language': 'en',
   'User-Agent':'Mozilla/5.0'
}
# ROBOTSTXT_OBEY 是否服从君子协议

# scrapy crawl xicidaili
# scrapy crawl xicidaili -o ip.json 执行并输出保存数据
# scrapy crawl xicidaili -o ip.csv
