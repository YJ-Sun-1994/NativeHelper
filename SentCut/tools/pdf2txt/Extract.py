#coding=utf-8
# Author:Sun Yujian
import sys
import io
import codecs


from binascii import b2a_hex
from tools.GetAddress import GetAddress
from pdfminer.pdfparser import PDFParser,PDFPage,PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator,TextConverter
from pdfminer.cmapdb import CMapDB
from pdfminer.pdfdevice import PDFDevice




from pdfminer.layout import LAParams, LTTextBox, LTTextLine, LTFigure, LTImage, LTChar,LTLine,LTAnon,LTText,LTCurve,LTItem,LTRect

class PDFExtract(object):

    address = ('','')
    save_address = ''
    def extract(self,pdf_doc, fn, pdf_pwd):
        result = None
        #print pdf_doc
        try:
            ##print(pdf_doc)
            # 打开pdf文件
            fp = open(pdf_doc, 'rb')
            # 针对这个pdf文件创建一个分析（PDFParser）对象
            parser = PDFParser(fp)
            # 创建一个PDFDocument对象存储文档结构
            doc = PDFDocument(parser)
            # 连接分析和文档独享
            parser.set_document(doc)
            doc.set_parser(parser)
            doc.initialize('')
            #如果PDFDocument对象不允许被访问则报错
            #if not doc.is_extractable:
                #raise PDFTextExtractionNotAllowed
                #print ('not found file')
                #raise
            #else:
                #result = fn(doc)
            result = fn(doc)
            # 关闭pdf文件
            fp.close()
        except IOError:
            #print("the file doesn't exist or similar problem")
            pass
        return result

    # 把统一编码转换为二进制流
    def to_bytestring(self,s, enc='utf-8'):
        if s:
            # print s
            if isinstance(s, str):
                return s
            else:
                return s.encode(enc)


#旧的提取方案
    def update_page_text_hash(self,h, lt_obj, pct=0.2):
        # x0表示文本左端的位置，x1减去x0即为该类文本的宽度
        # 用BBOX中X0，X1的值得到相同宽度的元组
        # 用pct代表偏移值，因为一个段落开始处具有28.16和153.32 X0和X1的值然而该段右下方它具有29.04的X0值和152.09的x1值
        # 用散列项（hash)来存储
        x0 = lt_obj.bbox[0]
        x1 = lt_obj.bbox[2]
        #print lt_obj.get_text()
        key_found = False
        for k, v in h.items():
            hash_x0 = k[0]
            if x0 >= (hash_x0 * (1.0 - pct)) and (hash_x0 * (1.0 + pct)) >= x0:
                hash_x1 = k[1]
                if x1 >= (hash_x1 * (1.0 - pct)) and (hash_x1 * (1.0 + pct)) >= x1:
                    # LT*对象中的文本是被定为在一系列相同宽度的文本，所以他们属于一个系列
                    key_found = True
                    v.append(self.to_bytestring(lt_obj.get_text()))

                    h[k] = v
        if not key_found:
            # 这种文本是一个新的类型，因此单独建立一个散列项
            h[(x0, x1)] = [self.to_bytestring(lt_obj.get_text())]
        #print h
        return h

    def parse_lt_objs(self,lt_objs, page_number):
        # 遍历LT*对象表， 获得每一个文本数据
        text_content = []
        page_text = {}
        str = ''
        str_num = 0
        for lt_obj in lt_objs:
            if (isinstance(lt_obj, LTText) or isinstance(lt_obj, LTChar)) and not(isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine)):
                str = str + self.to_bytestring(lt_obj.get_text())
                str_num = str_num + 1

            elif isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine):
                # 基于物理列宽来提取文本
                page_text = self.update_page_text_hash(page_text, lt_obj)

            elif isinstance(lt_obj, LTFigure):
                # LTFigure 对象是其他LT* objects对象的容器，所以我们通过其子对象来递归
                text_content.append(self.parse_lt_objs(lt_obj, page_number))
            # 无空格的情况只出现在LTFigure这个对象中
            elif isinstance(lt_obj,LTLine):
                text_content.append(' ')

            elif isinstance(lt_obj,LTCurve):
                text_content.append(' ')

            elif isinstance(lt_obj, LTImage):
                text_content.append(' ')

        if str_num != 0:
            text_content.append(str)
        #print text_content
        for k, v in sorted([(key, value) for (key, value) in page_text.items()]):
            # 通过x0.x1来排序page_text的散列表，产生的是一个自上而下自左而右的顺序列
            # 并将这个顺序列添加到text_content中
            text_content.append(''.join(v))
        #write(text_content)
        # 以作为'\n'分隔符，将text_content所有的元素合并成一个新的字符串
        return '\n'.join(text_content)
        #return '\n'.join(text_content)

    # 加工页面
    def _parse_pages(self,doc):
        i = 0 #当前已处理页数
        sum = 0 #总页数
        #预处理
        rsrcmgr = PDFResourceManager()
        laparams = LAParams()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        text_content = []
        doc.get_pages()

        for page in doc.get_pages():
            sum = sum + 1

        for page in doc.get_pages():
            #输出进度
            sys.stdout.write('当前进度' + str(100 * (i / (sum*2))) + '%')
            sys.stdout.flush()
            sys.stdout.write(' ' * 10 + '\r')
            sys.stdout.flush()

            i = i+1
            interpreter.process_page(page)
            # 从页面获取LTPage
            layout = device.get_result()
            # layout 是一个 LTPage 对象，包含 LTTextBox, LTFigure, LTImage,等子对象
            text_content.append(self.parse_lt_objs(layout, i))
        self.write(text_content)
        return text_content

    def run(self,pdf_address,save_address, pdf_pwd=''):
        # 分析每个PDF文件的页面返回一个列表代表每个页所找到的文本
        print("提取"+pdf_address+ '至' + save_address )
        self.save_address = save_address
        self.address = GetAddress().getNameUsr(pdf_address)
        return self.extract(pdf_address, self._parse_pages, pdf_pwd)

    def write(self,text_content):
        f = open(self.save_address,'a', encoding='utf-8') 
        f.writelines(text_content)
        f.close()

#idea2
class PDFExtract2(object):
    address = ('', '')
    save_address = ''
    pdf_str = ""
    def extract(self, pdf_doc, fn, pdf_pwd):
        result = None
        # print pdf_doc
        try:
            ##print(pdf_doc)
            # 打开pdf文件
            fp = open(pdf_doc, 'rb')
            # 针对这个pdf文件创建一个分析（PDFParser）对象
            parser = PDFParser(fp)
            # 创建一个PDFDocument对象存储文档结构
            doc = PDFDocument(parser)
            # 连接分析和文档独享
            parser.set_document(doc)
            doc.set_parser(parser)
            doc.initialize('')
            # 如果PDFDocument对象不允许被访问则报错
            # if not doc.is_extractable:
            # raise PDFTextExtractionNotAllowed
            # print ('not found file')
            # raise
            # else:
            # result = fn(doc)
            result = fn(doc)
            # 关闭pdf文件
            fp.close()
        except IOError:
            # print("the file doesn't exist or similar problem")
            pass
        return result

    # 把统一编码转换为二进制流
    def to_bytestring(self, s, enc='utf-8'):
        if s:
            # print s
            if isinstance(s, str):
                return s
            else:
                return s.encode(enc)
# 新的提取方案

    def update_page_text_new(self, lt_obj):
        flag_newline = 1
        flag_start = 0
        text_content = []
        str = ''
        for lt in lt_obj:
            str2 = lt.get_text()
            #str2 = self.to_bytestring(str2)
            #print(lt.get_text())
            if str2.endswith('\n') and str2[0] != '\n':
                str2 = str2.strip('\n')
                if flag_newline == 1:
                    if str2[0] == '-':
                        str = str + str2
                    elif str2[0].isupper():
                        str = str + '\n'
                        text_content.append(self.to_bytestring(str))
                        str = str2
                    elif str2[0] != '-':
                        str = str + str2
                    else:
                        str = str + ' ' + str2
                else:
                    str = str + str2
                flag_newline = 1
            else:
                if flag_newline == 1:
                    flag_newline = 0
                    if str2[0] == '-':
                        str = str + str2
                    elif str2[0].isupper():
                        str = str + '\n'
                        text_content.append(self.to_bytestring(str))
                        str = str2
                    elif str2[0] != '-':
                        str = str + str2
                    else:
                        str = str + ' ' + str2
                else:
                    str = str + str2
        return text_content

    def parse_lt_objs_new(self, lt_objs, page_number):
        # 遍历LT*对象表， 获得每一个文本数据
        text_content = []
        str = ''
        str_num = 0
        for lt_obj in lt_objs:
            if (isinstance(lt_obj, LTText) or isinstance(lt_obj, LTChar)) and not (
                        isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine)):
                str = str + self.to_bytestring(lt_obj.get_text())
                str_num = str_num + 1
            elif isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine):
                text_content1 = self.update_page_text_new(lt_obj)
                text_content.extend(text_content1)
            elif isinstance(lt_obj, LTFigure):
                text_content.append(self.parse_lt_objs_new(lt_obj, page_number))
            elif isinstance(lt_obj, LTLine):
                text_content.append(' ')
            elif isinstance(lt_obj, LTCurve):
                text_content.append(' ')
            elif isinstance(lt_obj, LTImage):
                text_content.append(' ')
        if str_num != 0:
            text_content.append(str)
        return '\n'.join(text_content)


    # 加工页面
    def _parse_pages(self, doc):
        sum = 0
        down = 0
        rsrcmgr = PDFResourceManager()
        laparams = LAParams()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        text_content = []
        # for i, page in enumerate(PDFCratePage.create_pages(doc)):
        doc.get_pages()
        i = 0
        for page in doc.get_pages():
            sum = sum + 1
        for page in doc.get_pages():
            sys.stdout.write('当前进度' + str(100 * (down/sum)) + '%')
            i = i + 1
            interpreter.process_page(page)
            # 从页面获取LTPage
            layout = device.get_result()
            self.pdf_str = ''
            # layout 是一个 LTPage 对象，包含 LTTextBox, LTFigure, LTImage,等子对象
            #####text_content.append(self.parse_lt_objs(layout, (i + 1)))
            text_content.append(self.parse_lt_objs_new(layout, i))
            down = down + 1
            # print text_content
        self.write(text_content)
        return text_content

    def run(self, pdf_address, save_address, pdf_pwd=''):
        # 分析每个PDF文件的页面返回一个列表代表每个页所找到的文本
        # print pdf_doc
        self.save_address = save_address
        self.address = GetAddress().getNameUsr(pdf_address)

        # print self.address
        return self.extract(pdf_address, self._parse_pages, pdf_pwd)

    def write(self, text_content):
        # print text_content
        name = ''
        usr = ''
        #print(text_content)
        (name, usr) = self.address
        add = '/home/' + usr + '/PDF2TXTSW/Temp/' + name
        add_file = add + '/11111.txt'
        # print add
        ####if not os.path.exists(add):
        ####    os.mkdir(add)
        # print add
        ####f = open(add_file, "a")
        f = open(self.save_address, 'a')
        # path = nltk.data.find('corpora/unicode_samples/polish-lat2.txt')
        # print(len(text_content))
        f.writelines(text_content)
        # print text_content
        # print self.address
        # ff = codecs.open(f, 'a', encoding='utf-8')
        f.close()

#idea3 未完成 缺少分词工具
class PDFExtract3(object):
    address = ('', '')
    save_address = ''
    pdf_str = ""
    str_list = []
    def extract(self, pdf_doc, fn, pdf_pwd):
        result = None
        # print pdf_doc
        try:
            ##print(pdf_doc)
            # 打开pdf文件
            fp = open(pdf_doc, 'rb')
            # 针对这个pdf文件创建一个分析（PDFParser）对象
            parser = PDFParser(fp)
            # 创建一个PDFDocument对象存储文档结构
            doc = PDFDocument(parser)
            # 连接分析和文档独享
            parser.set_document(doc)
            doc.set_parser(parser)
            doc.initialize('')
            result = fn(doc)
            # 关闭pdf文件
            fp.close()
        except IOError:
            pass
        return result

    # 把统一编码转换为二进制流
    def to_bytestring(self, s, enc='utf-8'):
        if s:
            # print s
            if isinstance(s, str):
                return s
            else:
                return s.encode(enc)
# 新的提取方案

    def update_page_text_new(self, lt_obj):
        flag_newline = 1
        flag_start = 0
        text_content = []
        str = ''
        for lt in lt_obj:
            str2 = lt.get_text()
            if str2.endswith('\n') and str2[0] != '\n':
                str2 = str2.strip('\n')
                if flag_newline == 1:
                    if str2[0] == '-':
                        str = str + str2
                    elif str2[0].isupper():
                        str = str + '\n'
                        text_content.append(self.to_bytestring(str))
                        str = str2
                    elif str2[0] != '-':
                        str = str + str2
                    else:
                        str = str + ' ' + str2
                else:
                    str = str + str2
                flag_newline = 1
            else:
                if flag_newline == 1:
                    flag_newline = 0
                    if str2[0] == '-':
                        str = str + str2
                    elif str2[0].isupper():
                        str = str + '\n'
                        text_content.append(self.to_bytestring(str))
                        str = str2
                    elif str2[0] != '-':
                        str = str + str2
                    else:
                        str = str + ' ' + str2
                else:
                    str = str + str2
        return text_content

    def parse_lt_objs_new(self, lt_objs, page_number):
        # 遍历LT*对象表， 获得每一个文本数据
        text_content = []
        str = ''
        str_num = 0
        for lt_obj in lt_objs:
            if isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine):
                self.parse_lt_objs_new(lt_obj,page_number)
            elif (isinstance(lt_obj, LTText) or isinstance(lt_obj, LTChar)):
                self.pdf_str = self.pdf_str + lt_obj.get_text()
            elif (isinstance(lt_obj,LTRect)):
                self.pdf_str = self.pdf_str + ' '
            elif isinstance(lt_obj, LTFigure):
                text_content.append(self.parse_lt_objs_new(lt_obj, page_number))
            #else:
                #print(lt_obj)
        if str_num != 0:
            text_content.append(str)
        return '\n'.join(text_content)


    # 加工页面
    def _parse_pages(self, doc):
        i = 0 #当前已处理页数
        sum = 0 #总页数
        #预处理
        rsrcmgr = PDFResourceManager()
        laparams = LAParams()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        text_content = []
        doc.get_pages()
        #统计总数
        for page in doc.get_pages():
            sum = sum + 1

        for page in doc.get_pages():
            #输出进度
            sys.stdout.write('当前进度' + str(100 * ((i+sum) / (sum*2))) + '%')
            sys.stdout.flush()
            sys.stdout.write(' ' * 10 + '\r')
            sys.stdout.flush()

            i = i + 1
            interpreter.process_page(page)
            # 从页面获取LTPage
            layout = device.get_result()
            self.str_list.append(self.pdf_str)
            self.pdf_str = ''
            text_content.append(self.parse_lt_objs_new(layout, i))
        for i in self.str_list:
            self.write(i)
        sys.stdout.write('当前进度' + '100%')
        sys.stdout.flush()
        sys.stdout.write(' ' * 10 + '\r')
        sys.stdout.flush()
        return text_content

    def run(self, pdf_address, save_address, pdf_pwd=''):
        # 分析每个PDF文件的页面返回一个列表代表每个页所找到的文本
        self.save_address = save_address
        self.address = GetAddress().getNameUsr(pdf_address)
        return self.extract(pdf_address, self._parse_pages, pdf_pwd)

    def write(self, text_content):
        f = open(self.save_address,'a', encoding='utf-8')  
        f.writelines(text_content)
        f.close()

#test example
#PDFExtract().run('/home/py35/Desktop/PDF/art%3A10.1007%2Fs10032-009-0083-y.pdf','/home/py35/Desktop/PDF/art%3A10.1007%2Fs10032-009-0083-y.txt')
#PDFExtract2().run('/home/py35/Desktop/PDF/1-s2.0-S095219761500161X-main.pdf','/home/py35/Desktop/PDF/1-s2.0-S095219761500161X-main.txt')
#PDFExtract3().run('/home/py35/Desktop/PDF/11.pdf','/home/py35/Desktop/PDF/11.txt')
