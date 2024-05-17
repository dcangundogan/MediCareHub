import customtkinter as ctk
from PIL import Image
import mysql.connector
from doctorEditProfile import EditDoctorProfilePage

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
        self.app.geometry("800x600")
        self.app.title("Doctor Profile")
        self.app.resizable(False, False)

        # Load images and convert them to CTkImage for customtkinter compatibility
        imgLogo = Image.open("images/logo.png").resize((300, 300))
        imgLogoicon = ctk.CTkImage(dark_image=imgLogo, light_image=imgLogo, size=(300, 300))
        userLogo = Image.open("images/medical-team.png").resize((120, 120))
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

        # Display doctor information
        self.display_doctor_info(frame)

        # Edit Profile Button
        edit_button = ctk.CTkButton(master=frame, text="Edit Profile", command=self.edit_profile)
        edit_button.place(x=200, y=500)  # Adjust placement

        self.app.mainloop()

    def display_doctor_info(self, frame):
        # Fetch and display extended doctor information
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
        EditDoctorProfilePage(self.doctor_id, self.mydb)

    def run(self):
        self.app.mainloop()

# Usage example
if __name__ == "__main__":
    doctor_id = 1  # Replace with the actual doctor ID
    DoctorProfileMainPage(doctor_id).run()
