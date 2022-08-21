#coding=utf-8
import csv
import os
import io
import traceback
class Row2Para(object):
    def batch_run(self, src_folder, dst_folder):
        file_address_list = []
        file_name_list = []
        file_list = []
        num = 0
        error_num = 0
        for parent, dirnames, filenames in os.walk(src_folder):
            for filename in filenames:
                file_name = os.path.join(parent, filename)
                if file_name.endswith('.csv'):
                    file_address_list.append(file_name)
                    file_name_list.append(filename)
                    file_list.append((parent, file_name, filename))
        for (parent, file_name, filename) in file_list:
            num = num + 1
            try:
                save_address = dst_folder + '/' + filename[:-4] + '.txt'
                print('Remaining' + str(len(file_list) - num))
                self.run(file_name, save_address)
            except BaseException as e:
                # print(file_name)
                error_num = error_num + 1
                error_file = dst_folder + '/error.txt'
                error_open = open(error_file, 'a')
                error_open.write('errornum:' + str(error_num) + '\n')
                error_open.write(file_name)
                error_open.write(traceback.format_exc())
                error_open.close()
                # break
                continue
    def run(self,src_address,dst_address):
        csv_list = self.readCSV(src_address)
        csv_list = self.row2Para(csv_list)
        self.writeTXT(csv_list,dst_address)
    def row2Para(self,csv_list):
        para = ''
        para_list = []
        row_length = 0
        row_num = 0
        temp = 0
        for i in csv_list:
            if i['flag'] == 'X':
                temp = temp + 1
            elif i['flag'] == 'B':
                para_list.append(para)
                para = i['content']
                temp = temp + 1
            elif i['flag'] == 'E':
                para = para + ' ' +  i['content']
                para_list.append(para)
                para = ''
                temp = temp + 1
            else:
                para = para + ' ' + i['content']
                temp = temp + 1

            if(temp+1==len(csv_list)):
                para_list.append(para)
        print(para_list)
        return para_list
    def readCSV(self,csv_address):
        csv_list = []
        csv_file = open(csv_address, encoding='gb18030')
        csv_read = csv.DictReader(csv_file)
        for i in csv_read:
            csv_list.append(i)
        csv_file.close()
        return csv_list

    def writeTXT(self, txt_list, save_address):
        save_txt = save_address
        txtFile = open(save_txt, "a")
        for i in txt_list:
            txtFile.write(i.encode().decode('gbk','ignore'))
            txtFile.write('\n')
        txtFile.close()
Row2Para().batch_run('C:\\Users\\Administrator\\Desktop\\SYJ\\FlagB','C:\\Users\\Administrator\\Desktop\\SYJ\\MergePara')
#Row2Para().run('D:\\C__Users_Administrator_Desktop_SYJ_PDF_Proceeding_ACL_ACL2011P11-2050.csv','D:\\111111.txt')
