# -*- coding: utf-8 -*-
"""
@time 2021-01-11
@author: yzm
"""
import os
import time
import requests
import json
import random
import urllib.parse
import logging
import string
import sys


class wechatRebot_send:
    def __init__(self):
        pass

    def test_robot_bak(self, WX_del_HOOK, project, start_time,prefix,total,merchant_check_url):
        """
        需要发送到企业微信的文案信息
        :param project:         项目名称
        :start_time:            开始时间
        :prefix                 商品前缀
        :param total:           总计
        :param succeed_title:   批量上货链接
        """
        url_list = []
        for key, value in merchant_check_url.items():
            url_list.append(key)
            url_list.append(':')
            url_list.append('[点击链接]')
            url_list.append('(')
            url_list.append(value)
            url_list.append(')')
            url_list.append('\n')
        print(''.join(url_list))
        str_url = ''.join(url_list)
        data = {
            "msgtype": "markdown",  # 消息类型，此时固定为markdown
            "markdown": {
                "content": "# **自动化上货反馈**\n#### **请相关同事注意，及时跟进！**\n"
                           "> 项目名称：<font color=\"info\">%s</font> \n"
                           "> 开始时间：<font color=\"info\">%s</font> \n"
                           "> 商品货号：<font color=\"info\">%s</font> \n"
                           "> 总计：<font color=\"info\">%s条</font>\n"
                           "> **-------运行详情-------**\n"                       
                           "> **批量上货链接:**<font color=\"info\">\n%s</font>\n"% (
                           project, start_time,prefix,total,str_url)
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

def select_tp_id(tp_name):
    """根据平台名称找到平台ID
    """
    tp_id = ''
    shop_url = CMS_HOST + '/merchant/shop/personal-center'
    response = requests.get(url = shop_url, headers = headers_cms).json()
    for shop_data in response["data"]:
        if shop_data["name"] == tp_name:
            tp_id = shop_data["id"]
    if len(str(tp_id)) == 0:
        raise Exception('未根据平台名称找到平台ID', tp_name)
    else:
        return int(tp_id)


def batch_info(shop_id, tp_name):
    """查找随机的物流与售后，需要传店铺shop_id和tp_id,规则如下,没有物流则报错！！！
    物流与售后，有默认选默认
    有一个,选一个
    没有默认就选第一个
     :return: 随机的物流与售后id：batch_id
    """
    tp_id = select_tp_id(tp_name)
    batch_info_url = CMS_HOST + '/merchant/config/batch_info?tp_id=%s&page=1&per_page=40' % tp_id
    response = requests.get(url=batch_info_url, headers=headers_cms).json()
    batch_list = {}
    for batch in response["data"]["results"]:
        if batch["shop_id"] == int(shop_id):
            if batch['is_selected'] == True:
                print('默认的物流与售后id', batch['id'])
                print('默认的物流与售后name', batch['name'])
                batch_id = batch["id"]
                return batch_id
            elif batch['is_selected'] == False:
                batch_list[batch["id"]] = batch["name"]
    print(batch_list)
    batch_id = [i for i in batch_list.keys()][0]
    print('没有默认,两个选第一个物流与售后id和ame', batch_id, batch_list[batch_id])
    return batch_id


def merchant_publishs_tm(product_ids, brand_id, shop_id, batch_info_id, tp_name):
    """空链上货和生成上货的链接
     :return: 查看上货的链接
    """
    tp_id = select_tp_id(tp_name)
    merchant_url = CMS_HOST + "/merchant/publish"
    data = []
    for index,product_id in enumerate(product_ids):
        print(product_id)
        data_singular = {
                "tp_id": tp_id, # 平台
                "shop_id": shop_id, #店铺ID
                "brand_id": brand_id, #品牌ID
                "product_id": product_id, # 商品ID
                "document_ids": ["0"], # 详情页id
                "batch_info_id": batch_info_id, # 物流与售后
                # "shop_categories": cid_list, # 店铺分类
                "water_mark_id": None, # 资源图水印
                "document_water_mark_id": None, # 详情页水印
                "shipping_template_id": None, # 运费模板ID
                # "main_video_id": None,  #3:4视频主图ID
                # "backup_code": None,  #备用货号
                #"taobao_model": None, #淘宝型号
                # "add_module_id": 22, # 详情页模块ID
                # document_type: "code" # 代码版详情页，当是图片版详情页的时候，则不传
        }
        # 需要优化的地方，可以把product_info存data_singular的值，这样就能添加上淘宝型号，且绑定了商品
        data.append(data_singular)
    print('访问上货接口的报文:', data)
    response = requests.post(url=merchant_url, headers=headers_cms, json=data).json()
    publish_id = list(map(str, response["data"]["publish_ids"]))
    publish_ids = ','.join(publish_id)
    merchant_check_url = CMS_PUB_HOST + '/publish/publish-results?pids=%s&sid=%s&t=publish' % (
        publish_ids, shop_id)
    print('上货链接', merchant_check_url)
    return merchant_check_url


def cms_account(CMS_HOST, cms_number, cms_password):
    """查找账号下的token
    """
    login_url = CMS_HOST + '/auth/login'
    login_body = {"mobile":str(cms_number),"password":str(cms_password),"login_way":"mobile"}
    response = requests.post(login_url,json=login_body)
    account_url = CMS_HOST + '/user/account/login'
    account_body = {"account_id": response.json()['data']['last_login_account']}
    headers = {}
    headers['authorization'] = 'Bearer '+ response.json()['data']['access_token']
    res = requests.post(account_url, json=account_body, headers=headers)
    token = res.json()['data']['access_token']
    cms_account_id = response.json()['data']['last_login_account']
    return token, cms_account_id


product_list_data = {}
product_list = {}
product_tps = {}
def search_publish(merchant_number,page=1, per_page=20):
    # 批量搜索商品
    product_list = {}
    product_list_data["product_overview"] = list()
    while 1:
        merchant_number = urllib.parse.quote(merchant_number)
        shop_url = CMS_HOST + '/merchant/v2/products/overview?page=%s&per_page=%s&codes=%s' % (page, per_page,
             merchant_number)
        response = requests.get(url = shop_url, headers = headers_cms).json()
        for product_overview in response["data"]["product_overview"]:
            product_list[product_overview["product"]["id"]] = product_overview["product"]["code"]
            product_list_data["product_overview"].append((
                {
                    'product_id':product_overview["product"]["id"],
                    'path': (product_overview["product"]["category_path"]),
                    'publish_shops': product_overview["publish_shops"]
                }))
        if (page * per_page) > response["data"]["total"]:
            break
        else:
            page += 1
    if len(product_list) == 0:
        raise Exception ('未搜索到商品', merchant_number)
    return product_list_data, product_list


def host(HOST, Version):
    if Version == '4.0' and HOST == 'on':
        cms_number = 18612210007
        cms_password = '18612210007'
        CMS_HOST = 'https://cms-next-api.ecpro.com'
        CMS_PUB_HOST = 'https://cms-next.ecpro.com'

    if Version == '4.0' and HOST == 'qa':
        cms_number = 18617847474
        cms_password = 'lf18617847474'
        CMS_HOST = 'https://aida-qa-api.ecpro.com'
        CMS_PUB_HOST = 'https://aida-qa.ecpro.com'

    if Version == '3.0' and HOST == 'on':
        cms_number = 18612210007
        cms_password = '18612210007'
        CMS_HOST = 'https://cms-api.ecpro.com'
        CMS_PUB_HOST = 'https://cms.ecpro.com'

    if Version == '3.0' and HOST == 'qa':
        cms_number = 18617847474
        cms_password = 'lf18617847474'
        CMS_HOST = 'https://cms-qa-api.ecpro.com'
        CMS_PUB_HOST = 'https://cms-qa.ecpro.com'

    if Version == '4.0' and HOST == 'dev':
        cms_number = 18617847474
        cms_password = '18617847474'
        CMS_HOST = 'https://cms-dev-api.ecpro.com'
        CMS_PUB_HOST = 'https://cms-dev.ecpro.com'

    if Version == '3.0' and HOST == 'dev':
        cms_number = 18617847474
        cms_password = '18617847474'
        CMS_HOST = 'https://cms-dev-api.ecpro.com'
        CMS_PUB_HOST = 'https://cms-dev.ecpro.com'

    # if HOST == 'qa':
    #     cms_number = 18617847474
    #     cms_password = 'lf18617847474'
    #     CMS_HOST = 'https://cms-qa-api.ecpro.com'
    #     CMS_PUB_HOST = 'https://cms-qa.ecpro.com'
    # elif HOST == 'dev':
    #     cms_number = 18617847474
    #     cms_password = '18617847474'
    #     CMS_HOST = 'https://cms-dev-api.ecpro.com'
    #     CMS_PUB_HOST = 'https://cms-dev.ecpro.com'
    # elif HOST == 'on':
    #     cms_number = 18612210007
    #     cms_password = '18612210007'
    #     # CMS_HOST = 'https://cms-next-api.ecpro.com'
    #     # CMS_PUB_HOST = 'https://cms-next.ecpro.com'
    #     CMS_HOST = 'https://cms-api.ecpro.com'
    #     CMS_PUB_HOST = 'https://cms.ecpro.com'
    return cms_number, cms_password, CMS_HOST, CMS_PUB_HOST


def select_brand(tp_name, shop_name, brand_name):
    """查找店铺和品牌
     :return: 店铺id和品牌id：shop["id"], shop["shop_id"]
    """
    brand_id = ''
    shop_url = CMS_HOST + '/merchant/shop/personal-center'
    response = requests.get(url = shop_url, headers = headers_cms).json()
    for shop_data in response["data"]:
        if shop_data["name"] == tp_name:
            for shops in shop_data["shops"]:
                # if shops["id"] == shop_id and shops["name"] == shop_name:
                if shops["name"] == shop_name:
                    # print(shops["id"], shops["open_id"])
                    shop_id = shops["id"]
                    for brand in shops["brands"]:
                        if brand['name'] == brand_name:
                            # print('店铺名称shop_name：', shops["name"])
                            # print('品牌名称brand_name：', brand["name"])
                            brand_id = brand["id"]
                            print('品牌brand_id：', brand_id)
                            break
                        else:
                            continue
    if len(str(brand_id)) == 0:
        raise Exception('未找到品牌', tp_name, shop_name, brand_name)
    else:
        return str(brand_id) , str(shop_id)


def select_brand_dict():
    """生成按照平台级别，男装女装级别，生成店铺的字典
    """
    shop_data_dict = {}
    shop_url = CMS_HOST + '/merchant/shop/personal-center'
    response = requests.get(url = shop_url, headers = headers_cms).json()
    for shop_data in response["data"]:
        shop_data_dict[shop_data['name']] = {}
        # 判断平台下没有店铺的情况
        if shop_data["shops"]:
            for shops in shop_data["shops"]:
                for brand in shops["brands"]:
                    # 天猫
                    if brand['name'] == '伊木子':
                        shop_data_dict[shop_data['name']].update({
                            '女装': {'shop_name': shops['name'], 'brand_name': brand['name']},
                            '男装': {'shop_name': shops['name'], 'brand_name': brand['name']}
                        })
                    elif brand['name'] == 'pureborn/博睿恩':
                        shop_data_dict[shop_data['name']].update({
                            '童装': {'shop_name': shops['name'], 'brand_name': brand['name']},
                        })
                    elif brand['name'] == 'ZHUCHONGYUN':
                        shop_data_dict[shop_data['name']].update({
                            '配饰': {'shop_name': shops['name'], 'brand_name': brand['name']},
                            '女鞋': {'shop_name': shops['name'], 'brand_name': brand['name']},
                        })
                    # 淘宝
                    elif brand['name'] == 'other/其他':
                        shop_data_dict[shop_data['name']].update({
                            '女装': {'shop_name': shops['name'], 'brand_name': brand['name']},
                            '童装': {'shop_name': shops['name'], 'brand_name': brand['name']},
                            '女鞋': {'shop_name': shops['name'], 'brand_name': brand['name']},
                            '配饰': {'shop_name': shops['name'], 'brand_name': brand['name']},
                        })
                    elif brand['name'] == '004':
                        shop_data_dict[shop_data['name']].update({
                            '男装': {'shop_name': shops['name'], 'brand_name': brand['name']},
                        })
                    # 京东
                    elif brand['name'] == '蓝地（LANDI）':
                        shop_data_dict[shop_data['name']].update({
                            '女装': {'shop_name': shops['name'], 'brand_name': brand['name']},
                        })
                    elif brand['name'] == '半墨':
                        shop_data_dict[shop_data['name']].update({
                            '男装': {'shop_name': shops['name'], 'brand_name': brand['name']},
                        })
                    elif brand['name'] == 'Baleno Junior':
                        shop_data_dict[shop_data['name']].update({
                            '童装': {'shop_name': shops['name'], 'brand_name': brand['name']},
                        })
                    # 拼多多
                    elif brand['name'] == '蜜胜':
                        shop_data_dict[shop_data['name']].update({
                            '女装': {'shop_name': shops['name'], 'brand_name': brand['name']},
                            '男装': {'shop_name': shops['name'], 'brand_name': brand['name']},
                            '童装': {'shop_name': shops['name'], 'brand_name': brand['name']}
                        })
                    # 唯品会
                    elif brand['name'] == 'LANDI':
                        shop_data_dict[shop_data['name']].update({
                            '女装': {'shop_name': shops['name'], 'brand_name': brand['name']},
                        })
                    elif brand['name'] == '班尼路':
                        shop_data_dict[shop_data['name']].update({
                            '男装': {'shop_name': shops['name'], 'brand_name': brand['name']},
                        })
                    elif brand['name'] == 'BALENO JUNIOR':
                        shop_data_dict[shop_data['name']].update({
                            '童装': {'shop_name': shops['name'], 'brand_name': brand['name']},
                        })
                    # 有赞
                    elif brand['name'] == 'JR':
                        shop_data_dict[shop_data['name']].update({
                            '女装': {'shop_name': shops['name'], 'brand_name': brand['name']},
                            '男装': {'shop_name': shops['name'], 'brand_name': brand['name']},
                            '童装': {'shop_name': shops['name'], 'brand_name': brand['name']}
                        })
                    # 快手
                    elif brand['name'] == '三彩':
                        shop_data_dict[shop_data['name']].update({
                            '女装': {'shop_name': shops['name'], 'brand_name': brand['name']},
                            '男装': {'shop_name': shops['name'], 'brand_name': brand['name']},
                            '童装': {'shop_name': shops['name'], 'brand_name': brand['name']}
                        })
                    # 爱库存
                    elif brand['name'] == '班尼路Baleno':
                        shop_data_dict[shop_data['name']].update({
                            '女装': {'shop_name': shops['name'], 'brand_name': brand['name']},
                            '男装': {'shop_name': shops['name'], 'brand_name': brand['name']},
                            '童装': {'shop_name': shops['name'], 'brand_name': brand['name']}
                        })
                    # 1688
                    elif brand['name'] == 'diff':
                        shop_data_dict[shop_data['name']].update({
                            '女装': {'shop_name': shops['name'], 'brand_name': brand['name']},
                            '男装': {'shop_name': shops['name'], 'brand_name': brand['name']},
                            '童装': {'shop_name': shops['name'], 'brand_name': brand['name']}
                        })

                    #小红书
                    elif brand['name'] == 'simple pieces':
                        shop_data_dict[shop_data['name']].update({
                            '女装': {'shop_name': shops['name'], 'brand_name': brand['name']},
                        })
        # 删除字典中value为空的键值对
        if not shop_data_dict.get(shop_data['name']):
            del shop_data_dict[shop_data['name']]
    print(shop_data_dict)
    return shop_data_dict


def search_product_list(product_list_data, path, tp_name, shop_name):
    # 过滤每个商品的信息
    product_id_list = []
    if product_list_data:
        for product_id, data_value in product_list_data.items():
            for data in data_value:
                if path in data['path']:
                    for publish_shop in data['publish_shops']:
                        if publish_shop['tp_name'] == tp_name and publish_shop['shop_name'] == shop_name:
                            print('查找到',data['product_id'])
                            product_id_list.append(data['product_id'])
                else:
                    continue
    return product_id_list


if __name__ == '__main__':
    #京东自营和得物，不处理
    #淘宝型号问题，不处理
    #店铺未授权的情况，不处理
    #快手得买服务，不处理
    # prefix = '0111QB'
    # HOST = 'qa'
    # Version = '3.0'
    prefix = sys.argv[1]
    HOST = sys.argv[2]
    Version = sys.argv[3]

    cms_number, cms_password, CMS_HOST, CMS_PUB_HOST = host(HOST, Version)
    CMS_token, CMS_account_id = cms_account(CMS_HOST, cms_number, cms_password)
    headers_cms = {}
    headers_cms['authorization'] = 'Bearer ' + CMS_token

    product_list_data, product_lists= search_publish(prefix)
    print('商品ID', product_lists)
    print('搜索到', len(product_lists), '款商品')
    print(product_list_data)

    print('生成店铺的字典')
    shop_data = select_brand_dict()
    merchant_check_url_dict = {}


    for tp_name, shop_name in shop_data.items():
        # gender_list = ['女装', '男装', '童装', '女鞋', '配饰']
        # for gender in gender_list:
        for gender, gender_data in shop_name.items():
            product_id_list = search_product_list(product_list_data, gender, tp_name, shop_data[tp_name][gender]['shop_name'])
            if len(product_id_list) != 0:
                brand_id, shop_id = select_brand(tp_name, shop_data[tp_name][gender]['shop_name'], shop_data[tp_name][gender]['brand_name'])
                batch_info_id = batch_info(shop_id, tp_name)
                merchant_check_url = merchant_publishs_tm(product_id_list, brand_id, shop_id, batch_info_id, tp_name)
                merchant_check_url_dict[tp_name + '_' + shop_data[tp_name][gender]['shop_name'] + '_' + gender] = merchant_check_url



    time.sleep(2)
    WX_del_HOOK = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=24692f61-7f4f-41f4-a4df-57b9b4660a57'
    project = '批量上货链接'
    start_time = time.strftime("%m%dT%H:%M:%S", time.localtime())
    total = len(product_lists)
    mess = wechatRebot_send().test_robot_bak(WX_del_HOOK, project, start_time, prefix, total, merchant_check_url_dict)

