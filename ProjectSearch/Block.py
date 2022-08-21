#coding=utf-8
import sys
import io
import os
import codecs
from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
import re
from chardet import detect
import csv
import chardet 
from bs4 import BeautifulSoup
from xlwt import *
from time import sleep
from selenium.common.exceptions import TimeoutException
import multiprocessing
import time
import math
#提取块
class Block(object):
    def extract2csv(self,src_address,save_address):
        
        print(save_address)
        list_temp = Block().extract2list(src_address)
        Block().write_csv(list_temp, save_address)
        return 0
    def extract2list(self,src_address):
        src_address = re.sub(r'%', '%25',src_address)
        url = "file:///" + src_address
        driver = webdriver.Firefox()       
        endcod = driver.get(url)
        #encoding = chardet.detect(endcod)
        #encoding = driver.page_source
        #print(encoding)
        #encoding = re.findall(r'<title>\S+</title>',html_text)
        
        #print(encoding)
        print("**++++++++++++****")
        #sleep(5)
        print("**++++++++++++****")
        # 用于点换页的
        disabled = None
        while disabled == None:
            print("***********")
            driver.find_element_by_xpath("//*[@id='next']").click()
            disabled = driver.find_element_by_xpath("//*[@id='next']").get_attribute('disabled')
            print(driver.find_element_by_xpath("//*[@id='next']").get_attribute('disabled'))
            sleep(3)
            # sleep(5)
        sleep(5)
        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')
        table = soup.find_all(class_="page")
        extract_list = []
        for i in table:
            page = re.search(r'data-page-number=".*?"', str(i))
            page = re.sub(r'data-page-number="','',page.group())
            page = re.sub(r'"',"",page)
            page = int(page)
            #print(page)

            div = i.find_all(class_="textLayer")
            div = div[0].find_all_next("div")

            i = 0
            while i < len(div):
                extract_dict = {
                    # 左侧距离左边界的像素
                    "left": Block().get_left(str(div[i])),
                    # 上测距离顶边界的距离
                    "top": Block().get_top(str(div[i])),
                    # 表示合并前每个元素的大小（像素）
                    "fontsize": Block().get_fontsize(str(div[i])),
                    "content": Block().get_content(str(div[i])),
                    "page": page

                }
                extract_list.append(extract_dict)
                i = i + 1
        driver.close()

        return extract_list
    def batch_pdf2csv(self,src_folder,save_folder):
        #src_add源地址,dst_add目标地址
        down = 0
        file_address_list = []
        file_name_list = []
        file_list = []
        file_list_extract = []
        #获取一个存放所有pdf文件路径的链表
        for parent, dirnames, filenames in os.walk(src_folder):
            for filename in filenames:
                file_name = os.path.join(parent,filename)
                if file_name.endswith('.pdf'):
                    file_address_list.append(file_name)
                    file_name_list.append(filename)
                    file_list.append((parent,file_name,filename))
        if not os.path.exists(save_folder):
            os.makedirs(save_folder)
                
        #提取
        index_address = save_folder + '//index.txt'
        index = open(index_address,'rb')
        read = index.readlines()
        dictt = {}
        for i in read:
            ii  = str(i.decode(encoding='UTF-8',errors='ignore')).split(' ')
            dictt[str(ii[0])] = 0
        index.close()
        f = open(index_address,'a',encoding= 'gb18030')
        print(index_address)
        driver = webdriver.Firefox()
        num = 0
        for parent,file_name,filename in file_list:
            try:
                if not file_name in dictt:
                    save_address = save_folder + '//' + re.sub(r':','_',re.sub(r'\\','_',re.sub(r'/','_',parent))) + re.sub(r'.pdf','.csv',filename)
                    extract_dict = Block().extract2list_goto(driver,file_name)
                    Block().write_csv(extract_dict, save_address)
                    index = file_name + ' to ' + save_address
                    print('use:' + str(num))
                    f.writelines(index+'\n')
                else:
                    num = num + 1
            except BaseException as e:
                print(e)
                except_address = save_folder  + '//except.txt'
                fe = open(index_address,'a',encoding= 'gb18030')
                fe.write(str(e))
                fe.close()
                continue
           # print(save_address)
        f.close()
        driver.close()
        
    def extract2list_goto(self,driver,src_address):
        src_address = re.sub(r'%', '%25',src_address)
        url = "file:///" + src_address
        #driver = webdriver.Firefox()       
        endcod = driver.get(url)
        #encoding = chardet.detect(endcod)
        #encoding = driver.page_source
        #print(encoding)
        #encoding = re.findall(r'<title>\S+</title>',html_text)
        
        #print(encoding)
        #print("**++++++++++++****")
        #sleep(5)
        print(src_address)
        # 用于点换页的
        disabled = None
        sleep(3)
        page_temp = 1
        extract_list = []
        
        driver.find_element_by_id("pageNumber").clear()
        driver.find_element_by_id("pageNumber").send_keys(Keys.CONTROL,'a')
        driver.find_element_by_id("pageNumber").send_keys("1")
        driver.find_element_by_id("pageNumber").send_keys(Keys.ENTER)
        disabled = driver.find_element_by_xpath("//*[@id='next']").get_attribute('disabled')
        sleep(5)
        while disabled == None:

            driver.find_element_by_xpath("//*[@id='next']").click()
            disabled = driver.find_element_by_xpath("//*[@id='next']").get_attribute('disabled')
            print(driver.find_element_by_xpath("//*[@id='next']").get_attribute('disabled')) 
            sleep(5)
            
            list_temp = Block().getPageContainer(driver,page_temp)
            if len(extract_list) == 0:
                extract_list = list_temp
            else:
                extract_list = extract_list + list_temp
            page_temp = page_temp + 1
            # sleep(5)
        sleep(5)
        if page_temp == 1:
            print("asassasa")
        list_temp = Block().getPageContainer(driver,page_temp)
        if len(extract_list) == 0:
            extract_list = list_temp
        else:
            extract_list = extract_list + list_temp

        

        return extract_list
#获取浏览器中的id为pageContainer的标签中的内容，并返回本页的list
    def getPageContainer(self,driver,page_temp):
        extract_list = []
        html = driver.page_source
        pageContainer = 'pageContainer'+str(page_temp)
        pageContainer_next = 'pageContainer'+str(page_temp+1)
        soup = BeautifulSoup(html, 'lxml')
        print(pageContainer)
        table = soup.find_all(id=pageContainer)
        page = re.search(r'data-page-number=".*?"', str(table[0]))
        page = re.sub(r'data-page-number="','',page.group())
        page = re.sub(r'"',"",page)
        page = int(page)
        print('page'+str(page))        
        div = table[0].find_all(class_="textLayer")
        print('len'+str(len(table)))
        if len(div) != 0:
            div = div[0].find_all_next("div")
            i = 0
            while (i < len(div)) and ((re.search(pageContainer_next,str(div[i])))==None):
                #print()
                extract_dict = {
                    # 左侧距离左边界的像素
                    "left": Block().get_left(str(div[i])),
                    # 上测距离顶边界的距离
                    "top": Block().get_top(str(div[i])),
                    # 表示合并前每个元素的大小（像素）
                    "fontsize": Block().get_fontsize(str(div[i])),
                    "content": Block().get_content(str(div[i])),
                    "page": page_temp

                }
                extract_list.append(extract_dict)
                i = i + 1
        return extract_list
                
    def test(self,pdf_address, save_address):
        #ubuntu下的特殊设置，文件路径中有 % 需要变成 % 25
        pdf_address = re.sub(r'%','%25',pdf_address)
        driver = webdriver.Firefox()
        url = "file://" + pdf_address
        driver.get(url)
        sleep(5)

        disabled = None
        while disabled == None:
            driver.find_element_by_xpath("//*[@id='next']").click()
            disabled = driver.find_element_by_xpath("//*[@id='next']").get_attribute('disabled')
            print(driver.find_element_by_xpath("//*[@id='next']").get_attribute('disabled'))
            sleep(5)
        sleep(5)
        html = driver.page_source
        #print(html)
        soup = BeautifulSoup(html, 'lxml')
        #print(soup)
        #div = driver.find_element_by_id('pageContainer1')
        #table = soup.find_all(class_="textLayer")
        table = soup.find_all(class_="textLayer")
        #print(table[0])
        # for t in table:
        #     div = t.find_all_next("div")
        div = table[0].find_all_next("div")
        #for ii in div:
            #print(ii)
        extract_list = []
        i = 0
        while i < len(div):
            #di = div[i]
            #print(di)
            #match = pattern.match(div[i])
            #print(div[i])
            extract_dict = {
                #左侧距离左边界的像素
                "left": Block().get_left(str(div[i])),
                #上测距离顶边界的距离
                "top": Block().get_top(str(div[i])),
                #表示行合并后本行字母数
                "fontsize": Block().get_fontsize(str(div[i])),
                # 表示行合并后本行元素像素的众数
                "content": Block.get_content(),
                #表示行合并后本行元素像素的平均值
                "page":0.0

            }
            extract_list.append(extract_dict)
            #print(PDFExtractBySpider().get_left(str(div[i])))
            #print(PDFExtractBySpider().get_top(str(div[i])))
            #print(PDFExtractBySpider().get_fontsize(str(div[i])))
            #print(PDFExtractBySpider().get_content(str(div[i])))
            #print(type(div[i]))
            i = i+1
        pdfViewer = driver.find_elements_by_class_name('pdfViewer')
        #page = driver.find_element_by_id('pageContainer1')
        #print(div)
        merge_list = Block().merge(extract_list)
        f = open(save_address, 'a')
        for m in merge_list:
            #print(m)
            f.writelines(str(m['content'])+'\n')
        f.close()
        driver.close()

        Block().write_csv(merge_list,save_address)
        #print('len'+str(len(merge_list)))
        #for i in merge_list:
            #print(i)
    def get_left(self,strs):
        left = re.search(r'left:.*?;', str(strs))
        if left != None:
            st = left.group()
            st = st[6:]
            st = st[:-3]
            st.replace('px; ', '')
            return float(st)
        else:
            return None
    def get_top(self,strs):
        top = re.search(r'top:.*?;', str(strs))
        if top != None:
            st = top.group()
            st = st[5:]
            st = st[:-3]
            st.replace('px; ', '')
            return float(st)
        else:
            return None
    def get_fontsize(self,strs):
        fontsize = re.search(r'font-size:.*?;', str(strs))
        if fontsize != None:
            st = fontsize.group()
            st = st[11:]
            st = st[:-3]
            st.replace('px; ', '')
            return float(st)
        else:
            return None
    def get_content(self,strs):

        if re.search(r'class="page"',strs):
            #print("*********************")
            return ""
        if re.search(r'class="textLayer"',strs):
            #print("*********************")
            return ""
        #content = strs
        #content = re.search(r'">.*?</', str(strs))
        #content.replace(str(other),"")
        #print(strs+'\n')
        #print("******************\n")
        content = re.sub(r'<div.*?>', "", strs)
        content = re.sub(r'</div>', "", content)
        return content
    def write_excel(self,list,save_address):
        save_xls = re.sub(r'.txt', ".xls", save_address)
        data = Workbook(encoding='utf-8')
        table = data.add_sheet('extract')
        row = 0
        col = 0
        for dat in list:
            table.write(row, 0, dat['left'])
            table.write(row, 1, dat['top'])
            table.write(row, 2, dat['fontsize'])
            table.write(row, 3, dat['content'])
            table.write(row, 4, dat['page'])
            row = row + 1
        data.save(save_xls)
    def write_csv(self,extract_list,save_address):
        save_csv = re.sub(r'.txt', ".csv", save_address)
        csvFile = open(save_csv, "w",newline='',encoding= 'gb18030')
        # 文件头以列表的形式传入函数，列表的每个元素表示每一列的标识
        fileheader = ["left", "top","fontsize","content","page"]
        dict_writer = csv.DictWriter(csvFile, fileheader)

        # 但是如果此时直接写入内容，会导致没有数据名，所以，应先写数据名（也就是我们上面定义的文件头）。
        # 写数据名，可以自己写如下代码完成：

        dict_writer.writerow(dict(zip(fileheader, fileheader)))
        print(len(extract_list))
        # 之后，按照（属性：数据）的形式，将字典写入CSV文档即可
        for dic in extract_list:
            
            #dic['content'] = dic['content'].encode()
            #dic['content'] = dic['content'].encode(encoding);
            #dic['content'] = dic['content'].decode('gbk', 'ignore')
            #print(dic)
            dic['content'] = str(dic['content'])
            #print(dic['content'])
            dict_writer.writerow(dic)
        csvFile.close()

#PDFExtractBySpider().test("/home/py35/Desktop/testPDF1/CSL2016/1-s2.0-S0885230816000048-main.pdf","/home/py35/Desktop/testPDF1/CSL2016/1-s2.0-S0885230816000048-main.txt")
    def test(self,src_address):
        src_address = re.sub(r'%', '%25', src_address)
        driver = webdriver.Firefox()
        url = "file://" + src_address
        driver.get(url)
        page_dict = {
            "page" : 0,
            "list" : []
        }
        sleep(5)
        # 用于点换页的
        disabled = None
        while disabled == None:
            driver.find_element_by_xpath("//*[@id='next']").click()
            disabled = driver.find_element_by_xpath("//*[@id='next']").get_attribute('disabled')
            print(driver.find_element_by_xpath("//*[@id='next']").get_attribute('disabled'))
            sleep(3)
            # sleep(5)
        sleep(5)
        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')
        table = soup.find_all(class_="page")
        extract_list = []
        for i in table:
            page = re.search(r'data-page-number=".*?"', str(i))
            page = re.sub(r'data-page-number="','',page.group())
            page = re.sub(r'"',"",page)
            page = int(page)
            #print(page)

            div = soup.find_all(class_="textLayer")
            div = div[0].find_all_next("div")

            i = 0
            while i < len(div):
                extract_dict = {
                    # 左侧距离左边界的像素
                    "left": Block().get_left(str(div[i])),
                    # 上测距离顶边界的距离
                    "top": Block().get_top(str(div[i])),
                    # 表示合并前每个元素的大小（像素）
                    "fontsize": Block().get_fontsize(str(div[i])),

                    "content": Block().get_content(str(div[i])),
                    "page": page

                }
                extract_list.append(extract_dict)
                i = i + 1
        #for i in extract_list:
            #print(i)
    
    def multithread_main(self,src_folder,save_folder,multithread_num):
        #src_add源地址,dst_add目标地址
        down = 0
        file_address_list = []
        file_name_list = []
        file_list = []
        file_list_extract = []
        #获取一个存放所有pdf文件路径的链表
        for parent, dirnames, filenames in os.walk(src_folder):
            for filename in filenames:
                file_name = os.path.join(parent,filename)
                if file_name.endswith('.pdf'):
                    file_address_list.append(file_name)
                    file_name_list.append(filename)
                    file_list.append((file_name,filename))
        
        if not os.path.exists(save_folder):
            os.makedirs(save_folder)
        cuting_list = Block().cut_list(file_list,multithread_num)
        for i in cuting_list:
            p = multiprocessing.Process(target=Block().multithread_pdf2csv, args=(i,save_folder))
            p.start()
            p.join()
            print(len(i))
        
    def multithread_pdf2csv(self,file_list,save_folder):       
        #提取
        print("ASSASA")
        driver = webdriver.Firefox()  
        for file_name,filename in file_list:
            save_address = save_folder+'//'+re.sub(r'.pdf','.csv',filename)
            extract_dict = Block().extract2list_goto(driver,file_name)
            Block().write_csv(extract_dict, save_address)
            print(save_address)
        driver.close()
    def cut_list(self,cutted_list,number):
        cuting_list = []
        temp_list = []
        if len(cutted_list)<number:
            cuting_list.append(cutted_list)
            return cut_list
        num = math.floor(len(cutted_list)/number)
        
        i = 0
        while i<len(cutted_list):
            if i%num!=0:
                temp_list.append(cutted_list[i])
            elif i%num==0:
                temp_list.append(cutted_list[i])
                cuting_list.append(temp_list)
                temp_list = []
            i = i + 1
        if (len(cutted_list) -1 )%num != 0:
            cuting_list.append(temp_list)
        return cuting_list
#Block().extract2csv('C://Users//yizhi//Desktop//1-s2.0-S0169023X13001055-main.pdf','C://Users//yizhi//Desktop//1-s0-S23X1305-main.txt')
#Block().batch_pdf2csv('C://Users//yizhi//Desktop//PDF7','C://Users//yizhi//Desktop//Extract311')

Block().batch_pdf2csv('C:\\Users\\Administrator\\Desktop\\SYJ\\PDF','C:\\Users\\Administrator\\Desktop\\SYJ\\Block')
#Block().multithread_main('C://Users//yizhi//Desktop//PDF6','C://Users//yizhi//Desktop//Extract7',5)                       
#if __name__ == "__main__":
#    Block().batch_pdf2csv(sys.argv[1],sys.argv[2])
