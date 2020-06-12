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

