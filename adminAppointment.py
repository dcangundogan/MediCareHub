import customtkinter as ctk
from tkinter import ttk
from tkcalendar import Calendar
from datetime import datetime, timedelta
import mysql.connector
from CTkMessagebox import CTkMessagebox

# Database Configuration
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="bercan2003",
    database="MediCareHub"
)

# Function to generate time slots every 30 minutes up to 18:00
def generate_time_slots():
    start_time = datetime.strptime("09:00", "%H:%M")
    end_time = datetime.strptime("18:00", "%H:%M")
    delta = timedelta(minutes=30)
    time_slots = []

    while start_time <= end_time:
        time_slots.append(start_time.strftime("%H:%M"))
        start_time += delta

    return time_slots

# Function to check if the patient exists in the database
def check_patient_exists(patient_id):
    cursor = mydb.cursor()
    cursor.execute("SELECT COUNT(*) FROM patient WHERE Patient_ID = %s", (patient_id,))
    count = cursor.fetchone()[0]
    cursor.close()
    return count > 0

# Function to fetch appointments by patient ID, including patient and doctor names
def fetch_appointments_by_patient(patient_id):
    if not check_patient_exists(patient_id):
        CTkMessagebox(title="Input Error", message="The entered Patient ID does not exist.", icon="cancel")
        return []

    try:
        cursor = mydb.cursor()
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
        cursor.execute(query, (patient_id,))
        rows = cursor.fetchall()
        cursor.close()
        return rows
    except mysql.connector.Error as e:
        CTkMessagebox(title="Database Error", message=f"An error occurred: {e}", icon="cancel")
        return []

# Function to display appointments filtered by patient ID in the table
def show_filtered_appointments():
    patient_id = patient_id_entry.get().strip()  # Use strip() to remove any leading/trailing whitespace
    if not patient_id:
        #CTkMessagebox(title="Input Error", message="Patient ID field is empty.", icon="cancel")
        return

    for item in appointments_tree.get_children():
        appointments_tree.delete(item)

    appointments = fetch_appointments_by_patient(patient_id)
    if not appointments:
        CTkMessagebox(title="No Appointments", message="No appointments found for this Patient ID.", icon="info")
        return

    for row in appointments:
        appointments_tree.insert('', 'end', values=row)

# Function to generate a random unique appointment ID
def generate_unique_appointment_id():
    import random
    while True:
        new_id = random.randint(1000, 9999)
        cursor = mydb.cursor()
        cursor.execute("SELECT COUNT(*) FROM appointment WHERE Appointment_ID = %s", (new_id,))
        if cursor.fetchone()[0] == 0:
            cursor.close()
            return new_id
        cursor.close()


def submit_new_appointment():
    appointment_id = generate_unique_appointment_id()
    date = new_appointment_date.get_date()
    time = new_appointment_time_combo.get()
    doctor_name = new_appointment_doctor_combo.get()
    patient_id = new_appointment_patient_entry.get()

    if not patient_id or not check_patient_exists(patient_id):
        CTkMessagebox(title="Input Error", message="Please enter a valid Patient ID.", icon="cancel")
        return

    # Find doctor ID based on the selected name
    cursor = mydb.cursor()
    cursor.execute("SELECT Doctor_ID FROM doctor WHERE CONCAT(DoctorName, ' ', DoctorSurname) = %s", (doctor_name,))
    doctor_id = cursor.fetchone()[0]
    cursor.close()

    query = """
    INSERT INTO appointment (Appointment_ID, Scheduled_On, Date, Time, Doctor_ID, Patient_ID)
    VALUES (%s, CURDATE(), %s, %s, %s, %s)
    """
    try:
        cursor = mydb.cursor()
        cursor.execute(query, (appointment_id, date, time, doctor_id, patient_id))
        mydb.commit()
        cursor.close()
        CTkMessagebox(title="Success", message="New appointment booked successfully.", icon="check")
    except mysql.connector.Error as e:
        CTkMessagebox(title="Database Error", message=f"An error occurred: {e}", icon="cancel")
    show_filtered_appointments()

# Function to open a form for creating a new appointment
def open_new_appointment_form():
    global new_appointment_date, new_appointment_time_combo, new_appointment_doctor_combo, new_appointment_patient_entry

    form_window = ctk.CTkToplevel(app)
    form_window.geometry("650x650")
    form_window.title("New Appointment Form")

    # Calendar widget for the appointment date
    new_appointment_date_label = ctk.CTkLabel(form_window, text="Appointment Date:",font=("Arial Bold", 18))
    new_appointment_date_label.pack(pady=10)
    new_appointment_date = Calendar(form_window, selectmode='day',font=("Arial Bold", 16), date_pattern='yyyy-mm-dd',text_color="#000000")
    new_appointment_date.pack(pady=5)

    # Generate and use dynamic time slots
    time_slots = generate_time_slots()

    # Combobox for selecting available times
    new_appointment_time_label = ctk.CTkLabel(form_window, text="Time (HH:MM):",font=("Arial Bold", 16))
    new_appointment_time_label.pack(pady=10)
    new_appointment_time_combo = ttk.Combobox(form_window, values=time_slots,width=20,height=50)
    new_appointment_time_combo.pack(pady=5)

    # Combobox for selecting a doctor name
    new_appointment_doctor_label = ctk.CTkLabel(form_window, text="Doctor:",font=("Arial Bold", 16))
    new_appointment_doctor_label.pack(pady=10)
    cursor = mydb.cursor()
    cursor.execute("SELECT CONCAT(DoctorName, ' ', DoctorSurname) FROM doctor")
    doctor_names = [row[0] for row in cursor.fetchall()]
    cursor.close()
    new_appointment_doctor_combo = ttk.Combobox(form_window, values=doctor_names)
    new_appointment_doctor_combo.pack(pady=5)

    # Entry field for the patient ID
    new_appointment_patient_label = ctk.CTkLabel(form_window, text="Patient ID:",font=("Arial Bold", 16))
    new_appointment_patient_label.pack(pady=10)
    new_appointment_patient_entry = ctk.CTkEntry(form_window,width=190,height=35)
    new_appointment_patient_entry.pack(pady=5)

    submit_button = ctk.CTkButton(form_window, text="Submit",font=("Arial Bold", 16), command=submit_new_appointment)
    submit_button.pack(pady=10)

# Initialize the main application
app = ctk.CTk()
app.geometry("1000x750")
app.title("MediCareHub Appointment Management")

# Create a tab view to separate pages
tab_view = ctk.CTkTabview(app)
tab_view.pack(expand=True, fill="both", padx=20, pady=20)

# Create a tab for appointment management
tab1 = tab_view.add("Manage Appointments")

# Entry to input patient ID for filtering
patient_id_label = ctk.CTkLabel(tab1, text="Enter Patient ID:",font=("Arial Bold", 18), text_color="#FFFFFF")
patient_id_label.pack(pady=10)
patient_id_entry = ctk.CTkEntry(tab1)
patient_id_entry.pack(pady=0)

# Button to filter appointments by patient ID
filter_button = ctk.CTkButton(tab1, text="Filter Appointments",font=("Arial Bold", 16), command=show_filtered_appointments)
filter_button.pack(pady=10)

# Table to display filtered appointments, with compact column widths
columns = ("Appointment_ID", "Patient_Name", "Date", "Time", "Doctor Name")
appointments_tree = ttk.Treeview(tab1, columns=columns, show='headings')
for col in columns:
    appointments_tree.heading(col, text=col)
    appointments_tree.column(col, width=150)

appointments_tree.pack(expand=True, fill='both')

# Button to create a new appointment
new_appointment_button = ctk.CTkButton(tab1, text="New Appointment", command=open_new_appointment_form)
new_appointment_button.pack(pady=10)

app.mainloop()