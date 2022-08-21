# Author:Sun Yujian
import sys
import getpass
class GetAddress(object):
    def getNameUsr(self,address):
        num = 0
        usr = getpass.getuser()
        for i in range(0, len(address))[::-1]:
            # print(i),
            if address[i] == '\\' or address[i] == '/':
                num = i + 1
                break
        name = address[num:len(address)-4]
        #folder = address[0:num]
        return (name,usr)
    def getAddress(self,address):
        num = 0
        #login = getpass.getuser()
        for i in range(0, len(address))[::-1]:
            # print(i),
            if address[i] == '\\' or address[i] == '/':
                num = i + 1
                break
        #name = address[num:len(address) - 4]
        folder = address[0:num]
        return folder
    def getThesisName(self,address):
        num1 = 0
        num2 = 0
        num3 = 0
        usr = getpass.getuser()
        for i in range(0, len(address))[::-1]:
            # print(i),
            if address[i] == '\\' or address[i] == '/':
                if num1 == 0:
                    num2 = i
                elif num1 == 1:
                    num3 = i + 1
                num1 = num1 + 1
                if num1 == 2:
                    break
        thesis_name = address[num3:num2]
        # folder = address[0:num]
        return (usr,thesis_name)

#print GetAddress().getThesisName('/home/yizhiai1994/PDF2TXTSW/Temp/a6-roos/Incomplete_temp.txt')
#print (GetAddress().getAddress('/home/yizhiai1994/a6-roos.pdf'))