import customtkinter as ctk
from tkinter import ttk
from tkcalendar import Calendar
from datetime import datetime, timedelta
import mysql.connector
from CTkMessagebox import CTkMessagebox


class AppointmentManager:
    def __init__(self, patient_id):
        self.patient_id = patient_id
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="bercan2003",
            database="MediCareHub"
        )
        self.app = ctk.CTk()
        self.app.geometry("1000x750")
        self.app.title("MediCareHub Appointment Management")
        self.new_appointment_date = None
        self.new_appointment_time_combo = None
        self.new_appointment_doctor_combo = None
        self.new_appointment_patient_entry = None
        self.appointments_tree = None
        self.initialize_ui()

    def generate_time_slots(self):
        start_time = datetime.strptime("09:00", "%H:%M")
        end_time = datetime.strptime("18:00", "%H:%M")
        delta = timedelta(minutes=30)
        time_slots = []

        while start_time <= end_time:
            time_slots.append(start_time.strftime("%H:%M"))
            start_time += delta

        return time_slots

    def check_patient_exists(self):
        cursor = self.mydb.cursor()
        cursor.execute("SELECT COUNT(*) FROM patient WHERE Patient_ID = %s", (self.patient_id,))
        count = cursor.fetchone()[0]
        cursor.close()
        return count > 0

    def fetch_appointments_by_patient(self):
        if not self.check_patient_exists():
            CTkMessagebox(title="Input Error", message="The entered Patient ID does not exist.", icon="cancel")
            return []

        try:
            cursor = self.mydb.cursor()
            query = """
            SELECT
                a.Appointment_ID,
                p.Patient_Fname,
                a.Date,
                a.Time,
                CONCAT(d.DoctorName, ' ', d.DoctorSurname) AS Doctor_FullName
            FROM
                appointment a
            JOIN
                patient p ON a.Patient_ID = p.Patient_ID
            JOIN
                doctor d ON a.Doctor_ID = d.Doctor_ID
            WHERE
                a.Patient_ID = %s
            """
            cursor.execute(query, (self.patient_id,))
            rows = cursor.fetchall()
            cursor.close()
            return rows
        except mysql.connector.Error as e:
            CTkMessagebox(title="Database Error", message=f"An error occurred: {e}", icon="cancel")
            return []

    def show_filtered_appointments(self):
        for item in self.appointments_tree.get_children():
            self.appointments_tree.delete(item)

        appointments = self.fetch_appointments_by_patient()
        if not appointments:
            CTkMessagebox(title="No Appointments", message="No appointments found for this Patient ID.", icon="info")
            return

        for row in appointments:
            self.appointments_tree.insert('', 'end', values=row)

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

    def submit_new_appointment(self):
        appointment_id = self.generate_unique_appointment_id()
        date = self.new_appointment_date.get_date()
        time = self.new_appointment_time_combo.get()
        doctor_name = self.new_appointment_doctor_combo.get()

        if not self.check_patient_exists():
            CTkMessagebox(title="Input Error", message="Please enter a valid Patient ID.", icon="cancel")
            return

        cursor = self.mydb.cursor()
        cursor.execute("SELECT Doctor_ID FROM doctor WHERE CONCAT(DoctorName, ' ', DoctorSurname) = %s", (doctor_name,))
        doctor_id = cursor.fetchone()[0]
        cursor.close()

        query = """
        INSERT INTO appointment (Appointment_ID, Scheduled_On, Date, Time, Doctor_ID, Patient_ID)
        VALUES (%s, CURDATE(), %s, %s, %s, %s)
        """
        try:
            cursor = self.mydb.cursor()
            cursor.execute(query, (appointment_id, date, time, doctor_id, self.patient_id))
            self.mydb.commit()
            cursor.close()
            CTkMessagebox(title="Success", message="New appointment booked successfully.", icon="check")
        except mysql.connector.Error as e:
            CTkMessagebox(title="Database Error", message=f"An error occurred: {e}", icon="cancel")
        self.show_filtered_appointments()

    def open_new_appointment_form(self):
        form_window = ctk.CTkToplevel(self.app)
        form_window.geometry("650x650")
        form_window.title("New Appointment Form")

        new_appointment_date_label = ctk.CTkLabel(form_window, text="Appointment Date:", font=("Arial Bold", 18))
        new_appointment_date_label.pack(pady=10)
        self.new_appointment_date = Calendar(form_window, selectmode='day', font=("Arial Bold", 16),
                                             date_pattern='yyyy-mm-dd', text_color="#000000")
        self.new_appointment_date.pack(pady=5)

        time_slots = self.generate_time_slots()

        new_appointment_time_label = ctk.CTkLabel(form_window, text="Time (HH:MM):", font=("Arial Bold", 16))
        new_appointment_time_label.pack(pady=10)
        self.new_appointment_time_combo = ttk.Combobox(form_window, values=time_slots, width=20, height=50)
        self.new_appointment_time_combo.pack(pady=5)

        new_appointment_doctor_label = ctk.CTkLabel(form_window, text="Doctor:", font=("Arial Bold", 16))
        new_appointment_doctor_label.pack(pady=10)
        cursor = self.mydb.cursor()
        cursor.execute("SELECT CONCAT(DoctorName, ' ', DoctorSurname) FROM doctor")
        doctor_names = [row[0] for row in cursor.fetchall()]
        cursor.close()
        self.new_appointment_doctor_combo = ttk.Combobox(form_window, values=doctor_names)
        self.new_appointment_doctor_combo.pack(pady=5)

        submit_button = ctk.CTkButton(form_window, text="Submit", font=("Arial Bold", 16),
                                      command=self.submit_new_appointment)
        submit_button.pack(pady=10)

    def initialize_ui(self):
        tab_view = ctk.CTkTabview(self.app)
        tab_view.pack(expand=True, fill="both", padx=20, pady=20)

        tab1 = tab_view.add("Manage Appointments")

        columns = ("AppointmentID", "Patient Name", "Date", "Time", "Doctor Name")
        self.appointments_tree = ttk.Treeview(tab1, columns=columns, show='headings')
        for col in columns:
            self.appointments_tree.heading(col, text=col)
            self.appointments_tree.column(col, width=150)

        self.appointments_tree.pack(expand=True, fill='both')

        filter_button = ctk.CTkButton(tab1, text="Show Appointments", font=("Arial Bold", 16),
                                      command=self.show_filtered_appointments)
        filter_button.pack(pady=10)

        new_appointment_button = ctk.CTkButton(tab1, text="New Appointment",font=("Arial Bold", 16), command=self.open_new_appointment_form)
        new_appointment_button.pack(pady=10)

    def run(self):
        self.app.mainloop()


# Usage example
if __name__ == "__main__":
    patient_id = "1"  # Replace with the actual patient ID
    manager = AppointmentManager(patient_id)
    manager.run()
