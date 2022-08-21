#coding='utf-8'
import os
import whoosh
import re
import time
import jieba
from whoosh.index import create_in
from whoosh.index import open_dir
from whoosh.fields import *
from whoosh.query import *
from whoosh.analysis import *
from whoosh.qparser import QueryParser
from whoosh.lang.porter import stem
from django.shortcuts import render
from whoosh import scoring
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import random
from django.http import HttpResponse
# Create your views here.
save_address = 'C:\\Users\\Administrator\\Desktop\\SYJ\\projectSearch\\'
vocabulary_address = 'C:\\Users\\Administrator\\Desktop\\SYJ\\projectSearch\\indexdir\\t3.txt'
vocabulary_engligsh_address = 'C:\\Users\\Administrator\\Desktop\\SYJ\\projectSearch\\indexdir\\t4.txt'
ix = open_dir(save_address+"indexdir_para")
def get_vocabulary(vocabulary_address):
    #print("building vocabulary")
    vocabulary = {}
    file = open(vocabulary_address, 'r', encoding='utf8')
    #print(vocabulary_address)
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
    #print("builded vocabulary")
    return vocabulary
def get_vocabulary_english(vocabulary_address):
    #print("building vocabulary")
    vocabulary = {}
    file = open(vocabulary_address, 'r', encoding='gbk')
    #print(vocabulary_address)
    file_read = file.readlines()
    for line in file_read:
        line_tmp = line.strip('\n').strip('\r')
        line_tmp = line_tmp.split('\t')
        if len(line_tmp) >= 2:
            if line_tmp[0] in vocabulary:
                vocabulary[line_tmp[0]] = vocabulary[line_tmp[0]] + line_tmp[1]
            else:
                li = ''
                li=line_tmp[1]
                vocabulary[line_tmp[0]] = li
    #print("builded vocabulary")
    return vocabulary
vocabulary = get_vocabulary(vocabulary_address)
vocabulary_english = get_vocabulary_english(vocabulary_engligsh_address)
def home(request):
    return render(request, 'home.html')
def search(request):
    requestData = request.GET.copy()
    search_content = str(requestData["search_content"])
    (search_result,segemented_results) = CreatIndex().search(search_content)
    results = {}
    result = []
    page = 0
    temp = 0
    for i in search_result:
        if temp < 50:
            #print(i['highlight'])
            i['id'] = 'a' + str(temp)
            result.append(i)
        else:
            temp = 0
            results[str(page)] = result
            result = []
            i['id'] = 'a' + str(temp)
            page = page + 1
            if i['highlight'] == '':
                i['highlight'] = i['wordgroup']
            result.append(i)
        temp = temp + 1
    results[str(page)] = result
    #print(results[str(0)])
    return render(request,'result.html',{'page':'0','maxpage':page,'result':results[str(0)],'search_content':search_content, 'segemented_results': segemented_results})
def nextPage(request):
    requestData = request.GET.copy()
    search_content = str(requestData["search_content"])
    (search_result,segemented_results) = CreatIndex().search(search_content)
    results = {}
    result = []
    page_cut = 0
    temp = 0
    page = int(requestData['page'])
    #print(page)
    page = page + 1
    maxpage = int(requestData['maxpage'])
    if page > maxpage:
        page = maxpage
    for i in search_result:
        if temp < 50:
            i['id'] = 'a' + str(temp)
            result.append(i)
        else:
            temp = 0
            results[str(page_cut)] = result
            result = []
            i['id'] = 'a' + str(temp)
            page_cut = page_cut + 1
            if i['highlight'] == '':
                i['highlight'] = i['wordgroup']
            result.append(i)
        temp = temp + 1
    results[str(page_cut)] = result
    return render(request, 'result.html', {'page': page, 'maxpage': maxpage, 'result': results[str(page)],'search_content': search_content, 'segemented_results': segemented_results})
def prePage(request):
    requestData = request.GET.copy()
    search_content = str(requestData["search_content"])
    (search_result,segemented_results) = CreatIndex().search(search_content)
    results = {}
    result = []
    page_cut = 0
    temp = 0
    page = int(requestData['page'])
    #print(page)
    page = page -1
    maxpage = int(requestData['maxpage'])
    if page < 0:
        page = 0
    for i in search_result:
        if temp < 50:
            i['id'] = 'a' + str(temp)
            result.append(i)
        else:
            temp = 0
            results[str(page_cut)] = result
            result = []
            i['id'] = 'a' + str(temp)
            page_cut = page_cut + 1
            if i['highlight'] == '':
                i['highlight'] = i['wordgroup']
            result.append(i)
        temp = temp + 1
    results[str(page_cut)] = result
    return render(request, 'result.html',
                  {'page': page, 'maxpage': maxpage, 'result': results[str(page)], 'search_content': search_content, 'segemented_results': segemented_results})


def listing(request):
    requestData = request.GET.copy()
    search_content = str(requestData["search_content"])
    search_result = CreatIndex().search(search_content)
    contact_list = CreatIndex().search(search_content)
    paginator = Paginator(contact_list, 25)  # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)

    return render(request, 'list.html', {'contacts': contacts})
class CreatIndex(object):
    vocabulary_address = '/home/py35/PycharmProjects/SentSearch1_2/OtherProject/indexdir/t3.txt'
    save_address = '/home/py35/PycharmProjects/SentSearch1_2/OtherProject/'
    def searchIndexByList(self,grouplist,color_dict,stem_dict):
        global vocabulary_english
        schema = Schema(title=TEXT(stored=True), path=TEXT(stored=True), content=TEXT(stored=True,analyzer=StemmingAnalyzer(stoplist=[]),sortable=True), para=TEXT(stored=True))
        #print(schema)
        #ix = open_dir(self.save_address+"indexdir")
        global ix
        #print(ix)
        #print(stem_dict)
        outcome = []
        #print(grouplist)
        with ix.searcher(weighting=scoring.BM25F()) as searcher:
            query = Or(grouplist)
            dictionary = {}
            results = searcher.search(query,limit=1000)
            print(3)
            print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
            for result in results:
                pos_list = []
                order_list = []
                replace_list = []
                highlight = ""
                pos_num = 0
                highlightwords = re.findall('<b class="match term\d">(.*?)</b>', result.highlights("content"))
                for w in highlightwords:
                    if w not in replace_list:
                        replace_list.append(w)
                for word1 in result['content'].split():
                    for word2 in replace_list:
                        if word2 in word1:
                            if word2 in vocabulary_english:
                                word1 = word1.replace(word2,'<b title="' + vocabulary_english[word2] + '" style="color:' + color_dict[stem(word2.lower())] + '">' + word2 + '</b>')
                            else:
                                word1 = word1.replace(word2,'<b style="color:' + color_dict[stem(word2.lower())] + '">' + word2 + '</b>')
                            pos_list.append(pos_num)
                            order_list.append(stem_dict[stem(word2.lower())])
                    highlight = highlight + ' ' + word1     
                    pos_num = pos_num + 1
                #print(pos_list)
                #print(order_list)
                dict_temp = {
                    'wordgroup' : result['content'],
                    'weight' : result.score,
                    'highlight' : highlight,
                    'pos_list' : pos_list,
                    'title' : result['title'][0:-4],
                    'para' : result['para']
                    }
                dictionary[result['content']] = dict_temp            
        return dictionary
    def search(self,sent):
        #vocabulary = self.get_vocabulary(self.vocabulary_address)
        global vocabulary
        ppl = self.get_inputPPL_ModelAll(sent)
        print(1)
        print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
        (wordgroup,color_dict,stem_dict,segemented_results) = self.get_wordgroup(ppl,vocabulary)
        #print(wordgroup)
        print(2)
        print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
        group = self.searchIndexByList(wordgroup,color_dict,stem_dict)
        print(4)
        print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
        group = self.sort_result(group)
        print(5)
        print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
        #print(group)
        #print(segemented_results)
        return (group,segemented_results)
        #print(group)
    def get_vocabulary(self,vocabulary_address):
        vocabulary = {}
        file = open(vocabulary_address,'r',encoding='utf8')
        #print(vocabulary_address)
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
        color_dict = {}
        stem_dict = {}
        wordgroup = []
        group = {}
        group_sum = 0.0
        group_no = 0
        class_num = 0
        color = CreatIndex().get_color()
        stem_class = 0
        flag = 1
        segemented_results = ""
        for word in ppl_list:
            segemented_results = segemented_results + '/' + word
            if word in vocabulary:
                transfer_list.append(vocabulary[word])
        #print(transfer_list)
        for l in transfer_list:
            for word in l:
                wordgroup.append(Term('content',word))
                color_dict[stem(word)] = color
                stem_dict[stem(word)] = stem_class
            color = CreatIndex().get_color()
            stem_class = stem_class + 1
        return (wordgroup,color_dict,stem_dict,segemented_results)

    def sort_result(self,result_list):
        new_list = []
        for result in result_list:
            if len(new_list) == 0:
                new_list.append(result_list[result])
            else:
                temp = 0
                #print(result_list[result])
                while temp<len(new_list) and (float(new_list[temp]['weight']) > float(result_list[result]['weight'])):
                    temp = temp + 1
                new_list.insert(temp,result_list[result])
        return new_list
    def get_color(self):
        seed = "123456789ABCDE"
        sa = []
        for i in range(6):
            sa.append(random.choice(seed))
        salt = ''.join(sa)
        salt = '#' + salt
        return salt

    def get_inputPPL_ModelAll(self,inputWord):
        ppl_list = jieba.cut(inputWord,cut_all=True)
        return ppl_list
    def get_inputPPL_ModelAcc(self,inputWord):
        ppl_list = jieba.cut(inputWord,cut_all=False)
        return ppl_list




#CreatIndex().search('爱世界和平')
