# -*- coding: utf-8 -*-
from spider import *
from spider_proxy import *
from model import *
import os
from bs4 import BeautifulSoup
import json
import urllib
import gc
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
	self.spider = Spider("http://default",
                     self.depth,
                     self.logfile, self.loglevel,
                     self.threads,
                     self.dbfile,
                     self.key)

    #get product_id,product_name
    def task_insert(i,m):
        n = 0
        print("商品id：%s \n 名称: %s \n 价格: %s 元  \n 链接: %s" % (i[0],i[1].strip(),i[2],i[3]))
        m.insert_into_product(i[0],i[1].strip(),i[3])
        m.insert_into_price(i[0],i[2])
        n=n+1
        all_price = m.select_from_price_by_product_id(i[0])
        old_price = 0
        for j in all_price:
            old_price = float(j[0])
            break
        print float(i[2]),old_price
        if float(i[2]) <= old_price * 80/100:
            m.update_from_product_by_product_id(i[0])

    def parse_data(self):
        pages = 20
        products = [ "毛呢外套", "毛衣","织衫" ,"羽绒服", "棉服", "连衣裙", "气场外套", "风衣", "裤子", "卫衣", "T恤", "阔腿裤", "衬衫", "牛仔裤", "半身裙", "大码女装", "时尚套装", "西装", "打底衫", "夹克", "皮衣","皮草" ,"妈妈装", "民族舞台", "腔调", "私服名媛", "甜美风", "文艺风", "街头风", "原创", "通勤风", "婚纱礼服",  "女鞋", "短靴", "切尔西", "长靴", "袜靴", "小白鞋", "运动鞋女", "帆布鞋", "雪地靴", "乐福鞋", "松糕厚底", "玛丽珍鞋", "低跟", "中跟", "高跟", "妈妈鞋", "男鞋", "靴子", "休闲鞋", "雕花布洛克", "板鞋", "帆布鞋", "运动风", "高帮鞋" ,"豆豆鞋", "乐福鞋", "船鞋", "增高鞋", "正装商务",
 "户外休闲鞋", "爸爸鞋","连衣裙","保暖连体","裤子","羽绒","居家睡衣","针织","帽子","亲子装","童鞋","学步鞋","女童运动鞋",
"男童运动鞋","毛毛虫童鞋","雪地靴","马丁靴","长靴","玩具","积木","毛绒玩具","早教","儿童自行车",
"电动童车","遥控模型","户外玩具","亲子玩具","学习用品","描红本","","美妈大衣","孕妇裤","月子服",
"哺乳文胸","吸奶器","防辐射","孕妇内裤","连衣裙","待产包","孕妇牛仔裤","孕妇营养品","防溢乳垫","美德乐",
"十月妈咪","三洋","Bravado","新生儿","婴儿床","婴儿推车","睡袋","抱被","隔尿垫","学步车","安抚奶嘴","体温计",
"纸尿裤","花王","洗衣液","湿巾","生活电器","厨房电器","个人护理","空气净化器","扫地机器人","吸尘器","取暖器",
"烤箱","豆浆机","榨汁料理","电饭煲","吹风机","足浴盆","剃须刀","卷发器","按摩器材","冬季火锅","蓝牙耳机","电暖桌",
"蓝牙音箱","电热毯","加湿器","暖风机","","iphone7plus","iphone6s","iphone7","华为mate9","苹果6S","苹果6plus",
"荣耀","三星","三星s7","小米","红米note3","华为mate8","魅族","oppovivo","","鱼线","鱼线轮","户外鞋","登山包",
"帐篷","睡袋","望远镜","皮肤衣","速干衣","速干裤","手电筒","山地车","公路车","骑行服","护具","军迷用品","舞蹈体操",
"羽毛球","游泳","瑜伽","跑步机","健身器","烧烤架","休闲鞋","冲锋裤","单车零件","骑行装备","遮阳棚","户外手表",
"户外风衣","军迷套装","战术鞋","","沙发","床","高低床","餐桌","床垫","茶几","电视柜","衣柜","鞋柜","椅凳","书桌",
"电脑桌","坐具","现代简约","美式家具","北欧家具","中式家具","儿童家具","真皮沙发","布艺沙发","皮床","实木床","儿童床",
"乳胶床垫","儿童学习桌","书架","花架","椅子","电脑椅","佛山家具","发夹","发圈","发网","头巾","头箍","假发","皮筋","耳环","丝巾扣","项链","胸针","腰带","手链","手镯","戒指","脚链","饰链","儿童饰品","手机饰品","笔类","薄","本","册","日用文具","办公设备","复印机","考勤机","办公家具","仿真花","叶","藤","仿真树木","仿真水果","光纤花","干花","盆花","盆景","耳机","耳塞","电动剃须刀","电子计算器","电子记事本","字典","电筒","电池","打火","烟具","插头，插座","稳压器","充电器","照明","灯具"," 钟表仪器","仪表","游戏机","卡激光产品门钟","门铃","防盗器","点","验钞机","定时器","指南针","电子保健品","电子配件元器件","随身听","照相器材","收音机","其他电子产品","复读机","手套","毛巾","浴巾","帽子","文胸","内衣","内裤","泳装","围巾","头巾","床上用品","坐垫","靠垫","窗帘布","鞋垫","台布","茶巾","皮带","拉链","纽扣","衬料","时尚饰品","帽子","领带","围巾","头巾","手套","袜子","针织服装","梭织服装","品牌服装","男装","女装","内衣","睡衣","浴衣","衬衣","毛衣","西服","裤子","休闲服装","婚纱","礼服","工作服","制服","袜子","锁具","指甲钳","钥匙坯","刀","剑","剪刀","美工刀","五金工具","园艺五金","刮剃刀","刀片","滑板车","门窗五金","装饰水暖","保温杯","口子杯","不锈钢厨房用具","安全扣","头盔","金属匙扣","金属架","台","测量工具","胶水制品","净水器","饮水机","榨汁机","咖啡机，豆浆机","电热壶，电热杯","电炒锅","电饭煲","湿度调节器","空气净化器","取暖电器","电吹风","吸尘器","电扇","排气扇","电熨斗","视听器材","耳机","遥控器","锂电池","镍氢电池","磁卡","IP卡","IC卡","拨号器","充电器","天线","电话机","可视电话","移动电话","手机及配件","传真机","网络通信产品","通讯","声讯系统","塑料玩具","填充玩具","绒毛玩具","电子玩具","电动玩具","玩具珠","球","礼品娃娃","玩具车","玩具枪","模型玩具","益智玩具","童车","卡通漫画海报","茶叶","调味品","糖果","饼干","炒货","酒类","饮品","小食品"]
        m = Model()
        result2 = []
	for product in products:
            i = 0
            while i < pages:
                page_num = i*60
                url_page = "https://s.taobao.com/search?initiative_id=tbindexz_20170306&ie=utf8&spm=a21bo.2017.201856-taobao-item.2&sourceId=tb.index&search_type=item&ssid=s5-e&commend=all&imgfile=&q="+urllib.quote(product)+"&suggest=0_9&_input_charset=utf-8&s="+str(page_num)
                #url_page = "https://www.baidu.com"
                #print url_page
                result = self.spider.get_page(url_page)
		
                i = i + 1
		if result == None:
                    continue
                data = result['content']
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
		        result2[0]=i["nid"]
		        result2[1]=i["raw_title"]
		        result2[2]=i["view_price"]
		        url = i["detail_url"].replace('\\u00','%')
		        result2[3]="http:" + urllib.unquote(url)
			self.task_insert(result2,m)
		    del url_page
		    del result
		    gc.collect()
		except:
		    pass

    def get_all_price(self):
        self.parse_data()
