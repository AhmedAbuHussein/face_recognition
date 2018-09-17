import tkinter
from tkinter import ttk
from tkinter import messagebox as msg
import cv2
import PIL.Image
import PIL.ImageTk
import time
import os
import QRcode
import database
import recognition
import videoStreem
from pyzbar.pyzbar import *


class App:
    def __init__(self, window, window_title, video_source=0, video_source2 = 0):
        self.window = window
        self.window.title(window_title)
        self.video_source = video_source
        self.video_source2 = video_source2

        # open video source (by default this will try to open the computer webcam)
        self.vid = videoStreem.MyVideoCapture(self.video_source)
        self.vid2 = videoStreem.MyVideoCapture(self.video_source2)

        self.mainframe = tkinter.Frame(window)
        self.mainframe.pack()


        self.label = tkinter.Label(self.mainframe,text="Face Detector", font=('Arial',18 ,'bold'))

        self.label.grid(row=0,column=0)

        # Create a canvas that can fit the above video source size
        self.canvas = tkinter.Canvas(self.mainframe, width = self.vid.width, height = self.vid.height)
        self.canvas.grid(row=1, column=0)

        self.label1 = tkinter.Label(self.mainframe, font=('Arial',18 ,'bold'), text="QRCode Detector")
        self.label1.grid(row=0, column=1)

        self.canvas2 = tkinter.Canvas(self.mainframe, width=self.vid2.width, height=self.vid2.height)
        self.canvas2.grid(row=1, column=1)

        self.mainframe2 = tkinter.Frame(self.window)
        self.mainframe2.pack()



        # Frame to set information about this user
        self.frame1 = tkinter.LabelFrame(self.mainframe2, text="Face information", width=self.vid.width, height= self.vid.height)
        self.frame1.config(relief = tkinter.SOLID)
        self.frame1.grid(row=0, column=0)
        self.facedata()

        self.frame = tkinter.LabelFrame(self.mainframe2, text="database information", width=self.vid2.width, height=self.vid2.height)
        self.frame.config(relief=tkinter.SOLID)
        self.frame.grid(row=0, column=1)
        self.databaseinfo()



    def databaseinfo(self):

        #id data
        self.database_id = tkinter.Label(self.frame,text="ID : ",font=('Times',13,'bold'), anchor=tkinter.NW)
        self.database_id.place(x=20, y=30)

        self.database_id_value = tkinter.Label(self.frame,font=('Times',12,'bold') ,text="Nothing detect")
        self.database_id_value.place(x=180, y=30)

        #name data
        self.database_name = tkinter.Label(self.frame, text="Full Name : ", font=('Times', 13, 'bold'),anchor=tkinter.NW)
        self.database_name.place(x=20, y=60)

        self.database_name_value = tkinter.Label(self.frame, font=('Times', 12, 'bold'), text="Nothing detect")
        self.database_name_value.place(x=180, y=60)

        # name data
        self.database_serial = tkinter.Label(self.frame, text="Serial Number : ", font=('Times', 13, 'bold'))
        self.database_serial.place(x=20, y=90)

        self.database_serial_value = tkinter.Label(self.frame, font=('Times', 12, 'bold'), text="Nothing detect")
        self.database_serial_value.place(x=180, y=90)

        # image data
        self.database_image = tkinter.Label(self.frame, text="Stored Image : ", font=('Times', 13, 'bold'))
        self.database_image.place(x=20, y=120)

        self.database_image_value = tkinter.Canvas(self.frame, width=150, height=150)
        self.database_image_value.config(relief=tkinter.SOLID)
        self.database_image_value.place(x=180, y=120)


        # Button that lets the user take a snapshot

        # self.btn_snapshot2 = tkinter.Button(window, text="Snap Code", width=50, command=self.code)
        # self.btn_snapshot2.grid(row=2, column=0)

        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 15
        self.update()

        self.window.mainloop()


    def facedata(self):
        # id data
        self.database_ = tkinter.Label(self.frame1, text="ID : ", font=('Times', 13, 'bold'), anchor=tkinter.NW)
        self.database_.place(x=20, y=30)

        self.database_value = tkinter.Label(self.frame1, font=('Times', 12, 'bold'), text="Nothing detect")
        self.database_value.place(x=180, y=30)

    def snapshot(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()
        if ret:
            imageName = os.path.curdir + "\\images\\frame-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg"
            cv2.imwrite(imageName, cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
            # face recognition here
            recognition.Recognition(os.path.curdir+"\\test\\"+self.knowImg,imageName)

    def code(self):
        # Get a frame from the video source
        ret, frame = self.vid2.get_frame()
        if ret:
            imageName = os.path.curdir + "\\images\\code-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg"
            cv2.imwrite(imageName, cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
            if os.path.isfile(imageName):
                QR = QRcode.QRCodeReader(imageName)
                info = QR.decoded()
                if info == False:
                    return
                db = database.database()
                data = db.connection(info)
                self.knowImg =  data[2]
                self.database_id_value.config(text=data[0])
                self.database_name_value.config(text=data[1])
                image = PIL.Image.open(os.path.curdir+"\\test\\"+data[2])
                image = image.resize((150, 150), PIL.Image.ANTIALIAS)
                self.database_image_value.create_image(0, 0, image = image, anchor=tkinter.NW)
                self.snapshot()
            else:
                msg.showwarning('Warnning', "Invalid Image Path")

    def update(self):
        size = 150,150
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()
        ret2, frame2 = self.vid2.get_frame()
        code = decode(frame2)
        if len(code) > 0:
            self.code()

        if ret:
            image = PIL.Image.fromarray(frame)
            image = image.resize((500, 300), PIL.Image.ANTIALIAS)
            self.photo = PIL.ImageTk.PhotoImage(image = image)
            self.canvas.create_image(0, 0, image = self.photo, anchor = tkinter.NW)

        if ret2:
            image2 = PIL.Image.fromarray(frame)
            image2 = image2.resize((500, 300), PIL.Image.ANTIALIAS)
            self.photo2 = PIL.ImageTk.PhotoImage(image=image2)
            self.canvas2.create_image(0, 0, image=self.photo2, anchor=tkinter.NW)

        #loop for taking frames from camera or video speed delay
        self.window.after(self.delay, self.update)





App(tkinter.Tk(), "Face Recognition", 0, 0)
