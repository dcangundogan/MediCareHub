import customtkinter as ctk
from tkinter import ttk, BOTH, LEFT, X, Y
import mysql.connector
from CTkMessagebox import CTkMessagebox
from PIL import Image


class AdminPatientPage:
    def __init__(self):
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="bercan2003",
            database="MediCareHub",
        )

        self.app = ctk.CTk()
        self.app.geometry("1400x900")
        self.app.title("Admin - Patient Management")
        self.app.resizable(False, False)

        self.initialize_ui()

    def initialize_ui(self):
        main_frame = ctk.CTkFrame(master=self.app, fg_color="#2E4053")
        main_frame.pack(fill=BOTH, expand=True)

        # Left Frame for Logo and Navigation
        left_frame = ctk.CTkFrame(master=main_frame, width=250, height=900, fg_color="#1C2833")
        left_frame.pack_propagate(0)
        left_frame.pack(side=LEFT, fill=Y)

        imgLogo = Image.open("images/logo.png")
        imgLogoicon = ctk.CTkImage(dark_image=imgLogo, light_image=imgLogo, size=(200, 200))
        logoLabel = ctk.CTkLabel(master=left_frame, text="", image=imgLogoicon)
        logoLabel.pack(pady=20)

        # Navigation Buttons
        nav_buttons = [
            ("View Patients", self.view_patients),
            ("Edit Patient", self.open_edit_patient_form),
            ("Add New Patient", self.open_new_patient_form),
            ("Delete Patient", self.delete_patient),
        ]

        for text, command in nav_buttons:
            button = ctk.CTkButton(master=left_frame, text=text, command=command, fg_color="#EEEEEE", hover_color="#08e590", font=("Arial Bold", 18), text_color="#601E88", width=200, height=50)
            button.pack(pady=10)

        # Main Content Frame
        self.right_frame = ctk.CTkFrame(master=main_frame, fg_color="#F2F3F4")
        self.right_frame.pack_propagate(0)
        self.right_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=20, pady=20)

        self.view_patients()

    def view_patients(self):
        self.clear_right_frame()
        label = ctk.CTkLabel(master=self.right_frame, text="Patients", font=("Arial Bold", 24), text_color="#1C2833")
        label.pack(pady=10)

        columns = ("Patient ID", "First Name", "Last Name", "Phone", "Blood Type", "Email", "Gender", "Condition", "Admission Date", "Discharge Date", "Address")
        self.tree = ttk.Treeview(self.right_frame, columns=columns, show='headings', style="mystyle.Treeview")

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, minwidth=0, width=150)

        self.tree.pack(expand=True, fill=BOTH, padx=10, pady=10)
        self.fetch_patients()

    def fetch_patients(self):
        try:
            cursor = self.mydb.cursor()
            query = """
                SELECT 
                    Patient_ID, 
                    Patient_Fname, 
                    Patient_Lname, 
                    Phone, 
                    Blood_Type, 
                    Email, 
                    Gender, 
                    Condition_, 
                    Admisson_Date, 
                    Discharge_Date, 
                    Address 
                FROM 
                    patient
            """
            cursor.execute(query)
            rows = cursor.fetchall()

            for row in rows:
                self.tree.insert('', 'end', values=row)

            cursor.close()
        except mysql.connector.Error as e:
            CTkMessagebox(title="Database Error", message=f"An error occurred: {e}", icon="cancel")

    def open_edit_patient_form(self):
        selected_item = self.tree.selection()
        if not selected_item:
            CTkMessagebox(title="Selection Error", message="Please select a patient to edit.", icon="cancel")
            return

        patient_id = self.tree.item(selected_item, 'values')[0]

        form_window = ctk.CTkToplevel(self.app)
        form_window.geometry("900x900")
        form_window.title("Edit Patient Form")

        label = ctk.CTkLabel(form_window, text="Edit Patient", font=("Arial Bold", 20), text_color="#1C2833")
        label.pack(pady=10)

        # Fetching existing patient details
        cursor = self.mydb.cursor(dictionary=True)
        cursor.execute("SELECT * FROM patient WHERE Patient_ID = %s", (patient_id,))
        patient = cursor.fetchone()
        cursor.close()

        # First Name
        fname_label = ctk.CTkLabel(form_window, text="First Name:", font=("Arial Bold", 16), text_color="#1C2833")
        fname_label.pack(pady=10)
        self.fname_entry = ctk.CTkEntry(form_window, width=300)
        self.fname_entry.insert(0, patient['Patient_Fname'])
        self.fname_entry.pack(pady=5)

        # Last Name
        lname_label = ctk.CTkLabel(form_window, text="Last Name:", font=("Arial Bold", 16), text_color="#1C2833")
        lname_label.pack(pady=10)
        self.lname_entry = ctk.CTkEntry(form_window, width=300)
        self.lname_entry.insert(0, patient['Patient_Lname'])
        self.lname_entry.pack(pady=5)

        # Phone
        phone_label = ctk.CTkLabel(form_window, text="Phone:", font=("Arial Bold", 16), text_color="#1C2833")
        phone_label.pack(pady=10)
        self.phone_entry = ctk.CTkEntry(form_window, width=300)
        self.phone_entry.insert(0, patient['Phone'])
        self.phone_entry.pack(pady=5)

        # Blood Type
        blood_type_label = ctk.CTkLabel(form_window, text="Blood Type:", font=("Arial Bold", 16), text_color="#1C2833")
        blood_type_label.pack(pady=10)
        self.blood_type_entry = ctk.CTkEntry(form_window, width=300)
        self.blood_type_entry.insert(0, patient['Blood_Type'])
        self.blood_type_entry.pack(pady=5)

        # Email
        email_label = ctk.CTkLabel(form_window, text="Email:", font=("Arial Bold", 16), text_color="#1C2833")
        email_label.pack(pady=10)
        self.email_entry = ctk.CTkEntry(form_window, width=300)
        self.email_entry.insert(0, patient['Email'])
        self.email_entry.pack(pady=5)

        # Gender
        gender_label = ctk.CTkLabel(form_window, text="Gender:", font=("Arial Bold", 16), text_color="#1C2833")
        gender_label.pack(pady=10)
        self.gender_entry = ctk.CTkEntry(form_window, width=300)
        self.gender_entry.insert(0, patient['Gender'])
        self.gender_entry.pack(pady=5)

        # Condition
        condition_label = ctk.CTkLabel(form_window, text="Condition:", font=("Arial Bold", 16), text_color="#1C2833")
        condition_label.pack(pady=10)
        self.condition_entry = ctk.CTkEntry(form_window, width=300)
        self.condition_entry.insert(0, patient['Condition_'])
        self.condition_entry.pack(pady=5)

        # Admission Date
        admission_date_label = ctk.CTkLabel(form_window, text="Admission Date:", font=("Arial Bold", 16), text_color="#1C2833")
        admission_date_label.pack(pady=10)
        self.admission_date_entry = ctk.CTkEntry(form_window, width=300)
        self.admission_date_entry.insert(0, patient['Admisson_Date'])
        self.admission_date_entry.pack(pady=5)

        # Discharge Date
        discharge_date_label = ctk.CTkLabel(form_window, text="Discharge Date:", font=("Arial Bold", 16), text_color="#1C2833")
        discharge_date_label.pack(pady=10)
        self.discharge_date_entry = ctk.CTkEntry(form_window, width=300)
        self.discharge_date_entry.insert(0, patient['Discharge_Date'])
        self.discharge_date_entry.pack(pady=5)

        # Address
        address_label = ctk.CTkLabel(form_window, text="Address:", font=("Arial Bold", 16), text_color="#1C2833")
        address_label.pack(pady=10)
        self.address_entry = ctk.CTkEntry(form_window, width=300)
        self.address_entry.insert(0, patient['Address'])
        self.address_entry.pack(pady=5)

        # Save Button
        save_button = ctk.CTkButton(form_window, text="Save Changes", command=lambda: self.save_patient_changes(patient_id, form_window), fg_color="#1C2833", text_color="#F2F3F4", hover_color="#1A5276")
        save_button.pack(pady=20)

    def open_new_patient_form(self):
        form_window = ctk.CTkToplevel(self.app)
        form_window.geometry("900x900")
        form_window.title("New Patient Form")

        label = ctk.CTkLabel(form_window, text="New Patient", font=("Arial Bold", 20), text_color="#1C2833")
        label.pack(pady=10)

        # First Name
        fname_label = ctk.CTkLabel(form_window, text="First Name:", font=("Arial Bold", 16), text_color="#1C2833")
        fname_label.pack(pady=10)
        self.fname_entry = ctk.CTkEntry(form_window, width=300)
        self.fname_entry.pack(pady=5)

        # Last Name
        lname_label = ctk.CTkLabel(form_window, text="Last Name:", font=("Arial Bold", 16), text_color="#1C2833")
        lname_label.pack(pady=10)
        self.lname_entry = ctk.CTkEntry(form_window, width=300)
        self.lname_entry.pack(pady=5)

        # Phone
        phone_label = ctk.CTkLabel(form_window, text="Phone:", font=("Arial Bold", 16), text_color="#1C2833")
        phone_label.pack(pady=10)
        self.phone_entry = ctk.CTkEntry(form_window, width=300)
        self.phone_entry.pack(pady=5)

        # Blood Type
        blood_type_label = ctk.CTkLabel(form_window, text="Blood Type:", font=("Arial Bold", 16), text_color="#1C2833")
        blood_type_label.pack(pady=10)
        self.blood_type_entry = ctk.CTkEntry(form_window, width=300)
        self.blood_type_entry.pack(pady=5)

        # Email
        email_label = ctk.CTkLabel(form_window, text="Email:", font=("Arial Bold", 16), text_color="#1C2833")
        email_label.pack(pady=10)
        self.email_entry = ctk.CTkEntry(form_window, width=300)
        self.email_entry.pack(pady=5)

        # Gender
        gender_label = ctk.CTkLabel(form_window, text="Gender:", font=("Arial Bold", 16), text_color="#1C2833")
        gender_label.pack(pady=10)
        self.gender_entry = ctk.CTkEntry(form_window, width=300)
        self.gender_entry.pack(pady=5)

        # Condition
        condition_label = ctk.CTkLabel(form_window, text="Condition:", font=("Arial Bold", 16), text_color="#1C2833")
        condition_label.pack(pady=10)
        self.condition_entry = ctk.CTkEntry(form_window, width=300)
        self.condition_entry.pack(pady=5)

        # Admission Date
        admission_date_label = ctk.CTkLabel(form_window, text="Admission Date:", font=("Arial Bold", 16), text_color="#1C2833")
        admission_date_label.pack(pady=10)
        self.admission_date_entry = ctk.CTkEntry(form_window, width=300)
        self.admission_date_entry.pack(pady=5)

        # Discharge Date
        discharge_date_label = ctk.CTkLabel(form_window, text="Discharge Date:", font=("Arial Bold", 16), text_color="#1C2833")
        discharge_date_label.pack(pady=10)
        self.discharge_date_entry = ctk.CTkEntry(form_window, width=300)
        self.discharge_date_entry.pack(pady=5)

        # Address
        address_label = ctk.CTkLabel(form_window, text="Address:", font=("Arial Bold", 16), text_color="#1C2833")
        address_label.pack(pady=10)
        self.address_entry = ctk.CTkEntry(form_window, width=300)
        self.address_entry.pack(pady=5)

        # Save Button
        save_button = ctk.CTkButton(form_window, text="Add Patient", command=lambda: self.add_new_patient(form_window), fg_color="#1C2833", text_color="#F2F3F4", hover_color="#1A5276")
        save_button.pack(pady=20)

    def save_patient_changes(self, patient_id, form_window):
        fname = self.fname_entry.get()
        lname = self.lname_entry.get()
        phone = self.phone_entry.get()
        blood_type = self.blood_type_entry.get()
        email = self.email_entry.get()
        gender = self.gender_entry.get()
        condition = self.condition_entry.get()
        admission_date = self.admission_date_entry.get()
        discharge_date = self.discharge_date_entry.get()
        address = self.address_entry.get()

        query = """
            UPDATE patient 
            SET Patient_Fname = %s, Patient_Lname = %s, Phone = %s, Blood_Type = %s, Email = %s, Gender = %s, Condition_ = %s, Admisson_Date = %s, Discharge_Date = %s, Address = %s 
            WHERE Patient_ID = %s
        """
        try:
            cursor = self.mydb.cursor()
            cursor.execute(query, (fname, lname, phone, blood_type, email, gender, condition, admission_date, discharge_date, address, patient_id))
            self.mydb.commit()
            cursor.close()
            CTkMessagebox(title="Success", message="Patient updated successfully.", icon="check")
            form_window.destroy()
            self.view_patients()
        except mysql.connector.Error as e:
            CTkMessagebox(title="Database Error", message=f"An error occurred: {e}", icon="cancel")

    def add_new_patient(self, form_window):
        fname = self.fname_entry.get()
        lname = self.lname_entry.get()
        phone = self.phone_entry.get()
        blood_type = self.blood_type_entry.get()
        email = self.email_entry.get()
        gender = self.gender_entry.get()
        condition = self.condition_entry.get()
        admission_date = self.admission_date_entry.get()
        discharge_date = self.discharge_date_entry.get()
        address = self.address_entry.get()

        patient_id = self.generate_unique_patient_id()

        query = """
            INSERT INTO patient (Patient_ID, Patient_Fname, Patient_Lname, Phone, Blood_Type, Email, Gender, Condition_, Admisson_Date, Discharge_Date, Address)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        try:
            cursor = self.mydb.cursor()
            cursor.execute(query, (patient_id, fname, lname, phone, blood_type, email, gender, condition, admission_date, discharge_date, address))
            self.mydb.commit()
            cursor.close()
            CTkMessagebox(title="Success", message="New patient added successfully.", icon="check")
            form_window.destroy()
            self.view_patients()
        except mysql.connector.Error as e:
            CTkMessagebox(title="Database Error", message=f"An error occurred: {e}", icon="cancel")

    def delete_patient(self):
        selected_item = self.tree.selection()
        if not selected_item:
            CTkMessagebox(title="Selection Error", message="Please select a patient to delete.", icon="cancel")
            return

        patient_id = self.tree.item(selected_item, 'values')[0]

        query = "DELETE FROM patient WHERE Patient_ID = %s"
        try:
            cursor = self.mydb.cursor()
            cursor.execute(query, (patient_id,))
            self.mydb.commit()
            cursor.close()
            CTkMessagebox(title="Success", message="Patient deleted successfully.", icon="check")
            self.view_patients()
        except mysql.connector.Error as e:
            CTkMessagebox(title="Database Error", message=f"An error occurred: {e}", icon="cancel")

    def generate_unique_patient_id(self):
        import random
        while True:
            new_id = random.randint(1000, 9999)
            cursor = self.mydb.cursor()
            cursor.execute("SELECT COUNT(*) FROM patient WHERE Patient_ID = %s", (new_id,))
            if cursor.fetchone()[0] == 0:
                cursor.close()
                return new_id
            cursor.close()

    def clear_right_frame(self):
        for widget in self.right_frame.winfo_children():
            widget.destroy()

    def run(self):
        self.app.mainloop()


