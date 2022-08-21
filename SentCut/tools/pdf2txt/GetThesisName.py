# Author:Sun Yujian
from PyPDF2 import PdfFileWriter, PdfFileReader
import io
import sys
import io
import getopt

from tools.GetAddress import GetAddress
from pdfminer.pdfparser import PDFParser,PDFPage,PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator,TextConverter
from pdfminer.cmapdb import CMapDB
from pdfminer.pdfdevice import PDFDevice
from pdfminer.layout import LAParams, LTTextBox, LTTextLine, LTFigure, LTImage, LTChar,LTLine,LTAnon,LTText,LTCurve,LTItem


class GetThesisName(object):
    def getName(self,address):
        input1 = PdfFileReader(io.open(address, "rb"))
        title = input1.getDocumentInfo().title
        #还可以按照单词是否有意义或者单词个数是否大于2来决定是否用title属性里的名字
        #若title属性中的名字含有类似.的禁止词汇或者title属性为空则不用
        i = 0
        if title == None:
            title = self.getName2(address)
            title = title.strip('\n')
        else:
            while i< len(title):
                if title[i] == '.':
                    title = self.getName2(address)
                    title = title.strip('\n')
                    break
                i = i + 1
        return title
    def getName2(self,address):
        try:
            fp = open(address, 'rb')
            parser = PDFParser(fp)
            doc = PDFDocument(parser)
            parser.set_document(doc)
            doc.set_parser(parser)
            doc.initialize('')
            rsrcmgr = PDFResourceManager()
            laparams = LAParams()
            device = PDFPageAggregator(rsrcmgr, laparams=laparams)
            interpreter = PDFPageInterpreter(rsrcmgr, device)
            text_content = []
            str = ''
            for page in doc.get_pages():
                #print(page)
                interpreter.process_page(page)
                layout = device.get_result()
                #print(layout)
                for lt_obj in layout:

                    if isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine):
                        #flag_newline表示之前换行了
                        flag_newline = 1
                        flag_start = 0
                        for lt in lt_obj:
                            #print('*****************')
                            #print(lt)


                            str2 = lt.get_text()
                            if str2.endswith('\n') and str2[0]!= '\n':
                                str2 = str2.strip('\n')
                                #str2 = self.to_bytestring(str2)
                                if flag_newline == 1:
                                    if str2[0] == '-':
                                        str = str + str2
                                    elif str2[0].isupper():
                                        str = str + '\n'
                                        text_content.append(str)
                                        str = str2
                                    elif str2[0]!='-':
                                        str = str + str2
                                    else:
                                        str = str + ' ' + str2
                                else:
                                    str =str + str2
                                flag_newline = 1
                            else:
                                if flag_newline == 1:
                                    flag_newline = 0
                                    if str2[0] == '-':
                                        str = str + str2
                                    elif str2[0].isupper():
                                        str = str + '\n'
                                        text_content.append(str)
                                        str = str2
                                    elif str2[0]!='-':
                                        str = str + str2
                                    else:
                                        str = str + ' ' + str2
                                else:
                                    str =str + str2

                    elif isinstance(lt_obj, LTChar) or isinstance(lt_obj, LTText):
                        #print(lt_obj.get_text())

                        if str.endswith('\n') :
                            str = str+self.to_bytestring(lt_obj.get_text())
                            text_content.append(str)
                            str = ''
                            #print(str)

                        else:
                            str = str + self.to_bytestring(lt_obj.get_text())
                break
            fp.close()
            for i in text_content:
                str3 = i
                if self.abc_number(str3) > 20 :
                    if len(str3)>200:
                        return str3[0:200]
                    else:
                        return str3
            #print(text_content)
        except IOError:
            pass
        return None

    def to_bytestring(self,s, enc='utf-8'):
        if s:
            # print s
            if isinstance(s, str):
                return s
            else:
                return s.encode(enc)

    def abc_number(self,str):
        i = 0
        number = 0
        while i < len(str) :
            #print(str[i])
            if str[i].isalpha():
                number = number + 1
            i = i + 1
        return number

# if __name__ == '__main__':
#     #out = GetThesisName()
#     print ("Title:"+out.getName(sys.argv[1]))
#test = GetThesisName()
#GetThesisName().getName('/home/py35/Desktop/PDF/a5-chiang.pdf')
#GetThesisName().getName2('/home/py35/Desktop/PDF/art%3A10.1007%2Fs10032-009-0083-y.pdf')
#GetThesisName().abc_number('/home/py35/Desktop/PDF/a5-chiang.pdf.pdf')