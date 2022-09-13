# -*- coding: utf-8 -*-
# Author: buckler
# CreateTime: 2021/11/11 11:05 下午
# Version: 1.0
# Software: PyCharm
# Description: 日志封装
import logging
import os


class Logger():
    def __init__(self):
        LOG_FORMAT = "%(asctime)s %(name)s %(levelname)s %(pathname)s %(message)s "  # 配置输出日志格式
        DATE_FORMAT = '%Y-%m-%d  %H:%M:%S %a '  # 配置输出时间的格式，注意月份和天数不要搞乱了
        logging.basicConfig(level=logging.DEBUG,
                            format=LOG_FORMAT,
                            datefmt=DATE_FORMAT,
                            filename=os.getcwd() + "/log.log"
                            # 有了filename参数就不会直接输出显示到控制台，而是直接写入文件
                            )

    def info(self, msg):
        logging.info(msg)

    def debug(self, msg):
        logging.debug(msg)
    def error(self, msg):
        logging.error(msg)

    def warning(self, msg):
        logging.warning(msg)


if __name__ == '__main__':
    log = Logger()
    log.info('test')
