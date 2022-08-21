#!/usr/bin/python3
# -*- coding:utf8 -*-
import codecs
import os
import whoosh
import jieba
from whoosh.index import create_in
from whoosh.index import open_dir
from whoosh.fields import *
from whoosh.analysis import *
from whoosh.qparser import QueryParser
from whoosh.lang.porter import stem
class CreatIndex(object):
    vocabulary_address = 'C:\\Users\\Administrator\\Desktop\\SYJ\\projectSearch\\'
    def creatIndex(self,src_folder):
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
        schema = Schema(title=TEXT, path=TEXT(stored=True), content=TEXT(stored=True,analyzer=StemmingAnalyzer(stoplist=[])))
        ix = create_in(self.vocabulary_address + "indexdir", schema)
        writer = ix.writer()
        for (parent, file_name, filename) in file_list:
            txt_file = open(file_name,'r',encoding='utf-8')
            txt_read = txt_file.readlines()
            for line in txt_read:
                #print(line)
                line = line.encode('utf-8','ignore').decode()
                writer.add_document(title=line, content=line,
                                   path=file_name)

        writer.commit()
    def searchIndexByWord(self,word):
        schema = Schema(title=TEXT(stored=True), path=TEXT(stored=True), content=TEXT)
        print(schema)
        ix = open_dir(self.vocabulary_address + "indexdir")
        print(ix)
        with ix.searcher() as searcher:
            line = "capacity"
            line = line.encode('gbk')
            query = QueryParser("title", ix.schema).parse(word)
            print(query)
            results = searcher.search(query,limit=None)
            print(results)
            for w in results:
                ww = word.split(' ')
                for www in ww:
                    if www not in w['title'].split(' '):
                        print(w['title'] + '\n')
            #print(results[12300])
    def searchIndexByList(self,grouplist):
        schema = Schema(title=TEXT(stored=True), path=TEXT(stored=True), content=TEXT)
        print(schema)
        ix = open_dir(self.vocabulary_address + "indexdir")
        print(ix)
        dictionary = {}
        with ix.searcher() as searcher:
            line = "capacity"
            line = line.encode('gbk')
            for word in grouplist:
                print(word['wordgroup'])
                query = QueryParser("title", ix.schema).parse(word['wordgroup'])
                results = searcher.search(query,limit=None)
                print(len(results))
                for result in results:
                    if result['title'] in dictionary:
                        if word['weight'] > dictionary[result['title']]['weight']:
                            dictionary[result['title']]['weight'] = word['weight']
                    else:
                        dictionary[result['title']] = {
                            'wordgroup': result['title'],
                            'weight' : word['weight']
                        }
            #print(results)
            # for w in results:
            #     ww = word.split(' ')
            #     for www in ww:
            #         if www not in w['title'].split(' '):
            #             print(w['title'] + '\n')
            #print(results[12300])
        return dictionary
    def search(self,sent):
        vocabulary = self.get_vocabulary(self.vocabulary_address + 'vocabulary.txt')
        ppl = self.get_inputPPL_ModelAll(sent)
        wordgroup = self.get_wordgroup(ppl,vocabulary)
        group = self.searchIndexByList(wordgroup)
        #wordgroup = self.sort_result(wordgroup)
        print(len(group))
    def get_vocabulary(self,vocabulary_address):
        vocabulary = {}
        file = open(vocabulary_address,'r',encoding='utf8')
        print(vocabulary_address)
        file_read = file.readlines()
        for line in file_read:
            line_tmp = line.strip('\n').strip('\r')
            line_tmp = line_tmp.split('\t')
            if line_tmp[1] in vocabulary:
                vocabulary[line_tmp[1]].append(line_tmp[0])
            else:
                li = []
                li.append(line_tmp[0])
                vocabulary[line_tmp[1]] = li
        return vocabulary
    def get_wordgroup(self,ppl_list,vocabulary):
        transfer_list = []
        wordgroup = []
        group = {}
        group_sum = 0.0
        group_no = 0
        class_num = 0
        class_No = 0
        No = 0
        flag = 1
        for word in ppl_list:
            if word in vocabulary:
                transfer_list.append(vocabulary[word])
        for wordlist in transfer_list:
            for word in wordlist:
                group[str(len(wordgroup))] = 1
                dictionary = {
                    'wordgroup' : word,
                    'NO' : len(wordgroup),
                    'class' : str(class_No),
                    'weight' : 1
                }
                wordgroup.append(dictionary)
            class_No = class_No + 1
        print(len(wordgroup))
        while flag != 0:
            flag = 0
            temp1 = 0
            sum_1 = len(wordgroup)
            while temp1 < sum_1:
                temp2 = temp1 + 1
                while temp2 < sum_1:
                    no = str(wordgroup[temp1]['NO']) + ' ' + str(wordgroup[temp2]['NO'])
                    if no in group:
                        #print(no)
                        temp2 = temp2 + 1
                        continue
                    else:
                        classno1 = wordgroup[temp1]['class'].split(' ')
                        classno2 = wordgroup[temp2]['class'].split(' ')
                        f = 0
                        for c in classno1:
                            # print('classno1:')
                            # print(classno1)
                            # print('\n')
                            # print('classno2:')
                            # print(classno2)
                            # print('\n')
                            if c in classno2:
                                f = 1
                                break
                            for cc in classno2:
                                if int(c) >int(cc):
                                    f = 1
                                    break
                            if f == 1:
                                break
                        if f == 1:
                            temp2 = temp2 + 1
                            continue
                        if wordgroup[temp1]['weight'] + wordgroup[temp1]['weight'] >len(transfer_list):
                            temp2 = temp2 + 1
                            continue
                        dictionary = {
                            'wordgroup' : wordgroup[temp1]['wordgroup'] + ' ' + wordgroup[temp2]['wordgroup'],
                            'NO':len(wordgroup),
                            'class' : wordgroup[temp1]['class'] + ' ' + wordgroup[temp2]['class'],
                            'weight' :  wordgroup[temp1]['weight'] +  wordgroup[temp2]['weight']
                        }
                        wordgroup.append(dictionary)
                        temp2 = temp2 + 1
                        group[no] = 1
                        flag = 1
                temp1 = temp1 + 1
            sum_1 = len(wordgroup)
        return wordgroup

    def sort_result(self,result_list):
        new_list = []
        for result in result_list:
            if len(new_list) == 0:
                new_list.append(result)
            else:
                temp = 0
                while result_list[temp]['weight'] > result['weight']:
                    temp = temp + 1
                new_list.insert(temp,result)
        return new_list



    def get_inputPPL_ModelAll(self,inputWord):
        ppl_list = jieba.cut(inputWord,cut_all=True)
        return ppl_list
    def get_inputPPL_ModelAcc(self,inputWord):
        ppl_list = jieba.cut(inputWord,cut_all=False)
        return ppl_list


CreatIndex().creatIndex('C:\\Users\\Administrator\\Desktop\\SYJ\\cleanedSent')
#CreatIndex().searchIndexByWord('computer is')
#CreatIndex().search('爱世界和平')
# def a():
#     schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT)
#     ix = create_in("indexdir", schema)
#     writer = ix.writer()
#     txt_file = open('/home/py35/Downloads/sent/C__Users_Administrator_Desktop_SYJ_PDF_Proceeding_ACL_ACL2010P10-1000.txt','r',encoding='gbk')
#     txt_read = txt_file.readlines()
#     for line in txt_read:
#         writer.add_document(title=line, path=u"/a",
#                         content=line)
#     writer.commit()
# a()
# schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT)
# ix = open_dir("indexdir")
# with ix.searcher() as searcher:
#     query = QueryParser("content", ix.schema).parse("conference")
#     results = searcher.search(query)
#     print(results)
#     for i in results:
#         print(i)
