# -*- coding: utf-8 -*-
from spider import *
import os
from bs4 import BeautifulSoup
import json

class tbSpider(spider_parse):
    def __init__(self):
	file = "download/tb/"
        dir = os.path.join(os.path.dirname(__file__),file)
	self.real_dir = os.path.join(dir , "s-taobao-com")
	os.system('rm -rf '+dir)
        os.system('rm -rf '+dir+'/.gwd')
	s=Spider("https://s.taobao.com/search?q=%E5%A4%96%E5%A5%97",dir)
        s.set_white("s\.taobao\.com/search")
        s.set_white("q=%E5%A4%96%E5%A5%97")
	s.run()
    
    #get product_id,product_name
    def parse_url(self,data):
	result1 = []
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
	    pass
	return result1

    def get_all_price(self):
        result=self.parse_data()
	return result
