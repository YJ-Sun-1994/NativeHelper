#!/usr/bin/python3
# -*- coding:utf-8 -*-
import io
import os
from whoosh.index import open_dir
from whoosh.fields import *
from whoosh.query import *
from whoosh.analysis import *
def get_wordtimes(src_address,dst_address,indexdir_address):
    src_open = open(src_address,'r',encoding='utf-8')
    src_read = src_open.readlines()
    word_list = []
    for word in src_read:
        word = word.replace('\n','').replace('\r','')
        word_list.append(word)
    src_open.close()
    dst_open = open(dst_address,'a',encoding='utf-8')
    ix = open_dir(indexdir_address)
    schema = Schema(title=TEXT(stored=True), path=TEXT(stored=True), init=TEXT(stored=True), content=TEXT(stored=True,analyzer=StemmingAnalyzer(stoplist=[]),sortable=True), sentstem=TEXT(stored=True), para=TEXT(stored=True))
    searcher = ix.searcher()
    temp = 0
    for word in word_list:
        if temp%1000 == 0:
            print(len(word_list) - temp)
        query = Term('sentstem',word)
        results = searcher.search(query)
        s = word + '\t' + str(len(results)) + '\n'
        dst_open.writelines(s)
        temp = temp + 1
        #if len(results)!=0:
            #print(word)
            #print(len(results))
    searcher.close()
    dst_open.close()
get_wordtimes('C:\\Users\\Administrator\\Desktop\\SYJ\\projectSearch\\NTS_January\\stemtimes\\vocabulary10.txt','C:\\Users\\Administrator\\Desktop\\SYJ\\projectSearch\\NTS_January\\stemtimes\\save3.txt','C:\\Users\\Administrator\\Desktop\\SYJ\\projectSearch\\NTS_January\\indexdir')
get_wordtimes('C:\\Users\\Administrator\\Desktop\\SYJ\\projectSearch\\NTS_January\\stemtimes\\vocabulary11.txt','C:\\Users\\Administrator\\Desktop\\SYJ\\projectSearch\\NTS_January\\stemtimes\\save3.txt','C:\\Users\\Administrator\\Desktop\\SYJ\\projectSearch\\NTS_January\\indexdir')
get_wordtimes('C:\\Users\\Administrator\\Desktop\\SYJ\\projectSearch\\NTS_January\\stemtimes\\vocabulary12.txt','C:\\Users\\Administrator\\Desktop\\SYJ\\projectSearch\\NTS_January\\stemtimes\\save3.txt','C:\\Users\\Administrator\\Desktop\\SYJ\\projectSearch\\NTS_January\\indexdir')
get_wordtimes('C:\\Users\\Administrator\\Desktop\\SYJ\\projectSearch\\NTS_January\\stemtimes\\vocabulary13.txt','C:\\Users\\Administrator\\Desktop\\SYJ\\projectSearch\\NTS_January\\stemtimes\\save3.txt','C:\\Users\\Administrator\\Desktop\\SYJ\\projectSearch\\NTS_January\\indexdir')
get_wordtimes('C:\\Users\\Administrator\\Desktop\\SYJ\\projectSearch\\NTS_January\\stemtimes\\vocabulary14.txt','C:\\Users\\Administrator\\Desktop\\SYJ\\projectSearch\\NTS_January\\stemtimes\\save3.txt','C:\\Users\\Administrator\\Desktop\\SYJ\\projectSearch\\NTS_January\\indexdir')

