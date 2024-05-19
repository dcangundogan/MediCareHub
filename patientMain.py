import subprocess
import tkinter as tk
import customtkinter as ctk
from customtkinter import *
from PIL import Image
import mysql.connector
from CTkMessagebox import CTkMessagebox
import patientsPrescription
import patientsHistory
import patientProfile
import patientInsurance
import patientAppointment
import patientInvoice
import patientLab


class PatientMainPage:
    ekran = "1200x1200"
    baslik = "Welcome"

    def __init__(self, patientid):
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="bercan2003",
            database="MediCareHub"
        )
        self.patientid = patientid
        patientname = self.get_patient_name(patientid)

        self.app = CTk()
        self.app.geometry(self.ekran)
        self.app.title(self.baslik)
        self.app.resizable(False, False)

        imgLogo = Image.open("images/logo.png")
        imgUser = Image.open("images/man.png")

        ıdlogo = Image.open("images/id.png")
        randevuimage = Image.open("images/appointment.png")
        recetelogo = Image.open("images/prescription.png")
        medikallogo = Image.open("images/insurance.png")
        sigortalogo = Image.open("images/healthcare.png")
        faturalogo = Image.open("images/bill.png")
        calışmaalanllogo = Image.open("images/surgery-room (2).png")

        imgLogoicon = CTkImage(dark_image=imgLogo, light_image=imgLogo, size=(450, 1200))


        userIcon = CTkImage(dark_image=imgUser, light_image=imgUser, size=(22, 22))

        ıdlogoIcon = CTkImage(dark_image=ıdlogo, light_image=ıdlogo, size=(50, 50))

        randevuimageIcon = CTkImage(dark_image=randevuimage, light_image=randevuimage, size=(40, 40))
        recetelogoIcon = CTkImage(dark_image=recetelogo, light_image=recetelogo, size=(40, 40))
        medikallogoIcon = CTkImage(dark_image=medikallogo, light_image=medikallogo, size=(40, 40))
        sigortalogoIcon = CTkImage(dark_image=sigortalogo, light_image=sigortalogo, size=(40, 40))
        faturalogoIcon = CTkImage(dark_image=faturalogo, light_image=faturalogo, size=(40, 40))
        calışmaalanllogoıcon = CTkImage(dark_image=calışmaalanllogo, light_image=calışmaalanllogo, size=(40, 40))

        logoLabel = CTkLabel(master=self.app, text="", image=imgLogoicon).pack(expand=True, side="left")

        frame = CTkFrame(master=self.app, width=900, height=1200, fg_color="#ffffff")
        frame.pack_propagate(0)
        frame.pack(expand=True, side="right")

        def homepageCommand():
            subprocess.Popen([sys.executable, "mainPage.py"])
            self.app.destroy()

        homepageButton = CTkButton(master=frame, command=homepageCommand, text=" Log out", fg_color="#ffffff",
                                   hover_color="#E44982", font=("Arial Bold", 14), text_color="#601E88", width=80,
                                   height=30).pack(anchor="w", pady=(20, 0), padx=(15, 0))

        welcomeLabel = CTkLabel(master=frame, text="MEDICAREHUB SYSTEM!",
                                font=("Arial Bold", 42), text_color="#261E76", anchor="w", justify=CENTER)
        welcomeLabel.pack(anchor="w", padx=(125, 0), pady=(20, 0))

        usernameLabel = CTkLabel(master=frame, text_color="#000000", anchor="w", justify=CENTER,
                                 text=f" Welcome {patientname}", font=("Arial Bold", 24), image=userIcon,
                                 compound="left").pack(anchor="w", pady=(25, 0), padx=(35, 0))

        def getappointment():
            self.app.destroy()
            manager = patientAppointment.AppointmentManager(self.patientid)
            manager.run()
        def getprescription():
            self.app.destroy()
            manager = patientsPrescription.PrescriptionsPage(self.patientid)
            manager.run()
        def getmedicalhistory():
            self.app.destroy()
            manager = patientsHistory.MedicalHistoryPage(self.patientid)
            manager.run()
        def getpatientprofile():
            self.app.destroy()
            manager = -patientProfile.ProfileMainPage(self.patientid)
            manager.run()
        def getpatientinsurance():
            self.app.destroy()
            manager = patientInsurance.InsuranceInfoPage(self.patientid)
            manager.run()
        def getpatientInvoice():
            self.app.destroy()
            manager= patientInvoice.InvoicePage(self.patientid)
            manager.run()
        def getpatientresult():
            self.app.destroy()
            manager = patientLab.LabPage(self.patientid)
            manager.run()

        randevuButton = CTkButton(master=frame, text="Appointment", fg_color="#EEEEEE", command=getappointment,
                                  hover_color="#08e590", font=("Arial Bold", 36), text_color="#601E88", width=325,
                                  height=90, image=randevuimageIcon).pack(anchor="w", pady=(50, 0), padx=(45, 0))

        reçeteButton = CTkButton(master=frame, text="Prescriptions ", fg_color="#EEEEEE", command=getprescription,
                                 hover_color="#08e590", font=("Arial Bold", 36), text_color="#601E88", width=325,
                                 height=90, image=recetelogoIcon).pack(anchor="w", pady=(30, 0), padx=(375, 0))

        medicalhistoryButton = CTkButton(master=frame, text="Medical History", fg_color="#EEEEEE", command=getmedicalhistory,
                                  hover_color="#08e590", font=("Arial Bold", 36), text_color="#601E88", width=325,
                                  height=90, image=medikallogoIcon).pack(anchor="w", pady=(30, 0), padx=(45, 0))

        insuranceButton = CTkButton(master=frame, text="Insurance", fg_color="#EEEEEE", command=getpatientinsurance,
                                  hover_color="#08e590", font=("Arial Bold", 36), text_color="#601E88", width=325,
                                  height=90, image=sigortalogoIcon).pack(anchor="w", pady=(30, 0), padx=(375, 0))

        profileButton = CTkButton(master=frame, text="Profile ", fg_color="#EEEEEE", command=getpatientprofile,
                                 hover_color="#08e590", font=("Arial Bold", 36), text_color="#601E88", width=325,
                                 height=90, image=ıdlogoIcon).pack(anchor="w", pady=(30, 0), padx=(45, 0))

        InvoiceButton = CTkButton(master=frame, text="Show Invoice ", fg_color="#EEEEEE", command=getpatientInvoice,
                                  hover_color="#08e590", font=("Arial Bold", 36), text_color="#601E88", width=325,
                                  height=90, image=ıdlogoIcon).pack(anchor="w", pady=(30, 0), padx=(375, 0))
        resultButton=CTkButton(master=frame, text="Results", fg_color="#EEEEEE", command=getpatientresult,
                                  hover_color="#08e590", font=("Arial Bold", 36), text_color="#601E88", width=325,
                                  height=90, image=ıdlogoIcon).pack(anchor="w", pady=(30, 0), padx=(45, 0))
        self.app.mainloop()

    def get_patient_name(self, patientid):
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="bercan2003",
            database="MediCareHub",
        )
        query = """SELECT CONCAT(Patient_Fname," ",Patient_Lname) AS FullName FROM Patient where Patient_ID=%s"""
        mycursor = mydb.cursor()
        mycursor.execute(query, (patientid,))
        result = mycursor.fetchone()
        username = result[0]
        return username

    def run(self):
        self.app.mainloop()


