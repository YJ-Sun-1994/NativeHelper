#!/usr/bin/python3
# -*- coding:utf8 -*-
import codecs
import os
import csv
import re
import io
import traceback
import sys



class NewPara(object):
    def run(self,src_folder1,src_folder2,dst_folder):
        file_address_list = []
        file_name_list = []
        file_list = []
        num = 0
        dictory = {}
        dict_file = open("C:\\Users\\Administrator\\Desktop\\SYJ\\clean_dict.txt","r",encoding="utf8")
        dict_read = dict_file.readlines()
        for l in dict_read:
            for w in l:
                dictory[w] = 1
        dict_file.close()
        for parent, dirnames, filenames in os.walk(src_folder1):
            for filename in filenames:
                file_name = os.path.join(parent,filename)
                if file_name.endswith('.csv'):
                    file_address_list.append(file_name)
                    file_name_list.append(filename)
                    file_list.append((parent,file_name,filename))
        for (parent,file_name,filename) in file_list:
            csv_content = self.readCSV(file_name)
            name = ''
            #print(file_name)
            #print(csv_content[0])
            if len(csv_content) < 1:
                continue
            page = int(csv_content[0]['page'])
            max = 0.0
            for line in csv_content:
                if page != int(line['page']):
                    break
                #print(line)
                #print(max)
                if line['fontsize']=='' or line['left']=='' or line['content']=='' or line['top']=='':
                    continue 
                if abs(float(line['fontsize'])-max)<5:
                    name = name + line['content']
                elif max < float(line['fontsize']):
                    max = float(line['fontsize'])
                    name = line['content']
            file_name2 = src_folder2 + '\\' + filename.replace("csv", 'txt')
            if not os.path.exists(file_name2):
                continue
            file_open = open(file_name2,'r',encoding='gbk')
            file_read = file_open.readlines()
            print(file_name2)
            name = name.replace("\t", '')
            name = name.replace("\r", '')
            name = name.replace("\\", ' ')
            name = name.replace("/", ' ')
            name = name.replace(":", ' ')
            name = name.replace("\"", ' ')
            name = name.replace("<", ' ')
            name = name.replace(">", ' ')
            name = name.replace("|", ' ')
            name = name.replace(".", ' ')
            name = name.replace("?", ' ')
            name = name.replace("*", ' ')
            if len(name) > 50:
                name = name[0:49]
            file_write = open(dst_folder + '\\' + name +'.txt','a',encoding='utf-8')
            for line in file_read:
                if (1):
                    space_flag = 0
                    hyphen_flag = 0
                    for word in line:
                        if word == ' ':
                            if space_flag == 1:
                                continue
                            elif hyphen_flag == 1:
                                continue
                            else:
                                space_flag = 1
                        else:
                            space_flag = 0
                        if word == '-':
                            hyphen_flag = 1
                        else:
                            hyphen_flag = 0
                        if word not in dictory:
                            file_write.write(word)
                        else:
                            file_write.write(" X ")
            #file_write.write('\n')
            file_write.close()
            file_open.close()

    def readCSV(self,csv_address):
        maxInt = sys.maxsize
        decrement = True
        while decrement:
    # decrease the maxInt value by factor 10 
    # as long as the OverflowError occurs.

            decrement = False
            try:
                csv.field_size_limit(maxInt)
            except OverflowError:
                maxInt = int(maxInt/10)
                decrement = True

        csv_list = []
        csv_file = open(csv_address, encoding='gb18030')
        csv_read = csv.DictReader(csv_file)
        for i in csv_read:
            csv_list.append(i)
            # print(i)
        csv_file.close()
        return csv_list
NewPara().run(r'C:\Users\Administrator\Desktop\SYJ\Block',r'C:\\Users\\Administrator\\Desktop\\SYJ\\MergePara',r'C:\Users\Administrator\Desktop\SYJ\SearchedPara')