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
                print('Remaining' + str(len(file_list) - num))
                FlagX().run(file_name, save_address)
                
            except BaseException as e:
                #print(file_name)
                error_num = error_num + 1
                error_file = dst_folder + '/error.txt'
                error_open = open(error_file,'a')
                error_open.write('errornum:' + str(error_num) + '\n')
                error_open.write(file_name)
                error_open.write(traceback.format_exc())
                error_open.close()
                #break
                continue
    def run(self,src_address,dst_address):
        #print()
        csv_list = self.readCSV(src_address)
        csv_list = self.flagB(csv_list)
        self.writeCSV(csv_list,dst_address)
    def flagB(self,csv_list):
        num = len(csv_list)
        temp = 0
        row_length = 0
        row_left = 0
        row_num = 0
        while temp < num:
            #print(csv_list[temp])
            if csv_list[temp]['flag'] == 'X':
                temp = temp + 1
                continue
            if ((not csv_list[temp]['content'][-1]=='.') or (len(csv_list[temp]['content'])>1 and not (csv_list[temp]['content'][-2]=='.' and
                 (csv_list[temp]['content'][-1]=='\r' or csv_list[temp]['content'][-1]=='\n'))or
                 (len(csv_list[temp]['content'])>2 and not (csv_list[temp]['content'][-3]=='.' and
                  (csv_list[temp]['content'][-1]=='\r' or csv_list[temp]['content'][-1]=='\n')) and
                 (csv_list[temp]['content'][-2]=='\r' or csv_list[temp]['content'][-2]=='\n')))) and len(csv_list[temp]['content'])>50 and csv_list[temp]['flag'] != 'X' and not csv_list[temp]['content'][0].isupper():
                if float(csv_list[temp]['minus(left1st)'])<20:
                    row_left = row_left + float(csv_list[temp]['minus(left1st)'])
                elif float(csv_list[temp]['minus(left2nd)'])<20:
                    row_left = row_left + float(csv_list[temp]['minus(left2nd)'])
                elif float(csv_list[temp]['minus(left3rd)'])<20:
                    row_left = row_left + float(csv_list[temp]['minus(left3rd)'])
                row_length = row_length + len(csv_list[temp]['content'])
                row_num = row_num + 1
            temp =temp + 1
        length_avg = float(row_length) / float(row_num)
        left_avg = float(row_left) / float(row_num)
        temp = 0
        while temp < num:
            if csv_list[temp]['flag'] == 'X':
                temp = temp + 1
                continue
            if (float(csv_list[temp]['minus(left1st)'])<20 and float(csv_list[temp]['minus(left1st)']) >3) or (float(csv_list[temp]['minus(left2nd)'])<20 and float(csv_list[temp]['minus(left2nd)']) >3) or (float(csv_list[temp]['minus(left3rd)'])<20 and float(csv_list[temp]['minus(left3rd)']) >3) and csv_list[temp]['flag'] != 'X':
                if csv_list[temp]['content'][0].isupper():
                    t = 0
                    flag_temp = 0
                    while flag_temp != 1:
                        if csv_list[temp + 1]['content'][t] != ' ' and csv_list[temp + 1]['content'][t] != '-':
                            flag_temp = 1
                            if not csv_list[temp + 1]['content'][t].isupper():
                                csv_list[temp]['flag'] = 'B'                            
                        else:
                            t = t + 1
            
            if len(csv_list[temp]['content'])<(length_avg - 10):
                if csv_list[temp]['content'][-1] == '.' or (len(csv_list[temp]['content'])>1 and csv_list[temp]['content'][-2] == '.'and
                 (csv_list[temp]['content'][-1]=='\r' or csv_list[temp]['content'][-1]=='\n')) or(len(csv_list[temp]['content'])>2 and 
                     csv_list[temp]['content'][-3]=='.' and
                  (csv_list[temp]['content'][-1]=='\r' or csv_list[temp]['content'][-1]=='\n') and
                 (csv_list[temp]['content'][-2]=='\r' or csv_list[temp]['content'][-2]=='\n')):
                    t = 0
                    flag_temp = 0
                    if temp+1<len(csv_list):
                        while flag_temp != 1 and t<len(csv_list[temp + 1]['content']) :
                            if csv_list[temp + 1]['content'][t] != ' ':
                                flag_temp = 1
                                if csv_list[temp + 1]['content'][t].isupper():
                                    csv_list[temp]['flag'] = 'E'                            
                            else:
                                t = t + 1
            temp = temp + 1
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
FlagX().batch_run('C:\\Users\\Administrator\\Desktop\\SYJ\\FlagX','C:\\Users\\Administrator\\Desktop\\SYJ\\FlagB')
