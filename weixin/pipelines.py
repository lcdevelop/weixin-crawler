# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import MySQLdb
from weixin.conn import Conn

class WeixinPipeline(object):
    def __init__(self):
        self.conn = Conn().getConnection()
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        sql = "insert ignore into CrawlPage(title, source, body, content, create_time) values(%s, %s, %s, %s, %s)"
        param = (item['title'], item['source'], item['body'], item['content'], item['create_time'])
        self.cursor.execute(sql,param)
        self.conn.commit()
