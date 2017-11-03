#coding=utf-8
import os
curdir = os.path.dirname(__file__)
import sys
sys.path.append(curdir) 
import os,web
from web.session import Session
import math
import threading
from time import ctime,sleep
import commands
from multiprocessing import Process, Pool
from model import *
from plog import *
from verifycode import *
from weixin import *
from jd import *
from tb import *
import sys
reload(sys)
sys.setdefaultencoding('utf8')

web.config.debug = False

urls = (
    '/', 'index',
    '/index','index',
    '/detail','detail',
    '/register','register',
    '/login','login',
    '/logout','logout',
    '/admin','admin'
    )

t_globals = {  
    'datestr': web.datestr,  
    'cookie': web.cookies,  
}
render = web.template.render(os.path.join(curdir,'templates'), base='base', globals=t_globals)
app = web.application(urls, locals())

class MySessionExpired(web.HTTPError):  
    def __init__(self, headers,message):  
        web.HTTPError.__init__(self, '200 OK', headers, data=message)  
   
class MySession(Session):  
    def __init__(self, app, store, initializer=None):  
        Session.__init__(self,app,store,initializer)  
   
    def expired(self):  
        self._killed = True  
        self._save()  
        message = self._config.expired_message  
        headers = {'Content-Type': 'text/html','Refresh':'2;url="/index"'}  
        raise MySessionExpired(headers, message)  

web.config.session_parameters['cookie_name'] = 'cj_session_id'
web.config.session_parameters['cookie_path'] = '/'
web.config.session_parameters['cookie_domain'] = None
web.config.session_parameters['timeout'] = 86400  # 24 hours
web.config.session_parameters['ignore_expiry'] = False
web.config.session_parameters['ignore_change_ip'] = True
web.config.session_parameters['secret_key'] = 'fLjUfxqXtfiNoIldA0A0J'
web.config.session_parameters['expired_message'] = ''
if web.config.get('_session') is None:
    sess = MySession(app, web.session.DiskStore(os.path.join(curdir,'sessions')), initializer = {'username': None})
    web.config._session = sess
else:
    sess = web.config._session
    print sess

class index:
    def GET(self):
	if sess.username == None:	
	    plog("who visit")
	else:
	    plog("%s visit"%sess.username)
	
	m = Model()
	result = m.select_from_product_cj()
	return render.index(result)
    def POST(self):
	search = web.input()	
	product_name = search.get('product_name')
	m = Model()
        result = m.select_from_product_by_product_name(product_name)
	return render.index(result)	

class detail:
    def GET(self):
	if sess.username == None:
            raise web.seeother('login')
        else:
            plog("%s view detail "%sess.username)
	search = web.input()
        product_id = search.get('product_id')
	m = Model()
        result = m.select_from_price_by_product_id(product_id)
	categories = ""
	series = ""
	for i in result:
	    categories = categories + i[1] + ","
	for i in result:
	    series = series + i[0] + ","
	product = m.select_from_product_by_product_id(product_id)
	return render.detail(categories.strip(","),series.strip(","),product)	

class register:
    def GET(self):
        vc = Verifycode()
        return render.register(vc.getcode())
    def POST(self):
        search = web.input()
        username = search.get('username')
        passwd1 = search.get('password1')
        passwd2 = search.get('password2')
        verifycode = search.get('verifycode')
        verifycode_hidden = search.get('verifycode_hidden')
        if passwd1 != passwd2:
            return render.message("registererr-passwd")
        if verifycode.lower() != verifycode_hidden.lower():
            return render.message("registererr-verify")
        m = Model()
        if m.select_userid_from_user_by_username(username) != None:
            return render.message("registererr-username")
        m.insert_into_user(username,passwd1)
        return render.message("registerok")

class login:
    def GET(self):
        return render.login()
    def POST(self):
        search = web.input()
        username = search.get('username')
        passwd = search.get('password')
        m = Model()
        result = m.select_rowcount_from_user_by_login(username,passwd)
        if result ==1:
            sess.username=username
            print sess.username
            web.setcookie('username', username)
            plog("%s login success"%sess.username)
	    raise web.seeother('index')
            
	plog("who login failed")
        return render.message("loginerr")

class logout:
    def GET(self):
        #print sess.username
        sess.username=None
        sess.kill()
        web.setcookie('username', '', expires=-1)
        raise web.seeother('index')

class admin:
    def GET(self):
        if sess.username == None or sess.username != "admin@admin":
	    raise web.seeother("/index")
	
	cmd = "tail -100 %s"%os.path.join(curdir,'cj.log')
	print cmd
 	web_log_content = commands.getoutput(cmd).split('\n')
	cmd = "tail -100 %s"%os.path.join(curdir,'spider.log')
        print cmd
        spider_log_content = commands.getoutput(cmd).split('\n')
	m = Model()
   	product = m.select_from_product()
        user = m.select_from_user_for_admin()
        count = []
        user_count = m.select_rowcount_from_user()
	product_count = m.select_rowcount_from_product()
        count.append(user_count)
        count.append(product_count)
	return render.admin(web_log_content,spider_log_content,user,product,count) 
    def POST(self):
	if sess.username == None or sess.username != "admin@admin":
            raise web.seeother("/index")
	pass

def task_del():
    m = Model()
    plog("start task del......")
    m.del_from_product_timeout()
    m.del_from_price_timeout()

def task_insert(result):
    n = 0
    m = Model()
    plog("start task insert......")
    for i in result:
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
    plog("product num : %d"%n)
 
def task_spider():
    while True:
        #sleep(60*60*24*random.random() + 24*60*60)
	sleep(10*random.random() + 6)
	task_del()
	####################################
        #jd_result = get_all_price()
	#task_insert(jd_result)
	####################################
        tb_result = get_all_tb_price()
	task_insert(tb_result)
	####################################

def task_web():
    app.run()

if __name__ == "__main__":  
    s = Process(target=task_spider)
    w = Process(target=task_web)
    s.daemon = True
    w.daemon = True
    s.start()
    w.start()
    s.join() 
    w.join()
