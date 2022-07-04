import xlrd
from os import path


class ExcelHandler:
    def __init__(self, file, configObj, sheetName=None):
        self.file_name = path.basename(file).split('.')[0]
        self.configObj = configObj
        self.sheetName = sheetName
        self.wb = xlrd.open_workbook(file)

    #获取sheet名称
    def get_sheets(self):
        sheets_name = self.wb.sheet_names()
        sheets_obj = self.wb.sheets()
        return dict(zip(sheets_name, sheets_obj))

    #获取sheet行数
    def get_sheet_rows(self, sheet_obj):
        rows = sheet_obj.nrows
        return rows

    #获取sheet第一行数据
    def get_first_row(self, sheet_obj):
        return sheet_obj.row_values(0)

    #获取一个sheet的数据，并返回字典格式。
    #格式：{'sheet_name':[{'casename1':'test1'}, {'casename2':'test2'}]}
    def get_sheet_data(self, sheet_name, sheet_obj):
        sheet_data_dic = {}
        sheet_rows_list = []

        rows = self.get_sheet_rows(sheet_obj)

        if sheet_name == 'config':
            if self.configObj.check_section(self.file_name):

                for i in range(rows):
                    data = sheet_obj.row_values(i)[0].strip().split('=')
                    self.configObj.set_data(self.file_name, data[0].strip(), data[1].strip())
        else:
            first_row = self.get_first_row(sheet_obj)

            for i in range(1, rows):
                row_value = sheet_obj.row_values(i)
                if row_value[0] != '':
                    sheet_rows_list.append(dict(zip(first_row, row_value)))
                else:
                    break

            sheet_data_dic[sheet_name] = sheet_rows_list

        return sheet_data_dic

    #获取sheets的数据，并返回字段格式。
    #格式：
    # [
    #   {'sheet_name1':[{'casename':'test1'}, {'casename':'test2'}]},
    #   {'sheet_name2':[{'casename':'test1'}, {'casename':'test2'}]}
    # ]
    def get_sheets_data(self):
        sheets_data_list = []

        sheets = self.get_sheets()
        keys = sheets.keys()
        if 'config' not in keys:
            print('Excel测试用例缺少配置文件')
            exit()
        elif self.sheetName:
            if self.sheetName not in keys:
                print(f'Excel sheet表名称{self.sheetName}错误，请确认')
                exit()
            else:
                for sheet_name, sheet_obj in sheets.items():
                    if sheet_name in [self.sheetName, 'config']:
                        data = self.get_sheet_data(sheet_name, sheet_obj)
                        if sheet_name != 'config':
                            sheets_data_list.append(data)
        else:
            for sheet_name, sheet_obj in sheets.items():
                data = self.get_sheet_data(sheet_name, sheet_obj)
                if sheet_name != 'config':
                    sheets_data_list.append(data)

        return self.file_name, sheets_data_list
