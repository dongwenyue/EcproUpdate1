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
import sys

class wechatRebot_send:
    def __init__(self):
        pass
    def test_robot(self, WX_del_HOOK, project, start_time, tp_name, shop_name, action):
        """
        需要发送到企业微信的文案信息
        :project:         项目名称
        :start_time:      开始时间
        :source_model     源环境
        :source_account:  源环境账号和密码
        :tar_model        目标环境
        :tar_account      目标环境账号和密码
        :tp_name          平台
        :shop_name:       店铺名称
        :action:          迁移方式
        """
        data = {
            "msgtype": "markdown",  # 消息类型，此时固定为markdown
            "markdown": {
                "content": "# **默认迁移店铺**\n#### **迁移详情！**\n"
                           "> 项目名称：<font color=\"info\">%s</font> \n"
                           "> 开始时间：<font color=\"info\">%s</font> \n"
                           "> 平台：<font color=\"info\">%s</font> \n"
                           "> 店铺名称：<font color=\"info\">%s</font> \n"
                           "> 迁移方式：<font color=\"info\">%s</font>\n"% (
                           project, start_time, tp_name, shop_name, action)
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

def select_mysql_pro(pro_account_id, tp_id, name):
    myConv = {FIELD_TYPE.LONG: int, FIELD_TYPE.DATETIME: str}
    id = ''
    # 打开数据库连接
    #db = MySQLdb.connect("rm-2zeb07rt531eym8of1o.mysql.rds.aliyuncs.com", "qa_v2", "lyp82nLF", "qa_v2_merchant", charset='utf8' )
    try:
        db = MySQLdb.connect(
            host = 'rm-2ze69dr39e1217univo.mysql.rds.aliyuncs.com',
            port=3306,
            user='prod_migration',
            passwd='lyp82nLF',
            db='prod_v2_merchant',
            charset='utf8',
            compress=1,
            connect_timeout=1,
            conv=myConv
        )
    except BaseException:
        print("Could not connect to MySQL server.")
    cursor = db.cursor()
    sql = "SELECT * FROM `prod_v2_merchant`.`shop` WHERE `account_id` = '{}' AND `tp_id` = '{}' AND `name` LIKE '%{}%' " .format(pro_account_id, tp_id, name)
    print(sql)
   # 执行SQL查询语句
    try:
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        print('线上数据库查询结果，二维元祖',results)
    except:
        print('查询失败')
    db.close()
    return results


def select_mysql_pro_dict(pro_account_id, tp_id, name):
    # myConv = {FIELD_TYPE.LONG: int, FIELD_TYPE.DATETIME: str, FIELD_TYPE.TINGINT: int}
    id = ''
    # 打开数据库连接
    #db = MySQLdb.connect("rm-2zeb07rt531eym8of1o.mysql.rds.aliyuncs.com", "qa_v2", "lyp82nLF", "qa_v2_merchant", charset='utf8' )
    try:
        db = MySQLdb.connect(
            host = 'rm-2ze69dr39e1217univo.mysql.rds.aliyuncs.com',
            port=3306,
            user='prod_migration',
            passwd='lyp82nLF',
            db='prod_v2_merchant',
            charset='utf8',
            compress=1,
            connect_timeout=1,
            # conv=myConv
        )
    except BaseException:
        print("Could not connect to MySQL server.")
    cursor = db.cursor(MySQLdb.cursors.DictCursor)
    sql = "SELECT * FROM `prod_v2_merchant`.`shop` WHERE `account_id` = '{}' AND `tp_id` = '{}' AND `name` LIKE '%{}%' " .format(pro_account_id, tp_id, name)
    print(sql)
   # 执行SQL查询语句
    try:
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchone()
        print('线上数据库查询结果，字典',results)
    except:
        print('查询失败')
    db.close()
    return results

def select_mysql_qa_dict(pro_account_id, tp_id, name):
    # myConv = {FIELD_TYPE.LONG: int, FIELD_TYPE.DATETIME: str, FIELD_TYPE.TINGINT: int}
    id = ''
    # 打开数据库连接
    #db = MySQLdb.connect("rm-2zeb07rt531eym8of1o.mysql.rds.aliyuncs.com", "qa_v2", "lyp82nLF", "qa_v2_merchant", charset='utf8' )
    try:
        db = MySQLdb.connect(
            host = 'rm-2ze5qeu2nyo0i5gm8lo.mysql.rds.aliyuncs.com',
            port=3306,
            user='qa_v2',
            passwd='lyp82nLF',
            db='qa_v2_merchant',
            charset='utf8',
            compress=1,
            connect_timeout=1
            # conv=myConv
        )
    except BaseException:
        print("Could not connect to MySQL server.")
    cursor = db.cursor(MySQLdb.cursors.DictCursor)
    sql = "SELECT * FROM `qa_v2_merchant`.`shop` WHERE `account_id` = '{}' AND `tp_id` = '{}' AND `name` LIKE '%{}%' " .format(pro_account_id, tp_id, name)
    print(sql)
   # 执行SQL查询语句
    try:
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchone()
        print('qa数据库查询结果，字典',results)
    except:
        print('查询失败')
    db.close()
    return results

def select_mysql_pro_brand_dict(tp_id, shop_id):
    # myConv = {FIELD_TYPE.LONG: int, FIELD_TYPE.DATETIME: str, FIELD_TYPE.TINGINT: int}
    id = ''
    # 打开数据库连接
    #db = MySQLdb.connect("rm-2zeb07rt531eym8of1o.mysql.rds.aliyuncs.com", "qa_v2", "lyp82nLF", "qa_v2_merchant", charset='utf8' )
    try:
        db = MySQLdb.connect(
            host = 'rm-2ze69dr39e1217univo.mysql.rds.aliyuncs.com',
            port=3306,
            user='prod_migration',
            passwd='lyp82nLF',
            db='prod_v2_merchant',
            charset='utf8',
            compress=1,
            connect_timeout=1,
            # conv=myConv
        )
    except BaseException:
        print("Could not connect to MySQL server.")
    cursor = db.cursor(MySQLdb.cursors.DictCursor)
    sql = "SELECT * FROM `prod_v2_merchant`.`shop_brand` WHERE `shop_id` = '{}' AND `tp_id` = '{}'" .format(shop_id, tp_id)
    print(sql)
   # 执行SQL查询语句
    try:
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        print('线上数据库品牌查询结果，字典',results)
    except:
        print('查询失败')
    db.close()
    return results

def select_mysql_qa_brand_dict(tp_id, shop_id):
    # myConv = {FIELD_TYPE.LONG: int, FIELD_TYPE.DATETIME: str, FIELD_TYPE.TINGINT: int}
    id = ''
    # 打开数据库连接
    #db = MySQLdb.connect("rm-2zeb07rt531eym8of1o.mysql.rds.aliyuncs.com", "qa_v2", "lyp82nLF", "qa_v2_merchant", charset='utf8' )
    try:
        db = MySQLdb.connect(
            host = 'rm-2ze5qeu2nyo0i5gm8lo.mysql.rds.aliyuncs.com',
            port=3306,
            user='qa_v2',
            passwd='lyp82nLF',
            db='qa_v2_merchant',
            charset='utf8',
            compress=1,
            connect_timeout=1
            # conv=myConv
        )
    except BaseException:
        print("Could not connect to MySQL server.")
    cursor = db.cursor(MySQLdb.cursors.DictCursor)
    sql = "SELECT * FROM `qa_v2_merchant`.`shop_brand` WHERE `shop_id` = '{}' AND `tp_id` = '{}'" .format(shop_id, tp_id)
    print(sql)
   # 执行SQL查询语句
    try:
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        print('qa数据库品牌查询结果，字典',results)
    except:
        print('查询失败')
    db.close()
    return results
def select_mysql_qa(pro_account_id, tp_id, name):
    # 打开数据库连接
    #db = MySQLdb.connect("rm-2zeb07rt531eym8of1o.mysql.rds.aliyuncs.com", "qa_v2", "lyp82nLF", "qa_v2_merchant", charset='utf8' )
    id = None
    try:
        db = MySQLdb.connect(
            # host='rm-2zeb07rt531eym8of1o.mysql.rds.aliyuncs.com',
            host = 'rm-2ze5qeu2nyo0i5gm8lo.mysql.rds.aliyuncs.com',
            port=3306,
            user='qa_v2',
            passwd='lyp82nLF',
            db='qa_v2_merchant',
            charset='utf8',
            compress=1,
            connect_timeout=1
        )
    except BaseException:
        print("Could not connect to MySQL server.")
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    # qa_v2_catalog 谨慎操作这张表，仅此一份
    sql = "SELECT * FROM `qa_v2_merchant`.`shop` WHERE `account_id` = '{}' AND `tp_id` = '{}' AND `name` LIKE '%{}%' " .format(pro_account_id, tp_id, name)
    print(sql)
   # 执行SQL查询语句
    try:
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        for row in results:
            id = row[0]
    except:
        print('查询失败')
    db.close()
    return id


def select_into(sql_into):
    try:
        db = MySQLdb.connect(
            host='rm-2ze5qeu2nyo0i5gm8lo.mysql.rds.aliyuncs.com',
            port=3306,
            user='qa_v2',
            passwd='lyp82nLF',
            db='qa_v2_merchant',
            charset='utf8',
            compress=1,
            connect_timeout=1
        )
    except BaseException:
        print("Could not connect to MySQL server.")
    cursor = db.cursor()
    sql = sql_into
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
        print('-------新增成功-------')
    except:
        # Rollback in case there is any error
        db.rollback()
        print('-------新增失败-------')

    # 关闭数据库连接
    db.close()

def select_update(sql_into):
    try:
        db = MySQLdb.connect(
            host='rm-2ze5qeu2nyo0i5gm8lo.mysql.rds.aliyuncs.com',
            port=3306,
            user='qa_v2',
            passwd='lyp82nLF',
            db='qa_v2_merchant',
            charset='utf8',
            compress=1,
            connect_timeout=1
        )
    except BaseException:
        print("Could not connect to MySQL server.")
    cursor = db.cursor()
    sql = sql_into
    print('执行覆盖',sql)
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
        print('-------覆盖成功-------')
    except:
        # Rollback in case there is any error
        print('-----覆盖失败------')
        db.rollback()
    # 关闭数据库连接
    db.close()

def cms_account(CMS_HOST, cms_number, cms_password):
    """查找账号下的token
    """
    # 获取access_token和account_id
    login_url = CMS_HOST + '/auth/login'
    login_body = {"mobile":str(cms_number),"password":str(cms_password),"login_way":"mobile"}
    response = requests.post(login_url,json=login_body)
    # 获取token
    account_url = CMS_HOST + '/user/account/login'
    account_body = {"account_id": response.json()['data']['last_login_account']}
    headers = {}
    headers['authorization'] = 'Bearer '+ response.json()['data']['access_token']
    res = requests.post(account_url, json=account_body, headers=headers)
    token = res.json()['data']['access_token']
    cms_account_id = response.json()['data']['last_login_account']
    return token, cms_account_id


if __name__ == '__main__':
    tp_name = sys.argv[1]
    shop_name = sys.argv[2]
    tp = {'淘宝': '1000', '天猫': '1001', '京东': '1003', '拼多多': '1004', '唯品会': '1005', '有赞': '1006', '快手': '1008',
          '京东自营': '1010', '爱库存': '1011', '抖音': '1012', '1688': '1013', '得物': '1014', '小红书': '1015'}
    tp_id = tp[tp_name]
    # tp_id = 1013
    # shop_name = 'diff'

    qa_cms_number = 18617847474
    qa_cms_password = 'lf18617847474'
    qa_CMS_HOST = 'https://cms-qa-api.ecpro.com'

    pro_cms_number = 18612210007
    pro_cms_password = '18612210007'
    pro_CMS_HOST = 'https://cms-api.ecpro.com'

    CMS_token, CMS_account_id = cms_account(qa_CMS_HOST, qa_cms_number, qa_cms_password)
    pro_token, pro_account_id = cms_account(pro_CMS_HOST, pro_cms_number, pro_cms_password)
    print(CMS_account_id, pro_account_id)

    results = select_mysql_pro(pro_account_id, int(tp_id), shop_name)
    print('<<<<<<',results)
    qa_results_dict = select_mysql_qa_dict(CMS_account_id, int(tp_id), shop_name)
    print('>>>>>>',qa_results_dict)

    results_dict = select_mysql_pro_dict(pro_account_id, int(tp_id), shop_name)
    qa_shop_id = select_mysql_qa(CMS_account_id, int(tp_id), shop_name)

    if qa_shop_id is None:
        print('新增',results)
        results_dict_backup = copy.deepcopy(results_dict)
        # 元祖转为列表，然后修改列表里的值，之后再转为元祖
        # 把线上环境的shop_id，修改为qa环境的shop_id
        # 把线上环境的account_id，修改为qa环境的account_id
        results_list = list(results)
        results_shop_list = list(results_list[0])
        results_shop_list[0] = qa_shop_id
        results_shop_list[1] = CMS_account_id
        print(results_shop_list)
        results_shop_tuple = tuple(results_shop_list)
        results_list = results_shop_tuple
        results_tuple = tuple(results_list)
        print('最后',results_tuple)
        tabel_name = 'qa_v2_merchant'
        sql_into =  "INSERT INTO `%s`.`shop`(`id`, `account_id`, `open_id`, `vendor_id`, `uid`, `status`, `tp_id`, `name`, `uname`, `published_number`, `synchronized_number`, `access_token`, `refresh_token`, `message`, `expires_in`, `created_at`, `updated_at`, `default`, `shop_type`) VALUES %s" % (tabel_name, results_tuple)
        sql_into = sql_into.replace('None', 'NULL')
        print(sql_into)
        select_into(sql_into)

        # 店铺新增之后，如果品牌为空，也把品牌也新增过去
        # 品牌
        # 新增之后，需要重新查一遍qa数据库，根据店铺名称查找shap_id
        qa_results_dict = select_mysql_qa_dict(CMS_account_id, int(tp_id), shop_name)
        print('新增店铺再次查询一遍>>>>>>',qa_results_dict)
        if qa_results_dict == None:
            raise Exception ('新增店铺之后，查询不到结果')

        results_pro_brand_dict = select_mysql_pro_brand_dict(int(tp_id), results_dict_backup['id'])
        results_qa_brand_dict = select_mysql_qa_brand_dict(int(tp_id), qa_results_dict['id'])

        if not results_qa_brand_dict:
            for results_pro_brand_data in results_pro_brand_dict:
                print(results_pro_brand_data)

                del results_pro_brand_data['id']
                results_pro_brand_data['shop_id'] = qa_results_dict['id']
                request_json = {
                    "shop_id": results_pro_brand_data["shop_id"],
                    "tp_id": results_pro_brand_data["tp_id"],
                    "original_vid": results_pro_brand_data["original_vid"],
                    "name": results_pro_brand_data["name"],
                    "default": results_pro_brand_data["default"],
                    "created_at": results_pro_brand_data["created_at"],
                    "updated_at": results_pro_brand_data["updated_at"],
                }
                print(request_json)
                sql_into = "INSERT INTO `qa_v2_merchant`.`shop_brand`(`shop_id`, `tp_id`, `original_vid`, `name`, `default`, `created_at`, `updated_at`) VALUES (%(shop_id)s, %(tp_id)s, %(original_vid)s, '%(name)s', %(default)s, '%(created_at)s', '%(updated_at)s');" % (request_json)
                sql_into = sql_into.replace('None', 'NULL')
                print(sql_into)
                select_into(sql_into)
    else :
        print('覆盖',results_dict)
        results_dict_backup = copy.deepcopy(results_dict)
        del results_dict['id']
        results_dict['account_id'] = CMS_account_id
        results_dict.pop("default")
        tar_shop_backup = copy.deepcopy(results_dict)
        for k, v in tar_shop_backup.items():
            if v in (0, "", "0"):
                results_dict.pop(k)
        update_fields = " ,".join(
            [f"{k}={v}" if isinstance(v, int) else f"{k}='{v}'" for k, v in results_dict.items() if v])
        sql_update = "UPDATE {}.shop SET {} WHERE id = {};".format('qa_v2_merchant', update_fields, qa_shop_id)
        print(sql_update)
        select_update(sql_update)

        # 店铺覆盖之后，如果品牌为空，也把品牌也更新过去
        # 品牌
        results_pro_brand_dict = select_mysql_pro_brand_dict(int(tp_id), results_dict_backup['id'])
        results_qa_brand_dict = select_mysql_qa_brand_dict(int(tp_id), qa_results_dict['id'])

        # qa环境为空的时候
        if not results_qa_brand_dict:
            for results_pro_brand_data in results_pro_brand_dict:
                print(results_pro_brand_data)
                del results_pro_brand_data['id']
                results_pro_brand_data['shop_id'] = qa_results_dict['id']
                # INSERT INTO `prod_v2_merchant`.`shop_brand`(`id`, `shop_id`, `tp_id`, `original_vid`, `name`, `default`, `created_at`, `updated_at`) VALUES (6207, 20089959, 1013, NULL, 'diff', 1, '2021-07-01 13:03:40', '2021-07-01 13:06:21.146961');
                request_json = {
                    "shop_id": results_pro_brand_data["shop_id"],
                    "tp_id": results_pro_brand_data["tp_id"],
                    "original_vid": results_pro_brand_data["original_vid"],
                    "name": results_pro_brand_data["name"],
                    "default": results_pro_brand_data["default"],
                    "created_at": results_pro_brand_data["created_at"],
                    "updated_at": results_pro_brand_data["updated_at"],
                }
                print(request_json)
                sql_into = "INSERT INTO `qa_v2_merchant`.`shop_brand`(`shop_id`, `tp_id`, `original_vid`, `name`, `default`, `created_at`, `updated_at`) VALUES (%(shop_id)s, %(tp_id)s, %(original_vid)s, '%(name)s', %(default)s, '%(created_at)s', '%(updated_at)s');" % (request_json)
                sql_into = sql_into.replace('None', 'NULL')
                print(sql_into)
                select_into(sql_into)

        # 判断线上环境比qa环境多品牌的现象，qa环境1688店铺：diff，线上环境1688店铺：diff 其他 其他2
        print(type(results_qa_brand_dict))
        if len(results_pro_brand_dict) > len(results_qa_brand_dict):
            # 线上数据库品牌查询结果，字典 ({'id': 6207, 'shop_id': 20089959, 'tp_id': 1013, 'original_vid': None, 'name': 'diff', 'default': 1, 'created_at': datetime.datetime(2021, 7, 1, 13, 3, 40), 'updated_at': '2021-07-01 13:06:21.146961'}, {'id': 7703, 'shop_id': 20089959, 'tp_id': 1013, 'original_vid': None, 'name': '其他', 'default': 0, 'created_at': datetime.datetime(2022, 1, 26, 7, 13, 20), 'updated_at': None})
            # qa数据库品牌查询结果，字典 ({'id': 2816, 'shop_id': 20090719, 'tp_id': 1013, 'original_vid': None, 'name': 'diff ', 'default': 1, 'created_at': datetime.datetime(2022, 4, 6, 12, 9, 16), 'updated_at': '2022-04-06 12:09:17.355264'},)
            qa_brand_name_list = []
            for qa_dict in results_qa_brand_dict:
                qa_brand_name_list.append(qa_dict['name'])

            data_list = []
            print('qa环境品牌',qa_brand_name_list)
            for pro_dict in results_pro_brand_dict:
                if pro_dict['name'] not in qa_brand_name_list:
                    print('线上环境多出的品牌',pro_dict)
                    data_list.append(pro_dict)
            print(data_list)

            for results_pro_brand_data in data_list:
                print(results_pro_brand_data)
                del results_pro_brand_data['id']
                results_pro_brand_data['shop_id'] = qa_results_dict['id']
                # INSERT INTO `prod_v2_merchant`.`shop_brand`(`id`, `shop_id`, `tp_id`, `original_vid`, `name`, `default`, `created_at`, `updated_at`) VALUES (6207, 20089959, 1013, NULL, 'diff', 1, '2021-07-01 13:03:40', '2021-07-01 13:06:21.146961');
                request_json = {
                    "shop_id": results_pro_brand_data["shop_id"],
                    "tp_id": results_pro_brand_data["tp_id"],
                    "original_vid": results_pro_brand_data["original_vid"],
                    "name": results_pro_brand_data["name"],
                    "default": results_pro_brand_data["default"],
                    "created_at": results_pro_brand_data["created_at"],
                    "updated_at": results_pro_brand_data["updated_at"],
                }
                print(request_json)
                sql_into = "INSERT INTO `qa_v2_merchant`.`shop_brand`(`shop_id`, `tp_id`, `original_vid`, `name`, `default`, `created_at`, `updated_at`) VALUES (%(shop_id)s, %(tp_id)s, %(original_vid)s, '%(name)s', %(default)s, '%(created_at)s', '%(updated_at)s');" % (request_json)
                sql_into = sql_into.replace('None', 'NULL')
                print(sql_into)
                select_into(sql_into)


        # WX_del_HOOK = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=6d9183af-870c-4e27-bfcb-3b230c1d76e2'
        # project = '迁移店铺'
        # start_time = time.strftime("%m%dT%H:%M:%S", time.localtime())
        # mess = wechatRebot_send().test_robot(WX_del_HOOK, project, start_time, tp_id, shop_name, '覆盖')
