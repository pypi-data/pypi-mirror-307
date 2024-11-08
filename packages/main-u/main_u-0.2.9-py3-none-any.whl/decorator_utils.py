#!/usr/bin/env python
# coding=utf-8

"""
for example:
    decorator = DecoratorUtils('root.log', 'demo')
    @decorator
    def test_func(a, b):
        time.sleep(1)
        return a + b
    test_func(1, 2)

    >>>
    2024-08-05 14:42:52,103 - demo - INFO - =========================test_func开始执行=========================
    2024-08-05 14:42:52,104 - demo - INFO - arg:-->(1, 2)
    2024-08-05 14:42:52,104 - demo - INFO - kwargs:-->{}
    2024-08-05 14:42:53,116 - demo - INFO - result:-->3
    2024-08-05 14:42:53,116 - demo - INFO - 耗时:1 秒
    2024-08-05 14:42:53,116 - demo - INFO - =========================test_func执行完毕=========================
"""

import time
from functools import wraps
from log_utils import LogUtils
from typing import Callable


class DecoratorUtils:
    def __init__(self, log_name: str ='app.log', name :str = 'root', char:str = '=', num:int = 25):
        """
        装饰器类
        :param log_name: 日志文件名
        :param name: 日志名称
        :param char: 日志分隔符
        :param num: 日志分隔符长度
        """
        self.logger = LogUtils(log_file=log_name, name=name).get_logger()
        self.char = char
        self.num = num

    def __call__(self, func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            self.logger.info(f"{self.char* self.num}{func.__name__}开始执行{self.char* self.num}")
            self.logger.info(f"arg:-->{args}")
            self.logger.info(f"kwargs:-->{kwargs}")
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            self.logger.info(f"result:-->{result}")
            self.logger.info(f"耗时:{(end_time - start_time):.0f} 秒")
            self.logger.info(f"{self.char*self.num}{func.__name__}执行完毕{self.char*self.num}")
            return result
        return wrapper
    

if __name__ == '__main__':
    decorator = DecoratorUtils('apk.log', 'demo')
    @decorator
    def test_func(a, b):
        time.sleep(1)
        return a + b
    test_func(1, 2)