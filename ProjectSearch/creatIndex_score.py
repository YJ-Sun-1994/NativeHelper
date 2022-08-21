#!/usr/bin/python3
# -*- coding:utf-8 -*-
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
        schema = Schema(title=TEXT, path=TEXT(stored=True), content=TEXT(stored=True,analyzer=StemmingAnalyzer(stoplist=[]),sortable=True))
        ix = create_in(self.vocabulary_address + "indexdir_score", schema)
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
