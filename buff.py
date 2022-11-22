from sys import exit
from urllib.request import quote, unquote
from datetime import datetime
import time
import smtplib
from email.mime.text import MIMEText
from email.header import Header




def mail(price,time,jiage,to_addr):
    from_addr = ''
    password = ''
    # 收信方邮箱
    # 发信服务器
    smtp_server = ''
    time=str(time)
    # 邮箱正文内容，第一个参数为内容，第二个参数为格式(plain 为纯文本)，第三个参数为编码
    msg = MIMEText('当前时间：'+time+'价格为：'+price , 'plain', 'utf-8')
    # 邮件头信息
    msg['From'] = Header('dev')  # 发送者
    msg['To'] = Header('ly')  # 接收者
    subject = jiage+'当前价格:'+str(price)
    msg['Subject'] = Header(subject, 'utf-8')  # 邮件主题
    try:
        smtpobj = smtplib.SMTP_SSL(smtp_server)
        # 建立连接--qq邮箱服务和端口号（可百度查询）
        smtpobj.connect(smtp_server, 465)
        # 登录--发送者账号和口令
        smtpobj.login(from_addr, password)
        # 发送邮件
        smtpobj.sendmail(from_addr, to_addr, msg.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException:
        print("无法发送邮件")
    finally:
        # 关闭服务器
        smtpobj.quit()

def sleeptime(hour, min, sec):
    return hour * 3600 + min * 60 + sec

def check_email_url(email_address):
    # check '@'
    at_count = 0
    for element in email_address:
        if element == '@':
            at_count = at_count + 1

    if at_count != 1:
        return 0

    # check ' '
    for element in email_address:
        if element == ' ':
            return 0

    # check '.com'
    postfix = email_address[-4:]
    if postfix != '.com':
        return 0

    # check char
    for element in email_address:
        if element.isalpha() == False and element.isdigit() == False:
            if element != '.' and element != '@' and element != '_':
                return 0

    return 1


class BUFFSpider():
    import requests
    def __init__(self, urls: str, headers: dict):
        # 初始化结果列表和源代码列表
        self.res = []
        self.pageSource = []
        self.imgurls = []
        # 初始化url列表和headers
        self.urls = urls
        self.headers = headers
        self.num = 0
        self.name = ''


    def cookiecheck(self):
        r = self.requests.get(self.urls, headers=self.headers)
        str1=''
        for i in r.json():
            str1=str1+i
        if str1=='codeerrorextra':
            return False
        else:
            return True

    def getPage_source(self):
        import time
        r = self.requests.get(self.urls, headers=self.headers)
        self.pageSource += r.json()['data']['items']

    def parse(self, datas=None):
        if datas == None:
            datas = self.pageSource
        for d in datas:
            data = {}
            # 商品名
            data['id'] = d.get('id')
            data['name'] = d.get('name')
            data['market_hash_name'] = d.get('market_hash_name')
            # 最小价格
            data['sell_min_price'] = d.get('sell_min_price')
            # 在售数量
            data['sell_num'] = d.get('sell_num')

            # 图片
            data['img'] = d.get('goods_info').get('icon_url')
            # 武器类型
            data['type'] = d.get('goods_info').get('info').get('tags').get('type').get('localized_name')

            try:
                data['fray'] = d.get('goods_info').get('info').get('tags').get('exterior').get('localized_name')
            except:
                # 武器箱等道具没有磨损
                data['fray'] = None
            # 质量
            data['quality'] = d.get('goods_info').get('info').get('tags').get('quality').get('localized_name')
            # 稀有度
            data['rarity'] = d.get('goods_info').get('info').get('tags').get('rarity').get('localized_name')
            self.imgurls.append((data['img'], data['name']))
            self.res.append(data)

    def run(self):
        self.getPage_source()
        self.parse()


    def CheckforCookie(self):
        if self.cookiecheck()==False:
            print("\ncookie不正确\n")
            return False
        else:
            return True

    def CheckforItem(self):
        self.getPage_source()
        self.parse()
        if self.res[0]=='':
            print("\n未查询到该物品")
            return False
        else:
            return True

    def chooseitem(self):
        if len(self.res)==1:
            return 0
        elif len(self.res)<=10:
            print("\n查询到多个物品")
            num = 1
            for i in self.res:
                print("\n编号："+str(num)+"\t\t"+str(i["name"])+"\t当前价格"+str(i["sell_min_price"]))
                num += 1
            choose = int(input("\n选择对应的编号：\n"))
            return choose
        else:
            print("\n查询到的物品太多，请修改搜索词")
            sys.exit(0)




if __name__ == '__main__':
    defcheck_cookie = False
    while defcheck_cookie == False:
        Cookies = input("\n请输入cookie\n")
        headers = {
            "accept": "application/json, text/javascript, */*; q=0.01",
            "cookie": Cookies,
            "referer": "https://buff.163.com/market/csgo",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
        }
        ur='https://buff.163.com/api/market/goods?game=csgo&page_num=1&search=%E5%9C%A3%E8%AF%9E%E8%80%81%E4%BA%BA'
        BUFF = BUFFSpider(ur, headers)
        if BUFF.CheckforCookie() == True:
            defcheck_cookie = True
        time.sleep(1)

    defcheck_item = False
    while defcheck_item == False:
        item = input("输入要监控的物品的全称（仅限一个,例如：AK-47 | 火神 (久经沙场)）：\n")
        ret1 = quote(item, safe=";/?:@&=+$,", encoding="utf-8")
        urls = 'https://buff.163.com/api/market/goods?game=csgo&page_num=1&search='+str(ret1)
        BUFF = BUFFSpider(urls , headers)
        if BUFF.CheckforItem() == True:
            defcheck_item = True
        time.sleep(1)
    choose = BUFF.chooseitem()-1

    sleepfor = float(input("输入邮件提示的小时间隔（整数且需大于等于1）例如：2\n"))
    if float(sleepfor).is_integer() == False:
        input("请输入整数")
        exit(0)

    sleepnum = int(sleepfor) * 12

    mubiao = float(input("当目标物品价格达到多少时发送邮件提醒（纯数字）：\n"))

    rise = float(input("每涨多少钱发送邮件提醒（纯数字）\n"))

    zhisun = float(input("当目标物品价格低于到多少时发送邮件提醒（纯数字）：\n"))

    email_add1 = input("请输入物品达到目标时的提醒邮箱\n")
    if check_email_url(email_add1) == 0:
        input("邮箱格式不合法\n")
        exit(0)

    email_add2 = input("请输入接收价格监控消息的提醒邮箱\n")
    if check_email_url(email_add2) == 0:
        input("邮箱格式不合法\n")
        exit(0)
    ok = True
    num =0
    while  ok == True:
        num += 1
        BUFF.run()
        timenow = datetime.now()
        dict1 = BUFF.res[choose]
        price = dict1["sell_min_price"]
        itemname = dict1["name"]
        print(itemname+"\t当前价格："+price +"\t当前目标提醒价格："+ str(mubiao) + "\t当前时间： " + str(timenow))
        if float(price) >= mubiao:
            mubiao += rise
            mail(price, timenow, '\t达到设定的目标价格！\t'+itemname+"\t当前设定提醒价格为："+str(mubiao), email_add1)
        if float(price) <= zhisun:
            mail(price, timenow, '\t低于设定的价格！\t'+itemname, email_add1)
        if num % sleepnum == 0:
            mail(price, timenow, itemname, email_add2)
        second = sleeptime(0, 5, 0)
        time.sleep(second)