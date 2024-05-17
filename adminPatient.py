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
        self.app.title("Admin - Patient Management Page")
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

        # Main Content Frame
        self.right_frame = ctk.CTkFrame(master=main_frame, fg_color="#F2F3F4")
        self.right_frame.pack_propagate(0)
        self.right_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=20, pady=20)

        self.view_patients()

    def clear_right_frame(self):
        for widget in self.right_frame.winfo_children():
            widget.destroy()

    def view_patients(self):
        self.clear_right_frame()
        label = ctk.CTkLabel(master=self.right_frame, text="Patients", font=("Arial Bold", 24), text_color="#1C2833")
        label.pack(pady=10)

        columns = ("Patient_ID", "First Name", "Last Name", "Phone", "Blood Type", "Email", "Gender", "Condition", "Admission Date", "Discharge Date", "Address")
        self.tree = ttk.Treeview(self.right_frame, columns=columns, show='headings', style="mystyle.Treeview")

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, minwidth=0, width=150)

        self.tree.pack(expand=True, fill=BOTH, padx=10, pady=10)
        self.fetch_patients()

        self.create_patient_buttons()

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

    def create_patient_buttons(self):
        button_frame = ctk.CTkFrame(self.right_frame, fg_color="#F2F3F4")
        button_frame.pack(fill=X, padx=10, pady=10)

        add_button = ctk.CTkButton(master=button_frame, text="Add Patient", command=self.add_patient_form, fg_color="#4CAF50", hover_color="#388E3C", font=("Arial Bold", 14))
        add_button.pack(side=LEFT, padx=10)

        edit_button = ctk.CTkButton(master=button_frame, text="Edit Patient", command=self.edit_patient_form, fg_color="#FFC107", hover_color="#FFA000", font=("Arial Bold", 14))
        edit_button.pack(side=LEFT, padx=10)

        delete_button = ctk.CTkButton(master=button_frame, text="Delete Patient", command=self.delete_patient, fg_color="#F44336", hover_color="#D32F2F", font=("Arial Bold", 14))
        delete_button.pack(side=LEFT, padx=10)

    def add_patient_form(self):
        self.clear_right_frame()

        form_frame = ctk.CTkFrame(master=self.right_frame, fg_color="#F2F3F4")
        form_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)

        label = ctk.CTkLabel(master=form_frame, text="Add Patient", font=("Arial Bold", 24), text_color="#1C2833")
        label.pack(pady=10)

        form_labels = ["First Name", "Last Name", "Phone", "Blood Type", "Email", "Gender", "Condition", "Admission Date", "Discharge Date", "Address"]
        self.form_entries = {}

        for label_text in form_labels:
            row_frame = ctk.CTkFrame(master=form_frame, fg_color="#F2F3F4")
            row_frame.pack(fill=X, pady=5)

            label = ctk.CTkLabel(master=row_frame, text=label_text, font=("Arial", 14), text_color="#1C2833")
            label.pack(side=LEFT, padx=5)

            entry = ctk.CTkEntry(master=row_frame, width=300)
            entry.pack(side=LEFT, padx=5)
            self.form_entries[label_text] = entry

        submit_button = ctk.CTkButton(master=form_frame, text="Submit", command=self.submit_new_patient, fg_color="#4CAF50", hover_color="#388E3C", font=("Arial Bold", 14))
        submit_button.pack(pady=10)

        back_button = ctk.CTkButton(master=form_frame, text="Back", command=self.view_patients, fg_color="#607D8B", hover_color="#455A64", font=("Arial Bold", 14))
        back_button.pack(pady=10)

    def submit_new_patient(self):
        fname = self.form_entries["First Name"].get()
        lname = self.form_entries["Last Name"].get()
        phone = self.form_entries["Phone"].get()
        blood_type = self.form_entries["Blood Type"].get()
        email = self.form_entries["Email"].get()
        gender = self.form_entries["Gender"].get()
        condition = self.form_entries["Condition"].get()
        admission_date = self.form_entries["Admission Date"].get()
        discharge_date = self.form_entries["Discharge Date"].get()
        address = self.form_entries["Address"].get()

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
            self.view_patients()
        except mysql.connector.Error as e:
            CTkMessagebox(title="Database Error", message=f"An error occurred: {e}", icon="cancel")

    def edit_patient_form(self):
        selected_item = self.tree.selection()
        if not selected_item:
            CTkMessagebox(title="Selection Error", message="Please select a patient to edit.", icon="cancel")
            return

        patient_values = self.tree.item(selected_item, 'values')
        self.clear_right_frame()

        form_frame = ctk.CTkFrame(master=self.right_frame, fg_color="#F2F3F4")
        form_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)

        label = ctk.CTkLabel(master=form_frame, text="Edit Patient", font=("Arial Bold", 24), text_color="#1C2833")
        label.pack(pady=10)

        form_labels = ["First Name", "Last Name", "Phone", "Blood Type", "Email", "Gender", "Condition", "Admission Date", "Discharge Date", "Address"]
        self.form_entries = {}

        for i, label_text in enumerate(form_labels):
            row_frame = ctk.CTkFrame(master=form_frame, fg_color="#F2F3F4")
            row_frame.pack(fill=X, pady=5)

            label = ctk.CTkLabel(master=row_frame, text=label_text, font=("Arial", 14), text_color="#1C2833")
            label.pack(side=LEFT, padx=5)

            entry = ctk.CTkEntry(master=row_frame, width=300)
            entry.insert(0, patient_values[i+1])
            entry.pack(side=LEFT, padx=5)
            self.form_entries[label_text] = entry

        submit_button = ctk.CTkButton(master=form_frame, text="Submit", command=lambda: self.submit_edit_patient(patient_values[0]), fg_color="#FFC107", hover_color="#FFA000", font=("Arial Bold", 14))
        submit_button.pack(pady=10)

        back_button = ctk.CTkButton(master=form_frame, text="Back", command=self.view_patients, fg_color="#607D8B", hover_color="#455A64", font=("Arial Bold", 14))
        back_button.pack(pady=10)

    def submit_edit_patient(self, patient_id):
        fname = self.form_entries["First Name"].get()
        lname = self.form_entries["Last Name"].get()
        phone = self.form_entries["Phone"].get()
        blood_type = self.form_entries["Blood Type"].get()
        email = self.form_entries["Email"].get()
        gender = self.form_entries["Gender"].get()
        condition = self.form_entries["Condition"].get()
        admission_date = self.form_entries["Admission Date"].get()
        discharge_date = self.form_entries["Discharge Date"].get()
        address = self.form_entries["Address"].get()

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
            self.view_patients()
        except mysql.connector.Error as e:
            CTkMessagebox(title="Database Error", message=f"An error occurred: {e}", icon="cancel")

    def delete_patient(self):
        selected_item = self.tree.selection()
        if not selected_item:
            CTkMessagebox(title="Selection Error", message="Please select a patient to delete.", icon="cancel")
            return

        patient_id = self.tree.item(selected_item, 'values')[0]
        cursor = self.mydb.cursor()

        query_patient = "DELETE  FROM patient, loginpagepatient FROM patient JOIN loginpagepatient ON loginpagepatient.Patient_ID = patient.Patient_ID WHERE patient.Patient_ID = %s"

        try:
            cursor.execute(query_patient, (patient_id,))

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

    def run(self):
        self.app.mainloop()


