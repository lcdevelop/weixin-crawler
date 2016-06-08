# coding:utf-8

import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
import MySQLdb

class Conn:
    def getConnection(self):
        conn = MySQLdb.connect(host="127.0.0.1",user="lichuang",passwd="qwerty",db="sharenote2.0",charset="utf8")
        return conn
