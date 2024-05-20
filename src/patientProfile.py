import customtkinter as ctk
from PIL import Image
import mysql.connector
from patientEditProfile import EditProfilePage
import patientMain  # Ensure this import is correct

class ProfileMainPage:
    def __init__(self, patient_id):
        self.patient_id = patient_id
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="bercan2003",
            database="MediCareHub"
        )

        self.app = ctk.CTk()
        self.app.geometry("800x600")
        self.app.title("Profile")
        self.app.resizable(False, False)

        # Load images and convert them to CTkImage for customtkinter compatibility
        imgLogo = Image.open("images/logo.png").resize((300, 300))
        imgLogoicon = ctk.CTkImage(dark_image=imgLogo, light_image=imgLogo, size=(300, 300))
        userLogo = Image.open("images/user.png").resize((120, 120))
        imgUsericon = ctk.CTkImage(dark_image=userLogo, light_image=userLogo, size=(120, 120))

        # Logo at the top left
        logoLabel = ctk.CTkLabel(master=self.app, text="", image=imgLogoicon)
        logoLabel.image = imgLogoicon  # Keep a reference!
        logoLabel.pack(side="left", fill="y")

        # Main Frame for content
        frame = ctk.CTkFrame(master=self.app, width=500, height=600, fg_color="#ffffff")
        frame.pack_propagate(0)
        frame.pack(side="right", fill="both", expand=True)

        # User icon
        userLabel = ctk.CTkLabel(master=frame, text="", image=imgUsericon, bg_color="#ffffff")
        userLabel.image = imgUsericon  # Keep a reference!
        userLabel.place(x=180, y=10)  # Adjust placement

        # Display patient information
        self.display_patient_info(frame)

        # Edit Profile Button
        edit_button = ctk.CTkButton(master=frame, text="Edit Profile", command=self.edit_profile)
        edit_button.place(x=200, y=500)  # Adjust placement

        # Back Button
        back_button = ctk.CTkButton(master=frame, text="Back", command=self.go_back_to_main_page)
        back_button.place(x=40, y=500)  # Adjust placement

        self.app.mainloop()

    def display_patient_info(self, frame):
        # Fetch and display extended patient information
        try:
            cursor = self.mydb.cursor()
            query = "SELECT Patient_Fname, Patient_Lname, Phone, Email, Gender, Address, Admisson_Date FROM Patient WHERE Patient_ID = %s"
            cursor.execute(query, (self.patient_id,))
            result = cursor.fetchone()

            if result:
                labels = ['First Name:', 'Last Name:', 'Phone:', 'Email:', 'Gender:', 'Address:', 'Admission Date:']
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
        EditProfilePage(self.patient_id)

    def go_back_to_main_page(self):
        self.app.destroy()
        patient_main_page = patientMain.PatientMainPage(self.patient_id)
        patient_main_page.run()

    def run(self):
        self.app.mainloop()

