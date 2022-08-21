# Author:Sun Yujian
import sys
import os
import getpass
from tools.txt2sent.GetAddress import GetAddress
class TXTCut(object):
    def cutTXT(self,thesis_name):
        usr = getpass.getuser()
        #(thesis_name,usr) = GetAddress().getThesisName(address)
        full = '/home/'+usr+'/PDF2TXTSW/Sent/Full'
        if not os.path.exists(full):
            os.mkdir(full)
        incomplete = '/home/'+usr+'/PDF2TXTSW/Sent/Incomplete'
        if not os.path.exists(incomplete):
            os.mkdir(incomplete)
        full_src = '/home/'+usr+'/PDF2TXTSW/Temp/'+thesis_name+'/clean_6.txt'
        incomplete_src = '/home/' + usr + '/PDF2TXTSW/Temp/' + thesis_name + '/Incomplete.txt'
        full_dst = self.cutFull(full_src)
        incomplete_dst = self.cutIncomplete(incomplete_src)
        return (full_dst,incomplete_dst)

    def cutFull(self,address):
        (usr,thesis_name) = GetAddress().getThesisName(address)
        full_address ='/home/py35/Desktop/Sent/'+thesis_name
        if not os.path.exists(full_address):
            os.mkdir(full_address)
        add = self.cutMain(address,full_address)
        return add

    def cutIncomplete(self,address):
        (usr, thesis_name) = GetAddress().getThesisName(address)
        incomplete_address = '/home/' + usr + '/PDF2TXTSW/Sent/Incomplete/'+thesis_name
        if not os.path.exists(incomplete_address):
            os.mkdir(incomplete_address)
        add = self.cutMain(address, incomplete_address)
        return add

    def cutMain(self,add_src,add_dst):
        f = open(add_src)
        if add_dst[len(add_dst)-1]!= '/' and add_dst[len(add_dst)-1]!= '\\':
            add_dst = add_dst+'/'
        num = 0
        for line in f:
            num = self.write(add_dst,num,line)
        return add_dst

    def write(self,add_dst,num,line):
        address = add_dst+str(num)+'.txt'
        #print (address)
        nu = 0
        while nu==0:
            if not os.path.isfile(address):
                a = open(address,'a')
                a.write(line)
                a.close()
                nu = 1
                num = num + 1
            else:
                num = num+1
                address = add_dst+str(num)+'.txt'
        return num

TXTCut().cutFull('/home/py35/Desktop/s1/all.txt')
#print TXTCut().cutIncomplete('/home/yizhiai1994/PDF2TXTSW/Temp/a6-roos/Incomplete_temp.txt')
#print TXTCut().cutTXT('a6-roos')