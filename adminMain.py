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







class AdminMainPage:

    def __init__(self,window,title,username):
        self.window = window
        self.title = title
        self.username = username
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

        randevuimage = Image.open("images/appointment.png")
        recetelogo = Image.open("images/prescription.png")
        medikallogo = Image.open("images/insurance.png")
        sigortalogo = Image.open("images/healthcare.png")
        faturalogo = Image.open("images/bill.png")
        calışmaalanllogo = Image.open("images/surgery-room (2).png")
        stafflogo = Image.open("images/staff.png")
        departmentlogo =Image.open("images/department.png")
        databaselogo = Image.open("images/database.png")



        imgRandevu = CTkImage(dark_image=randevuimage,light_image=randevuimage,size=(40,40))
        imgLogoCTk = CTkImage(dark_image=imgLogo, light_image=imgLogo, size=(450, 950))
        imgpatient = CTkImage(dark_image=patientLogo, light_image=patientLogo, size=(50,50))
        imgdoctor = CTkImage(dark_image=doctorLogo,light_image=doctorLogo,size=(20,20))
        imgadmin = CTkImage(dark_image=doctorLogo,light_image=doctorLogo,size=(20,20))

        doctorlogoicon = CTkImage(dark_image=doctorLogo, light_image=doctorLogo, size=(50, 50))
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
        calışmaalanllogoıcon =CTkImage(dark_image=calışmaalanllogo,light_image=calışmaalanllogo,size=(50,50))
        databaselogoicon = CTkImage(dark_image=databaselogo, light_image=databaselogo, size=(50, 50))
        stafflogoicon = CTkImage(dark_image=stafflogo, light_image=stafflogo, size=(50, 50))
        departmentlogoicon = CTkImage(dark_image=departmentlogo, light_image=departmentlogo, size=(50, 50))

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
                                 text=f" Welcome Admin : {username}",
                                 font=("Arial Bold", 24), image=userIcon, compound="left").pack(anchor="w",
                                                                                                pady=(25, 0),
                                                                                                padx=(35, 0))

        randevuButton =  CTkButton(master=frame, text="Appointments", fg_color="#EEEEEE", command=self.randevuCommand,
                                  hover_color="#08e590", font=("Arial Bold", 36), text_color="#601E88", width=325,height=90,
                                               image=randevuimageIcon).pack(anchor="w", pady=(50, 0), padx=(45, 0))

        doctorButton = CTkButton(master=frame, text="Doctors ", fg_color="#EEEEEE", command=self.receteCommand,
                                 hover_color="#08e590", font=("Arial Bold", 36), text_color="#601E88", width=325,
                                 height=90,
                                 image=doctorlogoicon).pack(anchor="w", pady=(30, 0), padx=(375, 0))

        patientButton = CTkButton(master=frame, text="Patients", fg_color="#EEEEEE", command=self.medikalCommand,
                                  hover_color="#08e590", font=("Arial Bold", 36), text_color="#601E88", width=325,
                                  height=90,
                                  image=imgpatient).pack(anchor="w", pady=(30, 0), padx=(45, 0))

        departmentButton = CTkButton(master=frame, text="Departments ", fg_color="#EEEEEE", command=self.calısmaCommand,
                               hover_color="#08e590", font=("Arial Bold", 36), text_color="#601E88", width=325,
                               height=90,
                               image=departmentlogoicon).pack(anchor="w", pady=(30, 0), padx=(375, 0))

        databaseButton = CTkButton(master=frame, text="SQL Editor", fg_color="#EEEEEE", command=self.calısmaCommand,
                               hover_color="#08e590", font=("Arial Bold", 36), text_color="#601E88", width=325,
                               height=90,
                               image=databaselogoicon).pack(anchor="w", pady=(30, 0), padx=(45, 0))

        staffButton = CTkButton(master=frame, text="Staff ", fg_color="#EEEEEE", command=self.faturaCommand,
                                 hover_color="#08e590", font=("Arial Bold", 36), text_color="#601E88", width=325,
                                 height=90,
                                 image=stafflogoicon).pack(anchor="w", pady=(30, 0), padx=(375, 0))

        mainpage.mainloop()


    def randevuCommand(self):
        subprocess.Popen([sys.executable, "randevuekran.py"])

        sys.exit()
    def receteCommand(self):
        subprocess.Popen([sys.executable,  "receteekran.py"])

        sys.exit()

    def medikalCommand(self):
        subprocess.Popen([sys.executable, "medikalekran.py"])

        sys.exit()

    def calısmaCommand(self):
        subprocess.Popen([sys.executable,  "sigortaekran.py"])

        sys.exit()

    def sigortaCommand(self):
        subprocess.Popen([sys.executable, "sigortaekran.py"])

        sys.exit()

    def faturaCommand(self):
        subprocess.Popen([sys.executable,  "faturaekran.py"])

        sys.exit()



mp =AdminMainPage(window="1280x950",title="Welcome to MediHubCare Services",username="D.can")