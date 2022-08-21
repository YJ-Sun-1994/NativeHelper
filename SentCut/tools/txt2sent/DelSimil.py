# Author:Sun Yujian
import io
import sys
import time
class DelSimil(object):
    time_temp = time.time()
    def delSim(self,src_add):
        f = open(src_add,'r', encoding='utf-8')
        line = f.readline()
        line_list = []
        judge = 255555

        while line:
            #print(line)
            judge = 255555
            for l in line_list:
                if line == l:
                    judge = 1
                #print('***************')
                #print(judge)
                #print(l)
                #print(line)
                #print('******************')
            if judge == 255555:
                #print(line)
                line_list.append(line)
            line = f.readline()
        f.close()
        f = open(src_add,'w+', encoding='utf-8')
        f.close()
        f = open(src_add, 'a', encoding='utf-8')
        i = 0
        num = len(line_list)
        for line in line_list:
            if time.time() - self.time_temp >= 0.2:
                sys.stdout.write(' '*10 + '\r')
                sys.stdout.flush()
                sys.stdout.write('当前文件:' + src_add + '  当前操作:去除重复' + '   处理进度:' + str((i/num)*100)+'%')
                self.time_temp = time.time()
                sys.stdout.flush()
                sys.stdout.flush()
            f.writelines(line)
            f.writelines('\n')
            #print(line)
            i = i + 1
        sys.stdout.write(' ' * 10 + '\r')
        sys.stdout.flush()
        f.close()
        sys.stdout.write('当前文件:' + src_add + '  当前操作:去除重复' + '   处理进度:' + '100%\n')
#DelSimil().delSim('/home/py35/Desktop/s1/_home_py35_Desktop_testPDF_CL2005_J05-1009.txt')
