import customtkinter as ctk
from tkinter import messagebox
import mysql.connector

class EditProfilePage:
    def __init__(self, patient_id, mydb):
        self.patient_id = patient_id
        self.mydb = mydb

        self.edit_window = ctk.CTkToplevel()
        self.edit_window.title("Edit Patient Profile")
        self.edit_window.geometry("600x500")

        # Fetch existing data
        self.patient_data = self.fetch_patient_data()
        if not self.patient_data:
            messagebox.showerror("Error", "Failed to fetch patient data.")
            self.edit_window.destroy()
            return

        # Entry widgets for data
        self.entries = {}
        labels = ['First Name:', 'Last Name:', 'Phone:', 'Email:', 'Gender:', 'Blood Type:', 'Condition:', 'Admission Date:', 'Discharge Date:', 'Address:']
        keys = ['Patient_Fname', 'Patient_Lname', 'Phone', 'Email', 'Gender', 'Blood_Type', 'Condition_', 'Admisson_Date', 'Discharge_Date', 'Address']
        for index, (label, key) in enumerate(zip(labels, keys)):
            row_frame = ctk.CTkFrame(self.edit_window)
            row_frame.pack(fill='x', padx=20, pady=5)
            ctk.CTkLabel(row_frame, text=label).pack(side='left')

            entry_var = ctk.StringVar(value=self.patient_data[key] if self.patient_data[key] else '')
            entry = ctk.CTkEntry(row_frame, textvariable=entry_var)
            entry.pack(side='right', expand=True)
            self.entries[key] = entry_var

        # Save button
        save_button = ctk.CTkButton(self.edit_window, text="Save Changes", command=self.save_changes)
        save_button.pack(pady=20)

    def fetch_patient_data(self):
        data = {}
        try:
            cursor = self.mydb.cursor(dictionary=True)
            cursor.execute(
                "SELECT Patient_Fname, Patient_Lname, Phone, Email, Gender, Blood_Type, Condition_, Admisson_Date, Discharge_Date, Address FROM Patient WHERE Patient_ID = %s",
                (self.patient_id,))
            data = cursor.fetchone()
        except mysql.connector.Error as error:
            messagebox.showerror("Database Error", f"An error occurred: {error}")
        finally:
            cursor.close()
        return data

    def save_changes(self):
        response = messagebox.askyesno("Confirm", "Do you want to save the changes?")
        if response:
            try:
                cursor = self.mydb.cursor()
                self.mydb.autocommit = False

                update_query = """
                UPDATE Patient SET
                    Patient_Fname=%s, Patient_Lname=%s, Phone=%s, Email=%s,
                    Gender=%s, Blood_Type=%s, Condition_=%s, Admisson_Date=%s,
                    Discharge_Date=%s, Address=%s
                WHERE Patient_ID=%s
                """
                values = (
                    self.entries['Patient_Fname'].get(), self.entries['Patient_Lname'].get(),
                    self.entries['Phone'].get(), self.entries['Email'].get(),
                    self.entries['Gender'].get(), self.entries['Blood_Type'].get(),
                    self.entries['Condition_'].get(), self.entries['Admisson_Date'].get(),
                    self.entries['Discharge_Date'].get(), self.entries['Address'].get(), self.patient_id
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


