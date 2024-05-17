import customtkinter as ctk
from tkinter import messagebox, ttk
import mysql.connector
from PIL import Image

class DoctorWorkFieldPage:
    def __init__(self, doctor_id):
        self.doctor_id = doctor_id
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="bercan2003",
            database="MediCareHub"
        )

        self.app = ctk.CTk()
        self.app.geometry("800x600")
        self.app.title("Doctor Work Field")
        self.app.resizable(False, False)


        imgLogo = Image.open("images/logo.png").resize((300, 300))
        imgLogoicon = ctk.CTkImage(dark_image=imgLogo, light_image=imgLogo, size=(300, 300))
        userLogo = Image.open("images/medical-team.png").resize((120, 120))
        imgUsericon = ctk.CTkImage(dark_image=userLogo, light_image=userLogo, size=(120, 120))


        logoLabel = ctk.CTkLabel(master=self.app, text="", image=imgLogoicon)
        logoLabel.image = imgLogoicon  # Keep a reference!
        logoLabel.pack(side="left", fill="y")


        frame = ctk.CTkFrame(master=self.app, width=500, height=600, fg_color="#ffffff")
        frame.pack_propagate(0)
        frame.pack(side="right", fill="both", expand=True)


        userLabel = ctk.CTkLabel(master=frame, text="", image=imgUsericon, bg_color="#ffffff")
        userLabel.image = imgUsericon  # Keep a reference!
        userLabel.place(x=180, y=10)  # Adjust placement


        self.display_work_field_info(frame)


        edit_button = ctk.CTkButton(master=frame, text="Edit Work Field", command=self.edit_work_field)
        edit_button.place(x=200, y=500)  # Adjust placement

        self.app.mainloop()

    def display_work_field_info(self, frame):

        try:
            cursor = self.mydb.cursor()
            query = """
                SELECT d.DoctorName, d.DoctorSurname, dept.Dept_Name 
                FROM Doctor d 
                JOIN Department dept ON d.Dept_ID = dept.Dept_ID 
                WHERE d.Doctor_ID = %s
            """
            cursor.execute(query, (self.doctor_id,))
            result = cursor.fetchone()

            if result:
                labels = ['First Name:', 'Last Name:', 'Current Department:']
                for index, (label, value) in enumerate(zip(labels, result)):
                    if value is not None:  # Check if the value is not None
                        info_label = ctk.CTkLabel(master=frame, text=f"{label} {value}", font=("Arial", 12), text_color="#000000")
                        info_label.place(x=20, y=150 + 30 * index)  # Adjust placement

        except mysql.connector.Error as error:
            print("Failed to read data from MySQL table:", error)
        finally:
            if cursor:
                cursor.close()

    def edit_work_field(self):
        edit_window = ctk.CTkToplevel()
        edit_window.title("Edit Work Field")
        edit_window.geometry("400x300")


        departments = self.fetch_departments()


        row_frame = ctk.CTkFrame(edit_window)
        row_frame.pack(fill='x', padx=20, pady=20)
        ctk.CTkLabel(row_frame, text="Select Department:").pack(side='left')

        dept_combo = ttk.Combobox(row_frame, values=[dept['Dept_Name'] for dept in departments])
        dept_combo.pack(side='right', expand=True)

        def save_new_department():
            dept_name = dept_combo.get()
            dept_id = None
            for dept in departments:
                if dept['Dept_Name'] == dept_name:
                    dept_id = dept['Dept_ID']
                    break

            if dept_id is None:
                messagebox.showerror("Input Error", "Please select a valid department.")
                return

            try:
                cursor = self.mydb.cursor()
                self.mydb.autocommit = False

                update_query = "UPDATE Doctor SET Dept_ID=%s WHERE Doctor_ID=%s"
                cursor.execute(update_query, (dept_id, self.doctor_id))
                self.mydb.commit()
                messagebox.showinfo("Update Successful", "Department updated successfully.")
                edit_window.destroy()
                self.app.destroy()
                self.__init__(self.doctor_id)  # Refresh the main page
            except mysql.connector.Error as error:
                self.mydb.rollback()
                messagebox.showerror("Database Error", f"An error occurred: {error}")
            finally:
                self.mydb.autocommit = True
                cursor.close()

        # Save button
        save_button = ctk.CTkButton(edit_window, text="Save Changes", command=save_new_department)
        save_button.pack(pady=20)

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
    def run(self):
        self.app.mainloop()


