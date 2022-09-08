# -*- coding: utf-8 -*-
import datetime
import json
import os
import time
import hashlib
import urllib.parse
import urllib.request
import ssl
import requests
# from taobao.prop_crawler import TbAPP
# from tmall.config import TM_NAN_ORIGINAL_CIDS, TM_NV_ORIGINAL_CIDS, TM_TONG_ORIGINAL_CIDS, tmall_ORIGINAL_CIDS
# from tmall.config import  TM_NV_ORIGINAL_CIDS

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

class APP:
    def __init__(self, app_key, app_secret):
        self.app_key = app_key
        self.app_secret = app_secret

    # 排序
    @staticmethod
    def sort_param(unsorted_dict):
        sorted_list = []
        sorted_keys = sorted(unsorted_dict.keys())
        for _ in sorted_keys:
            sorted_list.append((_, unsorted_dict[_]))
        sorted_dict = dict(sorted_list)
        return sorted_dict

    # MD5加密
    def encryption(self, orig_str):
        md_str = hashlib.md5(orig_str.encode())
        return md_str.hexdigest()

    # 计算sign
    def create_sign(self, param_arr):
        sign = self.app_secret
        param_arr = self.sort_param(param_arr)
        for k, v in param_arr.items():
            if k != '' and v != '':
                sign += k + v
        sign += self.app_secret
        sign = self.encryption(sign).upper()
        return sign

    # 参数排序
    @staticmethod
    def create_str_param(param_arr):
        str_param = ''
        for k, v in param_arr.items():
            if k != '' and v != '':
                str_param += k + '=' + urllib.parse.quote_plus(v) + '&'
        return str_param

    @staticmethod
    def create_folder():
        date = datetime.datetime.now().strftime('%Y%m%d')
        schema_folder = f'schemas/prop_schemas'
        folder = f'{schema_folder}/{date}'
        if not os.path.exists(folder):
            os.makedirs(folder)
        return folder


    def tp_api(self, token, method, post_parm):
        version = '2.0'
        sign_method = 'md5'
        time_stamp = time.strftime('%Y-%m-%d %H:%M:%S')
        param_arr = {
            'app_key': self.app_key,
            'v': version,
            'sign_method': sign_method,
            'format': 'json',
            'timestamp': time_stamp,
            'method': method,
            'session': token,
        }
        param_arr = {**param_arr, **post_parm}
        sign = self.create_sign(param_arr)
        str_param = self.create_str_param(param_arr)
        str_param += 'sign=' + sign
        url = 'http://gw.api.taobao.com/router/rest?' + str_param
        print(url)
        res = urllib.request.urlopen(url).read()
        # print(res)
        return res


class TMallAPP(APP):
    def taobao_products_search(self, token, methods):
        props_list = {}
        pageNo = 1
        page_size = 200
        while 1:
            post_parm = {
                'fields': 'title,num_iid,cid',
                'q': '测试',
                'banner': 'for_shelved',
                'page_no': str(pageNo),
                'page_size': str(page_size),
            }
            '''
            分类字段。可选值:
                    regular_shelved(定时上架)
                    never_on_shelf(从未上架)
                    off_shelf(我下架的)
                    for_shelved(等待所有上架)
                    sold_out(全部卖完)
                    violation_off_shelf(违规下架的)
                    默认查询for_shelved(等待所有上架)这个状态的商品
                    注：for_shelved(等待所有上架)=regular_shelved(定时上架)+never_on_shelf(从未上架)+off_shelf(我下架的)
            '''
            response = self.tp_api(token, methods, post_parm)
            json_response = json.loads(response)
            # print(json_response)
            response_key = 'items_inventory_get_response'
            if json_response[response_key]['total_results'] == 0:
                 print('无测试商品')
                 return props_list
            else:
                try:
                    for data in json_response[response_key]['items']['item']:
                        title = data['title']
                        num_iid = data['num_iid']
                        # print(title, num_iid)
                        props_list[num_iid] = title
                except TypeError or KeyError:
                    pass
            if (pageNo * page_size)  > json_response[response_key]['total_results']:
                break
            else:
                pageNo += 1
        return props_list


    def alibaba_item_operate_delete(self, token, methods, num_iid):
        param = {
            'item_id': str(num_iid),
        }
        # print(param)
        response = self.tp_api(token, methods, param)
        json_response = json.loads(response)
        # print(json_response)
        response_key = 'alibaba_item_operate_delete_response'
        if json_response[response_key]['result'] == 'success':
            print('删除成功')
        else:
            print('删除失败')


if __name__ == '__main__':
    app_key = '27727487'
    app_secret = '7c17ec2e103c7f6d786468ff8a3ce1e5'
    #淘宝 安奈儿
    TB_An_Token = '6201f26d3471c05734c63eecb5c31e26c3ZZbcb2ae6d5a7791922214'
    #淘宝 monkey_29
    TB_Monkey_Token = '620291368e3941a4f5fc7ZZ61a382b75a64cb6150b937fe111328967'


    methods = 'taobao.items.inventory.get'
    methods_delete = 'alibaba.item.operate.delete'


    tmall_app = TMallAPP(app_key, app_secret)
    props_list = tmall_app.taobao_products_search( TB_An_Token, methods)
    succeed_list = []
    error_list = []

    for num_iid, title in props_list.items():
        print(title, num_iid)

        num = 1
        while 1:
            try:
                # raise Exception
                tmall_app.alibaba_item_operate_delete( TB_An_Token, methods_delete, num_iid)
                succeed_list.append(title)
            except:
                print('删除重试', num_iid, num, '次')
                time.sleep(1)
                num += 1
                if num > 10:
                    print(num_iid, num, '10次失败')
                    error_list.append(title)
                    break
            else:
                break
    print('所有失败', error_list)
    
    WX_del_HOOK = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=9e04f752-749b-49a9-854c-ab7c7127f3f8'
    project = '删除'
    start_time = time.strftime("%m%dT%H:%M:%S", time.localtime())
    name = '淘宝安奈儿天使兔店:安奈儿天使兔:易尚货 Ane20220530'
    total = len(props_list)
    succeed_total = len(succeed_list)
    error_total = len(error_list)
    succeed_title = ", ".join([str(i) for i in succeed_list])
    failing_title = ", ".join([str(i) for i in error_list])
    mess = wechatRebot_send().test_robot(WX_del_HOOK,project,start_time,name,total,succeed_total,error_total,succeed_title,failing_title)

    #淘宝 monkey_29
    tmall_app = TMallAPP(app_key, app_secret)
    props_list = tmall_app.taobao_products_search(TB_Monkey_Token, methods)
    succeed_list = []
    error_list = []

    for num_iid, title in props_list.items():
        print(title, num_iid)

        num = 1
        while 1:
            try:
                # raise Exception
                tmall_app.alibaba_item_operate_delete(TB_Monkey_Token, methods_delete, num_iid)
                succeed_list.append(title)
            except:
                print('删除重试', num_iid, num, '次')
                time.sleep(1)
                num += 1
                if num > 10:
                    print(num_iid, num, '10次失败')
                    error_list.append(title)
                    break
            else:
                break
    print('所有失败', error_list)

    WX_del_HOOK = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=9e04f752-749b-49a9-854c-ab7c7127f3f8'
    project = '删除'
    start_time = time.strftime("%m%dT%H:%M:%S", time.localtime())
    name = '淘宝:monkey_29 monkey_29'
    total = len(props_list)
    succeed_total = len(succeed_list)
    error_total = len(error_list)
    succeed_title = ", ".join([str(i) for i in succeed_list])
    failing_title = ", ".join([str(i) for i in error_list])
    mess = wechatRebot_send().test_robot(WX_del_HOOK, project, start_time, name, total, succeed_total, error_total,
                                         succeed_title, failing_title)





