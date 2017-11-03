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

class tbSpider(spider_parse):
    def __init__(self,url):
	file = "download/"
        dir = os.path.join(os.path.dirname(__file__),file)
        self.real_dir = os.path.join(dir , "s-taobao-com")
        os.system("rm -rf "+self.real_dir)
	os.system("rm -rf "+dir+".gwd")
	proxys = getProxys()
        s=Spider(url,proxys,dir)
        s.set_white("s\.taobao\.com/list")
	s.run()
    #get product_id,product_name
    def parse_url(self,data):
	result1 = []
	g_page_config_s = data.find("g_page_config = ")
	if g_page_config_s == -1:
	    return result1
	g_page_config_e = data[g_page_config_s:].find("}};")
	if g_page_config_e == -1:
            result1
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
	    pass
	return result1

def get_all_tb_price():
    result = []
    products = ["外套","皮草衣","保暖内衣","华为","芭比娃娃","bb霜","钱包","家居用品","女童外套","男童外套","运动鞋","高跟鞋","皮鞋","凉鞋"]
    for product in products:
        i = 0
	pages = 20
	while i < pages:
	    page_num = i*60 
	    i = i + 1 
	    tb = tbSpider("https://s.taobao.com/list?spm=a21bo.50862.201867-links-0.38.7f35a3b33tWAVy&q="+product+"&style=grid&seller_type=taobao&bcoffset=12&s="+str(page_num))
            result = result + tb.parse_data()
    print result
    return result
