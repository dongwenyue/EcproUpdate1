# -*- coding: utf-8 -*-
import datetime
import json
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
                           "> 项目名称：<font color=\"info\">%s</font> \n"
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


def youzan_category_get_by_id(parent_id):
    str_param = 'access_token=' + access_token + '&' + \
                'pid=' + str(parent_id)
    url = 'https://open.youzanyun.com/api/youzan.category.listchildren/1.0.0?' + str_param
    response = urllib.request.urlopen(url).read()
    print(response)
    return response


def youzan_standard_search(token):
    props_list = {}
    page_no = 1
    page_size = 40
    while 1:
        text = '测试'
        str_param = 'access_token=' + token + '&' + 'q=' + urllib.parse.quote(text) + '&' + 'page_no=' + str(
            page_no) + '&' + 'page_size=' + str(page_size)
        print(str_param)
        url = 'https://open.youzanyun.com/api/youzan.items.inventory.get/3.0.0?' + str_param
        print(url)
        response = urllib.request.urlopen(url).read()
        json_response = json.loads(response)
        # print(json_response)
        if json_response['data']['count'] == 0:
            print('无测试商品')
            return props_list
        else:
            try:
                for data in json_response['data']['items']:
                    title = data['title']
                    item_id = data['item_id']
                    print(title, item_id)
                    props_list[item_id] = title
            except TypeError or KeyError:
                pass
        if (page_no * page_size) > json_response['data']['count']:
            break
        else:
            page_no += 1
    return props_list


def youzan_item_delete(token, item_id):
    str_param = 'access_token=' + token + '&' + \
                'item_id=' + str(item_id)
    print(str_param)
    url = 'https://open.youzanyun.com/api/youzan.item.delete/3.0.1?' + str_param
    print(url)
    response = urllib.request.urlopen(url).read()
    json_response = json.loads(response)
    print(json_response)

    if json_response['success']:
        print('删除成功')
    else:
        print('删除失败')


if __name__ == '__main__':
    '''
    应用名称：易尚货_美工机器人
    App Id：52029
    client_id：3313f8079d412d104d
    client_secret：1ca967029a62d584d21429fafd09fb16
    回调地址：https://cms-api.ecpro.com/oauth/callback/youzan
    '''
    app_key = '27727487'
    app_secret = '7c17ec2e103c7f6d786468ff8a3ce1e5'
    shop_token_dict = {
        '有赞男装|堡狮龙bossini|18718578553|xueqing486..': 'c36a5b2e2156f49edd56bf0d40d45e5',
    }

    # access_token = 'c36a5b2e2156f49edd56bf0d40d45e5'
    for name, shop_token in shop_token_dict.items():
        # 获取仓库中的商品列表
        props_list = youzan_standard_search(shop_token)
        succeed_list = []
        error_list = []
        print(props_list)
        # youzan_item_delete('2792695789')

        for num_iid, title in props_list.items():
            print(title, num_iid)
            num = 1
            while 1:
                try:
                    # raise Exception
                    youzan_item_delete(shop_token, num_iid)
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
        # name = '淘宝:monkey_29:ceshi ceshi123'
        total = len(props_list)
        succeed_total = len(succeed_list)
        error_total = len(error_list)
        succeed_title = ", ".join([str(i) for i in succeed_list])
        failing_title = ", ".join([str(i) for i in error_list])
        mess = wechatRebot_send().test_robot(WX_del_HOOK, project, start_time, name, total, succeed_total, error_total,
                                             succeed_title, failing_title)
