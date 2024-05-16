import time

import customtkinter
import tkinter
from tkinter import Tk, messagebox
from customtkinter import *
from tkinter import *
from PIL import *
import mysql.connector
from CTkMessagebox import *
import subprocess
import sys
import mysql.connector
from tkinter import messagebox
from doctorMain import doctorMainPage

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="bercan2003",
    database="MediCareHub",
)




app = CTk()

app.geometry("600x480")


app.resizable(True,True)
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



imgLogoCTk =CTkImage(dark_image=imgLogo,light_image=imgLogo,size=(300,480))

google_icon = CTkImage(dark_image=google_icon_data, light_image=google_icon_data, size=(17,17))

userIcon = CTkImage(dark_image=imgUser, light_image=imgUser,size=(20,20))

passwordIcon = CTkImage(dark_image=imgPassword,light_image=imgPassword, size=(20,20))

google_icon = CTkImage(dark_image=google_icon_data, light_image=google_icon_data, size=(17,17))
userIcon = CTkImage(dark_image=imgUser, light_image=imgUser,size=(22,22))
passwordIcon = CTkImage(dark_image=imgPassword,light_image=imgPassword, size=(22,22))
ıdlogoIcon = CTkImage(dark_image=ıdlogo ,light_image=ıdlogo, size=(22,22))
namelogoIcon = CTkImage(dark_image=namelogo ,light_image=namelogo, size=(22,22))
maillogoIcon = CTkImage(dark_image= maillogo,light_image=maillogo, size=(22,22))
genderlogoIcon = CTkImage(dark_image= genderlogo,light_image=genderlogo, size=(22,22))
bloodlogoIcon = CTkImage(dark_image= bloodlogo,light_image=bloodlogo, size=(22,22))
addresslogoIcon = CTkImage(dark_image= addresslogo,light_image=addresslogo, size=(22,22))


#MediCareHub frame kismi
logoLabel = CTkLabel(master=app, text="", image=imgLogoCTk).pack(expand=True, side="left")


frame = CTkFrame(master=app, width=300, height=480, fg_color="#ffffff")

frame.pack_propagate(0)

frame.pack(expand=True, side="right")

#MediCareHub frame bitis

def homepageCommand():

    subprocess.Popen([sys.executable, "mainPage.py"])
    exit()


homepageButton = (CTkButton(master=frame,command=homepageCommand, text="Home Page", fg_color="#ffffff", hover_color="#E44982",
                        font=("Arial Bold", 9), text_color="#601E88", width=60,height=20)
                        .pack(anchor="w", pady=(10, 0), padx=(10, 0)))


medicarehubLabel = CTkLabel(master=frame,text_color="#261E76",anchor="w",justify=CENTER,
                            text="Welcome to \n"
                                 "MediCareHub!",
                            font=("Arial Bold",28)).pack(anchor="w",pady=(50,5),padx=(65,0))

signLabel = CTkLabel(master=frame,text_color="#7E7E7E",anchor="w",justify="left",
                        text="Hello admin please login to    \n"
                                 "   MediCareHub System!",
                            font=("Arial Bold",14)).pack(anchor="w",pady=(5,0), padx=(75,0))

warningLabel = CTkLabel(master=frame,text_color="#7E7E7E",anchor="w",justify=CENTER,
                       text=" Unauthorized entry is prohibited!",
                       font=("Arial Bold",14)).pack(anchor="w",pady=(0,0), padx=(50,0))

workerLabel = CTkLabel(master=frame,text_color="#7E7E7E",anchor="w",justify=CENTER,
                       text="WİSH YOU GOOD WORK",
                       font=("Arial Bold",14)).pack(anchor="w",pady=(0,0), padx=(75,0))

usernameLabel = CTkLabel(master=frame,text_color="#7E7E7E",anchor="w",justify=CENTER,
                            text=" Username:",
                            font=("Arial Bold",14),image=userIcon,compound="left").pack(anchor="w",pady=(15,0),padx=(30,0))

usernameEntry = CTkEntry(master=frame,width=240,height=30 ,fg_color="#EEEEEE",border_color="#261E76",border_width=2
                         ,text_color="#000000")
usernameEntry.pack(anchor="w",padx=(30,0))



passwordLabel = CTkLabel(master=frame,text_color="#7E7E7E",anchor="w",justify="left",
                            text=" Password:",
                            font=("Arial Bold",14),image=passwordIcon,compound="left").pack(anchor="w",pady=(10,0),padx=(30,0))

passwordEntry = CTkEntry(master=frame,width=240,height=30 , fg_color="#EEEEEE",border_color="#261E76",border_width=2
                         ,text_color="#000000",show="*")
passwordEntry.pack(anchor="w",padx=(30,0))





def admingiriscommand():
    subprocess.Popen([sys.executable, "Anaekran.py"])

    sys.exit()

def loginChecker():
    try:
        username = usernameEntry.get()
        password = passwordEntry.get()

        if not username or not password:
            CTkMessagebox(title="Error", message="Username or password cannot be empty.", icon="cancel")
            return

        mycursor = mydb.cursor()



        # Update the column name based on your table schema
        query = "SELECT password FROM admin WHERE username = %s"
        mycursor.execute(query, (username,))

        myresult = mycursor.fetchone()

        if myresult:
            real_password = myresult[0]

            if real_password == password:
                CTkMessagebox(title="Info", message="Welcome to MediCareHub Services!")




            else:
                CTkMessagebox(title="Error", message="Username or password is incorrect.", icon="cancel")
        else:
            CTkMessagebox(title="Error", message="No access: User not found.", icon="cancel")

    except mysql.connector.Error as e:
        print(f"Database error: {e}")
        CTkMessagebox(title="Error", message="Database error: Please check the logs for details.", icon="cancel")







app.title("MediCareHub Login Page")

set_appearance_mode("light")







loginButton = CTkButton(master=frame,command=loginChecker, text="Login", fg_color="#601E88", hover_color="#E44982",
                        font=("Arial Bold", 12), text_color="#ffffff", width=240,height=35).pack(anchor="w", pady=(30, 0), padx=(30, 0))





app.mainloop()
