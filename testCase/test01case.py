import json
import unittest

import login as login

from common.configHttp import RunMain
import paramunittest
import geturlParams
import urllib.parse
import readExcel

url = geturlParams.geturlparams().get_url()     #调用并获取拼接的URL
property_xls = readExcel.readExcel().get_xls('test_1.xlsx','prop_id')

@paramunittest.parametrized(*login.xls)
class testattribute (unittest.TestCase):
    def setParameters(self,case_name,path,query,method):
        """

        :param case_name:
        :param path:
        :param query:
        :param method:
        :return:
        """
        self.case_name = str(case_name)
        self.path = str(path)
        self.query = str(query)
        self.method = str(method)

    def description(self) :
        """
        test report description
        :return:
        """
        self.case_name
    def setUp(self):
        """

        :return:
        """
        print(self.case_name+"测试开始前准备")
    def test01case(self):
        self.checkResult()

    def tearDown(self):
        print("测试结束，输出log完结\n\n")

    def checkResult(self): #断言
        """
        check test result
        :return:
        """
        url1 = "http://39.102.48.166/v1/catalog/props"
        new_url = url1 + self.query
        data1 = dict(urllib.parse.parse_qsl(urllib.parse.urlsplit(new_url).query))
        info = RunMain().run_main(self.method,url,data1)
        rep = json.loads(info)
        if self.case_name == '2043980':#如果case_name是2043980,说明合法，返回code=200
            self.assertEqual(rep['code'],200)
        if self.case_name == '39000':
            self.assertEqual(rep['code'],-1)
        if self.case_name == 'null':
            self.assertEqual(rep['code',10001])
    def productList(self):
        '''

        :return:
        '''
        url1 = "http://39.102.48.166/v1/catalog/props/catalog/tps"
