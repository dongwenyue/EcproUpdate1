import json
import unittest
import requests
from decimal import Decimal
from jsonpath import jsonpath
from common.login import login
from common.readlog import Log
from common.read_yaml import api_url
from unittestreport import ddt, list_data
from config.file_puload_wenjian import file_upload
hao'qi
from common.path_config import suplier_xlsx
from common.zip_excel import get_sheet_velus


values = get_sheet_velus(suplier_xlsx, 'Sheet1')
# print(values)

@ddt
class TestRecharge(unittest.TestCase):
    log = Log(__name__)
    logger = log.getLog()

    @classmethod
    def setUpClass(cls) -> None:
        cls.login = login()

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    @list_data(values)
    def testrecharge(self, values_info):
        url = api_url + values_info['url']
        method = values_info['method']
        head = values_info['headers']
        body = values_info['data']
        if "#token#" in values_info['headers']:
            new_token = self.login['data']['token']
            head = head.replace("#token#", new_token)
            if "#file#" in values_info['data']:
                body = body.replace("#file", file_upload)
        if values_info['hope'] == 'data':
            res = requests.request(method=method, url=url, data=body, headers=head)
            actual = res.json()
            actual = actual['expected']
        if values_info['hope'] == 'json':
            res = requests.request(method=method, url=url, json=body, headers=head)
            actual = res.json()
            actual = actual['expected']
        if values_info['hope'] == 'params':
            res = requests.request(method=method, url=url, params=body, headers=head)
            actual = res.text
            if '"code":0' in actual:
                actual = '0'

        try:
            self.assertEqual(values_info['expected'], actual)
            self.logger.info(values_info['title'], "运行完成")
        except AssertionError as err:
            self.logger.error("本次用例不通过", values_info['title'])
            raise err