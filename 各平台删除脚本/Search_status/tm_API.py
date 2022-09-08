import hashlib
import os
import urllib
import datetime
import time
import urllib.parse
import urllib.request
import  requests

"""
urllib.request 打开或请求url
urllib.error 捕获处理请求时产生的异常
urllib.parse 解析url
urllib.robotparser 用于解析robots.txt文件
"""

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