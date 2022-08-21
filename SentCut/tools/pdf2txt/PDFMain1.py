# Author:Sun Yujian
import sys
import os
sys.path.append("/home/py35/PycharmProjects/SentSearch")

from tools.pdf2txt.PDFCopy import PDFCopy
from tools.pdf2txt.ChangePDFName import  ChangePDFName
from tools.pdf2txt.GetThesisName import GetThesisName
from tools.pdf2txt.GetPDFName import GetPDFName
from tools.pdf2txt.Extract import PDFExtract
import os
import os.path
import sys
# class PDFMain(object):
#     def main(self,address):
#         add = PDFCopy().copyFile(address)
#         thesis_name = GetThesisName().getName(address)
#         if thesis_name == None:
#             thesis_name = GetPDFName().getPDFName(address)
#             # print name
#             thesis_name = thesis_name[:len(thesis_name) - 5]
#         #print add
#         add = ChangePDFName().changePDFName(add)
#         #print add
#         return (add,thesis_name)
# #print PDFMain().main('/home/yizhiai1994/a6-roos.pdf')
class PDFMain(object):
    def pdfMain(self, src_add,dst_add):
        file_list = []
        file_list_new1 = []
        file_list_new2 = []
        #获取一个存放所有pdf文件路径的链表
        for parent, dirnames, filenames in os.walk(src_add):
            for filename in filenames:
                file_name = os.path.join(parent,filename)
                if file_name.endswith('.pdf'):
                    file_list.append(file_name)

        # 提取
        for file_name, filename in file_list:
            index_list = dst_add + '/' + 'index.txt'
            f = open(index_list, 'a')
            extract_name = dst_add + '/' + filename.strip('.pdf') + ".txt"
            str = file_name + ' to ' + extract_name
            f.writelines(str)
            f.close()
            PDFExtract().run(file_name, extract_name)





if __name__ == '__main__':
    PDFMain().pdfMain(sys.argv[1],sys.argv[2])

