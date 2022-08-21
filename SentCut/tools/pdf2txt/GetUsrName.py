# Author:Sun Yujian
import getpass
class GetUsrName(object):
    def getUserName(self):
        login = getpass.getuser()
        #print login
        return login

#print name.getUserName()