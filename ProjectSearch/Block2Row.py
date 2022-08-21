#coding=utf-8
#'left': dic['left'],
#'top': dic['top'],
#'page': dic['page'],
#'content': dic['content'],
#'fontsize': dic['fontsize'],
#'leftest': dic_leftest,该元素所在行最左边元素的左边界
#'minus(left1st)': 当前元素所在行最左边元素左边界位置-第一多左边界,
#'minus(left2nd)': 当前元素所在行最左边元素左边界位置-第二多左边界,
#'minus(left3rd)': 当前元素所在行最左边元素左边界位置-第三多左边界,
#'minus(leftavg)': 当前元素所在行最左边元素左边界位置-左边界平均值,
#'minus(sizemode)': 当前元素大小-大小众数,
#'minus(sizeavg)': 当前元素大小-大小平均值,
#'minus(leftest)':当前元素左边界位置-当前元素所在行最左边元素左边界位置
#'flag': 标注类别
import csv
import re
import os
import io
class Block2Row(object):
    def batch_run(self,src_folder,dst_address):
        file_address_list = []
        file_name_list = []
        file_list = []
        num = 0
        index_address = src_folder + '\\' + 'index.txt'
        f = open(index_address,'a',encoding= 'gb18030')
        for parent, dirnames, filenames in os.walk(src_folder):
            for filename in filenames:
                file_name = os.path.join(parent,filename)
                if file_name.endswith('.csv'):
                    file_address_list.append(file_name)
                    file_name_list.append(filename)
                    file_list.append((parent,file_name,filename))
        for (parent,file_name,filename) in file_list:
            num = num + 1
            try:
                save_address = dst_address + '\\' + filename
                index = file_name + ' to ' + save_address
                f.writelines(index+'\n')
                print('deal with:' + file_name)
                print('processing to:' + save_address)
                print('Remaining' + str(len(file_list) - num))
                self.run(file_name,save_address)
            except BaseException as e:
                print(e)
                continue
        f.close()
    def run(self,src_address,dst_address):
        block_list = self.readCSV(src_address)
        word_list = self.initList2wordList(block_list)
        ABC_list = self.initList2ABCList(block_list)
        word_size_mode = self.get_topMode('fontsize', word_list)
        word_size_ave = self.get_average('fontsize', word_list)
        ABC_size_mode = self.get_topMode('fontsize', ABC_list)
        ABC_size_ave = self.get_average('fontsize', ABC_list)
        row_list = self.merge2row(block_list)
        left_ave = self.get_average('left', row_list)
        #print(len(row_list))
        #print(12312321312321321312312321321321321)
        left_mode = self.get_topMode('left', row_list)
        row_list = self.processRow(row_list,word_size_mode,word_size_ave,ABC_size_mode,ABC_size_ave,left_mode,left_ave)
        self.writeCSV(row_list,dst_address)

    #输入为csv地址，输出为读取的csv的字典链表
    def readCSV(self,csv_address):
        csv_list = []
        csv_file = open(csv_address, encoding='gb18030')
        csv_read = csv.DictReader(csv_file)
        for i in csv_read:
            csv_list.append(i)
            # print(i)
        return csv_list

    #将原始读取以块为最小单位的链表转化为以单词为最小单位的链表，所有属性与分割前所属的块一致,输出为list
    def initList2wordList(self,block_list):
        #strr = 'asdsa sadsad asadas asd ads'
        #strrr = strr.split(' ')
        #print(strrr)
        word_list = []
        for dict_old in block_list:

            if dict_old['content'] == None:
                continue
            if dict_old['content'] == '':
                continue
            if dict_old['left'] == None:
                continue
            if dict_old['left'] == '':
                continue
            if dict_old['fontsize'] == None:
                continue
            if dict_old['fontsize'] == '':
                continue
            if dict_old['top'] == None:
                continue
            if dict_old['top'] == '':
                continue
            content_new = dict_old['content'].split(' ')
            for word in content_new:
                #print(word)
                dict_new = {}
                dict_new['content'] = word
                dict_new['left'] = dict_old['left']
                dict_new['top'] = dict_old['top']
                dict_new['fontsize'] = dict_old['fontsize']
                word_list.append(dict_new)
        return word_list

    # 将原始读取以块为最小单位的链表转化为以单词为最小单位的链表，所有属性与分割前所属的块一致,输出为list
    def initList2ABCList(self,block_list):
        #strr = 'asdsa sadsad asadas asd ads'
        #strrr = strr.split(' ')
        #print(strrr)
        word_list = []
        for dict_old in block_list:

            if dict_old['content'] == None:
                continue
            if dict_old['content'] == '':
                continue
            if dict_old['left'] == None:
                continue
            if dict_old['left'] == '':
                continue
            if dict_old['fontsize'] == None:
                continue
            if dict_old['fontsize'] == '':
                continue
            if dict_old['top'] == None:
                continue
            if dict_old['top'] == '':
                continue
            content_new = dict_old['content']
            for word in content_new:
                #print(word)
                dict_new = {}
                dict_new['content'] = word
                dict_new['left'] = dict_old['left']
                dict_new['top'] = dict_old['top']
                dict_new['fontsize'] = dict_old['fontsize']
                word_list.append(dict_new)
        return word_list

    #获取所传链表的type众数,传入为dictionary的list,返回的是一个按众数排好序的链表
    def get_topMode(self,type,csv_list):
        dict_list = {}
        max_list = []
        # 得到需要的类型共有多少种，每种多少个，例如left有18.1818的1234个，{'18.1818':   1234}
        for i in csv_list:
            #print(type)
            #print(i[type])
            key = round(float(i[type]),2)
            if not dict_list.get(key):
                dict_list[key] = 1
            else:
                dict_list[key] = dict_list[key] + 1
        i = 0
        # 按数量排序
        #if type == 'left':
            #print(len(dict_list))
        while i <= len(dict_list):
            max_dict = {}
            max_number = 0
            max_key = ''
            for key in dict_list:
                if dict_list[key] > max_number:
                    if len(max_list) < 1:
                        max_number = dict_list[key]
                        max_key = key
                    else:
                        flag = 0
                        iii = 1
                        for ii in max_list:
                            if key != ii['key']:
                                flag = flag + 1
                            iii = iii + 1
                        if flag == len(max_list):
                           max_key = key
                           max_number = dict_list[key]
            max_dict[str(i + 1)] = i + 1
            max_dict['number'] = max_number
            max_dict['key'] = max_key
            if max_key != None and max_key != '':
                max_list.append(max_dict)
            i = i + 1
        max_list_new = []
        i = 1
        ttt = 0
        del_list = []
        #合并大小近似的众数
        for dic in max_list:

            max_dict_new = {}
            max_dict_new[str(i)] = i
            max_dict_new['number'] = dic['number']
            max_dict_new['key'] = dic['key']
            flag = 0
            for t in del_list:
                if ttt == t:
                    flag = 1
                    break
            del_list.append(ttt)
            ttt = ttt + 1
            if flag == 1:
                continue
            temp_1 = 0
            for d in max_list:
                flag = 0
                for tt in del_list:
                    if temp_1 == tt:
                        flag = 1
                        break
                temp_1 = temp_1 + 1
                if flag == 1:
                    continue
                if (dic != d) and (abs(float(dic['key']) -float(d['key'])) <= 1):
                    max_dict_new['number'] = max_dict_new['number'] + d['number']
                    del_list.append(temp_1 - 1)
            max_list_new.append(max_dict_new)
            i = i + 1
        return max_list_new

    # 获取平均值，传入为csvlist和需要得到平均值的类型如size，top，left之类的
    def get_average(self, type, csv_list):
        list_number = len(csv_list)
        type_number = 0.0
        last_number = 0.0
        for i in csv_list:
            type_number = type_number + float(i[type])
        last_number = type_number / list_number
        return last_number

    def merge2row(self,block_list):
        row_list = []
        flag = 0
        top_temp = 0.0
        num_temp = 0.0
        size_temp = 0.0
        dict_temp = {}
        for temp in block_list:
            #print(temp)
            if temp['content'] == None:
                continue
            if temp['content'] == '':
                continue
            if temp['left'] == None:
                continue
            if temp['left'] == '':
                continue
            if temp['fontsize'] == None:
                continue
            if temp['fontsize'] == '':
                continue
            if temp['top'] == None:
                continue
            if temp['top'] == '':
                continue
            if flag == 0:
                flag = 1
                dict_temp = temp
                top_temp = float(temp['top'])
                num_temp = 1.0
                size_temp = float(temp['fontsize'])
                continue
            if abs(top_temp - float(temp['top'])) <= 2:

                dict_temp['content'] = dict_temp['content'] + ' ' + temp['content']
                num_temp = num_temp + 1
                size_temp = size_temp + float(temp['fontsize'])
            else:

                dict_temp['fontsize'] = size_temp/num_temp
                #print(dict_temp['content'])
                row_list.append(dict_temp)
                dict_temp = temp
                top_temp = float(temp['top'])
                size_temp = float(temp['fontsize'])
                num_temp = 1.0
        row_list.append(dict_temp)
        return row_list

    def processRow(self,row_list,word_size_mode,word_size_ave,ABC_size_mode,ABC_size_ave,left_mode,left_ave):
        new_list = []
        for r in row_list:
            if left_mode[0] != None and left_mode[0]['key'] != '':
                r['minus(left1st)'] = abs(float(r['left']) - float(left_mode[0]['key']))
            else:
                return None
            if left_mode[1] != None and left_mode[1]['key'] != '':
                if float(float(left_mode[1]['number'])/float(left_mode[0]['number'])) >= 0.7:
                    r['minus(left2nd)'] = abs(float(r['left']) - float(left_mode[1]['key']))
                else:
                    r['minus(left2nd)'] = abs(float(r['left']) - 0)
            else:
                r['minus(left2nd)'] = abs(float(r['left']) - 0)
            if left_mode[2] != None and left_mode[2]['key'] != '':
                if float(float(left_mode[2]['number']) / float(left_mode[0]['number'])) >= 0.7:
                    r['minus(left3rd)'] = abs(float(r['left']) - float(left_mode[2]['key']))
                else:
                    r['minus(left3rd)'] = abs(float(r['left']) - 0)
            else:
                r['minus(left3rd)'] = abs(float(r['left']) - 0)
            r['minus(leftavg)'] = abs(float(r['left']) - float(left_ave))
            if word_size_mode[0] == None or word_size_mode[0] == '' or ABC_size_mode[0] == None or ABC_size_mode[0] == '':
                return None
            r['minus(sizemode_word)'] = abs(float(r['fontsize']) - float(word_size_mode[0]['key']))
            r['minus(sizemode_ABC)'] = abs(float(r['fontsize']) - float(ABC_size_mode[0]['key']))
            #print(word_size_ave)
            r['minus(sizeavg_word)'] = abs(float(r['fontsize']) - float(word_size_ave))
            r['minus(sizeavg_ABC)'] = abs(float(r['fontsize']) - float(ABC_size_ave))
            r['flag'] = ''
            new_list.append(r)
            #print(r['content'])
        return new_list

    def writeCSV(self,csv_list,save_address):
        save_csv = save_address
        csvFile = open(save_csv, "w", newline='', encoding='gb18030')
        # 文件头以列表的形式传入函数，列表的每个元素表示每一列的标识
        fileheader = ["left", "top", "fontsize", "content", "page",
                      "minus(left1st)","minus(left2nd)","minus(left3rd)","minus(leftavg)",
                      "minus(sizemode_word)","minus(sizemode_ABC)","minus(sizeavg_word)","minus(sizeavg_ABC)","flag"]
        dict_writer = csv.DictWriter(csvFile, fileheader)

        # 但是如果此时直接写入内容，会导致没有数据名，所以，应先写数据名（也就是我们上面定义的文件头）。
        # 写数据名，可以自己写如下代码完成：

        dict_writer.writerow(dict(zip(fileheader, fileheader)))
        #print(len(csv_list))
        # 之后，按照（属性：数据）的形式，将字典写入CSV文档即可
        for dic in csv_list:
            # dic['content'] = dic['content'].encode()
            # dic['content'] = dic['content'].encode(encoding);
            # dic['content'] = dic['content'].decode('gbk', 'ignore')
            # print(dic)
            dic['content'] = str(dic['content'])
            # print(dic['content'])
            dict_writer.writerow(dic)
        csvFile.close()
Block2Row().batch_run('C:\\Users\\Administrator\\Desktop\\SYJ\\Block','C:\\Users\\Administrator\\Desktop\\SYJ\\csv')
