import subprocess

from customtkinter import *
from PIL import Image
import mysql.connector
from adminAppointment import AdminAppointmentPage
from adminDoctors import AdminDoctorPage
from adminSQLEditor import SQLEditorPage
from adminStaffs import AdminStaffPage
from adminDepartment import AdminDepartmentPage
from adminPatient import AdminPatientPage
from adminSQLEditor import SQLEditorPage


class AdminMainPage:
    ekran = "1200x1000"
    baslik = "Welcome"

    def __init__(self, adminid):
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="bercan2003",
            database="MediCareHub"
        )
        self.adminid = adminid
        adminname = self.get_admin_name(adminid)

        self.app = CTk()
        self.app.geometry(self.ekran)
        self.app.title(self.baslik)
        self.app.resizable(False, False)

        imgLogo = Image.open("images/logo.png")
        google_icon_data = Image.open("images/google-icon.png")
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
        databaselogo= Image.open("images/database.png")

        imgRandevu = CTkImage(dark_image=randevuimage, light_image=randevuimage, size=(40, 40))
        imgLogoicon = CTkImage(dark_image=imgLogo, light_image=imgLogo, size=(450, 950))
        imgpatient = CTkImage(dark_image=patientLogo, light_image=patientLogo, size=(20, 20))
        imgdoctor = CTkImage(dark_image=doctorLogo, light_image=doctorLogo, size=(20, 20))

        userIcon = CTkImage(dark_image=imgUser, light_image=imgUser, size=(22, 22))

        ıdlogoIcon = CTkImage(dark_image=ıdlogo, light_image=ıdlogo, size=(50, 50))




        medikallogoIcon = CTkImage(dark_image=medikallogo, light_image=medikallogo, size=(40, 50))


        databaseicon=CTkImage(dark_image=databaselogo,light_image=databaselogo,size=(50,50))

        logoLabel = CTkLabel(master=self.app, text="", image=imgLogoicon).pack(expand=True, side="left")

        frame = CTkFrame(master=self.app, width=750, height=950, fg_color="#ffffff")
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
                                 text=f" Welcome {adminname}", font=("Arial Bold", 24), image=userIcon,
                                 compound="left").pack(anchor="w", pady=(25, 0), padx=(35, 0))
        # def getappointment():
        #     self.app.destroy()
        #     manager = AppointmentManager(self.doctorid)
        #     manager.run()
        # def getprescription():
        #     self.app.destroy()
        #     manager = DoctorPrescriptionsPage(self.doctorid)
        #     manager.run()
        # def getworkfield():
        #     self.app.destroy()
        #     manager = DoctorWorkFieldPage(self.doctorid)
        #     manager.run()
        # def getdoctorprofile():
        #     self.app.destroy()
        #     manager = DoctorProfileMainPage(self.doctorid)
        #     manager.run()
        # def getmedicalhistory():
        #     self.app.destroy()
        #     manager = DoctorMedicalHistoryPage(self.doctorid)
        #     manager.run()
        def getappointmentpage():
            self.app.destroy()
            manager = AdminAppointmentPage()
            manager.run()

        def getdoctorspage():
            self.app.destroy()
            manager = AdminDoctorPage()
            manager.run()
        def getstaffpage():
            self.app.destroy()
            manager = AdminStaffPage()
            manager.run()
        def getadminpatient():
            self.app.destroy()
            manager = AdminPatientPage()
            manager.run()
        def getadmindepartment():
            self.app.destroy()
            manager = AdminDepartmentPage()
            manager.run()
        def getsqleditor():
            self.app.destroy()
            manager = SQLEditorPage()
            manager.run()



        doctorsButton = CTkButton(master=frame, text="Doctors", fg_color="#EEEEEE",command=getdoctorspage,
                                  hover_color="#08e590", font=("Arial Bold", 36), text_color="#601E88", width=325,
                                  height=90, image=imgdoctor).pack(anchor="w", pady=(50, 0), padx=(45, 0))

        patientsButton = CTkButton(master=frame, text="Patients ", fg_color="#EEEEEE",command=getadminpatient,
                                 hover_color="#08e590", font=("Arial Bold", 36), text_color="#601E88", width=325,
                                 height=90, image=imgpatient).pack(anchor="w", pady=(30, 0), padx=(375, 0))

        departmentsButton = CTkButton(master=frame, text="Departments", fg_color="#EEEEEE",command=getadmindepartment,
                                  hover_color="#08e590", font=("Arial Bold", 36), text_color="#601E88", width=325,
                                  height=90, image=medikallogoIcon).pack(anchor="w", pady=(30, 0), padx=(45, 0))

        databaseButton = CTkButton(master=frame, text="SQL Editor ", fg_color="#EEEEEE",command=getsqleditor,
                                      hover_color="#08e590", font=("Arial Bold", 36), text_color="#601E88", width=325,
                                      height=90,
                                      image=databaseicon).pack(anchor="w", pady=(30, 0), padx=(375, 0))

        staffButton = CTkButton(master=frame, text="Stafffs", fg_color="#EEEEEE",command=getstaffpage,
                                 hover_color="#08e590", font=("Arial Bold", 36), text_color="#601E88", width=325,
                                 height=90, image=ıdlogoIcon).pack(anchor="w", pady=(30, 0), padx=(45, 0))

        appointmentsButton = CTkButton(master=frame, text="Appointments ", fg_color="#EEEEEE",command=getappointmentpage,
                                hover_color="#08e590", font=("Arial Bold", 36), text_color="#601E88", width=325,
                                height=90, image=imgRandevu).pack(anchor="w", pady=(30, 0), padx=(375, 0))
        self.app.mainloop()

    def get_admin_name(self, adminid):
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="bercan2003",
            database="MediCareHub",
        )
        query = """SELECT username AS FullName FROM admin where admin_id=%s"""
        mycursor = mydb.cursor()
        mycursor.execute(query, (adminid,))
        result = mycursor.fetchone()
        username = result[0]
        return username

    def run(self):
        self.app.mainloop()




