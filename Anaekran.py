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



#mysql.connector.connect(host="localhost",user="root",password="alperen0519",database="MediCareHub")



class MainPage:

    def __init__(self,window,title):
        mainpage=CTk()
        imgLogo = Image.open("/Users/alperen/Desktop/proje images/logo.png")
        google_icon_data = Image.open("/Users/alperen/Desktop/proje images/google-icon.png")
        imgEmail = Image.open("/Users/alperen/Desktop/proje images/email-icon.png")
        imgUser = Image.open("/Users/alperen/Desktop/proje images/man.png")
        imgPassword = Image.open("/Users/alperen/Desktop/proje images/password-icon.png")
        patientLogo = Image.open("/Users/alperen/Desktop/proje images/patient.png")
        doctorLogo = Image.open("/Users/alperen/Desktop/proje images/doctor.png")
        adminlogo = Image.open("/Users/alperen/Desktop/proje images/admin.png")

        ıdlogo = Image.open("/Users/alperen/Desktop/proje images/id.png")
        namelogo = Image.open("/Users/alperen/Desktop/proje images/id-card.png")
        maillogo = Image.open("/Users/alperen/Desktop/proje images/mail.png")
        genderlogo = Image.open("/Users/alperen/Desktop/proje images/symbol.png")
        bloodlogo = Image.open("/Users/alperen/Desktop/proje images/blood-analysis.png")
        addresslogo = Image.open("/Users/alperen/Desktop/proje images/location-pin.png")

        randevuimage = Image.open("/Users/alperen/Desktop/proje images/appointment.png")
        recetelogo = Image.open("/Users/alperen/Desktop/proje images/prescription.png")
        medikallogo = Image.open("/Users/alperen/Desktop/proje images/insurance.png")
        sigortalogo = Image.open("/Users/alperen/Desktop/proje images/healthcare.png")
        faturalogo = Image.open("/Users/alperen/Desktop/proje images/bill.png")



        imgRandevu = CTkImage(dark_image=randevuimage,light_image=randevuimage,size=(40,40))
        imgLogoCTk = CTkImage(dark_image=imgLogo, light_image=imgLogo, size=(450, 950))
        imgpatient = CTkImage(dark_image=patientLogo, light_image=patientLogo, size=(20,20))
        imgdoctor = CTkImage(dark_image=doctorLogo,light_image=doctorLogo,size=(20,20))
        imgadmin = CTkImage(dark_image=doctorLogo,light_image=doctorLogo,size=(20,20))

        google_icon = CTkImage(dark_image=google_icon_data, light_image=google_icon_data, size=(17, 17))
        userIcon = CTkImage(dark_image=imgUser, light_image=imgUser, size=(22, 22))
        passwordIcon = CTkImage(dark_image=imgPassword, light_image=imgPassword, size=(22, 22))
        ıdlogoIcon = CTkImage(dark_image=ıdlogo, light_image=ıdlogo, size=(50, 50))
        namelogoIcon = CTkImage(dark_image=namelogo, light_image=namelogo, size=(22, 22))
        maillogoIcon = CTkImage(dark_image=maillogo, light_image=maillogo, size=(22, 22))
        genderlogoIcon = CTkImage(dark_image=genderlogo, light_image=genderlogo, size=(22, 22))
        bloodlogoIcon = CTkImage(dark_image=bloodlogo, light_image=bloodlogo, size=(22, 22))
        addresslogoIcon = CTkImage(dark_image=addresslogo, light_image=addresslogo, size=(22, 22))

        randevuimageIcon = CTkImage(dark_image=randevuimage, light_image=randevuimage, size=(50, 50))
        recetelogoIcon = CTkImage(dark_image=recetelogo, light_image=recetelogo, size=(50, 50))
        medikallogoIcon = CTkImage(dark_image=medikallogo, light_image=medikallogo, size=(40, 50))
        sigortalogoIcon = CTkImage(dark_image=sigortalogo, light_image=sigortalogo, size=(50, 50))
        faturalogoIcon= CTkImage(dark_image=faturalogo, light_image=faturalogo, size=(50, 50))

        mainpage.geometry(window)
        mainpage.title(title)
        mainpage.resizable(False,False)



        logoLabel = CTkLabel(master=mainpage, text="", image=imgLogoCTk).pack(expand=False, side="left")

        frame = CTkFrame(master=mainpage, width=750, height=950, fg_color="#ffffff",)

        userIcon = CTkImage(dark_image=imgUser, light_image=imgUser, size=(20, 20))


        frame.pack_propagate(0)

        frame.pack(expand=True, side="right")

        def homepageCommand():
            subprocess.Popen([sys.executable, "mainPage.py"])
            # subprocess.run(["python", "mainPage.py"])
            exit()





        homepageButton = (CTkButton(master=frame, command=homepageCommand, text=" Log out", fg_color="#ffffff",
                                    hover_color="#E44982",
                                    font=("Arial Bold", 14), text_color="#601E88", width=80,height=30)
                        .pack(anchor="w", pady=(20, 0), padx=(15, 0)))

        welcomeLabel = CTkLabel(master=frame, text= "MEDICAREHUB SYSTEM!",
                                                   font=("Arial Bold",42),text_color="#261E76",
                                                   anchor="w",justify=CENTER,)
        welcomeLabel.pack(anchor="w",padx=(125,0),pady=(20,0))

        usernameLabel = CTkLabel(master=frame, text_color="#7E7E7E", anchor="w", justify=CENTER,
                                 text=" Welcome, databaseden gelen isim",
                                 font=("Arial Bold", 24), image=userIcon, compound="left").pack(anchor="w",
                                                                                                pady=(25, 0),
                                                                                                padx=(35, 0))

        randevuButton =  CTkButton(master=frame, text="Appointment", fg_color="#EEEEEE", command=self.randevuCommand,
                                  hover_color="#08e590", font=("Arial Bold", 36), text_color="#601E88", width=325,height=90,
                                               image=randevuimageIcon).pack(anchor="w", pady=(50, 0), padx=(45, 0))

        reçeteButton = CTkButton(master=frame, text="Prescriptions ", fg_color="#EEEEEE", command=self.receteCommand,
                                 hover_color="#08e590", font=("Arial Bold", 36), text_color="#601E88", width=325,
                                 height=90,
                                 image=recetelogoIcon).pack(anchor="w", pady=(30, 0), padx=(375, 0))

        medikalButton = CTkButton(master=frame, text="Medical History", fg_color="#EEEEEE", command=self.medikalCommand,
                                  hover_color="#08e590", font=("Arial Bold", 36), text_color="#601E88", width=325,
                                  height=90,
                                  image=medikallogoIcon).pack(anchor="w", pady=(30, 0), padx=(45, 0))

        sigortaButton = CTkButton(master=frame, text="Insurance ", fg_color="#EEEEEE", command=self.sigortaCommand,
                               hover_color="#08e590", font=("Arial Bold", 36), text_color="#601E88", width=325,
                               height=90,
                               image=sigortalogoIcon).pack(anchor="w", pady=(30, 0), padx=(375, 0))

        faturaButton = CTkButton(master=frame, text="Wage Slip ", fg_color="#EEEEEE", command=self.faturaCommand,
                               hover_color="#08e590", font=("Arial Bold", 36), text_color="#601E88", width=325,
                               height=90,
                               image=faturalogoIcon).pack(anchor="w", pady=(30, 0), padx=(45, 0))

        faturaButton = CTkButton(master=frame, text="Profile ", fg_color="#EEEEEE", command=self.faturaCommand,
                                 hover_color="#08e590", font=("Arial Bold", 36), text_color="#601E88", width=325,
                                 height=90,
                                 image=ıdlogoIcon).pack(anchor="w", pady=(30, 0), padx=(375, 0))

        mainpage.mainloop()


    def randevuCommand(self):
        subprocess.Popen([sys.executable, "randevuekran.py"])
        # subprocess.run(["python", "doctorLogin.py"])
        sys.exit()
    def receteCommand(self):
        subprocess.Popen([sys.executable,  "receteekran.py"])
        #subprocess.run(["python", "patientLogin.py"])
        sys.exit()

    def medikalCommand(self):
        subprocess.Popen([sys.executable, "medikalekran.py"])
        # subprocess.run(["python", "adminLogin.py"])
        sys.exit()

    def sigortaCommand(self):
        subprocess.Popen([sys.executable,  "sigortaekran.py"])
        # subprocess.run(["python", "adminLogin.py"])
        sys.exit()

    def faturaCommand(self):
        subprocess.Popen([sys.executable,  "faturaekran.py"])
        # subprocess.run(["python", "adminLogin.py"])
        sys.exit()



mp = MainPage(window="1200x950", title="Welcome to MediCareHub", )