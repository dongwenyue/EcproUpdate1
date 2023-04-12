# -*- coding: utf-8 -*-
import datetime
import hashlib
import json
import os
import ssl
import time
import urllib.parse
import urllib.request
import requests


class wechatRebot_send:
    def __init__(self):
        pass

    def test_robot(self, WX_del_HOOK, project, start_time, name, total, succeed_total, error_total, succeed_title,
                   failing_title):
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
                           "> 项目名称及批量搜索标题：<font color=\"info\">%s</font> \n"
                           "> 开始时间：<font color=\"info\">%s</font> \n"
                           "> 后台账号和密码：<font color=\"info\">%s</font> \n"
                           "> 总计：<font color=\"info\">%s条</font>\n"
                           "> 成功数：<font color=\"info\">%s条</font>\n"
                           "> 失败数：<font color=\"info\">%s条</font>\n"
                           "> **--------------------运行详情--------------------**\n"
                           "> **删除成功货号：**<font color=\"info\">%s</font>\n"
                           "> **删除失败货号：**<font color=\"info\">%s</font>\n" % (
                               project, start_time, name, total, succeed_total, error_total, succeed_title,
                               failing_title)
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


class APP:
    def __init__(self, app_key, appSecret):
        self.appId = app_key
        self.app_secret = appSecret

    def creat_sign(self, param):
        link = param["method"]
        link += "?"
        link += "appId=" + param["appId"] + "&timestamp=" + param["timestamp"] + "&version=" + param[
            "version"] + self.app_secret
        md_str = hashlib.md5(link.encode())
        return md_str.hexdigest()

        # 计算md5值并且将所有字母转换成大写
        # md5 = hashlib.md5()
        # md5.update(link.encode("UTF-8"))
        # return md5.hexdigest().upper()

    def tp_api(self, token, method, post_param):
        # 公共参数，一般不需要修改
        version = '2.0'
        time_stamp = int(round(time.time() * 1000))
        xiaohongshu_url = 'https://ark.xiaohongshu.com/ark/open_api/v3/common_controller'
        sign = self.creat_sign({
            "appId": self.appId,
            'timestamp': str(time_stamp),
            'version': version,
            'method': method,
        })
        json_data = {
            "appId": self.appId,
            "timestamp": str(time_stamp),
            "version": version,
            "appSecret": self.app_secret,
            "method": method,
            "sign": sign,
            "accessToken": token,
        }
        json_data.update(post_param)
        response = requests.post(xiaohongshu_url, json=json_data, headers={"content-type": "application/json"}).json()
        return response

    def getdetailltemlist(self, token, method):
        global words
        props_list_original = {}
        props_list = {}
        pageNo = 1
        pageSize = 10
        while 1:
            param = {
                "pageNo": pageNo,
                "pageSize": pageSize,
                'buyable': False,
            }
            json_response = self.tp_api(token, method, param)
            print(json_response)
            try:
                for data in json_response['data']['data']:
                    itemData_name = data['itemData']['name']
                    itemData_id = data['itemData']['id']
                    itemData_spuId = data['itemData']['spuId']
                    print('搜索到-->', itemData_name, itemData_id, itemData_spuId)
                    props_list_original[itemData_name] = {}
                    props_list_original[itemData_name].update(
                        {'itemData_id': itemData_id, 'itemData_spuId': itemData_spuId},
                    )
            except TypeError or KeyError:
                pass

            if (pageNo * pageSize) > json_response['data']['total']:
            # if (pageNo * pageSize) > 10:
                break
            else:
                pageNo += 1

        for name, product_data  in props_list_original.items():
            # if '测试' in name:
            if words in name:
                print('将会删除-----', name, product_data)
                props_list[name] = {}
                props_list[name].update(
                    {'itemData_id': product_data["itemData_id"], 'itemData_spuId': product_data["itemData_spuId"]},
                )
        return props_list

    def deleteItem(self, token, Method_delete, product_data):
        param ={
            'spuId' : str(product_data["itemData_spuId"]),
            'id' : str(product_data["itemData_id"]),
        }
        json_response = self.tp_api(token, Method_delete, param)
        print(json_response)
        if json_response['data'] == '删除成功':
            print('删除成功')
        else:
            print('删除失败')

if __name__ == '__main__':
    appKey = '441dfe9ffef844738eff'
    appSecret = '84c127b458415d742d8e6f68ef0ce044'
    Method = 'product.getDetailItemList'
    Method_delete = 'product.deleteItem'
    global words
    words = '测试'
    shop_token_dict = {
        '小红书|Clarks旗舰店': 'token-39afe49f6cf04c13b69e144ce94254e3-66135684dd2448f29ffb5d463a7f2299',
    }
    for name, shop_token in shop_token_dict.items():
        jd = APP(appKey, appSecret)
        props_list = jd.getdetailltemlist(shop_token, Method)

        print(props_list)
        succeed_list = []
        error_list = []
        for product_name, product_data in props_list.items():
            print('最后', product_name, product_data)
            num = 1
            while 1:
                try:
                    # raise Exception
                    jd.deleteItem(shop_token, Method_delete, product_data)
                    succeed_list.append(product_name)
                except:
                    print('删除重试', wareId, num, '次')
                    time.sleep(1)
                    num += 1
                    if num > 10:
                        print(wareId, num, '10次失败')
                        error_list.append(product_name)
                        break
                else:
                    break
        print('所有成功', succeed_list)
        print('成功个数', len(succeed_list))
        print('所有失败', error_list)

        WX_del_HOOK = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=9e04f752-749b-49a9-854c-ab7c7127f3f8'
        # project = '删除'
        project = words
        start_time = time.strftime("%m%dT%H:%M:%S", time.localtime())
        # name = '小红书:MO&Co.官方旗舰店 朱海辉'
        total = len(props_list)
        succeed_total = len(succeed_list)
        error_total = len(error_list)
        # succeed_title = ", ".join([str(i) for i in succeed_list])
        # failing_title = ", ".join([str(i) for i in error_list])
        succeed_title = ""
        failing_title = ""
        mess = wechatRebot_send().test_robot(WX_del_HOOK, project, start_time, name, total, succeed_total, error_total,
                                             succeed_title, failing_title)
