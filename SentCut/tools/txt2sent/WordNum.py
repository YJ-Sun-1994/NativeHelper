import  sys
# Author:Sun Yujian
class WordNum(object):
    # wordNum
    def wordNum(self,line):
        str = line.split(' ')
        num = len(str)
        return num
if __name__ == '__main__':
    WordNum().wordNum(sys.argv[1])