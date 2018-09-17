import face_recognition
import PIL.Image
import PIL.ImageTk
import numpy as np
import os
from tkinter import messagebox as msg

class Recognition:
    def __init__(self, knowImage, unknowImage):
        self.knownImage = knowImage
        self.unknowImage = unknowImage
        self.main()

    def main(self):

        known_image = face_recognition.load_image_file(self.knownImage)
        unknown_image = face_recognition.load_image_file(self.unknowImage)

        if max(unknown_image.shape) > 1600:
            pil_img = PIL.Image.fromarray(unknown_image)
            pil_img.thumbnail((1600, 1600), PIL.Image.LANCZOS)
            unknown_image = np.array(pil_img)

        encodes = face_recognition.face_encodings(unknown_image)
        if len(encodes) == 0:
            print "WARNING: No faces found in {}. Ignoring file.".format(self.unknowImage)
            msg.showwarning('Warnning', "No faces found in {}".format(self.unknowImage))
            return
        biden_encoding = face_recognition.face_encodings(known_image)[0]
        unknown_encoding = encodes[0]

        results = face_recognition.compare_faces([biden_encoding], unknown_encoding)
        print results

        if results[0] == True :
            msg.showinfo("Info", 'Access Granted')
        else:
            msg.showerror("Error", 'Access Denied')
