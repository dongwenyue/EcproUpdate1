# -*- coding: utf-8 -*-
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from common.getYaml import url
from email.mime.application import MIMEApplication  # 用于添加附件
from common.path import getTestReport
from common.readLog import Log
from email.utils import parseaddr, formataddr
import datetime


class SendMail:
    log = Log(__name__)
    logger = log.getLog()

    def __init__(self):
        self.host_server = 'smtp.exmail.qq.com'  # qq邮箱smtp服务器
        self.sender_qq = 'warning@microdreams.com'  # 发件人邮箱
        self.pwd = 'Weimeng123'
        urlInfo = url['url']['testUrl']
        if urlInfo == "https://misheji.wxbjq.top":
            self.receiver = ['yanfa-test@microdreams.com']
            self.mail_title = '【爱设计-PC端自动化测试】测试环境-执行用例结果'
        elif urlInfo == "https://v2-isj-copyright.wxbjq.top":
            self.receiver = ['yanfa-test@microdreams.com']
            self.mail_title = '【爱设计-版权站自动化测试】测试环境-执行用例结果'
        elif urlInfo == "https://www.isheji.com/":
            self.receiver = ['yanfa-test@microdreams.com']
            self.mail_title = '【爱设计-PC端自动化测试】线上环境-执行用例结果'
            # , 'dongwen@microdreams.com', 'yuandong@microdreams.com', 'Eric@isheji.com'
        elif urlInfo == "https://sc.isheji.com":
            self.receiver = ['yanfa-test@microdreams.com']
            self.mail_title = '【爱设计-版权站自动化测试】线上环境-执行用例结果'

    #自定义发件人和收件人信息
    def _format_addr(self,s):
        addr = parseaddr(s)
        return formataddr(addr)

    # 发送邮件
    def sendmail(self):
        # 发送邮件，可以实现群发
        urlInfo = url['url']['testUrl']
        # 邮件正文内容
        if urlInfo == "https://misheji.wxbjq.top":
            self.mail_content = "<p>Dear all: <br><br>&nbsp;&nbsp;&nbsp;&nbsp;【爱设计-PC端】自动化测试执行用例结果,请打开附件查看！！</p >"
        elif urlInfo == "https://v2-isj-copyright.wxbjq.top":
            self.mail_content = "<p>Dear all: <br><br>&nbsp;&nbsp;&nbsp;&nbsp;【爱设计-版权站】自动化测试执行用例结果,请打开附件查看！！</p >"
        elif urlInfo == "https://www.isheji.com/":
            self.mail_content = "<p>Dear all: <br><br>&nbsp;&nbsp;&nbsp;&nbsp;【爱设计-PC端】自动化测试执行用例结果,请打开附件查看！！</p >"
        elif urlInfo == "https://sc.isheji.com":
            self.mail_content = "<p>Dear all: <br><br>&nbsp;&nbsp;&nbsp;&nbsp;【爱设计-版权站】自动化测试执行用例结果,请打开附件查看！！</p >"
        from_addr = 'warning@microdreams.com'
        msg = MIMEMultipart('related')
        msg["Subject"] = Header(self.mail_title, 'utf-8')
        msg['Date'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        msg["From"] = self._format_addr(u'爱设计-自动化测试 <%s>'%from_addr)
        msg["To"] = Header(f"{self.receiver}", "utf-8")  # 收件人姓名

        msg.attach(MIMEText(self.mail_content, 'html', 'utf-8'))
        attachment = MIMEApplication(open(getTestReport(), 'rb').read())
        attachment["Content-Type"] = 'application/octet-stream'
        # 给附件重命名
        now_time = (datetime.datetime.now() - datetime.timedelta(seconds=1)).strftime("%Y-%m-%d %H:%M")
        basename = now_time + self.mail_title + '.html'
        # 注意：此处basename要转换为gbk编码，否则中文会有乱码。
        # attachment.add_header('Content-Dispositon','attachment',filename=('utf-8', '', basename))
        # 中、英文名称都支持
        attachment.add_header('Content-Disposition', 'attachment',
                              filename=(Header(basename.split('\\')[-1], 'utf-8').encode()))
        msg.attach(attachment)
        try:
            smtp = smtplib.SMTP_SSL(self.host_server, 465)  # ssl登录连接到邮件服务器
            smtp.set_debuglevel(0)  # 0是关闭，1是开启debug
            smtp.ehlo(self.host_server)  # 跟服务器打招呼，告诉它我们准备连接，最好加上这行代码
            smtp.login(self.sender_qq, self.pwd)
            smtp.sendmail(self.sender_qq, self.receiver, msg.as_string())
            smtp.quit()
            self.logger.info("邮件发送成功")
        except smtplib.SMTPException:
            self.logger.info("无法发送邮件")