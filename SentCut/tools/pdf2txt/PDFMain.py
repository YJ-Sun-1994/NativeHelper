# Author:Sun Yujian
import sys
import os
#sys.path.append("/home/py35/PycharmProjects/SentSearch")
from tools.pdf2txt.Extract import PDFExtract,PDFExtract3
import os
import os.path
class PDFMain(object):
    def pdfMain(self, src_add,dst_add):
        down = 0
        file_list = []
        file_list_extract = []
        #获取一个存放所有pdf文件路径的链表
        for parent, dirnames, filenames in os.walk(src_add):
            for filename in filenames:
                file_name = os.path.join(parent,filename)
                if file_name.endswith('.pdf'):
                    file_list.append(file_name)
        if not os.path.exists(dst_add):
            os.makedirs(dst_add)

        #提取
        for file_name in file_list:
            print('\n剩余:' + str(len(file_list) - down) + '\n')
            extract_name = dst_add + '//' +self.renamePDF(file_name)
            extract_name = extract_name + '.txt'
            file_list_extract.append(extract_name)
            PDFExtract().run(file_name, extract_name)
            PDFExtract3().run(file_name, extract_name)
            index = dst_add + '//index.txt'
            file_index = open(index, 'a')
            file_index.write(str(file_name) + ' 对应 ' + extract_name  + '\n')
            down = down + 1

        return file_list_extract

    #去除PDF提取至的txt的文件名中的非法字符
    def renamePDF(self,str1):
        str1 =  str(str1)
        str1 = str1.strip(".pdf")
        str1 = str1.replace('/','_')
        str1 = str1.replace('\\','_')
        str1 = str1.replace(':','_')
        return str1



# if __name__ == '__main__':
#     PDFMain().pdfMain(sys.argv[1],sys.argv[2])
#PDFMain().pdfMain('/home/py35/Desktop/testPDF', '/home/py35/Desktop/s1')
