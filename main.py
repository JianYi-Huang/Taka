import requests
import time
import random
import re
import pymysql
import json
from bs4 import BeautifulSoup


def get_config(id="all"):
    with open("C:/JianYi-Huang/config.json", "r") as config:
        result = json.load(config)
        if id == "all":
            return result
        else:
            try:
                return result[id]
            except:
                return result["error"] + id

config = get_config("mysql")
# 连接database
conn = pymysql.connect(
    host = '118.24.61.204',
    user = 'HuangJianYi',
    password = config['password'],
    database = 'proxies',
    charset = 'utf8')
# 得到一个可以执行SQL语句的光标对象
cursor = conn.cursor()  # 执行完毕返回的结果集默认以元组显示

def update_proxy(ipprot):
    sql = 'SELECT MAX(id) FROM default_ip_copy1;' # 获取default_ip_copy1表下id字段最大的值
    cursor.execute(sql)
    new_id = cursor.fetchone()[0]
    new_id += 1
    try:
        sql = 'insert into default_ip_copy1(id,ip) values(%s,"%s");' % (new_id, ipprot)
        # 执行sql语句
        cursor.execute(sql)
    except Exception as e:
        # 有异常就回滚
        conn.rollback()
        print('事务处理失败', e)
    else:
        # 正常提交
        conn.commit()

def get_header(use='computer'):
    computer_agents = [
        'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
        'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0);',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
        'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
        'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11',
        'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
        'Mozilla/5.0 (X11; Linux x86_64; rv:76.0) Gecko/20100101 Firefox/76.0'
    ]
    mobile_agents = [
        'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5',
        'Mozilla/5.0 (iPod; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5',
        'Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5',
        'Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
        'MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
        'Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10',
        'Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13',
        'Mozilla/5.0 (BlackBerry; U; BlackBerry 9800; en) AppleWebKit/534.1+ (KHTML, like Gecko) Version/6.0.0.337 Mobile Safari/534.1+',
        'Mozilla/5.0 (hp-tablet; Linux; hpwOS/3.0.0; U; en-US) AppleWebKit/534.6 (KHTML, like Gecko) wOSBrowser/233.70 Safari/534.6 TouchPad/1.0',
        'Mozilla/5.0 (SymbianOS/9.4; Series60/5.0 NokiaN97-1/20.0.019; Profile/MIDP-2.1 Configuration/CLDC-1.1) AppleWebKit/525 (KHTML, like Gecko) BrowserNG/7.1.18124',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Titan)',
        'UCWEB7.0.2.37/28/999',
        'NOKIA5700/ UCWEB7.0.2.37/28/999',
        'Openwave/ UCWEB7.0.2.37/28/999',
        'Mozilla/4.0 (compatible; MSIE 6.0; ) Opera/UCWEB7.0.2.37/28/999'
    ]
    if use == 'mobile':  # 随机获取一个headers
        agent = random.choice(mobile_agents)
    else:
        agent = random.choice(computer_agents)
    headers = {
        'User-Agent': agent,
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'zh-CN,zh;q=0.9',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Upgrade-Insecure-Requests':'1'
    }
    return headers

header = get_header()

def inspect_proxy(ipprot):

    url = 'http://httpbin.org/get'
    url = 'http://ip.cip.cc/'
    proxy = {'http': str(ipprot), 'https': str(ipprot)}

    request = requests.get(url, headers=header, proxies=proxy)
    print(request)

def inspect_ip(ipprot):
    time.sleep(1)

    url = 'http://118.24.61.204/ip'
    url = 'https://weibo.com/u/7230522444?is_all=1'
    url = 'https://www.douban.com/group/638298/discussion?start=25'
    # url = 'https://www.baidu.com'
    proxy = {'http': str(ipprot), 'https': str(ipprot)}
    try:
        request = requests.get(url, headers=header, proxies=proxy, verify=False, timeout=5)
        request.encoding = 'utf-8'
        soup = BeautifulSoup(request.text, 'html.parser')
        print(soup)
        if request.status_code == 200: 
            print('可用代理:' + ipprot)
            # 写入数据库
            update_proxy(ipprot)
        else:
            print('不可用代理:' + ipprot)
    except:
        print('代理超时:' + ipprot)

    # request = requests.get(url, headers=header, proxies=proxies)
    # print(request)
    # if request.status_code == 200: 
    #     print('可用代理:' + ipprot)
    #     # 写入数据库
    # else:
    #     print('不可用代理:' + ipprot)

def IPList_61():
    for q in range(1,30):
        url = 'http://www.66ip.cn/'+str(q)+'.html'
        html = requests.get(url, headers=header)
        html.encoding = 'gb18030'

        if html != None:
            iplist = BeautifulSoup(html.text, 'html.parser')
            iplist = iplist('tr')
            i = -2
            for ip in iplist:
                loader = ''
                initial = True
                if i >= 0:
                    for ipport in ip.find_all('td',limit=2):
                        if initial:
                            loader += ipport.text.strip() + ':'
                        else:
                            loader += ipport.text.strip()
                        initial = False
                    inspect_ip(loader)
                    # print(loader)
                i += 1
        time.sleep(1)

def IPList_jxl():
    for q in range(1,8):
        url = 'https://ip.jiangxianli.com/?page='+str(q)
        html = requests.get(url, headers=header)
        # html = requests.get(url, headers=header)
        html.encoding = 'utf-8'
        if html != None:
            iplist = BeautifulSoup(html.text, 'html.parser')
            iplist = iplist('tr')
            i = -1
            for ip in iplist:
                loader = ''
                initial = True
                if i >= 0:
                    for ipport in ip.find_all('td',limit=2):
                        if initial:
                            loader += ipport.text.strip() + ':'
                        else:
                            loader += ipport.text.strip()
                        initial = False
                    inspect_ip(loader)
                    # print(loader)
                i += 1
        time.sleep(1)




if __name__ == '__main__':
        # sql = 'select id,ip from default_ip_copy1;'
        # cursor.execute(sql)
        # ret2 = cursor.fetchmany(8)
        # print(ret2)
        # last_id = cursor.lastrowid
        # print('插入后最后一条数据的ID是:', last_id)
        # sql = 'SELECT MAX(id) FROM default_ip_copy1;' # 获取default_ip_copy1表下id字段最大的值
        # cursor.execute(sql)
        # new_id = cursor.fetchone()
        # print(new_id)
        # # 关闭连接
        # cursor.close()
        # conn.close()
    #IPList_61()
    IPList_jxl()
    # inspect_ip('105.27.238.166:80')
    # update_proxy('105.27.238.166:80')