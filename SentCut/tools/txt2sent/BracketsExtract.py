#coding=utf-8
# Author:Sun Yujian
import sys
class BracketsExtract(object):
    def bracketsExtract_s(self,str):
        # a = open(r'F:\BracketsClean.txt','a')
        # 剩余左括号数量
        numl = 0
        manage = 0
        judge = 0
        line = []
        line_brackets = []
        bracketsExtract_line = []
        line_write = ''
        str_clean = ''
        ii = ''
        for i in str:
            line.append(i)
            if i == '(' or i == '（':
                numl = numl + 1
                # print('a\n')
            if (i == ')' or i == '）') and numl > 0:
                # print(')')
                for ii in line[::-1]:
                    # while ii == '(' or ii == '（':
                    ii = line.pop()
                    # print('1\n')
                    if ii == '(' or ii == '（':
                        # print('2\n')
                        numl = numl - 1
                        for iii in line_brackets[::-1]:
                            # print(iii)
                            if iii != ')' or iii != '）':
                                line_write = line_write + iii
                        line_write = line_write.replace(")", "")
                        line_write = line_write.replace("）", "")
                        bracketsExtract_line.append(line_write)
                        # a.writelines(line_write+'\n'),
                        line_write = ''
                        line_brackets = []
                        break
                    else:
                        line_brackets.append(ii)
            line_brackets = []
            line_write = ''
        for i in line:
            str_clean = str_clean + i
        return (str_clean, bracketsExtract_line)

    # []
    def bracketsExtract_m(self,str):
        # a = open(r'F:\BracketsClean.txt','a')
        # 剩余左括号数量
        numl = 0
        manage = 0
        judge = 0
        line = []
        line_brackets = []
        bracketsExtract_line = []
        line_write = ''
        str_clean = ''
        ii = ''
        for i in str:
            line.append(i)
            if i == '[':
                numl = numl + 1
                ##print('a\n')
            if (i == ']') and numl > 0:
                ##print(']')
                for ii in line[::-1]:
                    # while ii == '(' or ii == '（':
                    ii = line.pop()
                    # print('1\n')
                    if ii == '[':
                        # print('2\n')
                        numl = numl - 1
                        for iii in line_brackets[::-1]:
                            # print(iii)
                            if iii != ']':
                                line_write = line_write + iii
                        line_write = line_write.replace("]", "")
                        bracketsExtract_line.append(line_write)
                        # a.writelines(line_write+'\n'),
                        line_write = ''
                        line_brackets = []
                        break
                    else:
                        line_brackets.append(ii)
            line_brackets = []
            line_write = ''
        for i in line:
            str_clean = str_clean + i
        return (str_clean, bracketsExtract_line)

    # {}
    def bracketsExtract_l(self,str):
        #a = open(r'F:\BracketsClean.txt', 'a')
        # 剩余左括号数量
        numl = 0
        manage = 0
        judge = 0
        line = []
        line_brackets = []
        bracketsExtract_line = []
        line_write = ''
        str_clean = ''
        ii = ''
        for i in str:
            line.append(i)
            if i == '{':
                numl = numl + 1
                # print('a\n')
            if (i == '}') and numl > 0:
                # print('}')
                for ii in line[::-1]:
                    # while ii == '(' or ii == '（':
                    ii = line.pop()
                    # print('1\n')
                    if ii == '{':
                        # print('2\n')
                        numl = numl - 1
                        for iii in line_brackets[::-1]:
                            # print(iii)
                            if iii != '}':
                                line_write = line_write + iii
                        line_write = line_write.replace("}", "")
                        bracketsExtract_line.append(line_write)
                        # a.writelines(line_write+'\n'),
                        line_write = ''
                        line_brackets = []
                        break
                    else:
                        line_brackets.append(ii)
            line_brackets = []
            line_write = ''
        for i in line:
            str_clean = str_clean + i
        return (str_clean, bracketsExtract_line)