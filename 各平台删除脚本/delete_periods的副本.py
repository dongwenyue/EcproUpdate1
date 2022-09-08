# -*- coding: utf-8 -*-
"""
@time 2020-1-25
@author: yzm
"""
import xlrd
import os
import time
import requests
import hashlib
import datetime
import re
import sys
import argparse
import json
import xlwt
import random
import urllib.parse
from selenium import webdriver

def read_url_get(code_url):
    response_2 = requests.get(url=code_url, headers=headers).json()
    response_str = str(response_2)
    return response_str


def read_url_delete_json(code_url, data):
    response2 = requests.delete(url=code_url, headers=headers, json=data).json()
    response_str = str(response2)
    return response_str

product_list = {}
def search(page=1, per_page=10, count = None):
    """搜索出期数下包含几款商品
     :return:product的字典，product id和期数名称和备注，期数名称和备注暂时用不是，只是为了查看方便
    """
    shop_url = CMS_HOST + '/merchant/v2/period?page=%s&per_page=%s' % (page, per_page)
    response = read_url_get(shop_url)
    response = eval(response)
    for product_overview in response["data"]["results"]:
        if product_overview["count"] == count:
            print("商品的期数id", product_overview["id"])
            print("商品的期数和备注", product_overview["period"], product_overview["period_describe"])
            product_list[product_overview["id"]] = (product_overview["period"], product_overview["period_describe"])
    if (page * per_page) - response["data"]["total"] < 0:
        search(page + 1, per_page, count)
    return product_list


def delete_period(product_list):
    """删除期数，期数下还有0款商品，若期数被删除，此0款商品的数据会被一起放入回收站，15天后自动清除，请谨慎选择
    """
    for product, name in product_list.items():
        time.sleep(0.1)
        print("删除期数", product, name)
        period_url = CMS_HOST + "/merchant/v2/period"
        data = {"periods": [product]}
        print("删除期数的报文：", data)
        response = read_url_delete_json(period_url, data=data)
        response = eval(response)
        print(response)
        if response['message'] == 'Success':
            print('删除成功')
        else:
            print('删除失败')


def cms_account(CMS_HOST, cms_number, cms_password):
    """查找账号下的token
    """
    # 获取access_token和account_id
    login_url = CMS_HOST + '/auth/login'
    login_body = {"mobile":str(cms_number),"password":str(cms_password),"login_way":"mobile"}
    print(login_body)
    response = requests.post(login_url,json=login_body)
    # print(response.json()['data']['access_token'],response.json()['data']['last_login_account'])
    print(response.json()['data']['last_login_account'])

    # 获取token
    account_url = CMS_HOST + '/user/account/login'
    account_body = {"account_id": response.json()['data']['last_login_account']}
    headers = {}
    headers['authorization'] = 'Bearer '+ response.json()['data']['access_token']
    res = requests.post(account_url, json=account_body, headers=headers)
    # print(res.json()['data']['access_token'])
    token = res.json()['data']['access_token']
    cms_account_id = response.json()['data']['last_login_account']
    print(token)
    return token, cms_account_id


if __name__ == '__main__':
    HOST = 'qa'
    count = 4

    if HOST == 'qa':
        cms_number = 18617847474
        cms_password = 'lf18617847474'
        CMS_HOST = 'https://cms-qa-api.ecpro.com'
    elif HOST == 'dev':
        cms_number = 18617847474
        cms_password = '18617847474'
        CMS_HOST = 'https://cms-dev-api.ecpro.com'
    elif HOST == 'on':
        cms_number = 18612210007
        cms_password = '18612210007'
        CMS_HOST = 'https://cms-api.ecpro.com'
    CMS_token, CMS_account_id= cms_account(CMS_HOST, cms_number, cms_password)
    headers = {}
    headers['authorization'] = 'Bearer ' + CMS_token
    product_lists = search(page=1, per_page=40, count=count)
    print(product_list)
    print('搜索到', len(product_list), '款期数')
    print("分隔线-----------------------------------------------------------------------------------------------------")
    delete_period(product_lists)
