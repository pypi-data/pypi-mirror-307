#!/usr/bin/env python
# coding=utf-8

"""
for example:
    from log_utils import LogUtils
    log = LogUtils('app.log', logging.DEBUG)
    log.debug('debug message')
    log.info('info message')
    log.warning('warning message')
    log.error('error message')
    
    >>>
    2022-01-01 00:00:00 - app.log - DEBUG - debug message
    2022-01-01 00:00:00 - app.log - INFO - info message
    2022-01-01 00:00:00 - app.log - WARNING - warning message
"""
import logging

class LogUtils:
    def __init__(self, log_file='app.log', name: str = 'root', log_level=logging.INFO):
        self.log_file = log_file
        self.log_level = log_level

        # 设置日志格式
        self.formatter = logging.Formatter(f'%(asctime)s - {name} - %(levelname)s - %(message)s')

        # 配置日志处理器
        self.file_handler = logging.FileHandler(self.log_file, encoding='utf-8')
        self.file_handler.setFormatter(self.formatter)

        # 配置控制台日志处理器
        self.console_handler = logging.StreamHandler()
        self.console_handler.setFormatter(self.formatter)

        # 获取根日志记录器并添加处理器
        self.logger = logging.getLogger()
        self.logger.setLevel(self.log_level)
        self.logger.addHandler(self.file_handler)
        self.logger.addHandler(self.console_handler)

    def get_logger(self):
        return self.logger

