# -*- coding: utf-8 -*-
"""
@time 2021-08-19
@author: yzm
"""
import json
import hashlib
import requests
import datetime
import time
import pprint
import pymysql


class wechatRebot_send:
    def __init__(self):
        pass
    def test_robot(self, WX_del_HOOK, project,start_time,name,total,succeed_total,error_total,succeed_title,failing_title):
        """
        需要发送到企业微信的文案信息
        :param project:         项目名称
        :start_time=:           开始时间
        :param name:            后台账号和密码
        :param total:           总计
        :param succeed_total    成功数
        :param error_total      失败数
        :param succeed_title:   删除成功货号
        :param failing_title:   删除失败货号
        """
        data = {
            "msgtype": "markdown",  # 消息类型，此时固定为markdown
            "markdown": {
                "content": "# **提醒！自动化测试反馈**\n#### **请相关同事注意，及时跟进！**\n"
                           "> 项目名称：<font color=\"info\">%s</font> \n"
                           "> 开始时间：<font color=\"info\">%s</font> \n"
                           "> 后台账号和密码：<font color=\"info\">%s</font> \n"
                           "> 总计：<font color=\"info\">%s条</font>\n"
                           "> 成功数：<font color=\"info\">%s条</font>\n"
                           "> 失败数：<font color=\"info\">%s条</font>\n"
                           "> **--------------------运行详情--------------------**\n"
                           "> **删除成功货号：**<font color=\"info\">%s</font>\n"
                           "> **删除失败货号：**<font color=\"info\">%s</font>\n"% (
                           project, start_time, name, total,succeed_total,error_total,succeed_title,failing_title)
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
def get_access_token_select_mysql():
    # 打开数据库连接
    # db = MySQLdb.connect("rm-2zeb07rt531eym8of1o.mysql.rds.aliyuncs.com", "qa_v2", "lyp82nLF", "qa_v2_merchant", charset='utf8' )
    Token_list = {}
    try:
        db = pymysql.connect(
            # host='rm-2zeb07rt531eym8of1o.mysql.rds.aliyuncs.com',
            host='rm-2ze69dr39e1217univo.mysql.rds.aliyuncs.com',
            port=3306,
            user='prod_migration',
            passwd='lyp82nLF',
            db='prod_v2_merchant',
            charset='utf8',
            compress=1,
            connect_timeout=1
        )
    except BaseException:
        print("Could not connect to MySQL server.")
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    sql = "select access_token from shop where account_id = 1001686 and tp_id =1012 and name = '清馨女装工厂'and status = 1"
    print(sql)
    # 执行SQL查询语句
    try:
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchone()
        print(results)
    except:
        print('查询失败')
    db.close()
    return results


def get_md5_string(params):
    hl = hashlib.md5()
    hl.update(params.encode(encoding='utf-8'))
    return hl.hexdigest()


def product_listV2(uri, app_key, app_secret, access_token):
    url = 'https://openapi-fxg.jinritemai.com'
    method = "product.listV2"
    page = 1
    size = 100
    props_list = {}
    props_list_original = {}
    while 1:
        param_json = {
            "page": str(page),
            "size": str(size),
            "status": 1, # 指定状态返回商品列表：0上架 1下架
            # "check_status": 7, # 指定审核状态返回商品列表：1未提审 2审核中 3审核通过 4审核驳回 5封禁 7审核通过，待上架状态
        }
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        params_str = (app_secret
                      + 'app_key' + app_key
                      + 'method' + method
                      + 'param_json' + json.dumps(param_json, separators=(',', ':'))
                      + 'timestamp' + timestamp
                      + 'v2'
                      + app_secret)
        # separators 是('元素之间用逗号隔开', 'key和内容之间'用冒号隔开)
        # 这里是'逗号','冒号' 中间的逗号不带引号
        sign = get_md5_string(params_str)
        res = requests.get(url + uri, params={
                "method": method,
                "app_key": app_key,
                "access_token": access_token,
                "param_json": json.dumps(param_json, separators=(',', ':')),
                "timestamp": timestamp,
                "v": "2",
                "sign": sign,
        })
        # if res.status_code == 200:
        #     print(res.text)
        # else:
        #     raise Exception('token error')
        if res.json()['msg'] == 'success':
            pass
        else:
            raise Exception('token error')





        print(res.url)
        # pprint.pprint(res.json())

        try:
            for data in res.json()["data"]['data']:
                name = data['name']
                product_id = data['product_id']
                # print(name, product_id)
                props_list_original[product_id] = name
        except TypeError or KeyError:
            pass

        if (page * size) > res.json()["data"]['total']:
            break
        else:
            page += 1

    for product_id, name in props_list_original.items():
        if '测试' in name:
            props_list[product_id] = name
    return props_list


def product_del(del_uri, app_key, app_secret, access_token, product_id):
    url = 'https://openapi-fxg.jinritemai.com'
    method = "product.del"
    param_json = {
        "product_id": product_id
    }
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    params_str = (app_secret
                  + 'app_key' + app_key
                  + 'method' + method
                  + 'param_json' + json.dumps(param_json, separators=(',', ':'))
                  + 'timestamp' + timestamp
                  + 'v2'
                  + app_secret)
    sign = get_md5_string(params_str)
    res = requests.get(url + del_uri, params={
        "method": method,
        "app_key": app_key,
        "access_token": access_token,
        "param_json": json.dumps(param_json, separators=(',', ':')),
        "timestamp": timestamp,
        "v": "2",
        "sign": sign,
    })
    print(res.url)
    # pprint.pprint(res.json())
    if res.json()['msg'] == 'success':
        print('删除成功')
    else:
        print('删除失败')


if __name__ == '__main__':
    url = '/product/listV2'
    del_uri = '/product/del'
    app_key = "6857846430536893960"
    app_secret = '605d9a9b-1003-45f2-8d5f-056a68f91616'
    # access_token = get_access_token_select_mysql()
    access_token = '33b2ffa9-78ea-4027-a75a-0828055ca53d'
    access_token_slicer = access_token[0]
    # 抖音token有效期为7天,抖音的刷新API不能用。都刷新不了
    # 伊木子：eaf40a32-5b84-49bb-8b80-f15cfa569e09

    props_list = product_listV2(url, app_key, app_secret, access_token)
    succeed_list = []
    error_list = []
    for product_id, name in props_list.items():
        print(name, product_id)
        num = 1
        while 1:
            try:
                # raise Exception
                product_del(del_uri, app_key, app_secret, access_token, product_id)
                succeed_list.append(name)
            except:
                print('删除重试', product_id, num, '次')
                time.sleep(1)
                num += 1
                if num > 10:
                    print(product_id, num, '10次失败')
                    error_list.append(name)
                    break
            else:
                break
    print('所有失败', error_list)

    WX_del_HOOK = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=9e04f752-749b-49a9-854c-ab7c7127f3f8'
    project = '删除'
    start_time = time.strftime("%m%dT%H:%M:%S", time.localtime())
    # name = '抖音清馨女装: 17852550399'
    name = 'EXCEPTIONDEMIXMIND服饰旗舰店'
    total = len(props_list)
    succeed_total = len(succeed_list)
    error_total = len(error_list)
    succeed_title = ", ".join([str(i) for i in succeed_list])
    failing_title = ", ".join([str(i) for i in error_list])
    mess = wechatRebot_send().test_robot(WX_del_HOOK,project,start_time,name,total,succeed_total,error_total,succeed_title,failing_title)
