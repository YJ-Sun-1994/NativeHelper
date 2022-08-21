# Author:Sun Yujian
import shutil
import sys
import os
# sys.path.append("/home/py35/PycharmProjects/SentSearch")
from tools.pdf2txt.GetUsrName import GetUsrName
from tools.pdf2txt.GetPDFName import GetPDFName


class PDFCopy(object):
    def copyFile(self,src_add,dst_add):

        usr = GetUsrName().getUserName()
        pdf_name = GetPDFName().getPDFName(src_add)
        pdf_folder_name = pdf_name.strip('.pdf')
        new_address_folder = dst_add+'/'+pdf_folder_name
        if not os.path.exists(new_address_folder):
            os.makedirs(new_address_folder)

        new_address = new_address_folder + '/' + pdf_name
        shutil.copy(src_add,new_address)

        text_content = 'source address: ' + src_add
        text_name = new_address_folder + '/' + 'help.txt'
        f = open(text_name,'a')
        f.writelines(text_content)
        f.close()

        #print(src_add)
        #print(new_address)

        return new_address


# if __name__ == '__main__':
#     PDFCopy().copyFile(sys.argv[1],sys.argv[2])

# PDFCopy().copyFile('/home/py35/Desktop/PDF/art%3A10.1007%2Fs10032-009-0083-y.pdf','/home/py35/Desktop')