# DangDang  sdk
import hashlib
import requests
import logging
from datetime import datetime, timedelta

from et_xmlfile import xmlfile

from exceptions import OpenApiError
from urllib.parse import urlencode
from tools import DictToXml, XmlToDict

DangDang_url = "https://gw-api.dangdang.com/openapi/rest?"

DangDangError = "dangdang_api_error"
XMLERRORFORMAT = "xml输入格式错误, 只能有单一最外层"
XMLERRORKEY = "xml输入格式错误, 键值不能为数字"


class DangDangAPi():
    Post = "post"
    Get = "get"

    def __init__(self, app_key, app_secret, access_token):
        self.app_key = app_key
        self.app_secret = app_secret
        self.access_token = access_token

    def build_system_args(self, method, v):
        system_args = {
            "method": method,  # 接口
            "timestamp": (datetime.utcnow() + timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S"),  # 时间戳
            "format": "xml",  # 返回格式
            "app_key": self.app_key,  # appkey
            "v": v,  # 版本
            "sign_method": "md5",  # 加密方式
            "session": self.access_token,  # 用户授权
        }
        system_args["sign"] = self.system_args_sgin(system_args)
        return system_args

    def system_args_sgin(self, args: dict):
        args_list = sorted(args.items(), key=lambda x: x[0])  # 排序
        sign_text = ""
        for x in args_list:
            sign_text = "{}{}{}".format(sign_text, x[0], x[1])
        sign_text = "{}{}{}".format(self.app_secret, sign_text, self.app_secret)
        hl = hashlib.md5()
        hl.update(sign_text.encode(encoding="utf-8"))
        return hl.hexdigest().upper()

    def send(self, method, apiName, v, params=None, data=None, file=None, _transport=True):
        request_arge = self.build_system_args(apiName, v)   # 初始化系统参数，并签名
        # if xmlfile:
        #     file = DictToXml(xmlfile).transport().encode()  # 字典数据转化为xml byte
        # params = {
        #     # "datatype":8990,
        #     # "name" : "测试"
        #     'it' : 11176029466
        # }
        if params:
            request_arge.update(params)     # 接口url参数添加
        data = DictToXml(data).transport() if data else None
        file = self.tempfile(file) if file else None
        req = self.sendRequest(method, data, request_arge, file)    # _transport 指是否转还为json
        if not _transport: return req
        else:
            # 解码格式不确定
            try:
                str_xml = req.decode()
            except Exception:
                str_xml = req.decode("GBK")
            request_data = XmlToDict(str_xml).transport()
        return request_data

    def sendRequest(self, method, data, request_arge, file):
        url = DangDang_url + urlencode(request_arge)
        try:
            if method == self.Get:
                resp = requests.get(url=url)
            else:
                resp = requests.post(url=url, data=data, files=file)
            logging.info(f"当当请求{url},方法{method},参数{data}，返回{resp.content}")
            print(f"当当请求 {url},方法 {method},参数 {data}，返回 {resp.content}")
            if resp.status_code != 200:
                raise OpenApiError(error_code=DangDangError, error_msg=f"接口调用失败: {resp.content}")
            else:
                return resp.content
        except Exception as e:
            raise OpenApiError(error_code=DangDangError, error_msg=str(e))




if __name__ == "__main__":
    DangDang_APP_KEY = "2100009643"
    DangDang_APP_SECRET = "54F12C7FA3115A6BE66A1BB2DBAA78DE"
    t = DangDangAPi(DangDang_APP_KEY, DangDang_APP_SECRET, "E5DC29D15647874342FDEC22D1B6AD4C6251F9744F65EFCFB84EA943BAC96908")
    # z = t.send(DangDangAPi.Get, "dangdang.items.list.get", "2.0")
    params = {
        # "datatype":8990,
        # "name" : "测试"
        'it': 11176029466
    }
    z = t.send(DangDangAPi.Get, "dangdang.item.get", "2.0",params)
    # z2 = t.send(DangDangAPi.Get,"dangdang.items.delete")
    print(z)