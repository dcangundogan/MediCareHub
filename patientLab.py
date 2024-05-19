import customtkinter as ctk
from PIL import Image
import mysql.connector
import random

class LabPage:
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
        self.app.title("Lab Information")
        self.app.resizable(False, False)

        # Load images and convert them to CTkImage for customtkinter compatibility
        imgLogo = Image.open("images/logo.png").resize((100, 100))
        imgLogoicon = ctk.CTkImage(dark_image=imgLogo, light_image=imgLogo, size=(250, 250))
        userLogo = Image.open("images/user.png").resize((60, 60))
        imgUsericon = ctk.CTkImage(dark_image=userLogo, light_image=userLogo, size=(60, 60))

        # Logo at the top left
        logoLabel = ctk.CTkLabel(master=self.app, text="", image=imgLogoicon)
        logoLabel.image = imgLogoicon  # Keep a reference!
        logoLabel.pack(side="left", fill="y")

        # Main Frame for content
        frame = ctk.CTkFrame(master=self.app, width=700, height=500, fg_color="#ffffff")
        frame.pack_propagate(0)
        frame.pack(side="right", fill="both", expand=True)

        # User icon
        userLabel = ctk.CTkLabel(master=frame, text="", image=imgUsericon, bg_color="#ffffff")
        userLabel.image = imgUsericon  # Keep a reference!
        userLabel.place(x=10, y=10)  # Adjust placement

        # Display lab information
        self.display_lab_info(frame)

        # Display random blood test results
        self.display_random_blood_test(frame)

        # Back button
        back_button = ctk.CTkButton(master=frame, text="Back", command=self.go_back_to_main_page)
        back_button.place(x=20, y=450)  # Adjust placement

        self.app.mainloop()

    def display_lab_info(self, frame):
        # Fetch and display lab information
        try:
            cursor = self.mydb.cursor(dictionary=True)
            query = """
            SELECT 
                lab.Lab_ID, 
                patient.Patient_Fname, 
                patient.Patient_Lname, 
                doctor.DoctorName, 
                doctor.DoctorSurname, 
                lab.Test_Cost, 
                lab.Date
            FROM lab
            JOIN patient ON lab.Patient_ID = patient.Patient_ID
            JOIN doctor ON lab.Doctor_ID = doctor.Doctor_ID
            WHERE lab.Patient_ID = %s
            """
            cursor.execute(query, (self.patient_id,))
            results = cursor.fetchall()

            if results:
                labels = ['Lab ID:', 'Patient Name:', 'Doctor Name:', 'Test Cost:', 'Date:']
                y_offset = 100

                for result in results:
                    for label in labels:
                        if label == 'Patient Name:':
                            value = f"{result['Patient_Fname']} {result['Patient_Lname']}"
                        elif label == 'Doctor Name:':
                            value = f"{result['DoctorName']} {result['DoctorSurname']}"
                        else:
                            value = result.get(label[:-1].replace(" ", "_"))
                        info_label = ctk.CTkLabel(master=frame, text=f"{label} {value}", font=("Arial", 12), text_color="#000000")
                        info_label.place(x=20, y=y_offset)  # Adjust placement
                        y_offset += 30
                    y_offset += 30  # Additional space between lab records

        except mysql.connector.Error as error:
            print("Failed to read data from MySQL table:", error)
        finally:
            if cursor:
                cursor.close()

    def display_random_blood_test(self, frame):
        # Generate and display random blood test results
        blood_test_results = {
            'Hemoglobin': (random.uniform(12.0, 18.0), "g/dL", 13.5, 17.5),
            'WBC': (random.randint(4000, 11000), "cells/mcL", 4500, 11000),
            'Platelets': (random.randint(150000, 450000), "cells/mcL", 150000, 450000),
            'RBC': (random.uniform(4.5, 5.9), "million cells/mcL", 4.7, 6.1),
            'Hematocrit': (random.uniform(37.0, 52.0), "%", 38.3, 48.6),
            'MCV': (random.uniform(80.0, 100.0), "fL", 80, 100)
        }

        y_offset = 250
        blood_test_label = ctk.CTkLabel(master=frame, text="Blood Test Results", font=("Arial", 14, "bold"), text_color="#000000")
        blood_test_label.place(x=20, y=y_offset)

        y_offset += 30
        for test, (result, unit, lower, upper) in blood_test_results.items():
            text_color = "#000000"
            font = ("Arial", 12)
            note = ""

            if result < lower or result > upper:
                text_color = "#FF0000"
                font = ("Arial", 12, "bold")
                note = " (Abnormal)"

            result_label = ctk.CTkLabel(master=frame, text=f"{test}: {result:.1f} {unit}{note}", font=font, text_color=text_color)
            result_label.place(x=20, y=y_offset)
            y_offset += 30

    def go_back_to_main_page(self):
        self.app.destroy()
        from patientMain import PatientMainPage  # Ensure this import is correct
        patient_main_page = PatientMainPage(self.patient_id)
        patient_main_page.run()

    def run(self):
        self.app.mainloop()

