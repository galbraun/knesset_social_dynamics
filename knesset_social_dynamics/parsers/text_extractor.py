import docx
#import win32com.client
from loguru import logger


def extract_raw_protocol(file_path):
    try:
        return extract_new_raw_protocol(file_path)
    except Exception as e:
        print(e)
        return extract_old_raw_protocol(file_path)


def extract_new_raw_protocol(file_path):
    logger.debug("Parsing new-version protocoal")
    doc = docx.Document(file_path)

    paras = []
    for para in doc.paragraphs:
        paras.append(para.text)

    return paras


# def extract_old_raw_protocol(file_path):
#     logger.debug("Parsing old-version protocoal")
#     doc = win32com.client.GetObject(file_path)
#     return doc.Content.Text.splitlines()
