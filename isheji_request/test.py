import requests
from common.login import token
from config.file_puload_wenjian import file_upload
from common.path_config import jepg_path

'''供应商管理'''
# #供应商管理列表==========================msg
# # url = 'https://pic.wxbjq.top/api/providers'
# head = {
#     'content-type': 'application/json;charset=UTF-8',
#     "is_test": "1",
#     'x-token': f'{token}'
# }
# body = {
#     "contact_name" : "左艺轩"
# }
# res = requests.request(method='get', url=url, headers=head, data=body)
# print(res.json())


# #获取供应商列表============================================================msg
# url = 'https://pic.wxbjq.top/api/providers/list'
# head = {
#     'content-type': 'application/json;charset=UTF-8',
#     "is_test": "1",
#     'x-token': f'{token}'
# }
# body = {
#     "contact_name" : "左艺轩"
# }
# res = requests.request(method='get', url=url, headers=head, data=body)
# print(res.json())


# #创建供应商=============================================================================msg
# url = 'https://pic.wxbjq.top/api/providers'
# head = {
#     'content-type': 'application/x-www-form-urlencoded',
#     "is_test": "1",
#     'x-token': f'{token}'
# }
# body = {
#     "name": "自动化测试供应商全称",
#     "type": 3,
#     "status": 1,
#     "country": "自动化国家",
#     "province": "自动化省份",
#     "city": "自动化城市",
#     "district": "自动化区/县",
#     "location": "自动化详细地址",
#     "level": 1,
#     "contact_name": "自动化联系人姓名",
#     "contact_mobile": "13213213213"
# }
# res = requests.request(method='post', url=url, headers=head, data=body)
# print(res.json())


# # 查找某一个供应商=================================msg
# url = 'https://pic.wxbjq.top/api/providers/provider/7'
# head = {
#     'content-type': 'application/json;charset=UTF-8',
#     "is_test": "1",
#     'x-token': f'{token}'
# }
# body = {
#     "name": "自动化测试供应商全称",
#     "type": 3,
#     "status": 1,
#     "country": "自动化国家",
#     "province": "自动化省份",
#     "city": "自动化城市",
#     "district": "自动化区/县",
#     "location": "自动化详细地址",
#     "level": 1,
#     "contact_name": "自动化联系人姓名",
#     "contact_mobile": "13213213213"
# }
# res = requests.request(method='get', url=url, headers=head, data=body)
# print(res.json())


'''供应商采购单管理'''  # =========最后一个需要调取文件
# # 供应商采购单管理列表=================================================================================msg
# url = 'https://pic.wxbjq.top/api/provider/orders'
# head = {
#     'content-type': 'application/json;charset=UTF-8',
#     "is_test": "1",
#     'x-token': f'{token}'
# }
# body = {
#     "page": 1,
#     "page_size": 1,
# }
# res = requests.request(method='get', url=url, headers=head, json=body)
# print(res.json())


# # #获取供应商采购单列表==================================================================================msg
# url = 'https://pic.wxbjq.top/api/provider/orders/list'
# head = {
#     'content-type': 'application/json;charset=UTF-8',
#     "is_test": "1",
#     'x-token': f'{token}'
# }
# body = {
#     "page": 1,
#     "page_size": 1,
# }
# res = requests.request(method='get', url=url, headers=head, data=body)
# print(res.json())


# #创建供应商采购单=======================================================ok
# url = 'https://pic.wxbjq.top/api/provider/orders'
# head = {
#     'content-type': 'application/x-www-form-urlencoded',
#     "is_test": "1",
#     'x-token': f'{token}'
# }
# body = {
#     "provider_id": 4,
#     "license": 1,
#     "license_type": 1,
#     "license_scope": "1",
#     "asset_type": 1,
#     "graphical_style": 0,
#     "authorized_year": 10,
#     "authorized_month": 10,
#     "authorized_day": 10,
#     "sale_type": 3,
#     "single_price": 99,
#     "authorized_ids": "4",
#     "start_time": "2021-12-30 00:00:00",
#     "end_time": "2021-12-31 00:00:00",
#     "subject_name": "采购单批次的主题/名称",
#     "responsible_person": "采购负责人",
#     "status": 1,
#     "has_risk": 2,
#     "has_sample_pic": 1,
#     "upload_progress": 0,
#     "use_location": "1",
#     "pay_method": "{\"buytype\":\"1\",\"settlementType\":\"1\",\"divide_val\":\"0.5\",\"fixedPrice_val\":\"\",\"packyear_val\":\"\",\"singleDownload_val\":\"\",\"cycle\":\"1\",\"payType\":\"1\",\"advance_val\":3940,\"floor_val\":\"\",\"date\":\"26\"}"
# }
# res = requests.request(method='post', url=url, headers=head, data=body)
# print(res.json())


# #查找某个供应商采购单======================ok
# url = 'https://pic.wxbjq.top/api/provider/orders/order/2'
# head = {
#     "content-type": "application/json;charset=UTF-8",
#     "is_test": "1",
#     "x-token": f"{token}"
# }
# body = {}
# res = requests.request(method='get', url=url, headers=head, data=body)
# print(res.json())


# #上传供应商采购单附件================================================ok=====需要调取文件
# url = 'https://pic.wxbjq.top/api/provider/orders/attachment'
# head = {
#     'content-type': 'application/x-www-form-urlencoded',
#     "is_test": "1",
#     'x-token': f'{token}'
# }
# # with open(upload_po_attachment_path, mode='rt', encoding='utf-8') as file:
# #     file_upload = file.read()
# body = {
#     "id": 2,
#     "attachments": file_upload
# }
# res = requests.request(method='post', url=url, headers=head, data=body)
# print(res.json())


'''商用授权配置接口'''
# #新建授权项========================================================     msg==''
# url = 'https://pic.wxbjq.top/api/authorizes/new'
# head = {
#     "is_test": "1",
#     'x-token': f'{token}',
#     'content-type': 'application/json;charset=UTF-8'
# }
# body = {
#     "use_location": "自动化使用位置",
#     "usage": "自动化授权用途",
#     "detail": "自动化授权项"
# }
# res = requests.request(method='post', url=url, json=body, headers=head)
# print(res.json())


# #查看授权项===========ok
# url = 'https://pic.wxbjq.top/api/authorizes/edit/3'
# head = {
#     "is_test": "1",
#     "x-token": f"{token}",
#     'content-type': 'application/json;charset=UTF-8'
# }
# body = {}
# res = requests.request(method='get', url=url, json=body, headers=head)
# print(res.json())


# #授权项列表==============================================     msg==''
# a = "json"
# url = 'https://pic.wxbjq.top/api/authorizes'
# head = {
#     "is_test": "1",
#     'x-token': f'{token}',
#     'content-type': 'application/json;charset=UTF-8'
# }
# body = {}
# res = requests.request(method='get', url=url, json=body, headers=head)
# print(res.json())


# # 删除授权项=============================================
# url = 'https://pic.wxbjq.top/api/authorizes/delete/6'
# head = {
#     "is_test": "1",
#     'x-token': f'{token}',
#     'content-type': 'application/json;charset=UTF-8'
# }
# body = {}
# res = requests.request(method='post', url=url, json=body, headers=head)
# print(res.json())

# # 编辑授权项===============================================     msg == ''
# url = 'https://pic.wxbjq.top/api/authorizes/edit'
# head = {
#     "is_test": "1",
#     'x-token': f'{token}',
#     'content-type': 'application/json;charset=UTF-8'
# }
# body = {
#     "id": 56,
#     "use_location": "自动化使用位置",
#     "usage": "自动化授权用途",
#     "detail": "自动化授权项"
# }
# res = requests.request(method='post', url=url, json=body, headers=head)
# print(res.json())


'''图库数据接入'''  # ==========doing
# #素材站图片内容接口入库================================tod0============================================
# url = 'https://pic.wxbjq.top/api/import/material'
# head = {
#     "is_test": "1",
#     'x-token': f'{token}',
#     'content-type': 'application/x-www-form-urlencoded'
# }
# body = {
#     "source": "图库内部上传",
#     "isheji_id": "2435",
#     "files": "[{\"name\":\"33.jpg\",\"title\":\"124\",\"url\":\"https://file-test.isheji.com/common/images/20211223/upmlxomuqhxqlgdk.jpg\"}]",
# }
# res = requests.request(method='post', url=url, json=body, headers=head)
# print(res.json())


'''图片管理'''#====第一个暂缓
# # 图片内容库接口文档=============================================ok=======暂缓
# url = 'https://pic.wxbjq.top/api/images/oss'
# body = {}
# files = [
#     ('file', ('jepg.jpeg', open(f'{jepg_path}', 'rb'), 'image/jepg'))
# ]
# res = requests.request(method='post', url=url, data=body, files=files)
# print(res.json())

# # 图片列表=============================================msg == ''
# url = 'https://pic.wxbjq.top/api/images'
# head = {
#     "is_test": "1",
#     'x-token': f'{token}',
#     'content-type': 'application/json;charset=UTF-8'
# }
# body = {
#     "page": 1,
#     "page_size": 1
# }
# res = requests.request(method='get', url=url, data=body, headers=head)
# print(res.json())

# #通过爱设计id获取图片信息===================================================
# url = 'https://pic.wxbjq.top/api/images/isjid'
# head = {
#     "is_test": "1",
#     'x-token': f'{token}',
#     'content-type': 'application/json;charset=UTF-8'
# }
# body = {
#     "isheji_id": "ISJ015919823506"
# }
# res = requests.request(method='get', url=url, params=body, headers=head)
# print(res.text)


'''图片组管理'''
#创建图片组======================================ok=========================
url = 'https://pic.wxbjq.top/api/image/groups'
head = {
    "is_test": "1",
    'x-token': f'{token}',
    'content-type': 'application/x-www-form-urlencoded'
}
body = {
    "name": "图片租名称",
    "sort": 3
}
res = requests.request(method='post', url=url, params=body, headers=head)
print(res.text)

# #获取图片组====================ok=================
# url = 'https://pic.wxbjq.top/api/image/groups'
# head = {
#     "is_test": "1",
#     'x-token': f'{token}',
#     'content-type': 'application/x-www-form-urlencoded'
# }
# body = {}
# res = requests.request(method='get', url=url, headers=head, json=body)
# print(res.json())


'''运营内部上传管理'''
# # 内部图片上传入口（运营内部上传管理）新建图片上传===================ok==========
# url = 'https://pic.wxbjq.top/api/image/uploads'
# body = {
#     "provider_id": 4,
#     "order_id": 7,
#     "upload_method": 2,
#     "files": "[{\"name\":\"33.jpg\",\"title\":\"124\",\"url\":\"https://file-test.isheji.com/common/images/20211223/upmlxomuqhxqlgdk.jpg\"}]",
#     "image_group_id": 0
# }
# head = {
#     "is_test": "1",
#     'x-token': f'{token}'
# }
# res = requests.request(method='post', url=url, data=body, headers=head)
# print(res.json())

# # 查询上传记录======================================================ok======
# url = 'https://pic.wxbjq.top/api/image/uploads'
# head = {
#     'content-type': 'application/json;charset=UTF-8',
#     "is_test": "1",
#     'x-token': f'{token}'
# }
# body = {
#     "page":1,
#     "page_size": 1,
#     "user_name": "左艺轩",
#     "is_test": "1"
# }
# res = requests.request(method='get', url=url, headers=head, data=body)
# print(res.json())


'''用户管理'''
# #登出
# url = 'https://pic.wxbjq.top/api/user/logout'
# head = {
#     "is_test": "1",
#     'x-token': f'{token}'
# }
# body = {}
# res = requests.request(method='post', url=url, data=body, headers=head)
# print(res.json())

# #获取当前用户信息
# url = 'https://pic.wxbjq.top/api/user/info'
# head = {
#     "is_test": "1",
#     'x-token': f'{token}'
# }
# body = {}
# res = requests.request(method='get', url=url, data=body, headers=head)
# print(res.json())