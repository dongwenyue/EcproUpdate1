import datetime
import hashlib

import  readConfig as readconfig

readconfig = readconfig.ReadConfig()

class geturlParams(): #将配置文件中读取进行拼接

    def __init__(self):
        pass


    # def get_time(self):
    #     """获取当前时间戳"""
    #     # now_time = (datetime.datetime.now() + datetime.timedelta(hours=-0)).strftime("T%H:%M:%S:%f")
    #     now_time = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    #     return now_time

    def url_string(self):
        # http_method = 'GET'
        timestamp = str(datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S'))

        signature_method = 'MD5'
        signature_version = '1.0'
        access_key = 'e174d6adbb8c41e5b53a10985dc0f0f4'
        access_secret = '139b2dd02d5f4a528addcd2f82ea3817'
        account_list = ['GET', timestamp, signature_method, signature_version, access_key, access_secret]
        signature = '&'.join(account_list)
        md5 = hashlib.md5()
        md5.update(signature.encode())
        sign = md5.hexdigest()
        signature = sign
        string_url = "&http_method=%s&timestamp=%s&access_key=%s&signature=%s&signature_method=%s&signature_version=%s" % (
            'GET', timestamp, access_key, signature, signature_method, signature_version)
        return string_url

    def get_url(self):
        new_url = readconfig.get_http('scheme') \
                  + '://' + readconfig.get_http('baseurl') + ('/v1/catalog') + ('/props/2043980/prop_values?category_id=13183&tp_ids=1000,1001,1004,1006,1008,1009') + self.url_string()
        return new_url
if __name__ == '__main__':
    print(geturlParams().get_url())