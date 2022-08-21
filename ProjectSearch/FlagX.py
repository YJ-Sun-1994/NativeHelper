import csv
import os
import traceback
class FlagX(object):
    def batch_run(self,src_folder,dst_folder):
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
                save_address = dst_folder + '/' + filename
                #print('Remaining' + str(len(file_list) - num))
                FlagX().run(file_name, save_address)
                
            except BaseException as e:                                
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
        #print()
        csv_list = self.readCSV(src_address)
        csv_list = self.flagX(csv_list)
        self.writeCSV(csv_list,dst_address)
    def flagX(self,csv_list):
        num = len(csv_list)
        temp = 0
        row_length = 0
        row_num = 0
        while temp < num:
            #print(float(csv_list[temp]['minus(left1st)']))
            #print(float(csv_list[temp]['minus(left2nd)']))
            #print(float(csv_list[temp]['minus(left3rd)']))
            #print(abs(float(csv_list[temp]['minus(sizemode_word)'])))
            #print((float(csv_list[temp]['minus(left1st)']))<20 or (float(csv_list[temp]['minus(left2nd)']))<20 or (float(csv_list[temp]['minus(left3rd)']))<20) and (abs(float(csv_list[temp]['minus(sizemode_word)'])) < 1.5)
            #print(csv_list[temp]['content'][0])
            #print(csv_list[temp]['content'][-1])
            #print(not csv_list[temp]['content'][0].isupper()) and (not csv_list[temp]['content'][-1] != '-')
            if ((float(csv_list[temp]['minus(left1st)']))<20 or (float(csv_list[temp]['minus(left2nd)']))<20 or (float(csv_list[temp]['minus(left3rd)']))<20) and (abs(float(csv_list[temp]['minus(sizemode_word)'])) < 1.5):  
                if(not csv_list[temp]['content'][0].isupper()) and (csv_list[temp]['content'][-1] != '.'):
                    row_length = row_length + len(csv_list[temp]['content'])
                    row_num = row_num + 1
            temp = temp + 1
        #print(row_num)
        row_avg = float(row_length)/float(row_num)
        temp = 0
        while temp < num:
            #print(csv_list[temp]['content'])
            #print(row_avg)
            #print(len(csv_list[temp]['content']))
            if ((float(csv_list[temp]['minus(left1st)']))<20 or (float(csv_list[temp]['minus(left2nd)']))<20 or (float(csv_list[temp]['minus(left3rd)']))<20) and (abs(float(csv_list[temp]['minus(sizemode_word)'])) < 1.5) and len(csv_list[temp]['content'])<row_avg + 15:
                
                temp = temp + 1
                continue
            else:
                #row_avg = float(row_length)/float(row_length)
                #if((csv_list[temp]['minus(left1st)'])>20 and (csv_list[temp]['minus(left2nd)'])>20 and (csv_list[temp]['minus(left3rd)'])>20) and (abs(float(len(csv_list[temp]['content']) - row_avg)<5)) and  (abs(float(csv_list[temp]['minus(sizemode_word)'])) < 2):
                csv_list[temp]["flag"] = 'X'
                temp = temp + 1
                continue
        return csv_list
    def readCSV(self,csv_address):
        csv_list = []
        csv_file = open(csv_address, encoding='gb18030')
        csv_read = csv.DictReader(csv_file)
        for i in csv_read:
            csv_list.append(i)
        csv_file.close()
        return csv_list

    def writeCSV(self, csv_list, save_address):
        save_csv = save_address
        csvFile = open(save_csv, "w", newline='', encoding='gb18030')
        fileheader = ["left", "top", "fontsize", "content", "page",
                      "minus(left1st)", "minus(left2nd)", "minus(left3rd)", "minus(leftavg)",
                      "minus(sizemode_word)", "minus(sizemode_ABC)", "minus(sizeavg_word)", "minus(sizeavg_ABC)",
                      "flag"]
        dict_writer = csv.DictWriter(csvFile, fileheader)
        dict_writer.writerow(dict(zip(fileheader, fileheader)))
        for dic in csv_list:
            dic['content'] = str(dic['content'])
            dict_writer.writerow(dic)
        csvFile.close()
FlagX().batch_run('C:\\Users\\Administrator\\Desktop\\SYJ\\MergedRow','C:\\Users\\Administrator\\Desktop\\SYJ\\FlagX')
#FlagX().run('D:\\C__Users_Administrator_Desktop_SYJ_PDF_Proceeding_DKE_DKE20131-s2.0-S0169023X13000785-main.csv','D:\\123qwe.csv')
