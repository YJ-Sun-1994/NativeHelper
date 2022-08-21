#!/usr/bin/python3
# -*- coding:utf8 -*-
import codecs
import os
import re
src_folder = "C:\\Users\\Administrator\\Desktop\\SYJ\\Sent"
save_folder = "C:\\Users\\Administrator\\Desktop\\SYJ\\cleanedSent"
file_address_list = []
file_name_list = []
file_list = []
name_dict = {}
num = 0
type = 1
dictory = {}
dict_file = open("C:\\Users\\Administrator\\Desktop\\SYJ\\clean_dict.txt","r",encoding="utf8")
dict_read = dict_file.readlines()
for l in dict_read:
    for w in l:
        dictory[w] = 1
dict_file .close()
print(dictory)
for parent, dirnames, filenames in os.walk(src_folder):
    for filename in filenames:
        file_name = os.path.join(parent, filename)
        if file_name.endswith('.txt'):
            # if filename.isdigit():
            # print(file_name)
            file_address_list.append(file_name)
            file_name_list.append(filename)
            file_list.append((parent, file_name, filename))
write_content = ""
dict1 = {}
print(len(file_list))
for (parent, file_name, filename) in file_list:
    file_open = open(file_name,'r',encoding='gbk')
    file_read = file_open.readlines()
    file_write = open(save_folder + '\\' + filename,'a',encoding='utf-8')
    for line in file_read:
        if (not line[0].islower()) and len(line) >= 50 and not line[-1].isalpha():
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
