# Author:Sun Yujian
import sys
import os
import time
sys.path.append("C:\\Users\\User\\Desktop\\SentSearch1_2")
from tools.txt2sent.CutMain import CutMain
from tools.pdf2txt.PDFMain import PDFMain


class PDFExtract(object):
    def pdfExtract(self,model,src_add,dst_add):
        #model1:debug 会保留所有文档
        #model:formal 只保留最后切分句子完成的
        time_old = time.time
        file_list_extract = PDFMain().pdfMain(src_add,dst_add)
        #print(file_list_extract)
        if not os.path.exists(src_add):
            print('Not Found ' + src_add)
            sys.exit()
        print('************提取完成***********')
        if model == '1':
            CutMain().cutMain(file_list_extract , model)
        elif model == '2':
            CutMain().cutMain(file_list_extract , model)
        else:
            print('the model is wrong')

        print('************清洗完成************')
        #print(time.time-time_old)

if __name__ == '__main__':
    PDFExtract().pdfExtract(sys.argv[1],sys.argv[2],sys.argv[3])
# for parent, dirnames, filenames in os.walk('/home/py35/Desktop/s1'):
#     for filename in filenames:
#         #print(filenames)
#         file_name = os.path.join(parent, filename)
#         if file_name.endswith('clean_1.txt'):
#             os.remove(file_name)
#
#         elif file_name.endswith('clean_2.txt'):
#             os.remove(file_name)
#
#         elif file_name.endswith('clean_3.txt'):
#             os.remove(file_name)
#
#         elif file_name.endswith('clean_4.txt'):
#             os.remove(file_name)
#
#         elif file_name.endswith('clean_5.txt'):
#             os.remove(file_name)
#
#         elif file_name.endswith('clean_Incomplete.txt'):
#             os.remove(file_name)
#
#         elif file_name.endswith('clean_Incomplete_temp.txt'):
#             os.remove(file_name)
#
#         elif file_name.endswith('clean_6.txt'):
#             print(file_name)
#             name = file_name[:-12]
#             name =name  + '.txt'
#             os.remove(name)
#
#             os.rename(file_name, name)
