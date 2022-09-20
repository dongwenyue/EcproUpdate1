# encoding=utf8

'''
    Python将2000个Word文件合并成一个Excel表格
'''

# 导入包
from docx import Document
import xlsxwriter
import os, sys, shutil


# 定义方法
def rewordlist(wordpath):
    '''返回一个目录下所有word文件路径的数组'''
    patharray = []
    for foldName, subfolders, filenames in os.walk(wordpath):
        de = 0
        for subfolder in subfolders:  # 遍历列表下的子文件夹名
            de = de + 1
            allpath = foldName + '/' + subfolder + '/' + subfolder + '.docx'
            dictjson = {"word_id": de, "word_txt": subfolder, "word_path": allpath}  # 组合字典
            patharray.append(dictjson)
    return patharray


def obtainwordtxt(wordpath):
    '''获取word中的所有文本'''
    document = Document(wordpath)
    all_paragraphs = document.paragraphs
    txtstr = ''
    for paragraph in all_paragraphs:
        txtstr = txtstr + paragraph.text
        # 打印每一个段落的文字
        # print(paragraph.text)
    return txtstr


def zbexceldata(patharray):
    '''将提取word中的文本，组合为一个数组json，待生成excel使用'''
    exceldataarray = []
    for dirs in patharray:
        txtstr = obtainwordtxt(dirs['word_path'])
        exdatajson = {"id": dirs['word_id'], "txt": dirs['word_txt'], "content": txtstr}
        exceldataarray.append(exdatajson)
    return exceldataarray


def createexcel(exceldata, tabpath):
    '''根据提供的json数组，创建需要的excel表格'''

    # 创建一个工作簿并添加一个工作表。
    workbook = xlsxwriter.Workbook(tabpath)
    worksheet = workbook.add_worksheet('Sheet1')

    # 表头字段格式
    header = {
        'bold': True,  # 粗体
        'font_name': '微软雅黑',
        'font_size': 11,
        'border': True,  # 边框线
        'align': 'center',  # 水平居中
        'valign': 'vcenter',  # 垂直居中
        "color": "#232323",  # 文字颜色
        'bg_color': '#D9E1F2'  # 背景颜色
    }
    headerpm = workbook.add_format(header)

    # 正文字段格式
    text = {
        'font_name': '微软雅黑',
        'font_size': 10,
        'border': True,
        'align': 'left',  # 左对齐
        "color": "#232323",  # 文字颜色
        'valign': 'vcenter'
    }
    textpm = workbook.add_format(text)

    # 编写一些头数据。
    worksheet.write('A1', '序号', headerpm)
    worksheet.write('B1', '名称', headerpm)
    worksheet.write('C1', '文稿内容', headerpm)
    worksheet.set_row(0, 30)  # 设置高度
    worksheet.set_column('C:C', 180)  # C列宽度

    # 从第一个单元格开始。 行和列的索引为零。
    row = 1
    col = 0

    # 遍历数据并逐行写出。
    for jsonc in exceldata:
        worksheet.write(row, col, str(jsonc['id']), textpm)
        worksheet.write(row, col + 1, jsonc['txt'], textpm)
        worksheet.write(row, col + 2, jsonc['content'], textpm)
        row += 1
    # 关闭对象
    workbook.close()

    print("\n表格创建完成: " + tabpath)


if __name__ == '__main__':
    # word文件存放目录
    wordpath = r'D:\test\wordlist'

    # 表格创建保存目录
    tabpath = r'D:\test\excelret\文稿汇总.xlsx'

    patharray = rewordlist(wordpath)
    exceldata = zbexceldata(patharray)
    createexcel = createexcel(exceldata, tabpath)