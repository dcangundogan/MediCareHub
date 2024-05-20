import customtkinter as ctk
from PIL import Image
import mysql.connector

class InsuranceInfoPage:
    def __init__(self, patient_id):
        self.patient_id = patient_id
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="bercan2003",
            database="MediCareHub",
        )

        self.app = ctk.CTk()
        self.app.geometry("800x600")
        self.app.title("Insurance Information")
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

        # Display insurance information
        self.display_insurance_info(frame)

        # Back button
        back_button = ctk.CTkButton(master=frame, text="Back", command=self.go_back_to_main_page)
        back_button.place(x=20, y=500)  # Adjust placement

        self.app.mainloop()

    def display_insurance_info(self, frame):
        # Fetch and display insurance information
        try:
            cursor = self.mydb.cursor(dictionary=True)
            query = """
            SELECT Policy_Number, Ins_Code, End_Date, Provider, Plan, Coop_Pay, Coverage, Dental, Optical 
            FROM Insurance 
            WHERE Patient_ID = %s
            """
            cursor.execute(query, (self.patient_id,))
            result = cursor.fetchone()

            if result:
                labels = ['Policy Number:', 'Insurance Code:', 'End Date:', 'Provider:', 'Plan:', 'Co-pay:', 'Coverage:', 'Dental:', 'Optical:']
                y_offset = 150
                for label in labels:
                    value = result.get(label[:-1].replace(" ", "_"))
                    if value is not None:  # Check if the value is not None
                        if label in ['Dental:', 'Optical:']:
                            value = 'Yes' if value else 'No'
                        info_label = ctk.CTkLabel(master=frame, text=f"{label} {value}", font=("Arial", 12), text_color="#000000")
                        info_label.place(x=20, y=y_offset)  # Adjust placement
                        y_offset += 30

        except mysql.connector.Error as error:
            print("Failed to read data from MySQL table:", error)
        finally:
            if cursor:
                cursor.close()

    def go_back_to_main_page(self):
        self.app.destroy()
        from patientMain import PatientMainPage  # Ensure this import is correct
        patient_main_page = PatientMainPage(self.patient_id)
        patient_main_page.run()

    def run(self):
        self.app.mainloop()


