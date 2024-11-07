"""
pip install pandas==1.3.4
pip install openpyxl==3.0.9
pip install xlrd==2.0.1 --- 用于解析.xls文件
@Author: kang.yang
@Date: 2024/3/16 09:23
"""
import xlrd
import pandas as pd


class Excel(object):

    def __init__(self, file_name: str):
        self.file_name = file_name

    def read(self, sheet_name=0, row_index: int = None, col_index: int = None, col_name: str = None):
        if self.file_name.endswith(".xls"):
            workbook = xlrd.open_workbook(self.file_name, ignore_workbook_corruption=True)
            if col_index:
                df = pd.read_excel(workbook, sheet_name=sheet_name, usecols=[col_index-1])
                return [r[0] for r in df.values.tolist()]
            else:
                df = pd.read_excel(workbook, sheet_name=sheet_name)
        else:
            if col_index:
                df = pd.read_excel(self.file_name, sheet_name=sheet_name, usecols=[col_index-1])
                return [r[0] for r in df.values.tolist()]
            else:
                df = pd.read_excel(self.file_name, sheet_name=sheet_name)

        if col_name:
            return df[col_name].values.tolist()

        if row_index is not None:
            values = [df.values[row_index-1].tolist()]
        else:
            values = df.values.tolist()

        row_list = []
        col_names = []

        for name in df:
            col_names.append(name)

        for row in values:
            row_dict = {}
            for name, value in zip(col_names, row):
                row_dict[name] = value
            row_list.append(row_dict)

        return row_list

    def write(self, sheet_dict: dict, append=False):
        """
        :param sheet_dict:
        数据格式: {
            'sheet1_name': {'标题列1': ['张三', '李四'], '标题列2': [80, 90]},
            'sheet2_name': {'标题列3': ['王五', '郑六'], '标题列4': [100, 110]}
        }
        :param append: 是否追加，默认覆盖
        """
        df_dict = {}
        for sheet_name, sheet_data in sheet_dict.items():
            df_dict[sheet_name] = pd.DataFrame(sheet_data)

        writer = pd.ExcelWriter(self.file_name)
        for sheet_name, sheet_data in sheet_dict.items():
            _df = pd.DataFrame(sheet_data)
            if append:
                _df = df_dict[sheet_name].append(_df)
            _df.to_excel(writer, sheet_name=sheet_name, index=False)
        writer.save()


class CSV(object):

    def __init__(self, file_name):
        self.file_name = file_name

    def read(self, row_index: int = None, col_index: int = None, col_name: str = None):

        if col_index:
            df = pd.read_csv(self.file_name, usecols=[col_index - 1])
            res = [r[0] for r in df.values.tolist()]
            return res

        if col_name:
            df = pd.read_csv(self.file_name, usecols=[col_name])
            res = [r[0] for r in df.values.tolist()]
            return res

        df = pd.read_csv(self.file_name)
        if row_index:
            values = [df.values[row_index - 1].tolist()]
        else:
            values = df.values.tolist()

        row_list = []
        col_names = []

        for name in df:
            col_names.append(name)

        for row in values:
            row_dict = {}
            for name, value in zip(col_names, row):
                row_dict[name] = value
            row_list.append(row_dict)

        return row_list

    def write(self, data: dict, append=False):
        """
        :param data:
        数据格式：{
            '标题列1': ['张三', '李四'],
            '标题列2': [80, 90]
        }
        :param append: 是否追加，默认覆盖
        """
        df = pd.DataFrame(data)
        if append:
            _df = pd.read_csv(self.file_name)
            df = _df.append(df)
        df.to_csv(self.file_name, index=False)


if __name__ == '__main__':
    pass





