import requests
import json
import time
import pymysql
import argparse
import os


class wechatRebot_send:
    def __init__(self):
        pass

    def test_robot_bak(self, WX_del_HOOK, project, start_time, qc_package, qc_main_image, qc_detail_page, total):
        """
        需要发送到企业微信的文案信息
        :param project:         项目名称
        :start_time:            开始时间
        :prefix                 商品前缀
        :param total:           总计
        :param succeed_title:   批量上货链接
        """
        data = {
            "msgtype": "markdown",  # 消息类型，此时固定为markdown
            "markdown": {
                "content": "# **QC设置状态反馈**\n#### **请相关同事注意，及时跟进！**\n"
                           "> 项目名称：<font color=\"info\">%s</font> \n"
                           "> 开始时间：<font color=\"info\">%s</font> \n"
                           "> 图片包状态：<font color=\"info\">%s</font> \n"
                           "> 资源图状态：<font color=\"info\">%s</font> \n"
                           "> 详情页状态：<font color=\"info\">%s</font> \n"
                           "> 总计：<font color=\"info\">%s条</font>\n" % (
                               project, start_time, qc_package, qc_main_image, qc_detail_page, total,)
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

    def upload_media(self, upload_media_url, export_file_path):
        data = {"file": open(export_file_path, 'rb')}
        print(data)
        r = requests.post(url=upload_media_url, files=data)
        print(r.text)
        res = json.loads(r.text)
        return res["media_id"]

    def test_file(self, WX_del_HOOK, media_id):
        data = {
            "msgtype": "file",
            "file": {
                "media_id": media_id
            }
        }
        print(data)
        r = requests.post(url=WX_del_HOOK, json=data)
        print(r.text)
        return (r.text)


# qa环境，数据库
def select_mysql_dict(sql):
    MYSQL_HOST = 'rm-2ze5qeu2nyo0i5gm8lo.mysql.rds.aliyuncs.com'
    MYSQL_USERNAME = 'qa_v2'
    MYSQL_PASSWORD = 'lyp82nLF'
    MYSQL_PORT = 3306
    MYSQL_DATABASE = 'qa_v2_catalog'
    conn = pymysql.connect(host=MYSQL_HOST, user=MYSQL_USERNAME, passwd=MYSQL_PASSWORD,
                           port=MYSQL_PORT, database=MYSQL_DATABASE)
    cursor = conn.cursor()
    cursor.execute(sql)
    # 获取所有记录列表
    results = cursor.fetchall()
    print('数据库查询结果，第一个值', results)
    conn.close()
    return results


def props_bulk(model: str, tp_id: str, tp_category_ids: str, scene: str):
    # 平台祥光->qa环境属性同步->场景上货—>同步规格属性
    # http://172.16.173.103/merchant-admin/props/bulk/pull?model=qa_v2_merchant&tp_id=1001&tp_category_ids=1629&code=&category_ids=&scene=pub
    # http://172.16.173.103/merchant-admin/props/bulk/pull?model=qa_v2_merchant&tp_id=1001&tp_category_ids=201394601&code=&category_ids=&scene=pub
    # http://172.16.173.103/merchant-admin/props/bulk/pull?model=qa_v2_merchant&tp_id=1000&tp_category_ids=201394601&code=&category_ids=&scene=pub
    err_dict = {}
    props_bulk_url = 'http://172.16.173.103/merchant-admin/props/bulk/pull?model={}&tp_id={}&tp_category_ids={}&code=&category_ids=&scene={}'.format(
        model, tp_id, tp_category_ids, scene)
    print(props_bulk_url)
    response = requests.get(url=props_bulk_url, proxies=proxies).json()
    print(response)
    if response['message'] == 'Success':
        if len(response['data']['errs']) == 0:
            print('属性同步->获取成功', '\n', tp_category_ids)
            return None
        elif len(response['data']['errs']) != 0:
            # raise Exception('拉取失败，原始类ID:', tp_category_ids)
            print('有错误', tp_category_ids)
            err_dict[tp_category_ids] = response
            return err_dict
    else:
        err_dict[tp_category_ids] = response
        return err_dict


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='manual to this script')
    parser.add_argument('--tp_name', type=str, default='淘宝')
    parser.add_argument('--model', type=str, default='qa_v2_merchant')
    args = parser.parse_args()
    tp_name = args.tp_name
    model = args.model


    # model = 'qa_v2_merchant'
    # model = 'prod_merchant'
    select_tp_id = "SELECT id FROM tp WHERE name LIKE '{}'".format(tp_name)
    tp_id = select_mysql_dict(select_tp_id)[0][0]
    # tp_id = '1000'
    # tp_name = '淘宝'

    # 删除属性同步结果的文件
    CURRENTPATH = os.getcwd()
    Create_failure_path = os.path.join(CURRENTPATH, tp_name + '_' + model[0:5] + '_' + 'Props_bulk_failure.txt')
    print(Create_failure_path)
    if os.path.exists(Create_failure_path):
        os.remove(Create_failure_path)

    select_original_data = "SELECT tp_category.original_cid FROM tp_category inner JOIN category_mapping ON tp_category.id=category_mapping.tp_category_id WHERE tp_category.tp_id={} AND tp_category.is_leaf = '1' GROUP BY tp_category.id LIMIT 0,1000".format(tp_id)
    print(select_original_data)
    original_data = select_mysql_dict(select_original_data)
    print(original_data)
    b = []
    for i in range(len(original_data)):
        p = lambda x: x[i][0]
        b.append(p(original_data))
    print(b)
    print('源类目总个数', len(b))

    # b = ['121396006', '121416004', '50019466']
    # b = ['121396006']

    err_data_list = []
    count = 0
    for original_cid in b:
        print(original_cid)
        # tp_category_ids = '1629'
        tp_category_ids = original_cid
        scene = 'pub'
        # 设置代理
        proxies = {
            "http": "http://172.16.173.103"
        }
        # qa环境->同步规格属性
        err_dict = props_bulk(model, tp_id, tp_category_ids, scene)
        # 判断是否同步规格——>属性同步成功,失败放到字典里，成功的话就是None就计数
        if err_dict is None:
            count = count + 1
            print(f'第{count}个类目,总数:{len(b)},原类目id:{tp_category_ids}')
        # 获取失败的，则记录到列表里
        elif err_dict:
            err_data_list.append(err_dict)
    print('获取失败的所有数据的列表------分割线--------')
    print(err_data_list)
    print('获取失败的------分割线--------')
    original_list = []

    for err_data in err_data_list:
        # 获取字典中的第一个键
        print(err_data)
        original_list.append(list(err_data.keys())[0])
    print(','.join(original_list))

    if original_list:
        # 把结果写入文件
        with open(Create_failure_path, 'a', encoding='utf-8') as f:
            f.write('源类目总数:' + str(len(b)) + '\n')
            f.write('平台：' + tp_name + '\n')
            f.write('环境：' + model + '\n')
            f.write('源类目失败总个数' + str(len(original_list)) + '\n')
            f.write('源类目:' + ','.join(original_list) + '\n')
            for err_dict in err_data_list:
                f.write(json.dumps(err_dict, ensure_ascii=False) + '\n')

        # 企业微信机器人，文件上传接口
        # key:调用接口凭证, 机器人webhookurl中的key参数
        upload_media_url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/upload_media?key=24692f61-7f4f-41f4-a4df-57b9b4660a57&type=file'
        media_id = wechatRebot_send().upload_media(upload_media_url, Create_failure_path)

        WX_del_HOOK = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=24692f61-7f4f-41f4-a4df-57b9b4660a57'
        mess = wechatRebot_send().test_file(WX_del_HOOK, media_id)
