from pyzbar.pyzbar import *
from PIL import Image
import os
import tkinter.messagebox as msg
class QRCodeReader:
    def __init__(self, image):
        self.image = image

    def decoded(self):
        if os.path.isfile(self.image):
            code = decode(Image.open(self.image))
            if len(code) > 0:
                return code[0][0]
            else:
                msg.showwarning("warning", "There is no QRcode in the picture ")
                return False
        else:
            msg.showwarning("warning","No such file or directory: {}".format(self.image))
            return False
