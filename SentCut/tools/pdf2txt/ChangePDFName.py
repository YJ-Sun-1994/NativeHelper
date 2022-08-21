# Author:Sun Yujian
import os
import sys
from tools.pdf2txt.GetUsrName import GetUsrName
from tools.pdf2txt.GetPDFName import GetPDFName
from tools.pdf2txt.GetThesisName import GetThesisName
class ChangePDFName(object):
    def changePDFName(self,address):
        name = GetThesisName().getName(address)
        #print address
        if name == None:
            name = GetPDFName().getPDFName(address)
            #print name
            name = name[:len(name)-5]

        old_name = os.path.basename(address)
        pdf_folder = address.strip(old_name)
        new_name = pdf_folder + name + '.pdf'

        os.rename(address,new_name)

        return new_name
# if __name__ == '__main__':
#     ChangePDFName().changePDFName(sys.argv[1])
#ChangePDFName().changePDFName('/home/py35/Desktop/PDF/a5-chiang.pdf')