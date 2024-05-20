import tkinter as tk
import customtkinter
from customtkinter import *
import tkinter as tk
import subprocess
import sys
import PIL
import mysql
import mysql.connector
import customtkinter
import tkinter
from customtkinter import *
from tkinter import *
from PIL import *
import mysql.connector
from CTkMessagebox import *



class MainPage:

    def __init__(self,window,title):
        mainpage=CTk()
        imgLogo = Image.open("images/logo.png")
        google_icon_data = Image.open("images/google-icon.png")
        imgEmail = Image.open("images/email-icon.png")
        imgUser = Image.open("images/man.png")
        imgPassword = Image.open("images/password-icon.png")
        patientLogo = Image.open("images/patient.png")
        doctorLogo = Image.open("images/doctor.png")
        adminlogo = Image.open("images/admin.png")
        ıdlogo = Image.open("images/id.png")
        namelogo = Image.open("images/id-card.png")
        maillogo = Image.open("images/mail.png")
        genderlogo = Image.open("images/symbol.png")
        bloodlogo = Image.open("images/blood-analysis.png")
        addresslogo = Image.open("images/location-pin.png")



        imgLogoCTk = CTkImage(dark_image=imgLogo, light_image=imgLogo, size=(300, 480))
        imgpatient = CTkImage(dark_image=patientLogo, light_image=patientLogo, size=(20,20))
        imgdoctor = CTkImage(dark_image=doctorLogo,light_image=doctorLogo,size=(20,20))
        imgadmin = CTkImage(dark_image=doctorLogo,light_image=doctorLogo,size=(20,20))
        google_icon = CTkImage(dark_image=google_icon_data, light_image=google_icon_data, size=(17, 17))
        userIcon = CTkImage(dark_image=imgUser, light_image=imgUser, size=(22, 22))
        passwordIcon = CTkImage(dark_image=imgPassword, light_image=imgPassword, size=(22, 22))
        ıdlogoIcon = CTkImage(dark_image=ıdlogo, light_image=ıdlogo, size=(22, 22))
        namelogoIcon = CTkImage(dark_image=namelogo, light_image=namelogo, size=(22, 22))
        maillogoIcon = CTkImage(dark_image=maillogo, light_image=maillogo, size=(22, 22))
        genderlogoIcon = CTkImage(dark_image=genderlogo, light_image=genderlogo, size=(22, 22))
        bloodlogoIcon = CTkImage(dark_image=bloodlogo, light_image=bloodlogo, size=(22, 22))
        addresslogoIcon = CTkImage(dark_image=addresslogo, light_image=addresslogo, size=(22, 22))

        mainpage.geometry(window)
        mainpage.title(title)
        mainpage.resizable(False,False)
        logoLabel = CTkLabel(master=mainpage, text="", image=imgLogoCTk).pack(expand=True, side="left")

        frame = CTkFrame(master=mainpage, width=320, height=480, fg_color="#ffffff",)


        frame.pack_propagate(0)

        frame.pack(expand=True, side="right")



        welcomeLabel = CTkLabel(master=frame, text="WELCOME TO \n"
                                                   "MEDICAREHUB \n"
                                                   " SYSTEM!",font=("Arial Bold",26),text_color="#261E76",
                                anchor="w",justify=CENTER,)
        welcomeLabel.pack(anchor="w",padx=(55,0),pady=(75,0))

        doctorButton =  CTkButton(master=frame, text="Doctor ", fg_color="#EEEEEE", command=self.doctorCommand,
                                  hover_color="#08e590", font=("Arial Bold", 18), text_color="#601E88", width=275,height=32,
                                               image=imgdoctor).pack(anchor="w", pady=(55, 0), padx=(15, 0))

        patientButton = CTkButton(master=frame, text="Patient ", fg_color="#EEEEEE", command=self.patientCommand,
                                 hover_color="#08e590", font=("Arial Bold", 18), text_color="#601E88", width=275,
                                 height=32,
                                 image=imgpatient).pack(anchor="w", pady=(20, 0), padx=(15, 0))

        adminButton = CTkButton(master=frame, text="Admin ", fg_color="#EEEEEE", command=self.adminCommand,
                                  hover_color="#08e590", font=("Arial Bold", 18), text_color="#601E88", width=275,
                                  height=32,
                                  image=imgdoctor).pack(anchor="w", pady=(20, 0), padx=(15, 0))

        mainpage.mainloop()


    def doctorCommand(self):
        subprocess.Popen([sys.executable, "doctorLogin.py"])

        sys.exit()
    def patientCommand(self):
        subprocess.Popen([sys.executable,  "patientLogin.py"])

        sys.exit()
    def adminCommand(self):
        subprocess.Popen([sys.executable,  "adminLogin.py"])

        sys.exit()


mp=MainPage(window="600x400",title="Welcome to MediCareHub",)
