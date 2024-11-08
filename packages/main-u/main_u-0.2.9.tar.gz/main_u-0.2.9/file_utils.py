#!/usr/bin/env python
# coding=utf-8
"""
for example:
    from file_utils import YamlFileUtils, JsonFileUtils, CsvFileUtils, ExcelFileUtils, IniFileUtils, CSVFileUtils
    yaml_file = YamlFileUtils()
    data = yaml_file.read('data.yaml')
    print(data)
    yaml_file.write('data.yaml', {'name': 'zhangsan', 'age': 18})

    >>>
    {'name': 'zhangsan', 'age': 18}

    json_file = JsonFileUtils()
    data = json_file.read('data.json')
    print(data)
    json_file.write('data.json', {'name': 'zhangsan', 'age': 18})

    >>>
    {'name': 'zhangsan', 'age': 18}

    excel_file_utils = ExcelFileUtils()
    excel_file_utils.write('test.xlsx', [['a', 'b', 'c'], [1, 2, 3]])
    print(excel_file_utils.read('test.xlsx'))

    >>>
    [['a', 'b', 'c'], [1.0, 2.0, 3.0]]

    csv_file_utils = CSVFileUtils()
    csv_file_utils.write('test.csv', [['a', 'b', 'c'], [1, 2, 3]])
    print(csv_file_utils.read('test.csv'))

    >>>
    [['a', 'b', 'c'], ['1', '2', '3']]

    inifile = IniFileUtils()
    inifile.write('config.ini', {'section1': {'key1': 'value1', 'key2': 'value2'}})
    data = inifile.read('config.ini')
    print(data)
    
    >>>
    {'section1': {'key1': 'value1', 'key2': 'value2'}}
"""


import json, yaml, xlrd, csv, configparser
from abc import ABCMeta, abstractmethod
from typing import Dict, List, Tuple, Union, Any
from openpyxl import workbook


class FileUtils(metaclass=ABCMeta):
    def __init__(self, file_path: str):
        """
        文件工具类，提供读取和写入文件的功能
        :param file_path: 文件路径
        """
        self.file_path = file_path

    @abstractmethod
    def read(self):
        """
        抽象方法，用于读取文件
        :return: 文件内容，可能是字符串或字节数组
        """
        pass

    @abstractmethod
    def write(self, content: Union[List, Dict, Tuple, str, bytes], mode: str = 'w'):
        """
        抽象方法，用于写入文件
        :param file_path: 文件路径
        :param content: 要写入的内容，可以是列表、字典、元组、字符串或字节数组
        :param mode: 写入模式，默认为'w'，表示覆盖写入
        """
        pass

class JsonFileUtils(FileUtils):
    def __init__(self, file_path: str):
        super().__init__(file_path)

    def read(self) -> Dict[Any, Any]:
        with open(self.file_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def write(self, content: Dict[Any, Any], mode: str = 'w'):
        with open(self.file_path, mode=mode, encoding='utf-8') as f:
            json.dump(content, f, indent=4, ensure_ascii=False)

class YamlFileUtils(FileUtils):
    def __init__(self, file_path: str):
        super().__init__(file_path)

    def read(self) -> Union[List[Any], Dict[Any, Any]]:
        with open(self.file_path, 'r', encoding='utf-8') as f:
            return yaml.load(f, Loader=yaml.FullLoader)

    def write(self, content: Union[Dict, List, Tuple, str], mode: str = 'w'):
        with open(self.file_path, mode=mode, encoding='utf-8') as f:
            yaml.dump(content, f, allow_unicode=True)  # 写入的中文不进行转码

class ExcelFileUtils(FileUtils):
    def read(self) -> List[List]:
        with xlrd.open_workbook(self.file_path) as f:
            sheet = f.sheet_by_index(0)
            rows = sheet.nrows
            cols = sheet.ncols
            data = []
            for row in range(rows):
                row_data = []
                for col in range(cols):
                    row_data.append(sheet.cell_value(row, col))
                data.append(row_data)
            return data
           
    def write(self, content: list[list]):
        wb = workbook.Workbook()
        sheet = wb.active

        for row, row_data in enumerate(content):
            for col, value in enumerate(row_data):
                sheet.cell(row=row + 1, column=col + 1, value=value)

        wb.save(self.file_path)

class CSVFileUtils(FileUtils):
    def read(self):
        with open(self.file_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            data = [row for row in reader]
            return data

    def write(self, content: list[list], mode: str = 'w'):
        with open(self.file_path, mode=mode, encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(content)
            
class IniFileUtils(FileUtils):
    config = configparser.ConfigParser()

    def read(self):
        self.config.read(self.file_path, encoding='utf-8')
        data = {}
        for section in self.config.sections():
            data[section] = {}
            for key, value in self.config.items(section):
                data[section][key] = value
        return data 
    
    def write(self, content: Dict[Any, Dict[Any, Any]], mode: str = 'w'):
        for section, values in content.items():
            self.config[section] = values
        with open(self.file_path, mode=mode, encoding='utf-8') as f:
            self.config.write(f)



if __name__ == '__main__':
    inifile = IniFileUtils('config.ini')