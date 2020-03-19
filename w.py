# coding:utf-8
import smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import json

import requests

#风和天气api，官网可以申请，只需要修改key即可
url = 'https://free-api.heweather.net/s6/weather/{}?location={}&key={}'
city1 = 'chongqing'
key = '****'

class PostWeatherEmail(object):
    def __init__(self):
        # 发件人地址
        self.from_addr = '******@qq.com'
        # 邮箱密码
        #如果使用QQ邮箱进行发送需要参照https://service.mail.qq.com/cgi-bin/help?subtype=1&&no=1001256&&id=28获得授权码
        self.password = '*******'
        self.SmtpServer = 'smtp.qq.com'

        # 收件人地址
        self.to_address = ['*****@qq.com']
        self.mail_text = ''
        self.url =url.format("now",city1,key)

    def _format_addr(self, s):
        """
        转化地址
        :param s:
        :return: 指定格式
        """
        name, addr = parseaddr(s)
        return formataddr((Header(name, 'utf-8').encode(), addr))

    def get_weather(self):
        """
        根据api获取天气信息
        :return: 天气信息文本
        """
        res = json.loads(requests.get(url.format("now", city1, key)).text)
        location = res['HeWeather6'][0]['basic']
        result = res['HeWeather6'][0]['now']
        city_name = location['location']
        cond_txt = result['cond_txt']
        tmp=result['tmp']
        pres = result['pres']
        wind_dir =result['wind_dir']
        fl=result['fl']
        return city_name, cond_txt, tmp,pres, wind_dir,fl

    def send_mail(self):
        # 设置邮件信息
        city_name, cond_txt, tmp,pres, wind_dir,fl = self.get_weather()
        weather = "城市：{}\n天气状况：{}\n温度：{}\n体感温度：{}\n气压：{}\n风向：{}" \
            .format(city_name, cond_txt, tmp,fl,pres, wind_dir)
        print(weather)
        msg = MIMEText(weather, 'plain', 'utf-8')
        for to_addr in to_address:

            # 发送邮件
            server = smtplib.SMTP(self.SmtpServer, 25)
            server.login(self.from_addr, self.password)
            server.sendmail(self.from_addr, [to_addr], msg.as_string())
            server.quit()


if __name__ == '__main__':
    try:
        to_address = ['********@qq.com']
        send_mail = PostWeatherEmail()
        send_mail.send_mail()
    except Exception as e:
        print(e)

