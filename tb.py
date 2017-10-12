# -*- coding: utf-8 -*-
from spider import *
import os
from bs4 import BeautifulSoup
import json
import sys
reload(sys)
sys.setdefaultencoding('utf8')

class tbSpider():
    def __init__(self):
        self.url = "https://s.taobao.com/list?spm=a21bo.50862.201867-links-0.38.7f35a3b33tWAVy&q=%E5%A4%96%E5%A5%97&cat=50344007&style=grid&seller_type=taobao"
	#self.url = "http://blog.csdn.net/ljp1205/article/details/77684550"
	self.depth = 1
	self.logfile = os.path.join(os.path.dirname(__file__),'./spider.log')
	self.loglevel = 5
	self.threads = 1
	self.dbfile = os.path.join(os.path.dirname(__file__),'./spider.db')
	self.key = "外套"
	#self.key = None
	os.system('rm -rf '+self.logfile)
	os.system('rm -rf '+self.dbfile)
	spider = Spider(self.url,
                    self.depth,
                    self.logfile, self.loglevel,
                    self.threads,
                    self.dbfile,
                    self.key)
	spider.start()
 
    #get product_id,product_name
    def parse_data(self):
	result1 = []
	spider = Spider(self.url,
                    self.depth,
                    self.logfile, self.loglevel,
                    self.threads,
                    self.dbfile,
                    self.key)
	all_pages = spider.sql_worker.select_all_pages()
	for i in all_pages:
	    data = str(i)
	    g_page_config_s = data.find("g_page_config = ")
	    if g_page_config_s == -1:
	        return []
	    g_page_config_e = data[g_page_config_s:].find("}};")
	    if g_page_config_e == -1:
                return []
	    product_info = data[g_page_config_s+16:g_page_config_s+g_page_config_e+2]
	    try:
	        p = json.loads(product_info)
	        itemlist = p["mods"]["itemlist"]["data"]["auctions"]	
	        for i in itemlist:
	            result2 = []
	            result2.append(i["nid"])
	            result2.append(i["raw_title"])
	            result2.append(i["view_price"])
	            result2.append("http:" + i["detail_url"])
	            result1.append(result2)
	    except:
	        break
	return result1

    def get_all_price(self):
        result=self.parse_data()
	return result
