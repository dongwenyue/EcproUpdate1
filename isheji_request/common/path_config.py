import os

now_position = os.path.abspath(__file__)
# print(now_position)

config_position = os.path.dirname(now_position)
# print(config_position)

root_directory = os.path.dirname(config_position)
# print(root_directory)

logs_path = os.path.join(root_directory, 'logs')

data_position = os.path.join(root_directory,'data')

suplier_xlsx = os.path.join(data_position, 'suplier.xlsx')

jepg_path = os.path.join(data_position, 'jepg.jpeg')


upload_po_attachment_path = os.path.join(data_position, "upload_po_attachment.txt")

xlsx_path = os.path.join(data_position,'excel文件名')


def getTestReport():
    file_path = ""
    reports_position = os.path.join(root_directory, 'reports')
    dirs = os.listdir(reports_position)
    listReport = []
    for file in dirs:
        listReport.append(file)
    if listReport.__len__() > 0:
        file_name = listReport[-1]
        file_path = os.path.join(reports_position, file_name)
    return file_path



