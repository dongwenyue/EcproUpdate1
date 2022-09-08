# -*- coding: UTF-8 -*-
import random
import sqlite3
import string
import time
import requests
import MySQLdb
import datetime
import copy
from MySQLdb.constants import FIELD_TYPE
import xlwt
from openpyxl import Workbook
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.mime.base import MIMEBase
import smtplib
import os


def get_font():
    font = xlwt.Font()
    # 字体类型
    font.name = '微软雅黑'
    # 字体颜色
    font.colour_index = 4
    # 字体大小，11为字号，20为衡量单位
    font.height = 20 * 18
    # 字体加粗
    font.bold = True
    # 下划线
    font.underline = True
    # 斜体字
    font.italic = False
    return font


class SendMail(object):
    """将Excel作为附件发送邮件"""

    def __init__(self, email_info):
        self.email_info = email_info
        # 使用SMTP_SSL连接端口为465
        self.smtp = smtplib.SMTP_SSL(self.email_info['server'], self.email_info['port'])
        # 创建两个变量
        self._attachements = []
        self._from = ''

    def login(self):
        # 通过邮箱名和smtp授权码登录到邮箱
        self._from = self.email_info['user']
        self.smtp.login(self.email_info['user'], self.email_info['password'])

    # def _format_addr(self, s):
    #     name, addr = parseaddr(s)
    #     return formataddr((Header(name, 'utf-8').encode(), addr))

    def add_attachment(self):
        # 添加附件内容
        # 注意：添加附件内容是通过读取文件的方式加入
        file_path = self.email_info['file_path']
        with open(file_path, 'rb') as file:
            filename = os.path.split(file_path)[1]
            mime = MIMEBase('application', 'octet-stream', filename=filename)
            mime.add_header('Content-Disposition', 'attachment', filename=('gbk', '', filename))
            mime.add_header('Content-ID', '<0>')
            mime.add_header('X-Attachment-Id', '0')
            mime.set_payload(file.read())
            encoders.encode_base64(mime)
            # 添加到列表，可以有多个附件内容
            self._attachements.append(mime)

    def sendMail(self):
        # 发送邮件，可以实现群发
        msg = MIMEMultipart()
        # html文件插入正文
        txt_html = """
                    <p>Hello!&nbsp;This is a test mail.</p>
                    """ + open("2022-04-19-15-49-07测试报告.html", "r", encoding='utf-8').read()
        contents = MIMEText(txt_html, 'html', 'utf-8')

        # 可以，但不美观
        # import pandas as pd
        # read_file = pd.read_excel("example.xls")
        # html_file = read_file.to_html(header=True, index=False, col_space=100)
        # contents = MIMEText(html_file, 'html')

        # 修改邮件正文的位置
        # contents = MIMEText(self.email_info['content'], 'plain', 'utf-8')

        msg['From'] = self.email_info['user']
        msg['To'] = self.email_info['to']
        msg['Subject'] = self.email_info['subject']

        for att in self._attachements:
            # 从列表中提交附件，附件可以有多个
            msg.attach(att)
        msg.attach(contents)
        try:
            self.smtp.sendmail(self._from, self.email_info['to'].split(','), msg.as_string())
            print('邮件发送成功，请注意查收'.center(30, '#'))
        except Exception as e:
            print('Error:', e)

    def close(self):
        # 退出smtp服务
        self.smtp.quit()


if __name__ == '__main__':

    # 邮件登录及内容信息
    email_dict = {
        # 手动填写，确保信息无误
        "user": "dongwenyue@infimind.com",
        "to": "dongwenyue@infimind.com",  # 多个邮箱以','隔开；
        "server": "smtp.exmail.qq.com",
        'port': 465,  # values值必须int类型
        "username": "董文跃",
        "password": "Jr199808066050",
        "subject": "线上环境：集中上货测试统计表",
        "content": '上货/同步统计信息',
        'file_path': '2022-04-19-15-49-07测试报告.html'
    }

    sendmail = SendMail(email_dict)
    sendmail.login()
    sendmail.add_attachment()
    sendmail.sendMail()
    sendmail.close()
