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

    def tp_api(self, token, method, post_parm):
        # 公共参数，一般不需要修改
        version = '2.0'
        time_stamp = time.strftime('%Y-%m-%d %H:%M:%S')
        buy_param_json = json.dumps(post_parm, ensure_ascii=False)
        jd_url = 'https://api.jd.com/routerjson?'

        param_arr = {
            'app_key': self.app_key,
            'v': version,
            'method': method,
            'access_token': token,
            'timestamp': time_stamp,
            '360buy_param_json': buy_param_json
        }

        sign = self.create_sign(param_arr)
        str_param = self.create_str_param(param_arr)
        str_param += 'sign=' + sign
        url = jd_url + str_param
        print(url)
        response = urllib.request.urlopen(url).read()
        ssl._create_default_https_context = ssl._create_unverified_context
        return response

    @staticmethod
    def create_folder():
        date = datetime.datetime.now().strftime('%Y%m%d')
        schema_folder = f'schemas/prop_schemas'
        folder = f'{schema_folder}/{date}'
        if not os.path.exists(folder):
            os.makedirs(folder)
        return folder

    def ware_read_search_Ware4Valid(self, token, method):
        props_list = {}
        ssl._create_default_https_context = ssl._create_unverified_context
        pageNo = 1
        pageSize = 50
        while 1:
            param = {
                "searchKey": '测试',
                "searchField": 'title',
                "wareStatusValue": [1,2,4,513,514,516,1028], # 商品状态,多个值属于[或]操作 1:从未上架 2:自主下架 4:系统下架 8:上架 513:从未上架待审 514:自主下架待审 516:系统下架待审 520:上架待审核 1028:系统下架审核失败
                "pageNo" : str(pageNo),
                "pageSize" : str(pageSize),
            }
            response = self.tp_api(token, method, param)
            json_response = json.loads(response, encoding='utf-8')
            print(json_response)
            response_key = 'jingdong_ware_read_searchWare4Valid_responce'

            if not bool(json_response[response_key]['page']['data']):
                print('无测试商品')
                return props_list
            try:
                for data in json_response[response_key]['page']['data']:
                    title = data['title']
                    wareId = data['wareId']
                    print(title, wareId)
                    props_list[wareId] = title
            except TypeError or KeyError:
                pass

            if (pageNo * pageSize)  > json_response[response_key]['page']['totalItem']:
                break
            else:
                pageNo += 1
        return props_list


    def ware_read_delete(self, token, method, wareId):
        ssl._create_default_https_context = ssl._create_unverified_context
        param = {
            "wareId": wareId,
        }
        print(param)
        response = self.tp_api(token, method, param)
        json_response = json.loads(response, encoding='utf-8')
        response_key = 'jingdong_ware_write_delete_responce'
        print(json_response)
        if json_response[response_key]['success'] == True:
            print('删除成功')
        else:
            print('删除失败')


if __name__ == '__main__':
    appKey = '175DE92C342EEAA29C0AC305DB79C996'
    appSecret = '37b0829a675f43a994d10d1a9da3b506'

    # 京东男装,半墨旗舰店9
    JD_NAN_TOKEN = 'b8bf81966d024d92b4f726a478dc24f0xoty'
    # 京东童装,班尼路童装旗舰店
    JD_TONG_TOKEN = 'b9759eabf4454dd8a349dc79b77dc03cywjm'
    Method = 'jingdong.ware.read.searchWare4Valid'
    Method_delete = 'jingdong.ware.write.delete'


    # 京东男装
    jd = APP(appKey, appSecret)
    num = 1
    while 1:
        try:
            props_list = jd.ware_read_search_Ware4Valid(JD_NAN_TOKEN, Method)
        except:
            print('查询重试', num, '次')
            time.sleep(2)
            num += 1
            if num > 10:
                print('查询10次失败')
                break
        else:
            break
    # props_list = jd.ware_read_search_Ware4Valid(JD_NV_TOKEN, Method)
    succeed_list = []
    error_list = []
    for wareId, title in props_list.items():
        print(wareId)
        num = 1
        while 1:
            try:
                # raise Exception
                jd.ware_read_delete(JD_NAN_TOKEN, Method_delete, wareId)
                succeed_list.append(title)
            except:
                print('删除重试',wareId,num,'次')
                time.sleep(1)
                num += 1
                if num > 10:
                    print(wareId, num,'10次失败')
                    error_list.append(title)
                    break
            else:
                break
    print('所有失败',error_list)


    WX_del_HOOK = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=9e04f752-749b-49a9-854c-ab7c7127f3f8'
    project = '删除'
    start_time = time.strftime("%m%dT%H:%M:%S", time.localtime())
    name = '京东:半墨旗舰店-潇潇 banmo520'
    total = len(props_list)
    succeed_total = len(succeed_list)
    error_total = len(error_list)
    succeed_title = ", ".join([str(i) for i in succeed_list])
    failing_title = ", ".join([str(i) for i in error_list])
    mess = wechatRebot_send().test_robot(WX_del_HOOK,project,start_time,name,total,succeed_total,error_total,succeed_title,failing_title)

    # 京东童装
    jd = APP(appKey, appSecret)
    num = 1
    while 1:
        try:
            props_list = jd.ware_read_search_Ware4Valid(JD_TONG_TOKEN, Method)
        except:
            print('查询重试', num, '次')
            time.sleep(2)
            num += 1
            if num > 10:
                print('查询10次失败')
                break
        else:
            break
    # props_list = jd.ware_read_search_Ware4Valid(JD_NV_TOKEN, Method)
    succeed_list = []
    error_list = []
    for wareId, title in props_list.items():
        print(wareId)
        num = 1
        while 1:
            try:
                # raise Exception
                jd.ware_read_delete(JD_TONG_TOKEN, Method_delete, wareId)
                succeed_list.append(title)
            except:
                print('删除重试',wareId,num,'次')
                time.sleep(1)
                num += 1
                if num > 10:
                    print(wareId, num,'10次失败')
                    error_list.append(title)
                    break
            else:
                break
    print('所有失败',error_list)

    WX_del_HOOK = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=9e04f752-749b-49a9-854c-ab7c7127f3f8'
    project = '删除'
    start_time = time.strftime("%m%dT%H:%M:%S", time.localtime())
    name = '京东班尼路童装:baleno-elaine baleno123'
    total = len(props_list)
    succeed_total = len(succeed_list)
    error_total = len(error_list)
    succeed_title = ", ".join([str(i) for i in succeed_list])
    failing_title = ", ".join([str(i) for i in error_list])
    mess = wechatRebot_send().test_robot(WX_del_HOOK,project,start_time,name,total,succeed_total,error_total,succeed_title,failing_title) 
    
