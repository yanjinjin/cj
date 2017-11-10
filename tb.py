# -*- coding: utf-8 -*-
from spider import *
from spider_proxy import *
import os
from bs4 import BeautifulSoup
import json
import urllib
import sys
reload(sys)
sys.setdefaultencoding('utf8')

class tbSpider():
    def __init__(self):
	#self.url = "http://blog.csdn.net/ljp1205/article/details/77684550"
	self.depth = 1
	self.logfile = os.path.join(os.path.dirname(__file__),'./spider.log')
	self.loglevel = 5
	self.threads = 1
	self.dbfile = os.path.join(os.path.dirname(__file__),'./spider.db')
	#self.key = "外套"
	self.key = None
	self.proxys = getProxys()
	os.system('rm -rf '+self.logfile)
	os.system('rm -rf '+self.dbfile)
	pages = 20
	products = ["外套","皮草衣","保暖内衣","华为","芭比娃娃","bb霜","钱包","家居用品","女童外套","男童外套","运动鞋","高跟鞋","皮鞋","凉鞋"]
	for product in products:
	    i = 0
	    while i < pages:
		page_num = i*60 
		url_page = "https://s.taobao.com/search?initiative_id=tbindexz_20170306&ie=utf8&spm=a21bo.2017.201856-taobao-item.2&sourceId=tb.index&search_type=item&ssid=s5-e&commend=all&imgfile=&q="+urllib.quote(product)+"&suggest=0_9&_input_charset=utf-8&s="+str(page_num)
		#url_page = "https://s.taobao.com/list?q="+urllib.quote(product)+"&style=grid&seller_type=taobao&bcoffset=12&s=" + str(page_num)
		print url_page
		spider = Spider(url_page,
					self.depth,
					self.logfile, self.loglevel,
					self.threads,
					self.dbfile,
					self.key,
	  				self.proxys)
		spider.start()
		i = i + 1 
    #get product_id,product_name
    def parse_data(self):
	result1 = []
	spider = Spider("http://default",
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
	        continue
	    g_page_config_e = data[g_page_config_s:].find("}};")
	    if g_page_config_e == -1:
                continue
	    product_info = data[g_page_config_s+16:g_page_config_s+g_page_config_e+2]
	    try:
	        p = json.loads(product_info)
	        itemlist = p["mods"]["itemlist"]["data"]["auctions"]	
	        for i in itemlist:
	            result2 = []
	            result2.append(i["nid"])
	            result2.append(i["raw_title"])
	            result2.append(i["view_price"])
		    url = i["detail_url"].replace('\\u00','%')
	            result2.append("http:" + urllib.unquote(url))
	            result1.append(result2)
	    except:
	        continue
	return result1

    def get_all_price(self):
        result=self.parse_data()
	return result
