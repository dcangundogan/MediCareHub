import customtkinter as ctk
from PIL import Image
import mysql.connector
import doctorEditProfile
import doctorMain

class DoctorProfileMainPage:
    def __init__(self, doctor_id):
        self.doctor_id = doctor_id
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="bercan2003",
            database="MediCareHub"
        )

        self.app = ctk.CTk()
        self.app.geometry("800x800")
        self.app.title("Doctor Profile")
        self.app.resizable(False, False)


        imgLogo = Image.open("images/logo.png").resize((300, 300))
        imgLogoicon = ctk.CTkImage(dark_image=imgLogo, light_image=imgLogo, size=(300, 300))
        userLogo = Image.open("images/medical-team.png").resize((120, 120))
        imgUsericon = ctk.CTkImage(dark_image=userLogo, light_image=userLogo, size=(120, 120))


        logoLabel = ctk.CTkLabel(master=self.app, text="", image=imgLogoicon)
        logoLabel.image = imgLogoicon  # Keep a reference!
        logoLabel.pack(side="left", fill="y")


        frame = ctk.CTkFrame(master=self.app, width=500, height=600, fg_color="#ffffff")
        frame.pack_propagate(0)
        frame.pack(side="right", fill="both", expand=True)


        userLabel = ctk.CTkLabel(master=frame, text="", image=imgUsericon, bg_color="#ffffff")
        userLabel.image = imgUsericon
        userLabel.place(x=180, y=10)


        self.display_doctor_info(frame)

        # Edit Profile Button
        edit_button = ctk.CTkButton(master=frame, text="Edit Profile", command=self.edit_profile)
        edit_button.place(x=200, y=500)  # Adjust placement

        # Back Button
        back_button = ctk.CTkButton(master=frame, text="Back", command=self.go_back, fg_color="#1C2833", text_color="#F2F3F4", hover_color="#1A5276")
        back_button.place(x=200, y=600)  # Adjust placement

        self.app.mainloop()

    def display_doctor_info(self, frame):

        try:
            cursor = self.mydb.cursor()
            query = """
                SELECT d.DoctorName, d.DoctorSurname, d.Specialization, dept.Dept_Name 
                FROM Doctor d 
                JOIN Department dept ON d.Dept_ID = dept.Dept_ID 
                WHERE d.Doctor_ID = %s
            """
            cursor.execute(query, (self.doctor_id,))
            result = cursor.fetchone()

            if result:
                labels = ['First Name:', 'Last Name:', 'Specialization:', 'Department:']
                for index, (label, value) in enumerate(zip(labels, result)):
                    if value is not None:  # Check if the value is not None
                        info_label = ctk.CTkLabel(master=frame, text=f"{label} {value}", font=("Arial", 12), text_color="#000000")
                        info_label.place(x=20, y=150 + 30 * index)  # Adjust placement

        except mysql.connector.Error as error:
            print("Failed to read data from MySQL table:", error)
        finally:
            if cursor:
                cursor.close()

    def edit_profile(self):
        doctorEditProfile.EditDoctorProfilePage(self.doctor_id, self.mydb)

    def go_back(self):
        self.app.destroy()
        doctor_main_page = doctorMain.DoctorMainPage(self.doctor_id)
        doctor_main_page.run()

    def run(self):
        self.app.mainloop()


