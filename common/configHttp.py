import requests
import  json

class RunMain():

    def send_post(self,url,data):   #定义一个方法，传入需要的参数 url，data
        result = requests.post(url=url,data=data)
        res = json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2)
        return result
    def send_get(self,url):
        result = requests.get(url=url).json()
        res = json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2)
        print(res)
    def run_main(self,method,url=None,data=None):   #定义一个run_namin函数，通过传过来的methon来进行不同get或者post请求
        result = None
        if method == 'post':
            result = self.send_post(url,data)
        elif method == 'get':
            result = self.send_get(url)
        else:
            print("method值错误!!!")
        return result


if __name__ == '__main__' : #写死参数
    result1 = RunMain().run_main('get','http://39.102.48.166/v1/catalog/props/2043980/prop_values?category_id=13183&tp_ids=1000,1001,1004,1006,1008,1009&http_method=GET&timestamp=2021-05-11T18:23:48&access_key=e174d6adbb8c41e5b53a10985dc0f0f4&signature=29bcf744bcfb0b1cccbf55ff03a22151&signature_method=MD5&signature_version=1.0')
    print(result1)