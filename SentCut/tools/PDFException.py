# Author:Sun Yujian
from pdfminer.psparser import PSObject
from pdfminer.psparser import PSException

class PDFObject(PSObject):
    pass

class PDFException(PSException):
    pass

class PDFTypeError(PDFException):
    pass

class PDFValueError(PDFException):
    pass

class PDFObjectNotFound(PDFException):
    pass

class PDFNotImplementedError(PDFException):
    pass