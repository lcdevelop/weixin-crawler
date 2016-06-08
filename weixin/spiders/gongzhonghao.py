#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import MySQLdb
import scrapy
import time
import subprocess
from scrapy.http import HtmlResponse
from scrapy.selector import Selector
from weixin.items import WeixinItem
from w3lib.html import remove_tags
from weixin.conn import Conn

class GongzhonghaoSpider(scrapy.Spider):
    name = "gongzhonghao"
    allowed_domains = ["qq.com"]
    start_urls = [
        "http://weixin.sogou.com/weixin?query=算法与数学之美",
        "http://weixin.sogou.com/weixin?query=大数据文摘",
        "http://weixin.sogou.com/weixin?query=大数据技术",
        "http://weixin.sogou.com/weixin?query=数据分析精选",
        "http://weixin.sogou.com/weixin?query=算法与数学之美",
        "http://weixin.sogou.com/weixin?query=数盟",
        "http://weixin.sogou.com/weixin?query=MachineLearning_",
        "http://weixin.sogou.com/weixin?query=犇犇机器学习",
        "http://weixin.sogou.com/weixin?query=我爱机器学习",
        "http://weixin.sogou.com/weixin?query=机器学习算法与Python学习",
        "http://weixin.sogou.com/weixin?query=机器学习与大数据",
        "http://weixin.sogou.com/weixin?query=PLY机器学习俱乐部",
        "http://weixin.sogou.com/weixin?query=机器学习与人工智能",
        "http://weixin.sogou.com/weixin?query=菜鸟的机器学习",
        "http://weixin.sogou.com/weixin?query=培乐园机器学习社区",
        "http://weixin.sogou.com/weixin?query=我为机器学习狂",
        "http://weixin.sogou.com/weixin?query=深度学习",
        "http://weixin.sogou.com/weixin?query=深度学习世界",
        "http://weixin.sogou.com/weixin?query=数据挖掘菜鸟",
        "http://weixin.sogou.com/weixin?query=数据挖掘DW",
        "http://weixin.sogou.com/weixin?query=数据挖掘",
        "http://weixin.sogou.com/weixin?query=大数据挖掘",
        "http://weixin.sogou.com/weixin?query=数据分析精选",
        "http://weixin.sogou.com/weixin?query=人工智能头条",
        "http://weixin.sogou.com/weixin?query=程序员的自留地",
        "http://weixin.sogou.com/weixin?query=互联网创业大佬",
        "http://weixin.sogou.com/weixin?query=互联网创业刊",
        "http://weixin.sogou.com/weixin?query=互联网创业交流",
        "http://weixin.sogou.com/weixin?query=互联网创业指南",
        "http://weixin.sogou.com/weixin?query=互联网创业空间",
        "http://weixin.sogou.com/weixin?query=互联网创业思维",
        "http://weixin.sogou.com/weixin?query=全栈笔记",
        "http://weixin.sogou.com/weixin?query=全栈人生",
        "http://weixin.sogou.com/weixin?query=全栈程序猿",
    ]

    def __init__(self):
        self.conn = Conn().getConnection()
        self.cursor = self.conn.cursor()

    def parse(self, response):
        href = response.selector.xpath('//div[@id="sogou_vr_11002301_box_0"]/@href').extract()[0]
        cmd="~/bin/phantomjs ./getBody.js '%s'" % href
        time.sleep(1)
        stdout, stderr = subprocess.Popen(cmd, shell=True, stdout = subprocess.PIPE, stderr = subprocess.PIPE).communicate()
        print stderr
        response = HtmlResponse(url=href, body=stdout)

        for selector in Selector(response=response).xpath('//*[@id="history"]/div/div/div/div'):
            href = selector.xpath('h4/@hrefs').extract()[0].strip()
            title = ""
            for elem in selector.xpath('h4/text()').extract():
                if len(elem.strip()) > 0:
                    title = elem.strip()
            abstract = selector.xpath('//*[contains(@class, "weui_media_desc")]/text()').extract()[0].strip()
            pubtime = selector.xpath('//*[contains(@class, "weui_media_extra_info")]/text()').extract()[0].strip()
            full_url = response.urljoin(href)
            n = 0
            if len(title) != 0:
                sql = "select * from CrawlPage where title='%s'" % title
                n = self.cursor.execute(sql)
            if len(title) == 0 or n == 0:
                yield scrapy.Request(full_url, callback=self.parse_profile)

    def parse_profile(self, response):
        title = response.xpath('//title/text()').extract()[0].strip()
        create_time = response.xpath('//em[@id="post-date"]/text()').extract()[0].strip()
        source = response.xpath('//a[@id="post-user"]/text()').extract()[0].strip()
        body = response.body.strip()
        tag_content = response.xpath('//div[@id="js_content"]').extract()[0].strip()
        content = remove_tags(tag_content).strip()
        item = WeixinItem()
        item['title'] = title
        item['create_time'] = create_time
        item['source'] = source
        item['body'] = body
        item['content'] = content
        return item
