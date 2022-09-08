import os


def get_Path():
    path = os.path.split(os.path.realpath(__file__))[0]
    return path

if __name__ == '__main__':#执行文件
    print('测试路径是否OK，路径为:',get_Path())