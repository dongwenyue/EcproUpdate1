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
    def __init__(self, app_id, app_secret):
        self.app_id = app_id
        self.app_secret = app_secret

    def creat_sign(self,param):
        link = param["method"]
        link +="?"
        link += "appId=" + param["appId"] + "&timestamp="+param["timestamp"] + "&version="+param["version"]+self.app_secret
        md_str = hashlib.md5(link.encode())
        # print(md_str.hexdigest(),"**")
        return md_str.hexdigest()

    def tp_api(self, token, method,post_param):
        # 公共参数，一般不需要修改
        version = '2.0'
        time_stamp = int(round(time.time()*1000))
        xiaohongshu_url = 'https://ark.xiaohongshu.com/ark/open_api/v3/common_controller'
        sign=self.creat_sign({
            'method': method,
            "appId":self.app_id,
            'timestamp': str(time_stamp),
            'version': version,
        })
        data = {
            'sign': sign,
            'method': method,
            "appId": app_id,
            'accessToken': 'token-6e5292fc29e04bee80f54f8ae4e0ce26-53f82c8cbf8a421489f7a5b3e9dbddfc',
            'timestamp': time_stamp,
            'version': '2.0',
            'method' : 'product.getDetailItemList',
        }
        data.update(post_param)
        response = requests.post(xiaohongshu_url, json=data,headers = {'Content_type': 'application/json'}).json()
        print(response)
        return response
    def ware_product_getDetailItemList(self, token, method):
        props_list = {}
        props_dict = {}
        pageNo = 1
        pageSize = 10
        buyable = False
        while 1:
            param = {
                    "pageNo" : pageNo ,
                    "pageSize" : pageSize,
                    "buyable" : buyable,
            }
            json_response = self.tp_api(self,method,param)
            # json_response = json.loads(response, encoding='utf-8')
            print(json_response["data"]["total"])

            try:
                for data in json_response['data']["hits"]['itemData']:
                    iteam_name = data['name']
                    iteam_id = data['id']
                    print(iteam_name,iteam_id )
                    props_list[iteam_id] = iteam_name
            except TypeError or KeyError:
                pass

            if (pageNo * pageSize) > json_response['data']['total']:
                break
            else:
                pageNo += 1
        for iteam_id ,iteam_name in props_list.items():
            if '测试' in iteam_name :
                props_dict[iteam_id] = iteam_name
        return props_dict
    # def little_red_book_ware_delete(self,token,method,id,spuId):
    #     param_json = {
    #         "id" : str(id),
    #         "spuId" : str(spuId),
    #     }
    #     print(param_json)
    #     response = self.tp_api(token, method, param_json)
    #     json_response = json.loads(response, encoding='utf-8')
    #     response_key = 'little_red_book_ware_write_delete_responce'
    #     print(json_response)
    #     if json_response[response_key]['success'] == True:
    #         print('删除成功')
    #     else:
    #         print('删除失败')




if __name__ == '__main__':
    app_id = '441dfe9ffef844738eff'
    appSecret = '84c127b458415d742d8e6f68ef0ce044'
    # 小红书店铺t
    little_red_book_token = 'token-6e5292fc29e04bee80f54f8ae4e0ce26-53f82c8cbf8a421489f7a5b3e9dbddfc'
    Method = 'product.getDetailItemList'
    red = APP(app_id, appSecret)
    red.ware_product_getDetailItemList(little_red_book_token,Method)
    # red.little_red_book_ware_delete(little_red_book_token,Method)
    # Method_delete = 'little_red_book_ware_delete'

    # 小红书女装
    jd = APP(app_id, appSecret)
    num = 1
    while 1:
        try:
            props_list = jd.ware_read_search_Ware4Valid(little_red_book_token, Method)
        except:
            print('查询重试', num, '次')
            time.sleep(2)
            num += 1
            if num > 20:
                print('查询20次失败')
                break
        else:
            break
    # props_list = jd.ware_read_search_Ware4Valid(JD_NV_TOKEN, Method)
    succeed_list = []
    error_list = []
    print("------------>")
    for wareId, title in props_list.items():
        print(wareId)
        num = 1
        while 1:
            try:
                # raise Exception
                jd.ware_read_delete(little_red_book_token, Method_delete, wareId)
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
    name = '小红书 wuhuixian@thebeamco.com'
    total = len(props_list)
    succeed_total = len(succeed_list)
    error_total = len(error_list)
    succeed_title = ", ".join([str(i) for i in succeed_list])
    failing_title = ", ".join([str(i) for i in error_list])
    mess = wechatRebot_send().test_robot(WX_del_HOOK,project,start_time,name,total,succeed_total,error_total,succeed_title,failing_title)

