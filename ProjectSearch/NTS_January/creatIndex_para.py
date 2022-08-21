#!/usr/bin/python3
# -*- coding:utf-8 -*-
import codecs
import os
import whoosh
import jieba
import nltk
from whoosh.index import create_in
from whoosh.index import open_dir
from whoosh.fields import *
from whoosh.lang import porter2
from whoosh.analysis import *
from whoosh.qparser import QueryParser
from whoosh.lang.porter import stem
class CreatIndex(object):
    #vocabulary_address = 'C:\\Users\\Administrator\\Desktop\\SYJ\\projectSearch\\'
    def creatIndex(self,src_folder,indexdir_address):
        file_address_list = []
        file_name_list = []
        file_list = []
        num = 0
        for parent, dirnames, filenames in os.walk(src_folder):
            for filename in filenames:
                file_name = os.path.join(parent, filename)
                if file_name.endswith('.txt'):
                    file_address_list.append(file_name)
                    file_name_list.append(filename)
                    file_list.append((parent, file_name, filename))
        stem_ana = StemmingAnalyzer()
        #schema = fields.Schema(title=TEXT(analyzer=stem_ana, stored=True),
                               #content=TEXT(analyzer=stem_ana))
        schema = Schema(title=TEXT(stored=True), path=TEXT(stored=True), init=TEXT(stored=True,analyzer=StandardAnalyzer(stoplist=[])), content=TEXT(stored=True,analyzer=StemmingAnalyzer(stoplist=[]),sortable=True), sentstem=TEXT(stored=True,analyzer=StandardAnalyzer(stoplist=[])),rootstem=TEXT(stored=True,analyzer=StandardAnalyzer(stoplist=[])), para=TEXT(stored=True),splitspace=TEXT(stored=True))
        ix = create_in(indexdir_address, schema)
        writer = ix.writer()
        for (parent, file_name, filename) in file_list:
            txt_file = open(file_name,'r',encoding='utf-8')
            txt_read = txt_file.readlines()
            para_list = []
            for paragraph in txt_read:
                #print(line)
                sent_list = []
                temp = 0
                sentences = nltk.sent_tokenize(paragraph)
                #print(len(sentences))
                #print(sentences)
                ttemp = -1 # ttemp = the number of readed line, it will compare with the number of sentences and get the lable of the end of sentences
                for line in sentences:
                    ttemp = ttemp + 1
                    line = line.encode('utf-8', 'ignore').decode()
                    if len(sent_list) == 0:
                        sent_list.append(line)
                    else:
                        temp = len(sent_list) - 1
                        #print(temp)
                        #print(sent_list[temp])
                        #﻿ 上一行过短
                        # 上一行数字或者字母结尾
                        # 本行非大写字母开头
                        # 本行太短
                        # 太短是指以空格切分后数量小于10
                        str_front = sent_list[temp]
                        str_now = line
                        num_front = len(str_front.split(' '))
                        num_now = len(str_now.split(' '))
                        #print(num_front)
                        #print(sent_list[temp].replace(' ','')[-1])
                        if num_front < 11:
                            sent_list[temp] = sent_list[temp] + ' ' + line
                            #print(111)
                            continue
                        elif sent_list[temp].replace(' ','')[-1].isalpha() or sent_list[temp].replace(' ','')[-1].isdigit() or sent_list[temp].replace(' ','')[-1].isspace():
                            sent_list[temp] = sent_list[temp] + ' ' + line

                            continue
                        elif not line[0].isupper():
                            for i in line:
                                if i.isalpha():
                                    if i.isupper():
                                        sent_list.append(line)

                                        break
                                    else:
                                        sent_list[temp] = sent_list[temp] + ' ' + line

                                        break
                            continue
                        elif num_now < 11  :
                            if ttemp < len(sentences)-1:
                                sent_list.append(line)
                            else:
                                sent_list[temp] = sent_list[temp] + ' ' + line
                            continue
                        else:
                            sent_list.append(line)

                temp = 0
                #print(len(sent_list))
                #print(sent_list)
                for line in sent_list:
                    context = ''
                    root_stem = ''
                    split_space = ''
                    line = line.replace('- ','')
                    s1 = line.lower().split(' ')
                    s2 = []
                    sent_stem = ''
                    for w1 in s1:
                        w2 = ''
                        for w3 in w1:
                            if w3.isalpha():
                                w2 = w2 + w3
                        s2.append(w2)
                    for w2 in s2:
                        s2 = porter2.stem(w2)
                        sent_stem = sent_stem + ' ' + s2
                        split_space = split_space + ' ' + w2
                        w3 = porter2.stem(w2)
                        while w3 != porter2.stem(w3):
                            w3 = porter2.stem(w3)
                        root_stem = root_stem + ' ' + w3
                    #print(line + '\n')
                    #print(sent_stem + '\n')
                    if len(sent_list) <= 5:
                        context = paragraph
                    else:
                        if temp <= 2:
                            for i in range(0,4):
                                context = context + sent_list[i]
                        elif temp <= len(sent_list) - 1 and temp >= len(sent_list) - 5:
                            for i in range(len(sent_list)-5,len(sent_list)-1):
                                context = context + sent_list[i]
                        else:
                            for i in range(temp-2,temp+2):
                                context = context + sent_list[i]
                    context = context.replace(line,'<b>' + line + '</b>')
                    
                    writer.add_document(title=filename, init=line, content=line, path=file_name, para=context,sentstem = sent_stem,rootstem = root_stem,splitspace = split_space)
                    temp = temp + 1
                #print(len(sent_list))
                #if len(sent_list) == 0:
                    #print(paragraph)
                #print('\n')
        writer.commit()
CreatIndex().creatIndex('C:\\Users\\Administrator\\Desktop\\SYJ\\SearchedPara','C:\\Users\\Administrator\\Desktop\\SYJ\\projectSearch\\NTS_January\\indexdir')
