import customtkinter as ctk
from customtkinter import *
from tkinter import *
from tkinter import ttk
from tkcalendar import Calendar
import mysql.connector
from CTkMessagebox import CTkMessagebox
from datetime import datetime, timedelta
from PIL import Image

class AdminAppointmentPage:
    def __init__(self):
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="bercan2003",
            database="MediCareHub",
        )

        self.app = CTk()
        self.app.geometry("1400x900")
        self.app.title("Admin - Appointment Management")
        self.app.resizable(False, False)

        self.initialize_ui()

    def initialize_ui(self):
        main_frame = CTkFrame(master=self.app, fg_color="#2E4053")
        main_frame.pack(fill=BOTH, expand=True)

        # Left Frame for Logo and Navigation
        left_frame = CTkFrame(master=main_frame, width=250, height=900, fg_color="#1C2833")
        left_frame.pack_propagate(0)
        left_frame.pack(side=LEFT, fill=Y)

        imgLogo = Image.open("images/logo.png")
        imgLogoicon = CTkImage(dark_image=imgLogo, light_image=imgLogo, size=(200, 200))
        logoLabel = CTkLabel(master=left_frame, text="", image=imgLogoicon)
        logoLabel.pack(pady=20)

        # Navigation Buttons
        nav_buttons = [
            ("View Appointments", self.view_appointments),
            ("Edit Appointment", self.open_edit_appointment_form),
            ("Add New Appointment", self.open_new_appointment_form),
        ]

        for text, command in nav_buttons:
            button = CTkButton(master=left_frame, text=text, command=command, fg_color="#EEEEEE", hover_color="#08e590", font=("Arial Bold", 18), text_color="#601E88", width=200, height=50)
            button.pack(pady=10)

        # Main Content Frame
        self.right_frame = CTkFrame(master=main_frame, fg_color="#F2F3F4")
        self.right_frame.pack_propagate(0)
        self.right_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=20, pady=20)

        self.view_appointments()

    def view_appointments(self):
        self.clear_right_frame()
        label = CTkLabel(master=self.right_frame, text="Appointments", font=("Arial Bold", 24), text_color="#1C2833")
        label.pack(pady=10)

        columns = ("Appointment ID", "Patient Name", "Doctor Name", "Date", "Time")
        self.tree = ttk.Treeview(self.right_frame, columns=columns, show='headings', style="mystyle.Treeview")

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, minwidth=0, width=200)

        self.tree.pack(expand=True, fill=BOTH, padx=10, pady=10)
        self.fetch_appointments()

    def fetch_appointments(self):
        try:
            cursor = self.mydb.cursor()
            query = """
                SELECT 
                    a.Appointment_ID, 
                    CONCAT(p.Patient_Fname, ' ', p.Patient_Lname) AS Patient_Name, 
                    CONCAT(d.DoctorName, ' ', d.DoctorSurname) AS Doctor_Name, 
                    a.Date, 
                    a.Time 
                FROM 
                    appointment a
                JOIN 
                    patient p ON a.Patient_ID = p.Patient_ID
                JOIN 
                    doctor d ON a.Doctor_ID = d.Doctor_ID
            """
            cursor.execute(query)
            rows = cursor.fetchall()

            for row in rows:
                self.tree.insert('', 'end', values=row)

            cursor.close()
        except mysql.connector.Error as e:
            CTkMessagebox(title="Database Error", message=f"An error occurred: {e}", icon="cancel")

    def open_edit_appointment_form(self):
        selected_item = self.tree.selection()
        if not selected_item:
            CTkMessagebox(title="Selection Error", message="Please select an appointment to edit.", icon="cancel")
            return

        appointment_id = self.tree.item(selected_item, 'values')[0]

        form_window = CTkToplevel(self.app)
        form_window.geometry("650x650")
        form_window.title("Edit Appointment Form")

        label = CTkLabel(form_window, text="Edit Appointment", font=("Arial Bold", 20), text_color="#1C2833")
        label.pack(pady=10)

        # Fetching existing appointment details
        cursor = self.mydb.cursor(dictionary=True)
        cursor.execute("SELECT * FROM appointment WHERE Appointment_ID = %s", (appointment_id,))
        appointment = cursor.fetchone()
        cursor.close()

        # Date Selection
        date_label = CTkLabel(form_window, text="Appointment Date:", font=("Arial Bold", 16), text_color="#1C2833")
        date_label.pack(pady=10)
        self.date_entry = Calendar(form_window, selectmode='day', font=("Arial Bold", 16), date_pattern='yyyy-mm-dd', text_color="#000000")
        self.date_entry.selection_set(appointment['Date'])
        self.date_entry.pack(pady=5)

        # Time Selection
        time_label = CTkLabel(form_window, text="Time (HH:MM):", font=("Arial Bold", 16), text_color="#1C2833")
        time_label.pack(pady=10)
        time_slots = self.generate_time_slots()
        self.time_combo = ttk.Combobox(form_window, values=time_slots, width=20, height=50)
        self.time_combo.set(appointment['Time'])
        self.time_combo.pack(pady=5)

        # Doctor Selection
        doctor_label = CTkLabel(form_window, text="Doctor:", font=("Arial Bold", 16), text_color="#1C2833")
        doctor_label.pack(pady=10)
        cursor = self.mydb.cursor()
        cursor.execute("SELECT CONCAT(DoctorName, ' ', DoctorSurname) FROM doctor")
        doctor_names = [row[0] for row in cursor.fetchall()]
        cursor.close()
        self.doctor_combo = ttk.Combobox(form_window, values=doctor_names)
        self.doctor_combo.set(f"{appointment['Doctor_ID']}")
        self.doctor_combo.pack(pady=5)

        # Patient Selection
        patient_label = CTkLabel(form_window, text="Patient:", font=("Arial Bold", 16), text_color="#1C2833")
        patient_label.pack(pady=10)
        cursor = self.mydb.cursor()
        cursor.execute("SELECT CONCAT(Patient_Fname, ' ', Patient_Lname) FROM patient")
        patient_names = [row[0] for row in cursor.fetchall()]
        cursor.close()
        self.patient_combo = ttk.Combobox(form_window, values=patient_names)
        self.patient_combo.set(f"{appointment['Patient_ID']}")
        self.patient_combo.pack(pady=5)

        # Save Button
        save_button = CTkButton(form_window, text="Save Changes", command=lambda: self.save_appointment_changes(appointment_id), fg_color="#1C2833", text_color="#F2F3F4", hover_color="#1A5276")
        save_button.pack(pady=20)

    def open_new_appointment_form(self):
        form_window = CTkToplevel(self.app)
        form_window.geometry("700x700")
        form_window.title("New Appointment Form")

        label = CTkLabel(form_window, text="New Appointment", font=("Arial Bold", 20), text_color="#1C2833")
        label.pack(pady=10)

        # Date Selection
        date_label = CTkLabel(form_window, text="Appointment Date:", font=("Arial Bold", 16), text_color="#1C2833")
        date_label.pack(pady=10)
        self.date_entry = Calendar(form_window, selectmode='day', font=("Arial Bold", 16), date_pattern='yyyy-mm-dd', text_color="#000000")
        self.date_entry.pack(pady=5)

        # Time Selection
        time_label = CTkLabel(form_window, text="Time (HH:MM):", font=("Arial Bold", 16), text_color="#FFFFFF")
        time_label.pack(pady=10)
        time_slots = self.generate_time_slots()
        self.time_combo = ttk.Combobox(form_window, values=time_slots, width=20, height=50)
        self.time_combo.pack(pady=5)

        # Doctor Selection
        doctor_label = CTkLabel(form_window, text="Doctor:", font=("Arial Bold", 16), text_color="#FFFFFF")
        doctor_label.pack(pady=10)
        cursor = self.mydb.cursor()
        cursor.execute("SELECT CONCAT(DoctorName, ' ', DoctorSurname) FROM doctor")
        doctor_names = [row[0] for row in cursor.fetchall()]
        cursor.close()
        self.doctor_combo = ttk.Combobox(form_window, values=doctor_names)
        self.doctor_combo.pack(pady=5)

        # Patient Selection
        patient_label = CTkLabel(form_window, text="Patient:", font=("Arial Bold", 16), text_color="#FFFFFF")
        patient_label.pack(pady=10)
        cursor = self.mydb.cursor()
        cursor.execute("SELECT CONCAT(Patient_Fname, ' ', Patient_Lname) FROM patient")
        patient_names = [row[0] for row in cursor.fetchall()]
        cursor.close()
        self.patient_combo = ttk.Combobox(form_window, values=patient_names)
        self.patient_combo.pack(pady=5)

        # Save Button
        save_button = CTkButton(form_window, text="Add Appointment", command=self.add_new_appointment, fg_color="#1C2833", text_color="#F2F3F4", hover_color="#1A5276")
        save_button.pack(pady=20)

    def generate_time_slots(self):
        start_time = datetime.strptime("09:00", "%H:%M")
        end_time = datetime.strptime("18:00", "%H:%M")
        delta = timedelta(minutes=30)
        time_slots = []

        while start_time <= end_time:
            time_slots.append(start_time.strftime("%H:%M"))
            start_time += delta

        return time_slots

    def save_appointment_changes(self, appointment_id):
        date = self.date_entry.get_date()
        time = self.time_combo.get()
        doctor_name = self.doctor_combo.get()
        patient_name = self.patient_combo.get()

        # Fetch doctor_id and patient_id
        cursor = self.mydb.cursor()
        cursor.execute("SELECT Doctor_ID FROM doctor WHERE CONCAT(DoctorName, ' ', DoctorSurname) = %s", (doctor_name,))
        doctor_id = cursor.fetchone()[0]

        cursor.execute("SELECT Patient_ID FROM patient WHERE CONCAT(Patient_Fname, ' ', Patient_Lname) = %s", (patient_name,))
        patient_id = cursor.fetchone()[0]

        # Update appointment in the database
        query = """
            UPDATE appointment 
            SET Date = %s, Time = %s, Doctor_ID = %s, Patient_ID = %s 
            WHERE Appointment_ID = %s
        """
        try:
            cursor.execute(query, (date, time, doctor_id, patient_id, appointment_id))
            self.mydb.commit()
            cursor.close()
            CTkMessagebox(title="Success", message="Appointment updated successfully.", icon="check")
            self.view_appointments()
        except mysql.connector.Error as e:
            CTkMessagebox(title="Database Error", message=f"An error occurred: {e}", icon="cancel")

    def add_new_appointment(self):
        date = self.date_entry.get_date()
        time = self.time_combo.get()
        doctor_name = self.doctor_combo.get()
        patient_name = self.patient_combo.get()

        # Fetch doctor_id and patient_id
        cursor = self.mydb.cursor()
        cursor.execute("SELECT Doctor_ID FROM doctor WHERE CONCAT(DoctorName, ' ', DoctorSurname) = %s", (doctor_name,))
        doctor_id = cursor.fetchone()[0]

        cursor.execute("SELECT Patient_ID FROM patient WHERE CONCAT(Patient_Fname, ' ', Patient_Lname) = %s", (patient_name,))
        patient_id = cursor.fetchone()[0]

        # Generate unique appointment ID
        appointment_id = self.generate_unique_appointment_id()

        # Insert new appointment into the database
        query = """
            INSERT INTO appointment (Appointment_ID, Scheduled_On, Date, Time, Doctor_ID, Patient_ID)
            VALUES (%s, CURDATE(), %s, %s, %s, %s)
        """
        try:
            cursor.execute(query, (appointment_id, date, time, doctor_id, patient_id))
            self.mydb.commit()
            cursor.close()
            CTkMessagebox(title="Success", message="New appointment added successfully.", icon="check")
            self.view_appointments()
        except mysql.connector.Error as e:
            CTkMessagebox(title="Database Error", message=f"An error occurred: {e}", icon="cancel")

    def generate_unique_appointment_id(self):
        import random
        while True:
            new_id = random.randint(1000, 9999)
            cursor = self.mydb.cursor()
            cursor.execute("SELECT COUNT(*) FROM appointment WHERE Appointment_ID = %s", (new_id,))
            if cursor.fetchone()[0] == 0:
                cursor.close()
                return new_id
            cursor.close()

    def clear_right_frame(self):
        for widget in self.right_frame.winfo_children():
            widget.destroy()

    def run(self):
        self.app.mainloop()


# Usage example

