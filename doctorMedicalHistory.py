import customtkinter as ctk
from customtkinter import *
from tkinter import *
from tkinter import ttk
import mysql.connector
from CTkMessagebox import CTkMessagebox
from PIL import Image

class DoctorMedicalHistoryPage:
    def __init__(self, doctor_id):
        self.doctor_id = doctor_id
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="bercan2003",
            database="MediCareHub",
        )

        self.app = CTk()
        self.app.geometry("1200x860")
        self.app.title("Medical History")
        self.app.resizable(False, False)

        self.initialize_ui()

    def initialize_ui(self):
        main_frame = CTkFrame(master=self.app, fg_color="#2E4053")
        main_frame.pack(fill=BOTH, expand=True)

        # Left Frame for Logo
        left_frame = CTkFrame(master=main_frame, width=250, height=800, fg_color="#1C2833")
        left_frame.pack_propagate(0)
        left_frame.pack(side=LEFT, fill=Y)

        imgLogo = Image.open("images/logo.png")
        imgLogoicon = CTkImage(dark_image=imgLogo, light_image=imgLogo, size=(200, 200))
        logoLabel = CTkLabel(master=left_frame, text="", image=imgLogoicon)
        logoLabel.pack(pady=20)

        # Right Frame for Medical History
        right_frame = CTkFrame(master=main_frame, fg_color="#F2F3F4")
        right_frame.pack_propagate(0)
        right_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=20, pady=20)

        label = CTkLabel(master=right_frame, text="Medical History", font=("Arial Bold", 24), text_color="#1C2833")
        label.pack(pady=10)

        # Appointment Combo Box
        appointment_label = CTkLabel(master=right_frame, text="Select Appointment:", font=("Arial", 16), text_color="#1C2833")
        appointment_label.pack(pady=5)
        self.appointment_combo = ttk.Combobox(master=right_frame)
        self.appointment_combo.pack(pady=5)
        self.appointment_combo.bind("<<ComboboxSelected>>", self.load_patient_info)

        # Patient Information
        self.patient_info = {}
        patient_labels = ['Patient ID:', 'First Name:', 'Last Name:', 'Phone:', 'Email:', 'Gender:', 'Blood Type:', 'Condition:', 'Admission Date:', 'Discharge Date:', 'Address:']
        for label in patient_labels:
            label_frame = CTkFrame(master=right_frame, fg_color="#F2F3F4")
            label_frame.pack(fill='x', padx=20, pady=2)
            lbl = CTkLabel(master=label_frame, text=label, font=("Arial", 12), text_color="#1C2833")
            lbl.pack(side='left')
            info = CTkLabel(master=label_frame, text="", font=("Arial", 12), text_color="#1C2833")
            info.pack(side='right')
            self.patient_info[label] = info

        # Medical History Entry
        medical_history_label = CTkLabel(master=right_frame, text="Medical History:", font=("Arial", 16), text_color="#1C2833")
        medical_history_label.pack(pady=10)
        self.medical_history_text = Text(master=right_frame, height=10, width=80, font=("Arial", 12))
        self.medical_history_text.pack(pady=5)

        # Submit Button
        submit_button = CTkButton(master=right_frame, text="Submit", command=self.submit_medical_history, fg_color="#1C2833", text_color="#F2F3F4", hover_color="#1A5276")
        submit_button.pack(pady=20)

        # Fetch and display appointments
        self.fetch_appointments()

    def fetch_appointments(self):
        try:
            cursor = self.mydb.cursor()
            query = """
                SELECT a.Appointment_ID, CONCAT(p.Patient_Fname, ' ', p.Patient_Lname, ' - ', a.Date) as Appointment_Info
                FROM appointment a
                JOIN patient p ON a.Patient_ID = p.Patient_ID
                WHERE a.Doctor_ID = %s
            """
            cursor.execute(query, (self.doctor_id,))
            appointments = cursor.fetchall()
            self.appointment_combo['values'] = [appointment[1] for appointment in appointments]
            self.appointment_data = {appointment[1]: appointment[0] for appointment in appointments}
            cursor.close()
        except mysql.connector.Error as e:
            CTkMessagebox(title="Database Error", message=f"An error occurred: {e}", icon="cancel")

    def load_patient_info(self, event):
        appointment_info = self.appointment_combo.get()
        appointment_id = self.appointment_data.get(appointment_info)

        if not appointment_id:
            return

        try:
            cursor = self.mydb.cursor(dictionary=True)
            query = """
                SELECT p.Patient_ID, p.Patient_Fname, p.Patient_Lname, p.Phone, p.Email, p.Gender, p.Blood_Type, p.Condition_, p.Admisson_Date, p.Discharge_Date, p.Address, mh.Pre_Conditions
                FROM patient p
                LEFT JOIN medical_history mh ON p.Patient_ID = mh.Patient_ID
                JOIN appointment a ON p.Patient_ID = a.Patient_ID
                WHERE a.Appointment_ID = %s
            """
            cursor.execute(query, (appointment_id,))
            patient = cursor.fetchone()
            cursor.close()

            if patient:
                self.patient_info['Patient ID:'].configure(text=patient['Patient_ID'])
                self.patient_info['First Name:'].configure(text=patient['Patient_Fname'])
                self.patient_info['Last Name:'].configure(text=patient['Patient_Lname'])
                self.patient_info['Phone:'].configure(text=patient['Phone'])
                self.patient_info['Email:'].configure(text=patient['Email'])
                self.patient_info['Gender:'].configure(text=patient['Gender'])
                self.patient_info['Blood Type:'].configure(text=patient['Blood_Type'])
                self.patient_info['Condition:'].configure(text=patient['Condition_'])
                self.patient_info['Admission Date:'].configure(text=patient['Admisson_Date'])
                self.patient_info['Discharge Date:'].configure(text=patient['Discharge_Date'])
                self.patient_info['Address:'].configure(text=patient['Address'])
                self.medical_history_text.delete('1.0', END)
                if patient['Pre_Conditions']:
                    self.medical_history_text.insert(END, patient['Pre_Conditions'])
        except mysql.connector.Error as e:
            CTkMessagebox(title="Database Error", message=f"An error occurred: {e}", icon="cancel")

    def submit_medical_history(self):
        appointment_info = self.appointment_combo.get()
        appointment_id = self.appointment_data.get(appointment_info)
        patient_id = self.patient_info['Patient ID:'].cget("text")
        medical_history = self.medical_history_text.get("1.0", END).strip()

        if not appointment_id or not patient_id or not medical_history:
            CTkMessagebox(title="Input Error", message="All fields are required.", icon="cancel")
            return

        try:
            cursor = self.mydb.cursor()

            query = "SELECT COUNT(*) FROM medical_history WHERE Patient_ID = %s"
            cursor.execute(query, (patient_id,))
            exists = cursor.fetchone()[0]

            if exists:
                query = "UPDATE medical_history SET Pre_Conditions = %s WHERE Patient_ID = %s"
                cursor.execute(query, (medical_history, patient_id))
            else:
                query = "INSERT INTO medical_history (Patient_ID, Pre_Conditions) VALUES (%s, %s)"
                cursor.execute(query, (patient_id, medical_history))

            self.mydb.commit()
            cursor.close()

            CTkMessagebox(title="Success", message="Medical history submitted successfully.", icon="check")
        except mysql.connector.Error as e:
            CTkMessagebox(title="Database Error", message=f"An error occurred: {e}", icon="cancel")
        except Exception as e:
            CTkMessagebox(title="Error", message=f"An error occurred: {e}", icon="cancel")

    def run(self):
        self.app.mainloop()



