import openpyxl
from common.path_config import suplier_xlsx
from openpyxl.worksheet.worksheet import Worksheet


def get_sheet_velus(file_path, sheet_name):
    workbook = openpyxl.load_workbook(file_path)
    sheet: Worksheet = workbook[sheet_name]
    values = list(sheet.values)
    workbook.close()
    title = values[0]
    rows = values[1:]
    new_rows = [dict(zip(title, row)) for row in rows]
    return new_rows


'''用例前调用'''
# excel_data = get_sheet_velus(xlsx_path, '文件名')
# excel_data = get_sheet_velus(suplier_xlsx, 'Sheet1')
# print(suplier_xlsx)
# print(excel_data)
# for i in excel_data:
#     print(i)