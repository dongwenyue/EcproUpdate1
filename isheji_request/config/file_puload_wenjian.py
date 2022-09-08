from common.path_config import upload_po_attachment_path


with open(upload_po_attachment_path, mode='rt', encoding='utf-8') as file:
    file_upload = file.read()