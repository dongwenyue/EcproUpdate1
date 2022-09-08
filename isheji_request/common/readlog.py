from common.path_config import logs_path
from common.datatime import DateTime
import logging
import os

class Log:

    def __init__(self, logname="Root"):
        # 日志存储路径

        logPath = logs_path+"/"

        if os.path.exists(logPath + DateTime.TODAY) == False:
            os.mkdir(logPath + DateTime.TODAY)
        # 日志存储文件
        alllogName = logPath + DateTime.TODAY + "/" + DateTime.TODAY + ".log"
        errorLogName = logPath + DateTime.TODAY + "/" + DateTime.TODAY + "_error.log"

        # 创建一个logger
        self.logger = logging.getLogger(logname)
        self.logger.setLevel(logging.INFO)
        # if not self.logger.handlers:
        # 创建handler写入所有日志
        fh = logging.FileHandler(alllogName)
        fh.setLevel(logging.INFO)

        # 创建handler写入错误日志
        eh = logging.FileHandler(errorLogName)
        eh.setLevel(logging.ERROR)

        # 创建handler写入到控制台日志
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)

        # 定义日志输出格式
        # 以时间-日志器名称-日志级别-日志内容的形式展示
        all_log_formatter = logging.Formatter('%(asctime)s - %(name)-25s - %(levelname)s - %(message)s')

        # 以时间-日志器名称-日志级别-文件名-函数行数-错误内容
        error_log_fomatter = logging.Formatter('%(asctime)s - %(name)-25s - %(levelname)s - %(module)s - %(lineno)s - %(message)s')

        # 将定义好的输出形式添加到handler
        fh.setFormatter(all_log_formatter)
        ch.setFormatter(all_log_formatter)
        eh.setFormatter(error_log_fomatter)

        # 给logger 添加handler
        if not self.logger.handlers:
            self.logger.addHandler(fh)
            self.logger.addHandler(ch)  # 如果将其注释则，不在往控制台输出日志
            self.logger.addHandler(eh)

    def getLog(self):
        return self.logger
