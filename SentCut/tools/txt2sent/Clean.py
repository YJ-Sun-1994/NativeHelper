#coding=utf-8
# Author:Sun Yujian
import sys
import os
import nltk
import codecs
import time
sys.path.append("/home/py35/PycharmProjects/SentSearch1_2")
from tools.txt2sent.BracketsExtract import BracketsExtract
from tools.txt2sent.WordNum import WordNum
import re
from tools.txt2sent.GetAddress import GetAddress


class Clean(object):
    #main
    time_temp = time.time()
    address = ''
    def main(self,address):
        self.address = address
        #print(address)
        cn = self.clean_1(address)
        cn = self.clean_2(cn)
        cn = self.clean_3(cn)
        cn = self.clean_4(cn)
        cn = self.clean_5(cn)
        #DelSimil().delSim(cn)
        cnn = self.clean_6(cn)

        #self.clean_incomplete(cn)
        return cnn
    # preClean
    def clean_1(self,address):
        # 使用该方法是因为经过测试如果直接打开不转换编码的话会丢失很多信息
        sum = 0
        print(address)
        f = codecs.open(address, encoding='utf-8')
        for line in f:
            sum = sum + 1
        f.close()
        f = codecs.open(address, encoding='utf-8')
        down = 0
        folder = address[:-4]
        folder_test = folder + '.txt'
        if not os.path.exists(folder_test):
            folder = address
            folder.rstrip('.txt')
            folder_test = folder + '.txt'
            if not os.path.exists(folder_test):
                folder = address
                folder.rstrip('txt')
                folder_test = folder + '.txt'
                if not os.path.exists(folder_test):
                    folder = address
                    folder.replace('.txt', '')
        clean_name = folder + '_clean_1.txt'
        a = open(clean_name, 'a', encoding='utf-8')
        for line in f:
            if down % 100 ==0:
                self.show_process(1,down,sum)
            # 规则1.1
            # 应注意的是在win下是-3，linux应为-2，因为在win下换行是\r\n而linux下为\n
            a1 = line[len(line) - 2].isdigit()
            a2 = line[len(line) - 2].isalpha()
            ##print(a1)
            if len(line) <= 30 and (a1 or a2):
                continue
            # 规则1.2
            elif line[0] == '†' or line[0] == '∗':
                continue
            elif line[len(line) - 2] == '†' or line[len(line) - 2] == '∗':
                continue
            elif re.search(r'http://', line):
                continue
            else:
                # line = line.replace("\n","")
                a.write(line)
            down = down + 1
        f.close()
        a.close()
        # 返回生成的文件地址
        cn = clean_name
        ##print(cn)
        return cn

    # mergeClean
    def clean_2(self,address):
        sum = 0
        down = 0
        f = open(address, encoding='utf-8')
        for line in f:
            sum = sum + 1
        f.close()
        f1 = open(address, encoding='utf-8')
        folder = address.strip('1.txt')
        clean_name = folder + '2.txt'
        a = open(clean_name, 'a', encoding='utf-8')
        num1 = 0
        line1 = []
        for line in f1:
            self.show_process(2, down, sum*2)
            if line == '\r\n' or line == '\n' or line == '\r':
                line1.append('1')
            else:
                line1.append('0')
            down = down + 1
        line1.append('0')
        f1.close()
        ##print(line1)
        f2 = open(address, encoding='utf-8')
        for line in f2:
            ##print(line1[num1])
            self.show_process(2, down, sum*2)
            if line1[num1] == '0' and line1[num1 + 1] == '0':
                line = line.replace("\r\n", "")
                line = line.replace("\n", "")
                line = line.replace("\r", "")
                if line[len(line) - 1].isalpha():
                    line = line + ' '
            a.writelines(line)
            num1 = num1 + 1
            down = down + 1
        f2.close()
        a.close()
        cn = clean_name
        return cn

    # bracketsClean
    def clean_3(self,address):
        sum = 0
        down = 0
        f = open(address, encoding='utf-8')
        for line in f:
            sum = sum + 1
        f.close()
        #print(sum)
        f1 = open(address, encoding='utf-8')
        folder = folder = address.strip('2.txt')
        clean_name = folder + '3.txt'
        #Incomplete_name = folder + 'Incomplete_temp.txt'
        line_Incomplete = []
        a1 = open(clean_name, 'a', encoding='utf-8')
        for line in f1:
            self.show_process(3, down, sum)
            (str1, Incomplete) = BracketsExtract().bracketsExtract_s(line)
            line_Incomplete = line_Incomplete + Incomplete
            (str2, Incomplete) = BracketsExtract().bracketsExtract_m(str1)
            line_Incomplete = line_Incomplete + Incomplete
            (str3, Incomplete) = BracketsExtract().bracketsExtract_l(str2)
            line_Incomplete = line_Incomplete + Incomplete
            a1.writelines(str3)
            down = down + 1
        f1.close()
        a1.close()
        #a2 = open(Incomplete_name, 'a')
        #sep = '\n'
        #a2.write(sep.join(line_Incomplete))
        #a2.close()

        cn = clean_name
        ##print(cn)
        return cn

    # preNLTKClean
    def clean_4(self,address):
        sum = 0
        down = 0
        f = codecs.open(address, encoding='utf-8')
        for line in f:
            sum = sum + 1
        f.close()
        f = codecs.open(address, encoding='utf-8')
        folder = address.strip('3.txt')
        clean_name = folder + '4.txt'
        a = open(clean_name, 'a', encoding='utf-8')
        raw = f.read()
        token = nltk.sent_tokenize(raw)
        for i in token:
            if down % 100 == 0:
                self.show_process(4, down, sum)
            a.write(i + '\n')
            down = down + 1
        f.close()
        a.close()
        cn = clean_name
        return cn

    # numClean
    def clean_5(self,address):
        sum = 0
        down = 0
        f = codecs.open(address, encoding='utf-8')
        for line in f:
            sum = sum + 1
        f.close()
        f = codecs.open(address, encoding='utf-8')
        folder = address.strip('4.txt')
        clean_name = folder + '5.txt'
        a = open(clean_name, 'a', encoding='utf-8')
        for line in f:
            if down % 100 ==0:
                self.show_process(5, down, sum)
            num1 = WordNum().wordNum(line)
            if num1 <= 4:
                continue
            else:
                a.writelines(line)
        down = down + 1
        f.close()
        a.close()
        cn = clean_name
        return cn

    # finalClean
    def clean_6(self,address):
        sum = 0
        down = 0
        f = open(address, encoding='utf-8')
        for line in f:
            sum = sum + 1
        f.close()
        f = open(address, encoding='utf-8')
        folder = address.strip('5.txt')
        clean_name = folder + '6.txt'
        Incomplete_name = folder + 'Incomplete_temp.txt'
        a = open(clean_name, 'a', encoding='utf-8')
        b = open(Incomplete_name, 'a', encoding='utf-8')
        for line in f:
            if down % 100 == 0:
                self.show_process(6, down, sum)
            a1 = line[0].isdigit()
            a2 = re.search('^[A-Z]$', line[0])
            a3 = line[len(line) - 2].isdigit()
            a4 = line[len(line) - 2].isalpha()
            if (a1 or a2) and not (a3 or a4):
                a.writelines(line)
                a.writelines('\n')
            else:
                b.writelines(line)
                # num1 = num1 + 1
            down = down + 1
        f.close()
        a.close()
        b.close()
        cn = (clean_name,Incomplete_name)
        return cn

    def clean_incomplete(self,address):
        folder = address.strip('5.txt')
        incomplete_temp_name = folder + 'Incomplete_temp.txt'
        incomplete_name = folder + 'Incomplete.txt'
        f = open(incomplete_temp_name, encoding='utf-8')
        a = open(incomplete_name,'a', encoding='utf-8')
        for line in f:
            if len(line) <= 30:
                continue
            else:
                a.write(line)
    def show_process(self,deal_num,down_num,sum_num):
        deal = ''
        if deal_num == 1:
            deal = '转换编码'
        elif deal_num == 2:
            deal = '合并换行'
        elif deal_num == 3:
            deal = '去除括号'
        elif deal_num == 4:
            deal = '分句'
        elif deal_num == 5:
            deal = '去除无意义数字'
        elif deal_num == 6:
            deal = '去除无意义句子'
        if time.time() - self.time_temp >= 0.3:
            sys.stdout.write(' ' * 10 + '\r')
            sys.stdout.flush()
            sys.stdout.write('当前文件:' + self.address + '  当前操作:' + deal + '   处理进度:' + str((down_num/sum_num)*100) +'%')
            sys.stdout.flush()
            sys.stdout.write(' ' * 10 + '\r')
            sys.stdout.flush()
            sys.stdout.write(' ' * 10 + '\r')
            sys.stdout.flush()
            self.time_temp = time.time()
        
#if __name__ == '__main__':
#    Clean().main(sys.argv[1])


#print Clean().clean_1('/home/yizhiai1994/PDF2TXTSW/Temp/a6-roos/Extract.txt')
#print Clean().clean_2('/home/yizhiai1994/PDF2TXTSW/Temp/a6-roos/clean_1.txt')
#print Clean().clean_3('/home/yizhiai1994/PDF2TXTSW/Temp/a6-roos/clean_2.txt')
#print Clean().clean_4('/home/yizhiai1994/PDF2TXTSW/Temp/a6-roos/clean_3.txt')
#print Clean().clean_5('/home/yizhiai1994/PDF2TXTSW/Temp/a6-roos/clean_4.txt')
#print Clean().clean_6('/home/yizhiai1994/PDF2TXTSW/Temp/a6-roos/clean_5.txt')
#Clean().main('/home/py35/Desktop/s1/_home_py35_Desktop_testPDF_LRE2005_art%3A10.1007%2Fs10579-005-7882-7.txt')
