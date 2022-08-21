# Author:Sun Yujian
import sys
import getpass
from Clean import Clean
from TXTCut import TXTCut
class SentenceMain(object):
    def main(self,address,thesis_name):
        PDFExtract().extract(address)
        usr = getpass.getuser()
        add_extract = '/home/'+usr+'/PDF2TXTSW/Temp/'+thesis_name+'/Extract.txt'
        (clean_name, Incomplete_name) = Clean().main(add_extract)
        (full_dst, incomplete_dst) = TXTCut().cutTXT(thesis_name)
        return (clean_name, Incomplete_name,full_dst, incomplete_dst)