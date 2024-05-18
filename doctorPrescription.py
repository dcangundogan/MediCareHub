import customtkinter as ctk
from customtkinter import *
from tkinter import *
from tkinter import ttk
import mysql.connector
from CTkMessagebox import CTkMessagebox
from PIL import Image
from tkcalendar import DateEntry
from datetime import datetime
import doctorMain  # Make sure this import is correct

class DoctorPrescriptionsPage:
    def __init__(self, doctor_id):
        self.doctor_id = doctor_id
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="bercan2003",
            database="MediCareHub",
        )

        self.app = CTk()
        self.app.geometry("900x600")
        self.app.title("Write Prescription")
        self.app.resizable(False, False)

        self.initialize_ui()

    def initialize_ui(self):
        main_frame = CTkFrame(master=self.app)
        main_frame.pack(fill=BOTH, expand=True)

        # Left Frame for Logo
        left_frame = CTkFrame(master=main_frame, width=200, height=600, fg_color="#2C3E50")
        left_frame.pack_propagate(0)
        left_frame.pack(side=LEFT, fill=Y)

        imgLogo = Image.open("images/logo.png")
        imgLogoicon = CTkImage(dark_image=imgLogo, light_image=imgLogo, size=(150, 150))
        logoLabel = CTkLabel(master=left_frame, text="", image=imgLogoicon)
        logoLabel.pack(pady=20)

        # Right Frame for Prescriptions
        right_frame = CTkFrame(master=main_frame, width=700, height=600, fg_color="#ECF0F1")
        right_frame.pack_propagate(0)
        right_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=20, pady=20)

        label = CTkLabel(master=right_frame, text="Write Prescription", font=("Arial Bold", 20), text_color="#000000")
        label.pack(pady=10)

        # Patient ID Entry
        patient_id_label = CTkLabel(master=right_frame, text="Patient ID:", font=("Arial", 16),text_color="#000000")
        patient_id_label.pack(pady=5)
        self.patient_id_entry = CTkEntry(master=right_frame,fg_color="#EEEEEE",border_color="#261E76",border_width=2
                         ,text_color="#000000")
        self.patient_id_entry.pack(pady=5)

        # Medicine Combo Box
        medicine_label = CTkLabel(master=right_frame, text="Select Medicine:", font=("Arial", 16),text_color="#000000")
        medicine_label.pack(pady=5)
        self.medicine_combo = ttk.Combobox(master=right_frame)
        self.medicine_combo.pack(pady=5)

        # Dosage Entry
        dosage_label = CTkLabel(master=right_frame, text="Dosage:", font=("Arial", 16),text_color="#000000")
        dosage_label.pack(pady=5)
        self.dosage_entry = CTkEntry(master=right_frame,fg_color="#EEEEEE",border_color="#261E76",border_width=2
                         ,text_color="#000000")
        self.dosage_entry.pack(pady=5)

        # Date Entry
        date_label = CTkLabel(master=right_frame, text="Date:", font=("Arial", 16),text_color="#000000")
        date_label.pack(pady=5)
        self.date_entry = DateEntry(master=right_frame, date_pattern='yyyy-mm-dd')
        self.date_entry.pack(pady=5)

        # Submit Button
        submit_button = CTkButton(master=right_frame, text="Submit", command=self.submit_prescription)
        submit_button.pack(pady=20)

        # Back Button
        back_button = CTkButton(master=right_frame, text="Back", command=self.go_back_to_main_page)
        back_button.pack(pady=10)

        # Fetch and display medicines
        self.fetch_medicines()

    def fetch_medicines(self):
        try:
            cursor = self.mydb.cursor()
            cursor.execute("SELECT M_Name FROM Medicine")
            medicines = cursor.fetchall()
            self.medicine_combo['values'] = [medicine[0] for medicine in medicines]
            cursor.close()
        except mysql.connector.Error as e:
            CTkMessagebox(title="Database Error", message=f"An error occurred: {e}", icon="cancel")

    def submit_prescription(self):
        patient_id = self.patient_id_entry.get()
        medicine_name = self.medicine_combo.get()
        dosage = self.dosage_entry.get()
        date = self.date_entry.get()

        if not patient_id or not medicine_name or not dosage or not date:
            CTkMessagebox(title="Input Error", message="All fields are required.", icon="cancel")
            return

        try:
            cursor = self.mydb.cursor()
            cursor.execute("SELECT Medicine_ID FROM Medicine WHERE M_Name = %s", (medicine_name,))
            medicine_id = cursor.fetchone()[0]

            prescription_query = """
                INSERT INTO Prescription (Patient_ID, Medicine_ID, Date, Dosage, Doctor_ID)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(prescription_query, (patient_id, medicine_id, date, dosage, self.doctor_id))
            self.mydb.commit()
            cursor.close()

            CTkMessagebox(title="Success", message="Prescription submitted successfully.", icon="check")
        except mysql.connector.Error as e:
            CTkMessagebox(title="Database Error", message=f"An error occurred: {e}", icon="cancel")
        except Exception as e:
            CTkMessagebox(title="Error", message=f"An error occurred: {e}", icon="cancel")

    def go_back_to_main_page(self):
        self.app.destroy()
        doctor_main_page = doctorMain.DoctorMainPage(self.doctor_id)
        doctor_main_page.run()

    def run(self):
        self.app.mainloop()