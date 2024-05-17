import customtkinter as ctk
from tkinter import messagebox, ttk
import mysql.connector

class EditDoctorProfilePage:
    def __init__(self, doctor_id, mydb):
        self.doctor_id = doctor_id
        self.mydb = mydb

        self.edit_window = ctk.CTkToplevel()
        self.edit_window.title("Edit Doctor Profile")
        self.edit_window.geometry("600x500")

        # Fetch existing data
        self.doctor_data = self.fetch_doctor_data()
        if not self.doctor_data:
            messagebox.showerror("Error", "Failed to fetch doctor data.")
            self.edit_window.destroy()
            return

        # Fetch department names
        self.departments = self.fetch_departments()

        # Entry widgets for data
        self.entries = {}
        labels = ['First Name:', 'Last Name:', 'Specialization:', 'Department:']
        keys = ['DoctorName', 'DoctorSurname', 'Specialization', 'Dept_Name']
        for index, (label, key) in enumerate(zip(labels, keys)):
            row_frame = ctk.CTkFrame(self.edit_window)
            row_frame.pack(fill='x', padx=20, pady=5)
            ctk.CTkLabel(row_frame, text=label).pack(side='left')

            if key == 'Dept_Name':
                dept_combo = ttk.Combobox(row_frame, values=[dept['Dept_Name'] for dept in self.departments])
                dept_combo.set(self.doctor_data[key] if self.doctor_data[key] else '')
                dept_combo.pack(side='right', expand=True)
                self.entries[key] = dept_combo
            else:
                entry_var = ctk.StringVar(value=self.doctor_data[key] if self.doctor_data[key] else '')
                entry = ctk.CTkEntry(row_frame, textvariable=entry_var)
                entry.pack(side='right', expand=True)
                self.entries[key] = entry_var

        # Save button
        save_button = ctk.CTkButton(self.edit_window, text="Save Changes", command=self.save_changes)
        save_button.pack(pady=20)

    def fetch_doctor_data(self):
        data = {}
        try:
            cursor = self.mydb.cursor(dictionary=True)
            cursor.execute(
                """SELECT d.DoctorName, d.DoctorSurname, d.Specialization, dept.Dept_Name 
                   FROM Doctor d 
                   JOIN Department dept ON d.Dept_ID = dept.Dept_ID 
                   WHERE d.Doctor_ID = %s""",
                (self.doctor_id,))
            data = cursor.fetchone()
        except mysql.connector.Error as error:
            messagebox.showerror("Database Error", f"An error occurred: {error}")
        finally:
            cursor.close()
        return data

    def fetch_departments(self):
        try:
            cursor = self.mydb.cursor(dictionary=True)
            cursor.execute("SELECT Dept_ID, Dept_Name FROM Department")
            departments = cursor.fetchall()
            cursor.close()
            return departments
        except mysql.connector.Error as error:
            messagebox.showerror("Database Error", f"An error occurred: {error}")
            return []

    def save_changes(self):
        response = messagebox.askyesno("Confirm", "Do you want to save the changes?")
        if response:
            try:
                cursor = self.mydb.cursor()
                self.mydb.autocommit = False

                dept_name = self.entries['Dept_Name'].get()
                dept_id = None
                for dept in self.departments:
                    if dept['Dept_Name'] == dept_name:
                        dept_id = dept['Dept_ID']
                        break

                if dept_id is None:
                    messagebox.showerror("Input Error", "Please select a valid department.")
                    return

                update_query = """
                UPDATE Doctor SET
                    DoctorName=%s, DoctorSurname=%s, Specialization=%s, Dept_ID=%s
                WHERE Doctor_ID=%s
                """
                values = (
                    self.entries['DoctorName'].get(), self.entries['DoctorSurname'].get(),
                    self.entries['Specialization'].get(), dept_id, self.doctor_id
                )
                cursor.execute(update_query, values)
                self.mydb.commit()
                messagebox.showinfo("Update Successful", "Profile updated successfully.")
                self.edit_window.destroy()
            except mysql.connector.Error as error:
                self.mydb.rollback()
                messagebox.showerror("Database Error", f"An error occurred: {error}")
            finally:
                self.mydb.autocommit = True
                cursor.close()

