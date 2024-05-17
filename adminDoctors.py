
import customtkinter as ctk
from customtkinter import *
from tkinter import *
from tkinter import ttk
import mysql.connector
from CTkMessagebox import CTkMessagebox
from PIL import Image


class AdminDoctorPage:
    def __init__(self):
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="bercan2003",
            database="MediCareHub",
        )

        self.app = CTk()
        self.app.geometry("1400x900")
        self.app.title("Admin - Doctor Management")
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
            ("View Doctors", self.view_doctors),
            ("Edit Doctor", self.open_edit_doctor_form),
            ("Add New Doctor", self.open_new_doctor_form),
            ("Delete Doctor", self.delete_doctor),
        ]

        for text, command in nav_buttons:
            button = CTkButton(master=left_frame, text=text, command=command, fg_color="#EEEEEE", hover_color="#08e590", font=("Arial Bold", 18), text_color="#601E88", width=200, height=50)
            button.pack(pady=10)

        # Main Content Frame
        self.right_frame = CTkFrame(master=main_frame, fg_color="#F2F3F4")
        self.right_frame.pack_propagate(0)
        self.right_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=20, pady=20)

        self.view_doctors()

    def view_doctors(self):
        self.clear_right_frame()
        label = CTkLabel(master=self.right_frame, text="Doctors", font=("Arial Bold", 24), text_color="#1C2833")
        label.pack(pady=10)

        columns = ("Doctor ID", "First Name", "Last Name", "Specialization", "Department")
        self.tree = ttk.Treeview(self.right_frame, columns=columns, show='headings', style="mystyle.Treeview")

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, minwidth=0, width=200)

        self.tree.pack(expand=True, fill=BOTH, padx=10, pady=10)
        self.fetch_doctors()

    def fetch_doctors(self):
        try:
            cursor = self.mydb.cursor()
            query = """
                SELECT 
                    d.Doctor_ID, 
                    d.DoctorName, 
                    d.DoctorSurname, 
                    d.Specialization, 
                    dp.Dept_Name 
                FROM 
                    doctor d
                JOIN 
                    department dp ON d.Dept_ID = dp.Dept_ID
            """
            cursor.execute(query)
            rows = cursor.fetchall()

            for row in rows:
                self.tree.insert('', 'end', values=row)

            cursor.close()
        except mysql.connector.Error as e:
            CTkMessagebox(title="Database Error", message=f"An error occurred: {e}", icon="cancel")

    def open_edit_doctor_form(self):
        selected_item = self.tree.selection()
        if not selected_item:
            CTkMessagebox(title="Selection Error", message="Please select a doctor to edit.", icon="cancel")
            return

        doctor_id = self.tree.item(selected_item, 'values')[0]

        form_window = CTkToplevel(self.app)
        form_window.geometry("700x700")
        form_window.title("Edit Doctor Form")

        label = CTkLabel(form_window, text="Edit Doctor", font=("Arial Bold", 20), text_color="#FFFFFF")
        label.pack(pady=10)

        # Fetching existing doctor details
        cursor = self.mydb.cursor(dictionary=True)
        cursor.execute("SELECT * FROM doctor WHERE Doctor_ID = %s", (doctor_id,))
        doctor = cursor.fetchone()
        cursor.close()

        # First Name
        fname_label = CTkLabel(form_window, text="First Name:", font=("Arial Bold", 16), text_color="#FFFFFF")
        fname_label.pack(pady=10)
        self.fname_entry = CTkEntry(form_window, width=300)
        self.fname_entry.insert(0, doctor['DoctorName'])
        self.fname_entry.pack(pady=5)

        # Last Name
        lname_label = CTkLabel(form_window, text="Last Name:", font=("Arial Bold", 16), text_color="#FFFFFF")
        lname_label.pack(pady=10)
        self.lname_entry = CTkEntry(form_window, width=300)
        self.lname_entry.insert(0, doctor['DoctorSurname'])
        self.lname_entry.pack(pady=5)

        # Specialization
        specialization_label = CTkLabel(form_window, text="Specialization:", font=("Arial Bold", 16), text_color="#FFFFFF")
        specialization_label.pack(pady=10)
        self.specialization_entry = CTkEntry(form_window, width=300)
        self.specialization_entry.insert(0, doctor['Specialization'])
        self.specialization_entry.pack(pady=5)

        # Department
        department_label = CTkLabel(form_window, text="Department:", font=("Arial Bold", 16), text_color="#FFFFFF")
        department_label.pack(pady=10)
        cursor = self.mydb.cursor()
        cursor.execute("SELECT Dept_Name FROM department")
        dept_names = [row[0] for row in cursor.fetchall()]
        cursor.close()
        self.department_combo = ttk.Combobox(form_window, values=dept_names)
        self.department_combo.set(f"{doctor['Dept_ID']}")
        self.department_combo.pack(pady=5)

        # Save Button
        save_button = CTkButton(form_window, text="Save Changes", command=lambda: self.save_doctor_changes(doctor_id), fg_color="#1C2833", text_color="#F2F3F4", hover_color="#1A5276")
        save_button.pack(pady=20)

    def open_new_doctor_form(self):
        form_window = CTkToplevel(self.app)
        form_window.geometry("650x650")
        form_window.title("New Doctor Form")

        label = CTkLabel(form_window, text="New Doctor", font=("Arial Bold", 20), text_color="#FFFFFF")
        label.pack(pady=10)

        # First Name
        fname_label = CTkLabel(form_window, text="First Name:", font=("Arial Bold", 16), text_color="#FFFFFF")
        fname_label.pack(pady=10)
        self.fname_entry = CTkEntry(form_window, width=300)
        self.fname_entry.pack(pady=5)

        # Last Name
        lname_label = CTkLabel(form_window, text="Last Name:", font=("Arial Bold", 16), text_color="#FFFFFF")
        lname_label.pack(pady=10)
        self.lname_entry = CTkEntry(form_window, width=300)
        self.lname_entry.pack(pady=5)

        # Specialization
        specialization_label = CTkLabel(form_window, text="Specialization:", font=("Arial Bold", 16), text_color="#FFFFFF")
        specialization_label.pack(pady=10)
        self.specialization_entry = CTkEntry(form_window, width=300)
        self.specialization_entry.pack(pady=5)

        # Department
        department_label = CTkLabel(form_window, text="Department:", font=("Arial Bold", 16), text_color="#1C2833")
        department_label.pack(pady=10)
        cursor = self.mydb.cursor()
        cursor.execute("SELECT Dept_Name FROM department")
        dept_names = [row[0] for row in cursor.fetchall()]
        cursor.close()
        self.department_combo = ttk.Combobox(form_window, values=dept_names)
        self.department_combo.pack(pady=5)

        # Save Button
        save_button = CTkButton(form_window, text="Add Doctor", command=self.add_new_doctor, fg_color="#1C2833", text_color="#F2F3F4", hover_color="#1A5276")
        save_button.pack(pady=20)

    def save_doctor_changes(self, doctor_id):
        fname = self.fname_entry.get()
        lname = self.lname_entry.get()
        specialization = self.specialization_entry.get()
        department_name = self.department_combo.get()

        cursor = self.mydb.cursor()
        cursor.execute("SELECT Dept_ID FROM department WHERE Dept_Name = %s", (department_name,))
        dept_id = cursor.fetchone()[0]

        query = """
            UPDATE doctor 
            SET DoctorName = %s, DoctorSurname = %s, Specialization = %s, Dept_ID = %s 
            WHERE Doctor_ID = %s
        """
        try:
            cursor.execute(query, (fname, lname, specialization, dept_id, doctor_id))
            self.mydb.commit()
            cursor.close()
            CTkMessagebox(title="Success", message="Doctor updated successfully.", icon="check")
            self.view_doctors()
        except mysql.connector.Error as e:
            CTkMessagebox(title="Database Error", message=f"An error occurred: {e}", icon="cancel")

    def add_new_doctor(self):
        fname = self.fname_entry.get()
        lname = self.lname_entry.get()
        specialization = self.specialization_entry.get()
        department_name = self.department_combo.get()

        cursor = self.mydb.cursor()
        cursor.execute("SELECT Dept_ID FROM department WHERE Dept_Name = %s", (department_name,))
        dept_id = cursor.fetchone()[0]

        doctor_id = self.generate_unique_doctor_id()

        query = """
            INSERT INTO doctor (Doctor_ID, DoctorName, DoctorSurname, Specialization, Dept_ID)
            VALUES (%s, %s, %s, %s, %s)
        """
        try:
            cursor.execute(query, (doctor_id, fname, lname, specialization, dept_id))
            self.mydb.commit()
            cursor.close()
            CTkMessagebox(title="Success", message="New doctor added successfully.", icon="check")
            self.view_doctors()
        except mysql.connector.Error as e:
            CTkMessagebox(title="Database Error", message=f"An error occurred: {e}", icon="cancel")

    def delete_doctor(self):
        selected_item = self.tree.selection()
        if not selected_item:
            CTkMessagebox(title="Selection Error", message="Please select a doctor to delete.", icon="cancel")
            return

        doctor_id = self.tree.item(selected_item, 'values')[0]

        query = "DELETE FROM doctor WHERE Doctor_ID = %s"
        try:
            cursor = self.mydb.cursor()
            cursor.execute(query, (doctor_id,))
            self.mydb.commit()
            cursor.close()
            CTkMessagebox(title="Success", message="Doctor deleted successfully.", icon="check")
            self.view_doctors()
        except mysql.connector.Error as e:
            CTkMessagebox(title="Database Error", message=f"An error occurred: {e}", icon="cancel")

    def generate_unique_doctor_id(self):
        import random
        while True:
            new_id = random.randint(1000, 9999)
            cursor = self.mydb.cursor()
            cursor.execute("SELECT COUNT(*) FROM doctor WHERE Doctor_ID = %s", (new_id,))
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
if __name__ == "__main__":
    app = AdminDoctorPage()
    app.run()
