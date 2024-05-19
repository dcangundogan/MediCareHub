import customtkinter as ctk
from customtkinter import *
from tkinter import *
from tkinter import ttk
import mysql.connector
from CTkMessagebox import CTkMessagebox
from PIL import Image


class AdminStaffPage:
    def __init__(self):
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="bercan2003",
            database="MediCareHub",
        )

        self.app = CTk()
        self.app.geometry("1400x900")
        self.app.title("Admin - Staff Management")
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
            ("View Staff", self.view_staff),

            ("Add New Staff", self.open_edit_staff_form),
            ("Delete Staff", self.delete_staff),
        ]

        for text, command in nav_buttons:
            button = CTkButton(master=left_frame, text=text, command=command, fg_color="#EEEEEE", hover_color="#08e590", font=("Arial Bold", 18), text_color="#601E88", width=200, height=50)
            button.pack(pady=10)

        # Main Content Frame
        self.right_frame = CTkFrame(master=main_frame, fg_color="#F2F3F4")
        self.right_frame.pack_propagate(0)
        self.right_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=20, pady=20)

        self.view_staff()

    def view_staff(self):
        self.clear_right_frame()
        label = CTkLabel(master=self.right_frame, text="Staff", font=("Arial Bold", 24), text_color="#1C2833")
        label.pack(pady=10)

        columns = ("Staff ID", "First Name", "Last Name", "Joining Date", "Separation Date", "Type", "Email", "Address", "Department", "SSN")
        self.tree = ttk.Treeview(self.right_frame, columns=columns, show='headings', style="mystyle.Treeview")

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, minwidth=0, width=150)

        self.tree.pack(expand=True, fill=BOTH, padx=10, pady=10)
        self.fetch_staff()

    def fetch_staff(self):
        try:
            cursor = self.mydb.cursor()
            query = """
                SELECT 
                    s.Emp_ID, 
                    s.Emp_FName, 
                    s.Emp_LName, 
                    s.Date_Joining, 
                    s.Date_Separation, 
                    s.Emp_Type, 
                    s.Email, 
                    s.Address, 
                    d.Dept_Name, 
                    s.SSN 
                FROM 
                    staff s
                JOIN 
                    department d ON s.Dept_ID = d.Dept_ID
            """
            cursor.execute(query)
            rows = cursor.fetchall()

            for row in rows:
                self.tree.insert('', 'end', values=row)

            cursor.close()
        except mysql.connector.Error as e:
            CTkMessagebox(title="Database Error", message=f"An error occurred: {e}", icon="cancel")

    def open_edit_staff_form(self):
        selected_item = self.tree.selection()
        if not selected_item:
            CTkMessagebox(title="Selection Error", message="Please select a staff member to edit.", icon="cancel")
            return

        staff_id = self.tree.item(selected_item, 'values')[0]

        form_window = CTkToplevel(self.app)
        form_window.geometry("700x700")
        form_window.title("Edit Staff Form")

        label = CTkLabel(form_window, text="Edit Staff", font=("Arial Bold", 20), text_color="#FFFFFF")
        label.pack(pady=10)

        # Fetching existing staff details
        cursor = self.mydb.cursor(dictionary=True)
        cursor.execute("SELECT * FROM staff WHERE Emp_ID = %s", (staff_id,))
        staff = cursor.fetchone()
        cursor.close()

        form_labels = ["First Name", "Last Name", "Joining Date", "Separation Date", "Type", "Email", "Address", "SSN"]
        self.form_entries = {}

        for label_text in form_labels:
            row_frame = CTkFrame(master=form_window, fg_color="#F2F3F4")
            row_frame.pack(fill=X, pady=5)

            label = CTkLabel(master=row_frame, text=label_text, font=("Arial", 14), text_color="#1C2833")
            label.pack(side=LEFT, padx=5)

            entry = CTkEntry(master=row_frame, width=300)
            entry.insert(0, staff[label_text.replace(" ", "_")])
            entry.pack(side=LEFT, padx=5)
            self.form_entries[label_text] = entry

        department_names = self.get_department_names()
        department_label = CTkLabel(form_window, text="Department", font=("Arial Bold", 16), text_color="#1C2833")
        department_label.pack(pady=10)
        self.department_combo = ttk.Combobox(form_window, values=department_names)
        cursor = self.mydb.cursor()
        cursor.execute("SELECT Dept_Name FROM department WHERE Dept_ID = %s", (staff['Dept_ID'],))
        dept_name = cursor.fetchone()[0]
        cursor.close()
        self.department_combo.set(dept_name)
        self.department_combo.pack(pady=5)

        # Save Button
        save_button = CTkButton(form_window, text="Save Changes", command=lambda: self.save_staff_changes(staff_id), fg_color="#1C2833", text_color="#F2F3F4", hover_color="#1A5276")
        save_button.pack(pady=20)

    def open_edit_staff_form(self):
        selected_item = self.tree.selection()
        if not selected_item:
            CTkMessagebox(title="Selection Error", message="Please select a staff member to edit.", icon="cancel")
            return

        staff_id = self.tree.item(selected_item, 'values')[0]

        form_window = CTkToplevel(self.app)
        form_window.geometry("700x700")
        form_window.title("Edit Staff Form")

        label = CTkLabel(form_window, text="Edit Staff", font=("Arial Bold", 20), text_color="#FFFFFF")
        label.pack(pady=10)

        # Fetching existing staff details
        cursor = self.mydb.cursor(dictionary=True)
        cursor.execute("SELECT * FROM staff WHERE Emp_ID = %s", (staff_id,))
        staff = cursor.fetchone()
        cursor.close()

        form_labels = ["First Name", "Last Name", "Joining Date", "Separation Date", "Type", "Email", "Address", "SSN"]
        self.form_entries = {}

        for label_text in form_labels:
            row_frame = CTkFrame(master=form_window, fg_color="#F2F3F4")
            row_frame.pack(fill=X, pady=5)

            label = CTkLabel(master=row_frame, text=label_text, font=("Arial", 14), text_color="#1C2833")
            label.pack(side=LEFT, padx=5)

            entry = CTkEntry(master=row_frame, width=300)
            entry.insert(0, staff[label_text.replace(" ", "_")])
            entry.pack(side=LEFT, padx=5)
            self.form_entries[label_text] = entry

        department_names = self.get_department_names()
        department_label = CTkLabel(form_window, text="Department", font=("Arial Bold", 16), text_color="#1C2833")
        department_label.pack(pady=10)
        self.department_combo = ttk.Combobox(form_window, values=department_names)
        cursor = self.mydb.cursor()
        cursor.execute("SELECT Dept_Name FROM department WHERE Dept_ID = %s", (staff['Dept_ID'],))
        dept_name = cursor.fetchone()[0]
        cursor.close()
        self.department_combo.set(dept_name)
        self.department_combo.pack(pady=5)

        # Save Button
        save_button = CTkButton(form_window, text="Save Changes",
                                command=lambda: self.save_staff_changes(staff_id, form_window), fg_color="#1C2833",
                                text_color="#F2F3F4", hover_color="#1A5276")
        save_button.pack(pady=20)

        # Back Button
        back_button = CTkButton(master=form_window, text="Back", command=form_window.destroy, fg_color="#607D8B",
                                hover_color="#455A64", font=("Arial Bold", 14))
        back_button.pack(pady=10)

    def save_staff_changes(self, staff_id, form_window):
        fname = self.form_entries["First Name"].get()
        lname = self.form_entries["Last Name"].get()
        joining_date = self.form_entries["Joining Date"].get()
        separation_date = self.form_entries["Separation Date"].get()
        emp_type = self.form_entries["Type"].get()
        email = self.form_entries["Email"].get()
        address = self.form_entries["Address"].get()
        department_name = self.department_combo.get()
        ssn = self.form_entries["SSN"].get()

        cursor = self.mydb.cursor()
        cursor.execute("SELECT Dept_ID FROM department WHERE Dept_Name = %s", (department_name,))
        dept_id = cursor.fetchone()[0]

        query = """
            UPDATE staff 
            SET Emp_FName = %s, Emp_LName = %s, Date_Joining = %s, Date_Separation = %s, Emp_Type = %s, Email = %s, Address = %s, Dept_ID = %s, SSN = %s 
            WHERE Emp_ID = %s
        """
        try:
            cursor.execute(query, (
            fname, lname, joining_date, separation_date, emp_type, email, address, dept_id, ssn, staff_id))
            self.mydb.commit()
            cursor.close()
            CTkMessagebox(title="Success", message="Staff updated successfully.", icon="check")
            form_window.destroy()
            self.view_staff()
        except mysql.connector.Error as e:
            CTkMessagebox(title="Database Error", message=f"An error occurred: {e}", icon="cancel")

    def add_new_staff(self):
        fname = self.form_entries["First Name"].get()
        lname = self.form_entries["Last Name"].get()
        joining_date = self.form_entries["Joining Date"].get()
        separation_date = self.form_entries["Separation Date"].get()
        emp_type = self.form_entries["Type"].get()
        email = self.form_entries["Email"].get()
        address = self.form_entries["Address"].get()
        department_name = self.department_combo.get()
        ssn = self.form_entries["SSN"].get()

        cursor = self.mydb.cursor()
        cursor.execute("SELECT Dept_ID FROM department WHERE Dept_Name = %s", (department_name,))
        dept_id = cursor.fetchone()[0]

        staff_id = self.generate_unique_emp_id()

        query = """
            INSERT INTO staff (Emp_ID, Emp_FName, Emp_LName, Date_Joining, Date_Separation, Emp_Type, Email, Address, Dept_ID, SSN)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        try:
            cursor.execute(query, (staff_id, fname, lname, joining_date, separation_date, emp_type, email, address, dept_id, ssn))
            self.mydb.commit()
            cursor.close()
            CTkMessagebox(title="Success", message="New staff added successfully.", icon="check")
            self.view_staff()
        except mysql.connector.Error as e:
            CTkMessagebox(title="Database Error", message=f"An error occurred: {e}", icon="cancel")

    def delete_staff(self):
        selected_item = self.tree.selection()
        if not selected_item:
            CTkMessagebox(title="Selection Error", message="Please select a staff member to delete.", icon="cancel")
            return

        staff_id = self.tree.item(selected_item, 'values')[0]

        cursor = self.mydb.cursor()
        try:
            cursor.execute("SELECT COUNT(*) FROM doctor WHERE Emp_ID = %s", (staff_id,))
            if cursor.fetchone()[0] > 0:
                CTkMessagebox(title="Foreign Key Constraint", message="Cannot delete staff member as it is referenced in doctor table.", icon="cancel")
                return

            cursor.execute("SELECT COUNT(*) FROM nurse WHERE Emp_ID = %s", (staff_id,))
            if cursor.fetchone()[0] > 0:
                CTkMessagebox(title="Foreign Key Constraint", message="Cannot delete staff member as it is referenced in nurse table.", icon="cancel")
                return

            query = "DELETE FROM staff WHERE Emp_ID = %s"
            cursor.execute(query, (staff_id,))
            self.mydb.commit()
            cursor.close()
            CTkMessagebox(title="Success", message="Staff member deleted successfully.", icon="check")
            self.view_staff()
        except mysql.connector.Error as e:
            CTkMessagebox(title="Database Error", message=f"An error occurred: {e}", icon="cancel")
        finally:
            cursor.close()

    def generate_unique_emp_id(self):
        import random
        while True:
            new_id = random.randint(1000, 9999)
            cursor = self.mydb.cursor()
            cursor.execute("SELECT COUNT(*) FROM staff WHERE Emp_ID = %s", (new_id,))
            if cursor.fetchone()[0] == 0:
                cursor.close()
                return new_id
            cursor.close()

    def get_department_names(self):
        cursor = self.mydb.cursor()
        cursor.execute("SELECT Dept_Name FROM department")
        department_names = [row[0] for row in cursor.fetchall()]
        cursor.close()
        return department_names

    def clear_right_frame(self):
        for widget in self.right_frame.winfo_children():
            widget.destroy()

    def run(self):
        self.app.mainloop()


# Usage example
if __name__ == "__main__":
    app = AdminStaffPage()
    app.run()
