# DangDang  sdk
import hashlib
import requests
import logging
from datetime import datetime, timedelta

from et_xmlfile import xmlfile

from urllib.parse import urlencode
from xml.dom.minidom import Document
from xml.dom.minidom import parseString

DangDang_url = "https://gw-api.dangdang.com/openapi/rest?"

DangDangError = "dangdang_api_error"
XMLERRORFORMAT = "xml输入格式错误, 只能有单一最外层"
XMLERRORKEY = "xml输入格式错误, 键值不能为数字"

XMLERROR = "xml_error"
XMLERRORFORMAT = "xml输入格式错误, 只能有单一最外层"
XMLERRORKEY = "xml输入格式错误, 键值不能为数字"

import time

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


class DictToXml():
    def __init__(self, data):
        self.Rnode = Document()
        if len(data) > 1:
            raise OpenApiError(error_code=XMLERROR, error_msg=XMLERRORFORMAT)
        self.data = data
        self.cdata_map = {
            "<": "&lt;",
            ">": "&gt;",
            "&": "&amp;",
        }

    def transport(self):
        return self._transport(self.Rnode, self.data)

    def _transport(self, this_node, data, Attribute=None):
        for key, value in data.items():
            if isinstance(value, str):
                self.set_node_StrValue(this_node, key, value, Attribute)
            elif isinstance(value, list):
                self.set_node_ListValue(this_node, key, value, Attribute)
            elif isinstance(value, dict):
                self.set_node_DictValue(this_node, key, value, Attribute)
            else:
                raise OpenApiError(error_code=XMLERROR, error_msg="未知格式")

        return self.Rnode.toprettyxml(indent="", newl="")

    def set_node_StrValue(self, this_node, key, value: str, Attribute: dict = None):
        _node = self.Rnode.createElement(key)
        this_node.appendChild(_node)
        if Attribute:
            for AttributeKey, AttributeValue in Attribute.items():
                _node.setAttribute(AttributeKey, AttributeValue)
        else:
            value = self.CDATA(str(value))
            _value = self.Rnode.createTextNode(str(value))
            _node.appendChild(_value)
        return _node

    def CDATA(self, value):
        for x, y in self.cdata_map.items():
            value = value.replace(x, y)
        return value

    def set_node_DictValue(self, this_node, key, value: dict, Attribute: dict = None):
        NextNode = self.Rnode.createElement(key)
        this_node.appendChild(NextNode)
        self._transport(NextNode, value, Attribute)

    def set_node_ListValue(self, this_node, key, value: list, Attribute: dict = None):
        for V in value:
            if isinstance(V, str):
                self.set_node_StrValue(this_node, key, V, Attribute)
            elif isinstance(V, list):
                self.set_node_ListValue(this_node, key, V, Attribute)
            elif isinstance(V, dict):
                self.set_node_DictValue(this_node, key, V, Attribute)
        return this_node


class XmlToDict():
    def __init__(self, xml):
        self.xml = xml
        self.data = {}
        self.dom = parseString(self.xml)

    def transport(self):
        rootNode = self.dom.documentElement  # 获取根节点
        key = rootNode.localName
        return {key: self._transport(rootNode)}

    def _transport(self, Node):
        res = {}
        for cNode in Node.childNodes:
            if not hasattr(cNode, "tagName"): continue
            key = cNode.tagName
            if len(cNode.childNodes) == 1 and cNode.childNodes[0].nodeType in (3, 4):
                # 只有唯一节点，且唯一节点为文字节点 真节点 - 文字
                self.setValue(res, key, cNode.childNodes[0].data)
            else:
                KV = self._transport(cNode)
                self.setValue(res, key, KV)
        return res

    def setValue(self, P_data, key, value):
        # 设定值
        if key not in P_data:
            P_data[key] = value
        elif key in P_data and isinstance(P_data[key], list):
            P_data[key].append(value)
        elif key in P_data and (isinstance(P_data[key], dict) or isinstance(P_data[key], str)):
            P_data[key] = [P_data[key]]
            P_data[key].append(value)
        return P_data


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
        request_arge = self.build_system_args(apiName, v)  # 初始化系统参数，并签名
        # if xmlfile:
        #     file = DictToXml(xmlfile).transport().encode()  # 字典数据转化为xml byte
        if params:
            request_arge.update(params)  # 接口url参数添加
        data = DictToXml(data).transport() if data else None
        file = self.tempfile(file) if file else None
        req = self.sendRequest(method, data, request_arge, file)  # _transport 指是否转还为json
        if not _transport:
            return req
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
    props_list = {}
    pageSize = 20
    P = 1
    while 1:
        params = {
            "datatype": 8990,
            "its": 9999,
            "pageSize": pageSize,
            "P": P,
            "name": "测试"
        }
        request_data = t.send(DangDangAPi.Get, "dangdang.items.list.get", "2.0", params)
        print(request_data)
        if len(request_data['response']['ItemsList']) < 1:
            raise Exception ("未搜索到测试商品")
        print(request_data['response']['ItemsList']['ItemInfo'])
        # 当搜索的时候，只有一个商品的时候，是字典类型
        if isinstance(request_data['response']['ItemsList']['ItemInfo'], dict):
            props_list[request_data['response']['ItemsList']['ItemInfo']['itemID']] = request_data['response']['ItemsList']['ItemInfo']['itemName']
        elif isinstance(request_data['response']['ItemsList']['ItemInfo'], list):
            for items in request_data['response']['ItemsList']['ItemInfo']:
                print('--->',items)
                print(items['itemID'], items['itemName'])
                props_list[items['itemID']] = items['itemName']

        if (P * pageSize) > int(request_data['response']['totalInfo']['itemsCount']):
            break
        else:
            P += 1
    print(props_list)

    # props_list = {'11176029466': '易尚货测试商品'}
    # params = {
    #     "it": 11176029466,
    # }
    # z2 = t.send(DangDangAPi.Get, "dangdang.items.delete", "2.0", params)
    # print(z2)

    succeed_list = []
    error_list = []
    for wareId, title in props_list.items():
        print(wareId)
        num = 1
        while 1:
            try:
                # raise Exception
                params = {
                    "it": int(wareId),
                }
                z2 = t.send(DangDangAPi.Get, "dangdang.items.delete", "2.0", params)
                print(z2)
                succeed_list.append(title)
            except:
                print('删除重试', wareId, num, '次')
                time.sleep(1)
                num += 1
                if num > 10:
                    print(wareId, num, '10次失败')
                    error_list.append(title)
                    break
            else:
                break
    print('所有失败', error_list)

    WX_del_HOOK = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=9e04f752-749b-49a9-854c-ab7c7127f3f8'
    project = '删除'
    start_time = time.strftime("%m%dT%H:%M:%S", time.localtime())
    name = '当当:18357967633 潘齐武'
    total = len(props_list)
    succeed_total = len(succeed_list)
    error_total = len(error_list)
    succeed_title = ", ".join([str(i) for i in succeed_list])
    failing_title = ", ".join([str(i) for i in error_list])
    mess = wechatRebot_send().test_robot(WX_del_HOOK, project, start_time, name, total, succeed_total, error_total,
                                         succeed_title, failing_title)