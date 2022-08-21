import codecs
import nltk
import os
import traceback
class Para2Sent(object):
    def batch_run(self, src_folder, dst_folder):
        file_address_list = []
        file_name_list = []
        file_list = []
        num = 0
        error_num = 0
        for parent, dirnames, filenames in os.walk(src_folder):
            for filename in filenames:
                file_name = os.path.join(parent, filename)
                if file_name.endswith('.txt'):
                    file_address_list.append(file_name)
                    file_name_list.append(filename)
                    file_list.append((parent, file_name, filename))
        for (parent, file_name, filename) in file_list:
            num = num + 1
            try:
                save_address = dst_folder + '/' + filename[:-4] + '.txt'
                print('Remaining' + str(len(file_list) - num))
                self.run(file_name, save_address)
            except BaseException as e:
                # print(file_name)
                error_num = error_num + 1
                error_file = dst_folder + '/error.txt'
                error_open = open(error_file, 'a')
                error_open.write('errornum:' + str(error_num) + '\n')
                error_open.write(file_name)
                error_open.write(traceback.format_exc())
                error_open.close()
                # break
                continue
    def run(self,src_address,save_address):
        txt_list = self.cutSent(src_address)
        self.writeTXT(txt_list,save_address)
        list = []
    def cutSent(self,src_address):
        sum = 0
        #f = codecs.open(src_address, encoding='utf-8')
        #raw = f.read()
        f = open(src_address,'r',encoding='gbk')
        f_read = f.readlines()
        sent = []
        for i in f_read:
            token = nltk.sent_tokenize(i)
            sent = sent + token
        
        f.close()
        return sent
    def writeTXT(self, txt_list, save_address):
        save_txt = save_address
        txtFile = open(save_txt, "a")
        for i in txt_list:
            txtFile.write(i)
            txtFile.write('\n')
        txtFile.close()
Para2Sent().batch_run('C:\\Users\\Administrator\\Desktop\\SYJ\\MergePara','C:\\Users\\Administrator\\Desktop\\SYJ\\Sent')
#Para2Sent().batch_run('D:\\C__Users_Administrator_Desktop_SYJ_PDF_Proceeding_SIGKDD_SIGKDD200557.txt','D:\\asdasdsadads.txt')
