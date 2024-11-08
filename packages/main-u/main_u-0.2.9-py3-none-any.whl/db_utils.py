#!/usr/bin/env python
# coding=utf-8
"""
for example:
    from db_utils import MysqlUtils

    base = MysqlUtils(database='base', use_dotenv=False, host='localhost', user='root', password='123456', port=3306) 
    print(get_db_data(base, 'select * from user'))
    
    >>>
    [{'id': 1, 'name': 'admin', 'password': 'admin', 'role': 'admin'}, {'id': 2, 'name': 'admin', 'password': 'admin', 'role': 'admin'}]
"""
import os
import json
import pymysql
from abc import ABCMeta, abstractmethod
from typing import Union, List, Dict, Tuple, Any
from sshtunnel import SSHTunnelForwarder


class DBUtils(metaclass=ABCMeta):
    def __init__(self, database:str, host:str, user:str, password:str, port:int, is_ssh:bool = False, ssh_host:int = None, ssh_user:str = None, ssh_password:str = None, ssh_port:int = None):
        """
        初始化数据库连接
        :param database: 数据库名称
        :param is_ssh: 是否使用SSH隧道
        """
        self.database = database
        self.host = host
        self.user = user
        self.password = password
        self.port = int(port)
        self.ssh_host = ssh_host
        self.ssh_user = ssh_user
        self.ssh_password = ssh_password
        self.ssh_port = int(ssh_port) if ssh_port else None
        self.is_ssh = is_ssh

    
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def query(self, sql, params=None) -> Union[None, List[Dict[str, Any]]]:
        pass

    @abstractmethod
    def select_one(self) -> Union[None, Dict[str, Any]]:
        pass

    @abstractmethod
    def select_all(self) -> Union[None, List[Dict[str, Any]]]:
        pass

    @abstractmethod
    def close(self):
        pass
    
    def __str__(self) -> str:
        attrs = vars(self)
        return '\n'.join("%s: %s" % item for item in attrs.items())
    
class MysqlUtils(DBUtils):
    def __init__(self, database:str, host:str, user:str, password:str, port:int, is_ssh:bool = None, ssh_host:str = None, ssh_user:str = None, ssh_password:str = None, ssh_port:int = None):
        super().__init__(database, host, user, password, port, is_ssh, ssh_host, ssh_user, ssh_password, ssh_port)

    def connect(self) -> None:
        try:
            if self.is_ssh:
                with SSHTunnelForwarder(
                    # 指定ssh登录的跳转机的address
                    ssh_address_or_host=(self.ssh_host, self.ssh_port),
                    ssh_username=self.ssh_user,
                    ssh_password=self.ssh_password,
                    # 设置数据库服务地址及端口
                    remote_bind_address=(self.host, self.port)) as server:
                    self.conn = pymysql.connect(
                        database=self.database,
                        user=self.user,
                        password=self.password,
                        host='127.0.0.1',
                        port=server.local_bind_port
            )
            else:
                self.conn = pymysql.connect(
                    host=self.host, port=self.port, user=self.user, password=self.password, database=self.database
            )
        except pymysql.MySQLError as e:
            print(f"数据库连接失败: {e}")

    def query(self, sql, params=None) -> None:
        try:
            self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)
            self.cursor.execute(sql, params)
            self.conn.commit()
        except pymysql.MySQLError as e:
            print(f"查询失败: {e}")
        finally:
            print(f"执行SQL: {sql}")

    def select_one(self) -> Union[None, Dict[str, Any]]:
        return self.cursor.fetchone()

    def select_all(self) ->  Union[None, List[Dict[str, Any]]]:
        result = self.cursor.fetchall()
        return self._format_datetime(result)

    # 格式化查询结果输出时间格式
    def _format_datetime(self, data: Union[None, Dict[str, Any], List[Dict[str, Any]]]) -> Union[None, Dict[str, Any], List[Dict[str, Any]]]:
        time_lst = ["begin_time", "end_time", "start_time", "update_time", "insert_time", "delete_time", "operate_time", "create_time"]
        # 格式化时间
        if isinstance(data, dict):
            for key, value in data.items():
                if key in time_lst:
                    data[key] = str(value)
            return data
        elif isinstance(data, list):
            for row in data:
                for key, value in row.items():
                    if key in time_lst:
                        # 如果时间字符串数为7，补全 如 01:00:00
                        row[key] = f"0{str(value)}" if len(str(value)) == 7 else str(value)
            return self._format_json(data)

    # 格式化json字符串
    def _format_json(self, data: Union[None, Dict[str, Any], List[Dict[str, Any]]]):
        # 遍历查询结果，检查每个字段输出结果，若是json字符串则进行转化为列表或字典
        for row in data:
            for k, v in row.items():
               # 判断 v 是不是json 字符串
                if isinstance(v, str) and v.startswith('{') and v.endswith('}'):
                    try:
                        row[k] = json.loads(v)
                    except json.JSONDecodeError:
                        raise "Invalid JSON format"
                elif isinstance(v, str) and v.startswith('[') and v.endswith(']'):
                    try:
                        row[k] = json.loads(v)
                    except json.JSONDecodeError:
                        raise "Invalid JSON format"
        return data

    def close(self) -> None:
        self.cursor.close()
        self.conn.close()

def get_db_data(conn: DBUtils, sql: str, params: Tuple = (), is_one: bool = False) -> Union[None, Dict[str, Any], List[Dict[str, Any]]]:
    try:
        conn.connect()
        conn.query(sql, params)
        if is_one:
            return conn.select_one()
        else:
            return conn.select_all()
    except Exception as e:
        print(f"查询失败: {e}")
        return None
    
    finally:
        conn.close()

if __name__ == '__main__':
    base = MysqlUtils(database='base', host='localhost', user='root', password='123456', port='3306')
    print(get_db_data(base, 'select * from user'))
