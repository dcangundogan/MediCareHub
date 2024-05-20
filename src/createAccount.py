import customtkinter
import tkinter
from customtkinter import *
from tkinter import *
from PIL import *
import mysql.connector
from CTkMessagebox import *
import subprocess
import sys

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="bercan2003",
    database="MediCareHub",
      # Authentication plugin
)





app = CTk()

app.geometry("860x1000")

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
phoneLogo = Image.open("images/phone.png")

imgLogoCTk =CTkImage(dark_image=imgLogo,light_image=imgLogo,size=(400,1000))

google_icon = CTkImage(dark_image=google_icon_data, light_image=google_icon_data, size=(17,17))
userIcon = CTkImage(dark_image=imgUser, light_image=imgUser,size=(22,22))
passwordIcon = CTkImage(dark_image=imgPassword,light_image=imgPassword, size=(22,22))
ıdlogoIcon = CTkImage(dark_image=ıdlogo ,light_image=ıdlogo, size=(22,22))
namelogoIcon = CTkImage(dark_image=namelogo ,light_image=namelogo, size=(22,22))
maillogoIcon = CTkImage(dark_image= maillogo,light_image=maillogo, size=(22,22))
genderlogoIcon = CTkImage(dark_image= genderlogo,light_image=genderlogo, size=(22,22))
bloodlogoIcon = CTkImage(dark_image= bloodlogo,light_image=bloodlogo, size=(22,22))
addresslogoIcon = CTkImage(dark_image= addresslogo,light_image=addresslogo, size=(22,22))
phonelogoIcon = CTkImage(dark_image= phoneLogo,light_image=phoneLogo, size=(22,22))








#MediCareHub frame kismi
logoLabel = CTkLabel(master=app, text="", image=imgLogoCTk).pack(expand=False, side="left")


frame = CTkFrame(master=app, width=480, height=1000, fg_color="#ffffff")

frame.pack_propagate(0)

frame.pack(expand=True, side="right")

#MediCareHub frame bitis

def patientpageCommand():
    subprocess.Popen([sys.executable,  "patientLogin.py"])
    # subprocess.run(["python", "mainPage.py"])
    exit()


homepageButton = (CTkButton(master=frame,command=patientpageCommand, text="Home Page", fg_color="#ffffff", hover_color="#E44982",
                        font=("Arial Bold", 10), text_color="#601E88", width=80,height=30)
                        .pack(anchor="w", pady=(20, 0), padx=(15, 0)))



medicarehubLabel = CTkLabel(master=frame,text_color="#261E76",anchor="w",justify=CENTER,
                            text="Welcome to MediCareHub!",
                            font=("Arial Bold",30)).pack(anchor="w",pady=(40,5),padx=(60,0))

signLabel = CTkLabel(master=frame,text_color="#7E7E7E",anchor="w",justify="left",
                            text="Please enter your information correctly.",
                            font=("Arial Bold",16)).pack(anchor="w",pady=(2,0), padx=(95,0))

workerLabel = CTkLabel(master=frame,text_color="#7E7E7E",anchor="w",justify=CENTER,
                       text="We wish you a healthy day!",
                       font=("Arial Bold",16)).pack(anchor="w",pady=(0,0), padx=(140,0))

PatientIDLabel = CTkLabel(master=frame,text_color="#7E7E7E",anchor="w",justify=CENTER,
                            text=" Patient ID:",
                            font=("Arial Bold",16),image=ıdlogoIcon,compound="left").pack(anchor="w",pady=(25,0),padx=(80,0))

PatientIDEntry = CTkEntry(master=frame,width=300,height=35 ,fg_color="#EEEEEE",border_color="#261E76",border_width=2
                         ,text_color="#000000")
PatientIDEntry.pack(anchor="w",padx=(80,0))


firstnameLabel = CTkLabel(master=frame,text_color="#7E7E7E",anchor="w",justify=CENTER,
                            text=" First Name:",
                            font=("Arial Bold",16),image=namelogoIcon,compound="left").pack(anchor="w",pady=(10,0),padx=(80,0))

firstnameEntry = CTkEntry(master=frame,width=300,height=35 ,fg_color="#EEEEEE",border_color="#261E76",border_width=2
                         ,text_color="#000000")
firstnameEntry.pack(anchor="w",padx=(80,0))

SurnameLabel = CTkLabel(master=frame,text_color="#7E7E7E",anchor="w",justify=CENTER,
                            text=" Surname:",
                            font=("Arial Bold",16),image=namelogoIcon,compound="left").pack(anchor="w",pady=(10,0),padx=(80,0))

SurnameEntry = CTkEntry(master=frame,width=300,height=35 ,fg_color="#EEEEEE",border_color="#261E76",border_width=2
                         ,text_color="#000000")
SurnameEntry.pack(anchor="w",padx=(80,0))

phoneLabel = CTkLabel(master=frame,text_color="#7E7E7E",anchor="w",justify=CENTER,
                            text="Phone Number:",
                            font=("Arial Bold",16),image=phonelogoIcon,compound="left").pack(anchor="w",pady=(10,0),padx=(80,0))

phoneEntry = CTkEntry(master=frame,width=300,height=35 ,fg_color="#EEEEEE",border_color="#261E76",border_width=2
                         ,text_color="#000000")
phoneEntry.pack(anchor="w",padx=(80,0))

usernameLabel = CTkLabel(master=frame,text_color="#7E7E7E",anchor="w",justify=CENTER,
                            text=" Username:",
                            font=("Arial Bold",16),image=userIcon,compound="left").pack(anchor="w",pady=(10,0),padx=(80,0))

usernameEntry = CTkEntry(master=frame,width=300,height=35 ,fg_color="#EEEEEE",border_color="#261E76",border_width=2
                         ,text_color="#000000")
usernameEntry.pack(anchor="w",padx=(80,0))


emailLabel = CTkLabel(master=frame,text_color="#7E7E7E",anchor="w",justify=CENTER,
                            text="E-mail address:",
                            font=("Arial Bold",16),image=maillogoIcon,compound="left").pack(anchor="w",pady=(10,0),padx=(80,0))

emailEntry = CTkEntry(master=frame,width=300,height=35 ,fg_color="#EEEEEE",border_color="#261E76",border_width=2
                         ,text_color="#000000")
emailEntry.pack(anchor="w",padx=(80,0))

GenderLabel = CTkLabel(master=frame,text_color="#7E7E7E",anchor="w",justify=CENTER,
                            text=" Gender (female/male):",
                            font=("Arial Bold",16),image=genderlogoIcon,compound="left").pack(anchor="w",pady=(10,0),padx=(80,0))

GenderEntry = CTkEntry(master=frame,width=300,height=35 ,fg_color="#EEEEEE",border_color="#261E76",border_width=2
                         ,text_color="#000000")
GenderEntry.pack(anchor="w",padx=(80,0))

BloodLabel = CTkLabel(master=frame,text_color="#7E7E7E",anchor="w",justify=CENTER,
                            text=" Blood Type (0,AB,A,B(+, -)):",
                            font=("Arial Bold",16),image=bloodlogoIcon ,compound="left").pack(anchor="w",pady=(10,0),padx=(80,0))

BloodEntry = CTkEntry(master=frame,width=300,height=35 ,fg_color="#EEEEEE",border_color="#261E76",border_width=2
                         ,text_color="#000000")
BloodEntry.pack(anchor="w",padx=(80,0))

AddressLabel = CTkLabel(master=frame,text_color="#7E7E7E",anchor="w",justify=CENTER,
                            text=" Address:",
                            font=("Arial Bold",16),image=addresslogoIcon,compound="left").pack(anchor="w",pady=(10,0),padx=(80,0))

AddressEntry = CTkEntry(master=frame,width=300,height=35 ,fg_color="#EEEEEE",border_color="#261E76",border_width=2
                         ,text_color="#000000")
AddressEntry.pack(anchor="w",padx=(80,0))



passwordLabel = CTkLabel(master=frame,text_color="#7E7E7E",anchor="w",justify="left",
                            text=" Password:",
                            font=("Arial Bold",16),image=passwordIcon,compound="left").pack(anchor="w",pady=(10,0),padx=(80,0))

passwordEntry = CTkEntry(master=frame,width=300,height=35 , fg_color="#EEEEEE",border_color="#261E76",border_width=2
                         ,text_color="#000000",show="*")
passwordEntry.pack(anchor="w",padx=(80,0))












nextpatientID = 8
def patientinsertcommand():
    # Retrieve data from entry fields
    patientid = PatientIDEntry.get()
    username = usernameEntry.get()
    password = passwordEntry.get()
    firstname = firstnameEntry.get()
    surname = SurnameEntry.get()
    phone = phoneEntry.get()
    blood = BloodEntry.get()
    email = emailEntry.get()
    gender = GenderEntry.get()
    address = AddressEntry.get()
    condition =   None
    admission_date =   None
    discharge_date =  None


    if not (patientid and firstname and surname and phone and email and gender and address):
        CTkMessagebox(title="Missing Data", message="Please fill in all required fields.", icon="warning")
        return

    query = """
    INSERT INTO patient(
        `Patient_ID`,
        `Patient_Fname`,
        `Patient_Lname`,
        `Phone`,
        `Blood_Type`,
        `Email`,
        `Gender`,
        `Condition_`,
        `Admisson_Date`,
        `Discharge_Date`,
        `Address`)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    try:
        mycursor = mydb.cursor()
        mycursor.execute(
            query,(patientid, firstname, surname, phone, blood, email, gender, condition, admission_date, discharge_date, address)
        )
        mydb.commit()
        patientlogin(patientid,username,password)
        mycursor.close()
        CTkMessagebox(title="Success", message="Patient inserted successfully.", icon="check")
    except mysql.connector.Error as e:
        CTkMessagebox(title="Database Error", message=f"An error occurred: {e}", icon="cancel")
    except Exception as e:
        CTkMessagebox(title="Error", message=f"An unexpected error occurred: {e}", icon="cancel")


def patientlogin(patientid,username,password):
    if not (patientid and username and password):
        CTkMessagebox(title="Missing Data", message="Please fill in all required fields.", icon="warning")
        return
    query = """INSERT INTO `loginpagepatient` (
      `User_id`, 
      `Patient_ID`, 
      `Username`, 
      `Password`
    ) VALUES
    (%s,%s,%s,%s)
    """
    try:
        mycursor = mydb.cursor()
        mycursor.execute(
            query,(patientid,patientid,username,password)
        )
        mydb.commit()
        mycursor.close()
        CTkMessagebox(title="Success", message="Patient inserted successfully.", icon="check")
    except mysql.connector.Error as e:
        CTkMessagebox(title="Database Error", message=f"An error occurred: {e}", icon="cancel")
    except Exception as e:
        CTkMessagebox(title="Error", message=f"An unexpected error occurred: {e}", icon="cancel")




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





app.title("MediCareHub Account Creator")

set_appearance_mode("light")

loginButton = CTkButton(master=frame,command=patientinsertcommand, text="Sign Up", fg_color="#601E88", hover_color="#E44982",
                        font=("Arial Bold", 12), text_color="#ffffff", width=300,height=40).pack(anchor="w", pady=(30, 0), padx=(80, 0))



app.mainloop()
