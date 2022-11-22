from sys import exit
from urllib.request import quote, unquote
import requests
from lxml import etree
from datetime import datetime
import time
import smtplib
from email.mime.text import MIMEText
from email.header import Header





def itemconfirm(url,headers):
    resp = requests.get(url, headers=headers)
    html = etree.HTML(resp.text)  # 将HTML源码进行预加载
    list1 = html.xpath('/html//div[@class="list list"]/a')
    if len(list1)==1:
        return 1
    elif len(list1)<=10:
        print("\n查询到多个物品")
        num = 1
        for i in list1:
            print("\n编号："+str(num)+"\t"+str(html.xpath('//*[@id="__layout"]/div/div[2]/div/div[4]/a[{:}]/div[2]/text()'.format(num))[0])+"\t\t当前价格："+str(html.xpath('//*[@id="__layout"]/div/div[2]/div/div[4]/a[{:}]/div[3]/div[1]/text()'.format(num))[0])+str(html.xpath('//*[@id="__layout"]/div/div[2]/div/div[4]/a[{:}]/div[3]/div[1]/sub/text()'.format(num))[0]))
            num+=1
        choose = int(input("\n选择对应的编号：\n"))
        return choose
    else:
        print("\n查询到的物品太多，请修改搜索词")
        exit(0)

def ParseConfimCode(url,headers):
    resp = requests.get(url,headers = headers)
    html = etree.HTML(resp.text) #将HTML源码进行预加载
    div1 = html.xpath("/html/body/div[1]/div/div/div[2]/div/div[4]/a/div[3]/div[1]/text()")
    div2 = html.xpath("/html/body/div[1]/div/div/div[2]/div/div[4]/a/div[3]/div[1]/sub/text()")
    price = div1[0]+div2[0]
    return price

def parsecode(url,headers,choose):
    resp = requests.get(url,headers = headers)
    html = etree.HTML(resp.text) #将HTML源码进行预加载
    div1 = str(html.xpath('//*[@id="__layout"]/div/div[2]/div/div[4]/a[{:}]/div[3]/div[1]/text()'.format(choose))[0])
    div2 = str(html.xpath('//*[@id="__layout"]/div/div[2]/div/div[4]/a[{:}]/div[3]/div[1]/sub/text()'.format(choose))[0])
    price = div1+div2
    name = str(html.xpath('//*[@id="__layout"]/div/div[2]/div/div[4]/a[{:}]/div[2]/text()'.format(choose))[0])
    return price,name

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


if __name__ == "__main__":
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0"
    }
    num = 0
    item = input("输入要监控的物品的全称（仅限一个,例如：AK-47 | 火神 (久经沙场)）：\n")
    ret1 = quote(item, safe=";/?:@&=+$,", encoding="utf-8")
    url='https://www.igxe.cn/market/csgo?keyword='+str(ret1)
    ok = True
    try:
        ParseConfimCode(url, headers)
    except:
        ok = False
        a = input("未查询到对应物品\n")
        exit(0)
    choose = itemconfirm(url,headers)
    sleepfor = float(input("输入邮件提示的小时间隔（整数且需大于等于1）例如：2\n"))
    if float(sleepfor).is_integer() == False:
        input("请输入整数")
        exit(0)
    sleepnum = int(sleepfor)*12

    mubiao = float(input("当目标物品价格达到多少时发送邮件提醒（纯数字）：\n"))

    rise = float(input("每涨多少钱发送邮件提醒（纯数字）\n"))

    zhisun = float(input("当目标物品价格低于到多少时发送邮件提醒（纯数字）：\n"))

    email_add1 = input("请输入物品达到目标时的提醒邮箱\n")
    if check_email_url(email_add1)==0:
        input("邮箱格式不合法\n")
        exit(0)

    email_add2 = input("请输入接收价格监控消息的提醒邮箱\n")
    if check_email_url(email_add2)==0:
        input("邮箱格式不合法\n")
        exit(0)

    while  ok == True:
        num += 1
        timenow = datetime.now()
        list1= parsecode(url, headers,choose)
        price = list1[0]
        itemname = list1[1]
        print(itemname+"\t当前价格："+price +"\t当前目标提醒价格："+ str(mubiao) + "\t当前时间： " + str(timenow))
        if float(price) >= mubiao:
            mubiao += rise
            mail(price, timenow, '达到设定的目标价格！'+itemname+"\t当前设定提醒价格为："+str(mubiao), email_add1)
        if float(price) <= zhisun:
            mail(price, timenow, '低于设定的价格！'+itemname, email_add1)
        if num % sleepnum == 0:
            mail(price, timenow, itemname, email_add2)
        second = sleeptime(0, 5, 0)
        time.sleep(second)