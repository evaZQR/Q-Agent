import os 
import pdfplumber
import pandas as pd


import docx
# from docx.document import Document
import os


def read_txt_document(file_name):
    data = []
    file = open(file_name,'r',encoding='utf-8')  #打开文件
    
    file_data = file.readlines() #读取所有行P
    for row in file_data:
        tmp_list = row.split(' ') #按‘，’切分每行的数据
        #tmp_list[-1] = tmp_list[-1].replace('\n',',') #去掉换行符
        data.append(tmp_list) #将每行数据插入data中
    # print(data)
    return data
file_name = "E:\\Agent\\Q-Agent\\data\\test.txt"
read_txt_document(file_name)
def read_word_document(file_path):
    doc = docx.Document(file_path)
    text = []

    for paragraph in doc.paragraphs:
        text.append(paragraph.text)

    return '\n'.join(text)

# # 使用示例
# file_path="E:\\Agent\\Q-Agent\\data\\Test.docx"
# paragraphs = read_word_document(file_path)

def read_pdf_document(file_path):
    
    # 打开PDF文件
    with pdfplumber.open(file_path) as pdf:
        # 遍历每一页
        for page in pdf.pages:
            # 提取页面文本
            text = page.extract_text()
            # # 打印文本内容
            # print(text)
        
def read_excel_document(file_path):
    # 读取Excel文件
    data = pd.read_excel(file_path,keep_default_na=False)

    return data
    # 打印数据的前5行
    # print(data)
    # print(data.head())



# 指定要遍历的文件夹路径
folder_path = 'E:\\Agent\\Q-Agent\\data'

# 使用os.walk()函数遍历文件夹
for foldername, subfolders, filenames in os.walk(folder_path):
    for filename in filenames:
        file_path = os.path.join(foldername, filename)
        
        # 获取文件的扩展名
        file_extension = os.path.splitext(filename)[-1].lower()
        # print(file_extension)
        if file_extension == '.txt':
            Txt = read_txt_document(file_path)
            # print(Txt)
        elif file_extension == '.docx':
            Docx = read_word_document(file_path)
            # print(Docx)
        elif file_extension == '.pdf':
            Pdf = read_pdf_document(file_path)
            # print(Pdf)
        elif file_extension == '.xlsx':
            Xlsx = read_excel_document(file_path)
            # print(Xlsx)

 


