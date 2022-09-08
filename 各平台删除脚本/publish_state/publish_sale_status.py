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

    def test_robot_bak(self, WX_del_HOOK, project, start_time, prefix, total, merchant_check_url):
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
                           "> **批量上货链接:**<font color=\"info\">\n%s</font>\n" % (
                               project, start_time, prefix, total, str_url)
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
    response = requests.get(url=shop_url, headers=headers_cms).json()
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


def category_code(shop_id):
    """查找驿氪的分类设置，需要传店铺shop_id,规则如下,没有分类设置则上货校验住
    分类设置，随机选择
    没有分类设置则报错
     :return: 随机的分类设置code
    """
    # https://aida-qa-api.ecpro.com/merchant/v3/yike-category-mapping?shop_id=20090783
    category_code_url = CMS_HOST + '/merchant/v3/yike-category-mapping?shop_id=%s' % shop_id
    response = requests.get(url=category_code_url, headers=headers_cms).json()
    category_code_list = []
    for data in response["data"]["results"]:
        if data["shop_id"] == int(shop_id):
            category_code_list.append(data['code'])
    print('分类设置列表', category_code_list)
    code = random.choice(category_code_list)
    print('随机取分类设置', code)
    return code


def merchant_publishs_tm(product_ids, brand_id, shop_id, batch_info_id, code, tp_name,sale_status):
    """空链上货和生成上货的链接
     :return: 查看上货的链接
    """
    tp_id = select_tp_id(tp_name)
    merchant_url = CMS_HOST + "/merchant/publish"
    data = []
    # for index,product_id in enumerate(product_ids):
    for product_id, templates_id in product_ids.items():
        print('上货时商品ID和详情页ID', product_id, templates_id)
        # 判断没有详情页的时候
        if not templates_id:
            print('详情页ID为空了,"document_ids": ["0"]')
            data_singular = {
                "tp_id": tp_id,  # 平台
                "shop_id": shop_id,  # 店铺ID
                "brand_id": brand_id,  # 品牌ID
                "product_id": product_id,  # 商品ID
                "document_ids": ["0"],  # 详情页id
                # 4.0唯品会多色多详情页
                # "new_documents": [{color: "黑色", document_id: 93335}],  # 详情页id
                "batch_info_id": batch_info_id,  # 物流与售后
                # "shop_categories": cid_list, # 店铺分类
                "water_mark_id": None,  # 资源图水印
                "document_water_mark_id": None,  # 详情页水印
                "shipping_template_id": None,  # 运费模板ID
                # "main_video_id": None,  #3:4视频主图ID
                # "backup_code": None,  #备用货号
                # "taobao_model": None, #淘宝型号
                # "add_module_id": 22, # 详情页模块ID
                # document_type: "code" # 代码版详情页，当是图片版详情页的时候，则不传
            }
            if tp_id == 1016:
                data_singular['category_code'] = code
            elif tp_id ==1001:
                data_singular['sale_status'] = sale_status
                # data_singular['sale_status'] = 'instock'
            # elif tp_id == 1001:
                # data_singular['sale_status'] = 'onsale'
            # 需要优化的地方，可以把product_info存data_singular的值，这样就能添加上淘宝型号，且绑定了商品
            data.append(data_singular)
        else:
            data_singular = {
                "tp_id": tp_id,  # 平台
                "shop_id": shop_id,  # 店铺ID
                "brand_id": brand_id,  # 品牌ID
                "product_id": product_id,  # 商品ID
                "document_ids": [templates_id],  # 详情页id
                "batch_info_id": batch_info_id,  # 物流与售后
                # "shop_categories": cid_list, # 店铺分类
                "water_mark_id": None,  # 资源图水印
                "document_water_mark_id": None,  # 详情页水印
                "shipping_template_id": None,  # 运费模板ID
                # "main_video_id": None,  #3:4视频主图ID
                # "backup_code": None,  #备用货号
                # "taobao_model": None, #淘宝型号
                # "add_module_id": 22, # 详情页模块ID
                # document_type: "code" # 代码版详情页，当是图片版详情页的时候，则不传
            }
            if tp_id == 1016:
                data_singular['category_code'] = code
            elif tp_id ==1001:
                data_singular['sale_status'] = 'instock'
            # 需要优化的地方，可以把product_info存data_singular的值，这样就能添加上淘宝型号，且绑定了商品
            data.append(data_singular)
    print('访问上货接口的报文:', data)
    response = requests.post(url=merchant_url, headers=headers_cms, json=data).json()
    print('上货接口返回结果:', response)
    # publish_id = list(map(str, response["data"]["publish_ids"]))
    publish_id = map(str, response["data"]["publish_ids"])
    publish_ids = ','.join(publish_id)
    merchant_check_url = CMS_PUB_HOST + '/publish/publish-results?pids=%s&sid=%s&t=publish' % (
        publish_ids, shop_id)
    print('上货链接', merchant_check_url)
    return merchant_check_url


def cms_account(CMS_HOST, cms_number, cms_password):
    """查找账号下的token
    """
    login_url = CMS_HOST + '/auth/login'
    login_body = {"mobile": str(cms_number), "password": str(cms_password), "login_way": "mobile"}
    response = requests.post(login_url, json=login_body)
    account_url = CMS_HOST + '/user/account/login'
    account_body = {"account_id": response.json()['data']['last_login_account']}
    headers = {}
    headers['authorization'] = 'Bearer ' + response.json()['data']['access_token']
    res = requests.post(account_url, json=account_body, headers=headers)
    token = res.json()['data']['access_token']
    cms_account_id = response.json()['data']['last_login_account']
    return token, cms_account_id


def select_detail(code):
    """根据货号查找详情页ID，
     :return: 随机返回一个详情页ID,因为上货只支持一个详情页模板
    """
    templates_id_list = []
    code = urllib.parse.quote(code)
    details_url = CMS_HOST + '/merchant/v2/details_list?page=1&per_page=10&codes=%s' % code
    response = requests.get(url=details_url, headers=headers_cms).json()
    if response["data"]["total"] != 1:
        raise Exception('详情页列表搜索到多个商品，查找详情页模板数据冗余', code, response["data"]["total"])
    # print('详情页列表',response["data"]["results"])
    for templates_data in response["data"]["results"]:
        for templates in templates_data['templates']:
            for items_data in templates['items']:
                # print('详情页列表', items_data['id'])
                templates_id_list.append(items_data['id'])

    print('详情页列表', templates_id_list)
    templates_id = random.choice(templates_id_list)
    print('随机取详情页', templates_id)
    return templates_id


product_list_data = {}
product_list = {}
product_tps = {}


def search_publish(merchant_number, page=1, per_page=20):
    # 批量搜索商品
    product_list = {}
    product_list_data["product_overview"] = list()
    while 1:
        merchant_number = urllib.parse.quote(merchant_number)
        shop_url = CMS_HOST + '/merchant/v2/products/overview?page=%s&per_page=%s&codes=%s' % (page, per_page,
                                                                                               merchant_number)
        response = requests.get(url=shop_url, headers=headers_cms).json()
        for product_overview in response["data"]["product_overview"]:
            product_list[product_overview["product"]["id"]] = product_overview["product"]["code"]
            # 商品制作了详情页
            if product_overview["detail_status"] == 'made':
                templates_id = select_detail(product_overview["product"]["code"])
                product_list_data["product_overview"].append((
                    {
                        'product_id': product_overview["product"]["id"],
                        'path': (product_overview["product"]["category_path"]),
                        'publish_shops': product_overview["publish_shops"],
                        'templates_id': templates_id,
                    }))
            else:
                product_list_data["product_overview"].append((
                    {
                        'product_id': product_overview["product"]["id"],
                        'path': (product_overview["product"]["category_path"]),
                        'publish_shops': product_overview["publish_shops"],
                        'templates_id': '',
                    }))
        if (page * per_page) > response["data"]["total"]:
            break
        else:
            page += 1
    if len(product_list) == 0:
        raise Exception('未搜索到商品', merchant_number)
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
    return cms_number, cms_password, CMS_HOST, CMS_PUB_HOST


def select_brand(tp_name, shop_name, brand_name):
    """查找店铺和品牌
     :return: 店铺id和品牌id：shop["id"], shop["shop_id"]
    """
    brand_id = ''
    shop_url = CMS_HOST + '/merchant/shop/personal-center'
    response = requests.get(url=shop_url, headers=headers_cms).json()
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
        return str(brand_id), str(shop_id)


def select_brand_dict():
    """生成按照平台级别，男装女装级别，生成店铺的字典
    """
    shop_data_dict = {}
    shop_url = CMS_HOST + '/merchant/shop/personal-center'
    response = requests.get(url=shop_url, headers=headers_cms).json()
    for shop_data in response["data"]:
        shop_data_dict[shop_data['name']] = {}
        # 判断平台下没有店铺的情况
        if shop_data["shops"]:
            for shops in shop_data["shops"]:
                for brand in shops["brands"]:
                    # 天猫
                    if brand['name'] == '伊木子' and brand['tp_id'] == 1001:
                        shop_data_dict[shop_data['name']].update({
                            '女装': {'shop_name': shops['name'], 'brand_name': brand['name']},
                            '男装': {'shop_name': shops['name'], 'brand_name': brand['name']}
                        })
                    elif brand['name'] == 'pureborn/博睿恩' and brand['tp_id'] == 1001:
                        shop_data_dict[shop_data['name']].update({
                            '童装': {'shop_name': shops['name'], 'brand_name': brand['name']},
                        })
                    elif brand['name'] == 'ZHUCHONGYUN' and brand['tp_id'] == 1001:
                        shop_data_dict[shop_data['name']].update({
                            '女鞋': {'shop_name': shops['name'], 'brand_name': brand['name']},
                            # '服饰配件': {'shop_name': shops['name'], 'brand_name': brand['name']},
                        })
                    elif brand['name'] == 'Mark Fairwhale/马克华菲' and brand['tp_id'] == 1001:
                        shop_data_dict[shop_data['name']].update({
                            '服饰配件': {'shop_name': shops['name'], 'brand_name': brand['name']},
                        })
                    elif brand['name'] == 'DESCENTE/迪桑特' and brand['tp_id'] == 1001:
                        shop_data_dict[shop_data['name']].update({
                            '运动鞋': {'shop_name': shops['name'], 'brand_name': brand['name']},
                            '运动/瑜伽': {'shop_name': shops['name'], 'brand_name': brand['name']},
                            '运动包': {'shop_name': shops['name'], 'brand_name': brand['name']},
                        })
                    elif brand['name'] == '拓路者（服饰）' and brand['tp_id'] == 1001:
                        shop_data_dict[shop_data['name']].update({
                            '运动服': {'shop_name': shops['name'], 'brand_name': brand['name']},
                            '儿童配饰': {'shop_name': shops['name'], 'brand_name': brand['name']},
                            '户外服装': {'shop_name': shops['name'], 'brand_name': brand['name']},
                        })
                    elif brand['name'] == 'bossini.X' and brand['tp_id'] == 1001:
                        shop_data_dict[shop_data['name']].update({
                            '男鞋': {'shop_name': shops['name'], 'brand_name': brand['name']}
                        })
                    # 淘宝
                    elif 'other/其他' in brand['name'] and brand['tp_id'] == 1000:
                        shop_data_dict[shop_data['name']].update({
                            '女装': {'shop_name': shops['name'], 'brand_name': brand['name']},
                            '童装': {'shop_name': shops['name'], 'brand_name': brand['name']},
                            '女鞋': {'shop_name': shops['name'], 'brand_name': brand['name']},
                            '服饰配件': {'shop_name': shops['name'], 'brand_name': brand['name']},
                            '儿童配饰': {'shop_name': shops['name'], 'brand_name': brand['name']},
                        })
                    elif brand['name'] == '004' and brand['tp_id'] == 1000:
                        shop_data_dict[shop_data['name']].update({
                            '男装': {'shop_name': shops['name'], 'brand_name': brand['name']},
                        })
                    # 京东
                    # 京东蓝地店铺，不用了,修改为堡狮龙服饰旗舰店
                    elif brand['name'] == '堡狮龙（bossini）' and brand['tp_id'] == 1003:
                        shop_data_dict[shop_data['name']].update({
                            '女装': {'shop_name': shops['name'], 'brand_name': brand['name']},
                            '童装': {'shop_name': shops['name'], 'brand_name': brand['name']},
                            '儿童配饰': {'shop_name': shops['name'], 'brand_name': brand['name']},
                        })
                    elif brand['name'] == '半墨' and brand['tp_id'] == 1003:
                        shop_data_dict[shop_data['name']].update({
                            '男装': {'shop_name': shops['name'], 'brand_name': brand['name']},
                        })
                    # 安奈儿店铺，客户不给用，删除掉，修改为堡狮龙店铺
                    # elif brand['name'] == '安奈儿（Annil）' and brand['tp_id'] == 1003:
                    #     shop_data_dict[shop_data['name']].update({
                    #         '童装': {'shop_name': shops['name'], 'brand_name': brand['name']},
                    #         '儿童配饰': {'shop_name': shops['name'], 'brand_name': brand['name']},
                    #     })
                    # 京东班尼路店铺，不用了,修改为堡狮龙服饰旗舰店
                    # elif brand['name'] == 'bossini kids' and brand['tp_id'] == 1003:
                    #     shop_data_dict[shop_data['name']].update({
                    #         '童装': {'shop_name': shops['name'], 'brand_name': brand['name']},
                    #     })
                    elif brand['name'] == '迪桑特（DESCENTE）' and brand['tp_id'] == 1003:
                        shop_data_dict[shop_data['name']].update({
                            '儿童配饰': {'shop_name': shops['name'], 'brand_name': brand['name']},
                            '运动服/休闲服装': {'shop_name': shops['name'], 'brand_name': brand['name']},
                            '运动鞋': {'shop_name': shops['name'], 'brand_name': brand['name']},
                            '运动包': {'shop_name': shops['name'], 'brand_name': brand['name']},
                            '户外服装': {'shop_name': shops['name'], 'brand_name': brand['name']},
                        })
                    # 拼多多
                    elif '蜜胜' in brand['name'] and brand['tp_id'] == 1004:
                        shop_data_dict[shop_data['name']].update({
                            '女装': {'shop_name': shops['name'], 'brand_name': brand['name']},
                            '男装': {'shop_name': shops['name'], 'brand_name': brand['name']},
                            '童装': {'shop_name': shops['name'], 'brand_name': brand['name']}
                        })
                    # 唯品会
                    elif brand['name'] == 'LANDI' and brand['tp_id'] == 1005:
                        shop_data_dict[shop_data['name']].update({
                            '女装': {'shop_name': shops['name'], 'brand_name': brand['name']},
                        })
                    # 唯品会，班尼路店铺不能用了
                    # elif brand['name'] == '班尼路' and brand['tp_id'] == 1005:
                    #     shop_data_dict[shop_data['name']].update({
                    #         '男装': {'shop_name': shops['name'], 'brand_name': brand['name']},
                    #     })
                    # elif brand['name'] == 'BALENO JUNIOR' and brand['tp_id'] == 1005:
                    #     shop_data_dict[shop_data['name']].update({
                    #         '童装': {'shop_name': shops['name'], 'brand_name': brand['name']},
                    #     })
                    elif brand['name'] == '安奈儿' and brand['tp_id'] == 1005:
                        shop_data_dict[shop_data['name']].update({
                                '童装': {'shop_name': shops['name'], 'brand_name': brand['name']},
                            })
                    elif brand['name'] == '堡狮龙' and brand['tp_id'] == 1005:
                        shop_data_dict[shop_data['name']].update({
                            '儿童配饰': {'shop_name': shops['name'], 'brand_name': brand['name']},
                        })
                    # 有赞
                    elif brand['name'] == 'JR' and brand['tp_id'] == 1006:
                        shop_data_dict[shop_data['name']].update({
                            '女装': {'shop_name': shops['name'], 'brand_name': brand['name']},
                            '男装': {'shop_name': shops['name'], 'brand_name': brand['name']},
                            '童装': {'shop_name': shops['name'], 'brand_name': brand['name']}
                        })
                    # 快手
                    elif brand['name'] == '三彩' and brand['tp_id'] == 1008:
                        shop_data_dict[shop_data['name']].update({
                            '女装': {'shop_name': shops['name'], 'brand_name': brand['name']},
                            '男装': {'shop_name': shops['name'], 'brand_name': brand['name']},
                            '童装': {'shop_name': shops['name'], 'brand_name': brand['name']}
                        })
                    # 京东自营
                    elif brand['name'] == '班尼路（Baleno）' and brand['tp_id'] == 1010:
                        shop_data_dict[shop_data['name']].update({
                            '女装': {'shop_name': shops['name'], 'brand_name': brand['name']},
                            '男装': {'shop_name': shops['name'], 'brand_name': brand['name']},
                            '童装': {'shop_name': shops['name'], 'brand_name': brand['name']}
                        })
                    # 爱库存
                    # 广州友谊班尼路服饰有限公司 授权已经过期，先去掉
                    # elif brand['name'] == '班尼路Baleno' and brand['tp_id'] == 1011:
                    #     shop_data_dict[shop_data['name']].update({
                    #         '女装': {'shop_name': shops['name'], 'brand_name': brand['name']},
                    #         '男装': {'shop_name': shops['name'], 'brand_name': brand['name']},
                    #         '童装': {'shop_name': shops['name'], 'brand_name': brand['name']}
                    #     })
                    elif brand['name'] == '安奈儿annil' and brand['tp_id'] == 1011:
                        shop_data_dict[shop_data['name']].update({
                            '童装': {'shop_name': shops['name'], 'brand_name': brand['name']},
                            '儿童配饰': {'shop_name': shops['name'], 'brand_name': brand['name']},
                            '童鞋': {'shop_name': shops['name'], 'brand_name': brand['name']}
                        })
                    # 抖音
                    elif brand['name'] == 'GXG' and brand['tp_id'] == 1012:
                        shop_data_dict[shop_data['name']].update({
                            '女装': {'shop_name': shops['name'], 'brand_name': brand['name']},
                        })
                    # 堡狮龙休闲服饰店，没有后台测试账号，先不管
                    elif brand['name'] == '堡狮龙' and brand['tp_id'] == 1012:
                        shop_data_dict[shop_data['name']].update({
                            '童装': {'shop_name': shops['name'], 'brand_name': brand['name']},
                        })
                    # 1688
                    elif brand['name'] == 'diff' and brand['tp_id'] == 1013:
                        shop_data_dict[shop_data['name']].update({
                            '女装': {'shop_name': shops['name'], 'brand_name': brand['name']},
                            '男装': {'shop_name': shops['name'], 'brand_name': brand['name']},
                            '童装': {'shop_name': shops['name'], 'brand_name': brand['name']}
                        })
                    # 小红书
                    elif brand['name'] == 'simple pieces' and brand['tp_id'] == 1015:
                        shop_data_dict[shop_data['name']].update({
                            '女装': {'shop_name': shops['name'], 'brand_name': brand['name']},
                        })
                    # 驿氪
                    elif brand['name'] == '外购产品' and brand['tp_id'] == 1016:
                        shop_data_dict[shop_data['name']].update({
                            '女装': {'shop_name': shops['name'], 'brand_name': brand['name']},
                            '男装': {'shop_name': shops['name'], 'brand_name': brand['name']},
                            '服饰配件': {'shop_name': shops['name'], 'brand_name': brand['name']},
                        })
        # 删除字典中value为空的键值对
        if not shop_data_dict.get(shop_data['name']):
            del shop_data_dict[shop_data['name']]
    print(shop_data_dict)
    return shop_data_dict


def search_product_list(product_list_data, path, tp_name, shop_name):
    # 过滤每个商品的信息
    product_id_list = []
    product_id_data = {}
    if product_list_data:
        for product_id, data_value in product_list_data.items():
            for data in data_value:
                if path in data['path']:
                    for publish_shop in data['publish_shops']:
                        # 查找商品，到店铺是：未上货，状态，
                        if publish_shop['tp_name'] == tp_name and publish_shop['shop_name'] == shop_name and \
                                publish_shop['status'] == 'unpublished':
                            print('查找到', data['product_id'])
                            product_id_list.append(data['product_id'])
                            product_id_data[data['product_id']] = data['templates_id']
                else:
                    continue
    # return product_id_list
    return product_id_data


if __name__ == '__main__':
    # 得物，不处理
    # 淘宝型号问题，不处理
    # 店铺未授权的情况，不处理
    # 唯品会多色多详情页，不处理
    # prefix = '0112GZgirl161939'
    # HOST = 'qa'
    # Version = '3.0'
    prefix = sys.argv[1]
    HOST = sys.argv[2]
    Version = sys.argv[3]
    sale_status = sys.argv[4]

    cms_number, cms_password, CMS_HOST, CMS_PUB_HOST = host(HOST, Version)
    CMS_token, CMS_account_id = cms_account(CMS_HOST, cms_number, cms_password)
    headers_cms = {}
    headers_cms['authorization'] = 'Bearer ' + CMS_token

    product_list_data, product_lists = search_publish(prefix)
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
            product_id_data = search_product_list(product_list_data, gender, tp_name,
                                                  shop_data[tp_name][gender]['shop_name'])
            if len(product_id_data) != 0:
                brand_id, shop_id = select_brand(tp_name, shop_data[tp_name][gender]['shop_name'],
                                                 shop_data[tp_name][gender]['brand_name'])
                batch_info_id = batch_info(shop_id, tp_name)
                if tp_name == '驿氪':
                    code = category_code(shop_id)
                else:
                    code = ''
                print(product_id_data)
                merchant_check_url = merchant_publishs_tm(product_id_data, brand_id, shop_id, batch_info_id, code, tp_name, sale_status)
                merchant_check_url_dict[
                    tp_name + '_' + shop_data[tp_name][gender]['shop_name'] + '_' + gender] = merchant_check_url
            # product_id_list = search_product_list(product_list_data, gender, tp_name, shop_data[tp_name][gender]['shop_name'])
            # print(product_id_list)
            # if len(product_id_list) != 0:
            #     brand_id, shop_id = select_brand(tp_name, shop_data[tp_name][gender]['shop_name'], shop_data[tp_name][gender]['brand_name'])
            #     batch_info_id = batch_info(shop_id, tp_name)
            #     merchant_check_url = merchant_publishs_tm(product_id_list, brand_id, shop_id, batch_info_id, tp_name)
            #     merchant_check_url_dict[tp_name + '_' + shop_data[tp_name][gender]['shop_name'] + '_' + gender] = merchant_check_url

    if merchant_check_url_dict:
        WX_del_HOOK = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=24692f61-7f4f-41f4-a4df-57b9b4660a57'
        project = '批量上货链接'
        start_time = time.strftime("%m%dT%H:%M:%S", time.localtime())
        total = len(product_lists)
        mess = wechatRebot_send().test_robot_bak(WX_del_HOOK, project, start_time, prefix, total,
                                                 merchant_check_url_dict)
