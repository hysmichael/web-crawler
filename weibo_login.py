# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import re, json, base64, binascii, rsa, requests, random

WBCLIENT = 'ssologin.js(v1.4.5)'
user_agent = (
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.11 (KHTML, like Gecko) '
    'Chrome/20.0.1132.57 Safari/536.11'
)
session = requests.session()
session.headers['User-Agent'] = user_agent
 
 
def encrypt_passwd(passwd, pubkey, servertime, nonce):
    key = rsa.PublicKey(int(pubkey, 16), int('10001', 16))
    message = str(servertime) + '\t' + str(nonce) + '\n' + str(passwd)
    passwd = rsa.encrypt(message.encode('utf-8'), key)
    return binascii.b2a_hex(passwd)
 
 
def wblogin(username, password):
    resp = session.get(
        'http://login.sina.com.cn/sso/prelogin.php?'
        'entry=sso&callback=sinaSSOController.preloginCallBack&'
        'su=%s&rsakt=mod&client=%s' %
        (base64.b64encode(username.encode('utf-8')), WBCLIENT)
    )
 
    pre_login_str = re.match(r'[^{]+({.+?})', resp.text).group(1)
    pre_login = json.loads(pre_login_str)
 
    pre_login = json.loads(pre_login_str)
    data = {
        'entry': 'weibo',
        'gateway': 1,
        'from': '',
        'savestate': 7,
        'userticket': 1,
        'ssosimplelogin': 1,
        'su': base64.b64encode(requests.utils.quote(username).encode('utf-8')),
        'service': 'miniblog',
        'servertime': pre_login['servertime'],
        'nonce': pre_login['nonce'],
        'vsnf': 1,
        'vsnval': '',
        'pwencode': 'rsa2',
        'sp': encrypt_passwd(password, pre_login['pubkey'],
                             pre_login['servertime'], pre_login['nonce']),
        'rsakv' : pre_login['rsakv'],
        'encoding': 'UTF-8',
        'prelt': '115',
        'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.si'
               'naSSOController.feedBackUrlCallBack',
        'returntype': 'META'
    }
    resp = session.post(
        'http://login.sina.com.cn/sso/login.php?client=%s' % WBCLIENT,
        data=data
    )
 
    login_url = re.search(r'replace\([\"\']([^\'\"]+)[\"\']',
                          resp.text).group(1)
    resp = session.get(login_url)
    login_str = re.match(r'[^{]+({.+?}})', resp.text).group(1)
    return json.loads(login_str)
 

def initialize_url(url):
    r = session.get(url, stream=True)
    r.encoding = 'utf-8'
    return BeautifulSoup(r.raw.read())


### login to weibo
print 'TRYING TO LOGIN'
wblogin('hongyanshu1994@yahoo.com.cn', 'R354K1d0')
print 'LOGIN SUCCESSFUL'


while True:
    identifier = random.randint(1000000000, 6000000000)
    url = 'http://www.weibo.com/u/%d' % (identifier)
    page = initialize_url(url)
    
    print url

    title = page.find('title').string
    if title != u'404错误':        

        print page

        counters = page.find('table', class_='tb_counter').tbody.tr.contents
        following   = counters[0].a.strong.string 
        follower    = counters[1].a.strong.string
        weibos      = counters[2].a.strong.string

        print following
        print follower
        print weibos


