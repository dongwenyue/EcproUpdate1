# -*- coding: utf-8 -*-
"""
@time 2021-06-09
@author: yzm
@删除回收站所有的商品
"""
import requests
import urllib

def cms_account(CMS_HOST, cms_number, cms_password):
    """查找账号下的token"""
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

product_dict = {}
def search(merchant_number,page=1, per_page=40):
    """批量搜索，然后点击提交
    筛选出图片包：已上传 商品字段：已录入 资源图：未设置
     :return:product的字典，product id和货号，货号暂时用不是，只是为了查看方便
    """
    merchant_number = urllib.parse.quote(merchant_number)
    shop_url = CMS_HOST + '/merchant/v2/products/overview?page=%s&per_page=%s&codes=%s' % (page, per_page, merchant_number)
    response =  requests.get(url=shop_url,headers=headers_cms)
    response = response.json()
    for product_overview in response["data"]["product_overview"]:
        product_dict[product_overview["product"]["id"]] = product_overview["product"]["code"]
    if (page * per_page) - response["data"]["total"] < 0:
        search(merchant_number, page + 1, per_page)
    return product_dict


def dele_product(id):
    '''批量永久删除'''
    url = CMS_HOST + '/merchant/v2/products'
    body = {"source":"overview","product_ids":id ,}
    print(body)
    res = requests.delete(url,  headers=headers_cms, json=body)
    print(res.json())
    if res.json()['message'] == "Success":
        print('删除成功, 并放到回收站')
    else:
        print('删除失败')


if __name__ == '__main__':
    codes = '0928'
    HOST = 'qa'
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
    CMS_token, CMS_account_id = cms_account(CMS_HOST, cms_number, cms_password)
    headers_cms = {}
    headers_cms['authorization'] = 'Bearer ' + CMS_token

    product_dicts = search(codes)
    print('搜索到', len(product_dicts), '款商品')
    data_list = []
    for k, v in product_dicts.items():
        print(k,v)
        data_list.append(k)
    dele_product(data_list)


