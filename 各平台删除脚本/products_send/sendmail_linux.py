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
import sys
import json
import random
import argparse
import pymysql


class wechatRebot_send:
    def __init__(self):
        pass

    def test_robot_bak(self, WX_del_HOOK, project, start_time, tp_names, product_name, total_num, fail_num, rate,
                       publishing_num):
        """
        需要发送到企业微信的文案信息
        :param project:         项目名称
        :start_time:            开始时间
        :prefix                 商品前缀
        :param total:           总计
        :param succeed_title:   批量上货链接
        """
        data = {
            "msgtype": "markdown",  # 消息类型，此时固定为markdown
            "markdown": {
                "content": "# **自动化上货统计信息**\n#### **请相关同事注意，及时跟进！**\n"
                           "> 项目名称：<font color=\"info\">%s</font> \n"
                           "> 开始时间：<font color=\"info\">%s</font> \n"
                           "> 平台：<font color=\"info\">%s</font> \n"
                           "> 货号前缀：<font color=\"info\">%s</font> \n"
                           "> **-------运行详情-------**\n"
                           "> 上货总数：<font color=\"info\">%s</font>\n"
                           "> 上货失败数：<font color=\"info\">%s</font>\n"
                           "> 上新率：<font color=\"info\">%s</font>\n"
                           "> 上货中：<font color=\"info\">%s</font>\n" % (
                               project, start_time, tp_names, product_name, total_num, fail_num, rate, publishing_num)
                # 加粗：**需要加粗的字**
                # 引用：> 需要引用的文字
                # 字体颜色(只支持3种内置颜色)
                # 标题 （支持1至6级标题，注意#与文字中间要有空格）
                # 绿色：info、灰色：comment、橙红：warning
            }
        }
        print(data)
        r = requests.post(url=WX_del_HOOK, headers={"Content-Type": "application/json"}, json=data)
        print(r.text)
        return (r.text)

    def upload_media(self, upload_media_url, export_file_path):
        data = {"file": open(export_file_path, 'rb')}
        print(data)
        r = requests.post(url=upload_media_url, files=data)
        print(r.text)
        res = json.loads(r.text)
        return res["media_id"]

    def test_file(self, WX_del_HOOK, media_id):
        data = {
            "msgtype": "file",
            "file": {
                "media_id": media_id
            }
        }
        print(data)
        r = requests.post(url=WX_del_HOOK, json=data)
        print(r.text)
        return (r.text)


def select_mysql_qa_dict_bak(sql):
    try:
        db = MySQLdb.connect(
            # host='rm-2zeb07rt531eym8of1o.mysql.rds.aliyuncs.com',
            host='rm-2ze5qeu2nyo0i5gm8lo.mysql.rds.aliyuncs.com',
            port=3306,
            user='qa_v2',
            passwd='lyp82nLF',
            db='qa_v2_merchant',
            charset='utf8',
            compress=1,
            connect_timeout=1
            # conv=myConv
        )
    except BaseException as e:
        print("Could not connect to MySQL server.", e)
    cursor = db.cursor(MySQLdb.cursors.DictCursor)
    print(sql)
    # 执行SQL查询语句
    try:
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        print('qa数据库查询结果，字典', results)
    except Exception as e:
        print('查询失败:', e)
    db.close()
    return results


'''只能是线上数据库'''
def select_mysql_qa_dict(sql):
    try:
        db = MySQLdb.connect(
            host='rm-2ze69dr39e1217univo.mysql.rds.aliyuncs.com',
            port=3306,
            user='prod_migration',
            passwd='lyp82nLF',
            db='prod_v2_merchant',
            charset='utf8',
            compress=1,
            connect_timeout=1
            # conv=myConv
        )
    except BaseException as e:
        print("Could not connect to MySQL server.", e)
    cursor = db.cursor(MySQLdb.cursors.DictCursor)
    print(sql)
    # 执行SQL查询语句
    try:
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        print('线上数据库查询结果，字典', results)
    except Exception as e:
        print('查询失败:', e)
    db.close()
    return results


'''可以切换线上环境和qa环境，数据库'''
def select_mysql_dict(sql):
    if Environment == 'pro':
        db = MySQLdb.connect(
            host='rm-2ze69dr39e1217univo.mysql.rds.aliyuncs.com',
            port=3306,
            user='prod_migration',
            passwd='lyp82nLF',
            db='prod_v2_merchant',
            charset='utf8',
            compress=1,
            connect_timeout=1
            # conv=myConv
        )
        print("---当前为线上数据库---")
    elif Environment == 'beta':
        db = MySQLdb.connect(
            host='rm-2ze5qeu2nyo0i5gm8lo.mysql.rds.aliyuncs.com',
            port=3306,
            user='qa_v2',
            passwd='lyp82nLF',
            db='qa_v2_merchant',
            charset='utf8',
            compress=1,
            connect_timeout=1
            # conv=myConv
        )
        print("---当前为qa数据库---")
    cursor = db.cursor(MySQLdb.cursors.DictCursor)
    print(sql)
    # 执行SQL查询语句
    cursor.execute(sql)
    # 获取所有记录列表
    results = cursor.fetchall()
    print('数据库查询结果，字典', results)
    db.close()
    return results


table_head = ["发布ID", "用户", "货号", "类目ID", "类目名称", "商品ID", "平台", "店铺ID", "店铺名称", "上货失败", "同步失败", "上货链接"]


def get_font():
    font = xlwt.Font()
    # 字体类型
    font.name = '微软雅黑'
    # 字体颜色
    font.colour_index = 4
    # 字体大小，11为字号，20为衡量单位
    font.height = 20 * 11
    # 字体加粗
    font.bold = True
    # 下划线
    font.underline = True
    # 斜体字
    font.italic = False
    return font


# 获取字符串长度，一个中文的长度为2
def len_byte(value):
    length = len(str(value)) + 5
    # utf8_length = len(str(value).encode('utf-8'))
    # length = (utf8_length - length) + length
    # length = (utf8_length - length) / 2 + length
    return int(length)


def get_server_url():
    if Environment == 'pro':
        server_url = 'https://cms.ecpro.com'
    elif Environment == 'beta':
        server_url = 'https://cms-qa.ecpro.com'
    return server_url
    

def get_account_id():
    if Environment == 'pro':
        publish_account_id = 1000201
    elif Environment == 'beta':
        publish_account_id = 1000189
    return publish_account_id


def write_result_to_content(results):
    server_url = get_server_url()
    if results is None:
        return
    # 创建excel工作表
    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet = workbook.add_sheet('sheet1')
    # 初始化样式
    style_font = xlwt.XFStyle()
    # 获取设置字体格式
    style_font.font = get_font()
    # 设置表头前的统计信息
    head_list = ["上货/同步统计信息", f"前日上货总数:{total_num}", "前日上货失败数:{}".format(fail_num), f"上新率:{rate}"]
    ls = 0
    for head in head_list:
        worksheet.write(ls, 0, head)
        ls += 1

    # 设置表头
    ls = 0
    for head in table_head:
        worksheet.write(6, ls, head, style_font)
        ls += 1

    # 设置超链接的样式，斜体，下划线
    style = xlwt.XFStyle()  # 格式信息
    font = xlwt.Font()  # 字体基本设置
    # 下划线
    font.underline = True
    # 字体颜色
    font.colour_index = 4
    style.font = font

    i = 7
    # 将数据分两次循环写入表中 外围循环行
    for results_data in results:
        j = 0
        # 确定栏位宽度
        col_width_list = []
        # 内围循环列
        # https://cms.ecpro.com/publish/publish-results?pids=611815&sid=2007057&t=publish
        publish_url = "%s/publish/publish-results?pids=%s&sid=%s&t=publish" % (server_url, results_data['id'], results_data['shop_id'])
        results_data['publish_url'] = publish_url

        for key, value in results_data.items():
            print(value)
            value = str(value)
            if not value:
                continue
            elif 'https://' in value:
                worksheet.write(i, j, xlwt.Formula('HYPERLINK("{}", "{}")'.format(value, value)), style)
            else:
                worksheet.write(i, j, value)
                '''设置列宽, 还是有点问题，列宽没有根据字长度自适应'''
                col_width_list.append(len_byte(value))
                # 在列表中找到任何字符串的最大长度
                maxlength = max(len(str(s)) for s in col_width_list)
                print('______________>', maxlength, len_byte(value), len_byte(maxlength))
                len_byte_maxlength = len_byte(maxlength)
                if len_byte_maxlength < len_byte(value):
                    len_byte_maxlength = len_byte(value)
                    # 设置最大列宽
                    if len_byte_maxlength > 100:
                        worksheet.col(j).width = 256 * 100
                    else:
                        # 设置固定列宽
                        worksheet.col(j).width = 256 * len_byte_maxlength
                else:
                    # 设置最大列宽
                    if len_byte_maxlength > 100:
                        worksheet.col(j).width = 256 * 100
                    else:
                        # 设置固定列宽
                        worksheet.col(j).width = 256 * len_byte_maxlength
            j += 1
        i += 1
    workbook.save(export_file_path)
    print('数据写入完毕', export_file_path)


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

        import pandas as pd
        import codecs
        xd = pd.ExcelFile(export_file_path)
        df = xd.parse(header=5)
        pd.set_option('colheader_justify', 'center')
        # 左右对齐列标签。默认为 None时，使用打印配置中的选项（由 set_option 控制），则右对齐。
        html_str = df.to_html(header=False, index=False, justify='center', col_space=100, na_rep='-')
        # col_space=100设置列的宽度，以防止出现省略号, na_rep空的显示, justify列标签内容居中对齐  border=0:边框宽度设为 2, 设为 0 则 无边框
        html_str = html_str.replace('class', 'cellspacing=\"0\" class')
        # 让边框线变实心的功能，html 表格的属性存放在 table 标签中，我们可以在 class 前面插入边框线实心的参数。
        count = total_num
        failed_count = fail_num
        success_rate = rate
        style = f'''
        <body>
            <h1>上货/同步统计信息</h1>
            <h3>前日上货总数: {count}</h3>
            <h3>前日上货失败数: {failed_count}</h3>
            <h3>上新率: {success_rate}</h3>
            <h2>上货失败信息</h1>
            <span><font color="red">附件中有更详细的信息，请相关业务负责人，定位下问题，并做简单描述，回复这封邮件</font></span>
        </body>
        '''
        html_str = style + html_str
        contents = MIMEText(html_str, 'html')

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
    parser = argparse.ArgumentParser(description='manual to this script')
    parser.add_argument('--start_time', type=str, default='2022-03-07')
    parser.add_argument('--end_time', type=str, default='2022-03-15')
    parser.add_argument('--tp_names', type=str, default='天猫,淘宝')
    parser.add_argument('--product_name', type=str, default='0602OI')
    parser.add_argument('--Environment', type=str, default='beta')
    args = parser.parse_args()
    start_time = args.start_time
    end_time = args.end_time
    tp_names = args.tp_names
    product_name = args.product_name
    Environment = args.Environment

    # start_time = (datetime.datetime.now() - datetime.timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')
    # 2022-03-07 2022-03-09
    # sql = "SELECT	publish.id,	qa_v2_user.account.NAME,	product.CODE,	product.category_id,	product.category_path,	publish.product_id,	tp.NAME,	publish.pub_description,	publish.sync_description FROM	publish	LEFT JOIN product ON publish.product_id = product.id	LEFT JOIN tp ON publish.tp_id = tp.id 	LEFT JOIN qa_v2_user.account ON publish.account_id = qa_v2_user.account.id WHERE	publish.account_id = 1000189 	AND ( publish.pub_status = 'publish_failed' OR publish.sync_status = 'sync_failed' ) 	AND pub_date BETWEEN '2022-03-07' 	AND '2022-03-09'  ORDER BY	publish.id DESC 	LIMIT 100;"

    account_id = get_account_id()
    # `disable` != '1' 去除publish表中，状态失效，因为商品重新上货了，前一个上货链接就失效了
    # pub_date 等待的上货结束时间间隔，不对，因为有的还在上货中，但时间已经过了20秒，暂时选择创建时间字段 publish.created_at
    sql = "SELECT	publish.id,	publish.account_id, product.CODE,	product.category_id,	product.category_path,	" \
          "publish.product_id,	tp.NAME,	publish.shop_id, shop.name, publish.pub_description,	publish.sync_description FROM	publish	LEFT " \
          "JOIN product ON publish.product_id = product.id	LEFT JOIN tp ON publish.tp_id = tp.id  LEFT JOIN shop ON publish.shop_id = shop.id WHERE	" \
          "publish.account_id = '{}'  AND publish.disable != 1   AND ( publish.pub_status = 'publish_failed' OR publish.sync_status = " \
          "'sync_failed' ) 	AND publish.created_at BETWEEN '{}' 	AND '{}'  ORDER BY	publish.id DESC;".format(account_id, start_time,
                                                                                                            end_time)
    sql_fail_number = "SELECT count(publish.id) FROM	publish	LEFT JOIN product ON publish.product_id = " \
                      "product.id	LEFT JOIN tp ON publish.tp_id = tp.id  WHERE	publish.account_id = '{}' AND ( " \
                      "publish.pub_status = 'publish_failed' OR publish.sync_status = 'sync_failed' ) 	AND publish.created_at " \
                      "BETWEEN '{}' 	AND '{}'  ORDER BY	publish.id DESC; ".format(account_id, start_time, end_time)
    sql_total_number = "SELECT count(publish.id) FROM	publish	LEFT JOIN product ON publish.product_id = " \
                       "product.id	LEFT JOIN tp ON publish.tp_id = tp.id WHERE	publish.account_id = '{}' AND " \
                       "publish.created_at BETWEEN '{}' 	AND '{}'  ORDER BY	publish.id DESC; ".format(account_id, start_time, end_time)

    '''
    SELECT count(publish.id) FROM	publish	LEFT JOIN product ON publish.product_id = product.id	LEFT JOIN tp ON publish.tp_id = tp.id  WHERE	publish.account_id = 1000201 AND ( publish.pub_status = 'publishing') 	AND pub_date BETWEEN '2021-08-30' 	AND '2021-08-31'  ORDER BY	publish.id DESC; 
    '''

    sql_publishing_number = "SELECT count(publish.id) FROM	publish	LEFT JOIN product ON publish.product_id = " \
                            "product.id	LEFT JOIN tp ON publish.tp_id = tp.id  WHERE	publish.account_id = '{}' " \
                            "AND ( publish.pub_status = 'publishing') 	AND publish.created_at BETWEEN '{}' 	AND '{}'  ORDER " \
                            "BY	publish.id DESC; ".format(account_id, start_time, end_time)
    print('查询上货中总数的sql命令', sql_publishing_number)
    publishing_number = select_mysql_dict(sql_publishing_number)
    publishing_num = publishing_number[0]['count(publish.id)']

    time_start = datetime.datetime.now()

    while 1:
        publishing_number = select_mysql_dict(sql_publishing_number)
        publishing_num = publishing_number[0]['count(publish.id)']
        # 间隔10秒查询一次上货中
        time.sleep(10)
        time_end = datetime.datetime.now()
        time_difference = (time_end - time_start).total_seconds()
        time_difference = int(time_difference)
        print('每次间隔10秒查询，如果上货中为0或者查询了半小时，则终止', time_difference)
        print('上货中个数', publishing_num)
        if publishing_num == 0:
            break
        elif time_difference > 1800:
            break
        else:
            continue
    print('查询上货总数的sql命令', sql_total_number)
    total_number = select_mysql_dict(sql_total_number)
    print('查询上货失败数的sql命令', sql_fail_number)
    fail_number = select_mysql_dict(sql_fail_number)
    print('查询上货失败和同步失败的sql命令', sql)
    qa_results_dict = select_mysql_dict(sql)
    # Python生成2位的英文大写的随机数
    random_str = ''.join([random.choice(string.ascii_uppercase) for i in range(2)])
    # export_file_path = '易尚货' + time.strftime("%Y-%m-%d", time.localtime()) + '上货统计表.xls'
    export_file_path = '易尚货' + time.strftime("%Y-%m-%d", time.localtime()) + random_str + '上货统计表.xls'
    # export_file_path = 'example.xls'
    fail_num = fail_number[0]['count(publish.id)']
    total_num = total_number[0]['count(publish.id)']
    print('失败数和总数', fail_num, total_num)
    rate = format(1 - fail_num / total_num, '.2%')
    print(total_num, fail_num, rate)
    write_result_to_content(qa_results_dict)

    # 邮件登录及内容信息
    email_dict = {
        # 手动填写，确保信息无误
        "user": "yinzhengmao@infimind.com",
        # "to": "yinzhengmao@infimind.com,dongwenyue@infimind.com,shenzhicong@infimind.com",  # 多个邮箱以','隔开；
        "to": "yinzhengmao@infimind.com",  # 多个邮箱以','隔开；
        "server": "smtp.exmail.qq.com",
        'port': 465,  # values值必须int类型
        "username": "尹正茂",
        "password": "Jr2468",
        "subject": "线上环境：集中上货测试统计表",
        "content": '上货/同步统计信息',
        'file_path': export_file_path
    }

    sendmail = SendMail(email_dict)
    sendmail.login()
    sendmail.add_attachment()
    sendmail.sendMail()
    sendmail.close()


    WX_del_HOOK = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=24692f61-7f4f-41f4-a4df-57b9b4660a57'
    project = '上货统计信息'
    start_time = time.strftime("%m%dT%H:%M:%S", time.localtime())
    mess = wechatRebot_send().test_robot_bak(WX_del_HOOK, project, start_time, tp_names, product_name, total_num, fail_num, rate, publishing_num)

    
    # 企业微信机器人，文件上传接口
    # key:调用接口凭证, 机器人webhookurl中的key参数
    upload_media_url = ' https://qyapi.weixin.qq.com/cgi-bin/webhook/upload_media?key=24692f61-7f4f-41f4-a4df-57b9b4660a57&type=file'
    media_id = wechatRebot_send().upload_media(upload_media_url, export_file_path)

    WX_del_HOOK = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=24692f61-7f4f-41f4-a4df-57b9b4660a57'
    mess = wechatRebot_send().test_file(WX_del_HOOK, media_id)

