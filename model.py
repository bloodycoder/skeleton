#coding=utf-8 
# -*- coding:cp936 -*-
import MySQLdb
class Model(object):
    def __init__(self):
    	    self.host = 'localhost'
    	    self.port = 3306
    	    self.user = 'root'
    	    self.passwd = '992288'
    	    self.db = 'xieyi'
    def build_connect(self):
    	self.conn = MySQLdb.connect(
    		host = self.host,
    		port = self.port,
    		user = self.user,
    		passwd = self.passwd,
    		db = self.db
    		)
    def exec_ins(self,ins):
    	cur = self.conn.cursor()
    	num = cur.execute(ins)
    	info = {} 
    	if(num>0):
    		info = cur.fetchmany(num)
    	cur.close()
    	self.conn.commit()
    	return info
    def close(self):
    	self.conn.close()