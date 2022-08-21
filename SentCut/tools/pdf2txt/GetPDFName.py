# Author:Sun Yujian
import sys
class GetPDFName(object):
    def getPDFName(self,address):
        num = 0
        for i in range(0, len(address))[::-1]:
            #print(i),
            if address[i] == '\\' or address[i] == '/':
                num = i+1
                break
        name = address[num:]
        return name

# if __name__ == '__main__':
#     out = GetPDFName()
#     print (out.getPDFName(sys.argv[1]))

#print(GetPDFName().getPDFName('/home/yizhiai1994/a6-roos.pdf'))