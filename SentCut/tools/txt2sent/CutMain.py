# Author:Sun Yujian
import sys
import os
#sys.path.append("/home/py35/PycharmProjects/SentSearch")
from tools.txt2sent.Clean import Clean
from tools.txt2sent.DelSimil import DelSimil
import os
import os.path

class CutMain(object):
    def cutMain(self,file_list_extract,model_num):
        num = 0
        # 获取一个存放所有文件路径的链表

        if model_num == '1':
            for filename in file_list_extract:
                Clean().main(filename)
        elif model_num == '2':
            for filename in file_list_extract:
                #print(file_list)
                num = num + 1
                remind = len(file_list_extract) - num
                print('开始清洗:' + filename + '  剩余:'+str(remind)+'个')
                Clean().main(filename)
                name = filename
                name = name.strip('.txt')
                if not os.path.exists(name + '.txt'):
                    name = filename
                    name = name.rstrip('.txt')
                    if not os.path.exists(name + '.txt'):
                        name = filename
                        name = name[:-4]
                        if not os.path.exists(name + '.txt'):
                            print('1')
                            name = filename
                            name = name.replace('.txt', '')
                os.remove(name + '_clean_1.txt')
                os.remove(name + '_clean_2.txt')
                os.remove(name + '_clean_3.txt')
                os.remove(name + '_clean_4.txt')
                os.remove(name + '_clean_5.txt')
                #os.remove(name + '_clean_Incomplete.txt')
                os.remove(name + '_clean_Incomplete_temp.txt')
                name_fin = name + '_clean_6.txt'
                DelSimil().delSim(name_fin)
                name = name + '.txt'
                os.remove(name)
                os.rename(name_fin, name)
            #print(filename)


#CutMain().cutMain('/home/py35/Desktop/s1','2')