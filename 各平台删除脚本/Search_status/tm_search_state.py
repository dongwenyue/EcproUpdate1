# -*- coding: utf-8 -*-
import datetime
import json
from tm_API import *


class TMallAPP(APP):
    def taobao_item_seller_get(self, token, methods, num_iid):
        param = {
            'fields': 'title,num_iid,approve_status',
            'num_iid': num_iid,
        }
        response = self.tp_api(token, methods, param)
        json_response = json.loads(response)
        response_key = 'item_seller_get_response'
        props_name = json_response[response_key]['item']['approve_status']
        print(props_name)



if __name__ == '__main__':
    app_key = '27727487'
    app_secret = '7c17ec2e103c7f6d786468ff8a3ce1e5'
    # 男装&女装,伊木子旗舰店99
    TM_TOKEN = '62002222266396f4b5d22c4a1f1471ZZ746046cd9d648fd436157429'
    num_iid = '677744040064'
    methods = 'taobao.item.seller.get'
    tmall_app = TMallAPP(app_key, app_secret)
    tm_props_dist = tmall_app.taobao_item_seller_get(TM_TOKEN, methods, num_iid)
