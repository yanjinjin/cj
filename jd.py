# -*- coding: utf-8 -*-
from spider import *
import os
from bs4 import BeautifulSoup
import json

class jdSpider(spider_parse):
    def __init__(self):
	file = "download/jd/"
        dir = os.path.join(os.path.dirname(__file__),file)
	self.real_dir = os.path.join(dir , "list-jd-com")
	s=Spider("http://list.jd.com/list.html?cat=9987,653,655&page=1&delivery=1&trans=1&JL=4_21_0",dir)
        s.set_white("list\.jd\.com/list")
        s.set_white("cat=9987,653,655")
	#s.run()
    
    #get product_id,product_name
    def parse_url(self,data):
	result1 = []
	try:
	    soup = BeautifulSoup(data, "html.parser")
	    items = soup.select('li.gl-item')
	except AttributeError as e:
	    return []
	for item in items:
    	    result2 = []
	    sku = item.find('div')['data-sku']
	    if sku == None:
		return []

    	    price_url = 'http://p.3.cn/prices/mgets?skuIds=J_' + str(sku)
    	    #s = Spider_one(url)
    	    #result=s.parse_html()
	    #price = result.json()[0]['p']
    	    price=str(int(60*random.random()+1))
	    name = item.find('div', class_="p-name").find('em').string
    	    item_url = 'http:' + item.find('div', class_="p-name").find('a')['href']
	    result2.append(str(sku))
	    result2.append(name)
	    result2.append(price)
	    result2.append(item_url)
	    result1.append(result2)
	return result1

    def get_all_price(self):
        result=self.parse_data()
	return result
