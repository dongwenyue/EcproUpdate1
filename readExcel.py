import os
import getpathInfo

from xlrd import open_workbook
#拿到该项目的绝对路径

path = getpathInfo.get_path()

class readExcel():
    def get_xls(self,xls_name,sheet_name):
        #xls_name填写用例的Excel名称sheet_name该Excel的sheet名称
        cls = []
        #获取用例文件路径
        xlspath = os.path.join(path, "testFile",'case',xls_name)
        # print(xlspath)
        file = open_workbook(xlspath)#打开用例Excel
        sheet = file.sheet_by_name(sheet_name)#获取打开Excel的sheet
        #获取这个sheet行数
        nrows = sheet.nrows
        for i in range(nrows):
            if sheet.row_values(i)[0] != u'case_name':#如果这个Excel的这个sheet的第i行第一列不等于case_name那么把这行的数据添加到cls[]
                cls.append(sheet.row_values(i))
        return cls
if __name__ == '__main__':
    print(readExcel().get_xls('test_1.xlsx','sheet_name'))
    print(readExcel().get_xls('test_1.xlsx','sheet_name')[0][1])
    # print(readExcel().get_xls('test_1.xlsx','sheet_name')[1][2])
