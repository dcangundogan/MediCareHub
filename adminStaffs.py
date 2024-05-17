import customtkinter as ctk
from tkinter import ttk, BOTH, LEFT, X, Y, TOP
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

        self.app = ctk.CTk()
        self.app.geometry("1400x900")
        self.app.title("Admin - Staff Management Page")
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

        self.view_staff()

    def clear_right_frame(self):
        for widget in self.right_frame.winfo_children():
            widget.destroy()

    def view_staff(self):
        self.clear_right_frame()
        label = ctk.CTkLabel(master=self.right_frame, text="Staff", font=("Arial Bold", 24), text_color="#1C2833")
        label.pack(pady=10)

        columns = ("Emp_ID", "First Name", "Last Name", "Joining Date", "Separation Date", "Type", "Email", "Address", "Department", "SSN")
        self.tree = ttk.Treeview(self.right_frame, columns=columns, show='headings', style="mystyle.Treeview")

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, minwidth=0, width=150)

        self.tree.pack(expand=True, fill=BOTH, padx=10, pady=10)
        self.fetch_staff()

        self.create_staff_buttons()

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

    def create_staff_buttons(self):
        button_frame = ctk.CTkFrame(self.right_frame, fg_color="#F2F3F4")
        button_frame.pack(fill=X, padx=10, pady=10)

        add_button = ctk.CTkButton(master=button_frame, text="Add Staff", command=self.add_staff_form, fg_color="#4CAF50", hover_color="#388E3C", font=("Arial Bold", 14))
        add_button.pack(side=LEFT, padx=10)

        edit_button = ctk.CTkButton(master=button_frame, text="Edit Staff", command=self.edit_staff_form, fg_color="#FFC107", hover_color="#FFA000", font=("Arial Bold", 14))
        edit_button.pack(side=LEFT, padx=10)

        delete_button = ctk.CTkButton(master=button_frame, text="Delete Staff", command=self.delete_staff, fg_color="#F44336", hover_color="#D32F2F", font=("Arial Bold", 14))
        delete_button.pack(side=LEFT, padx=10)

    def add_staff_form(self):
        self.clear_right_frame()

        form_frame = ctk.CTkFrame(master=self.right_frame, fg_color="#F2F3F4")
        form_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)

        label = ctk.CTkLabel(master=form_frame, text="Add Staff", font=("Arial Bold", 24), text_color="#1C2833")
        label.pack(pady=10)

        form_labels = ["First Name", "Last Name", "Joining Date", "Separation Date", "Type", "Email", "Address", "Department", "SSN"]
        self.form_entries = {}

        for label_text in form_labels:
            row_frame = ctk.CTkFrame(master=form_frame, fg_color="#F2F3F4")
            row_frame.pack(fill=X, pady=5)

            label = ctk.CTkLabel(master=row_frame, text=label_text, font=("Arial", 14), text_color="#1C2833")
            label.pack(side=LEFT, padx=5)

            entry = ctk.CTkEntry(master=row_frame, width=300)
            entry.pack(side=LEFT, padx=5)
            self.form_entries[label_text] = entry

        department_names = self.get_department_names()
        self.department_combo = ttk.Combobox(form_frame, values=department_names, state='readonly')
        self.department_combo.pack(pady=10)

        submit_button = ctk.CTkButton(master=form_frame, text="Submit", command=self.submit_new_staff, fg_color="#4CAF50", hover_color="#388E3C", font=("Arial Bold", 14))
        submit_button.pack(pady=10)

        back_button = ctk.CTkButton(master=form_frame, text="Back", command=self.view_staff, fg_color="#607D8B", hover_color="#455A64", font=("Arial Bold", 14))
        back_button.pack(pady=10)

    def get_department_names(self):
        cursor = self.mydb.cursor()
        cursor.execute("SELECT Dept_Name FROM department")
        department_names = [row[0] for row in cursor.fetchall()]
        cursor.close()
        return department_names

    def submit_new_staff(self):
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

        emp_id = self.generate_unique_emp_id()

        query = """
            INSERT INTO staff (Emp_ID, Emp_FName, Emp_LName, Date_Joining, Date_Separation, Emp_Type, Email, Address, Dept_ID, SSN)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        try:
            cursor.execute(query, (emp_id, fname, lname, joining_date, separation_date, emp_type, email, address, dept_id, ssn))
            self.mydb.commit()
            cursor.close()
            CTkMessagebox(title="Success", message="New staff added successfully.", icon="check")
            self.view_staff()
        except mysql.connector.Error as e:
            CTkMessagebox(title="Database Error", message=f"An error occurred: {e}", icon="cancel")

    def edit_staff_form(self):
        selected_item = self.tree.selection()
        if not selected_item:
            CTkMessagebox(title="Selection Error", message="Please select a staff member to edit.", icon="cancel")
            return

        staff_values = self.tree.item(selected_item, 'values')
        self.clear_right_frame()

        form_frame = ctk.CTkFrame(master=self.right_frame, fg_color="#F2F3F4")
        form_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)

        label = ctk.CTkLabel(master=form_frame, text="Edit Staff", font=("Arial Bold", 24), text_color="#1C2833")
        label.pack(pady=10)

        form_labels = ["First Name", "Last Name", "Joining Date", "Separation Date", "Type", "Email", "Address", "Department", "SSN"]
        self.form_entries = {}

        for i, label_text in enumerate(form_labels):
            row_frame = ctk.CTkFrame(master=form_frame, fg_color="#F2F3F4")
            row_frame.pack(fill=X, pady=5)

            label = ctk.CTkLabel(master=row_frame, text=label_text, font=("Arial", 14), text_color="#1C2833")
            label.pack(side=LEFT, padx=5)

            entry = ctk.CTkEntry(master=row_frame, width=300)
            entry.insert(0, staff_values[i+1])
            entry.pack(side=LEFT, padx=5)
            self.form_entries[label_text] = entry

        department_names = self.get_department_names()
        self.department_combo = ttk.Combobox(form_frame, values=department_names, state='readonly')
        self.department_combo.set(staff_values[8])
        self.department_combo.pack(pady=10)

        submit_button = ctk.CTkButton(master=form_frame, text="Submit", command=lambda: self.submit_edit_staff(staff_values[0]), fg_color="#FFC107", hover_color="#FFA000", font=("Arial Bold", 14))
        submit_button.pack(pady=10)

        back_button = ctk.CTkButton(master=form_frame, text="Back", command=self.view_staff, fg_color="#607D8B", hover_color="#455A64", font=("Arial Bold", 14))
        back_button.pack(pady=10)

    def submit_edit_staff(self, emp_id):
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
            cursor.execute(query, (fname, lname, joining_date, separation_date, emp_type, email, address, dept_id, ssn, emp_id))
            self.mydb.commit()
            cursor.close()
            CTkMessagebox(title="Success", message="Staff member updated successfully.", icon="check")
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

        query = "DELETE FROM staff WHERE Emp_ID = %s"
        try:
            cursor.execute(query, (staff_id,))
            self.mydb.commit()
            cursor.close()
            CTkMessagebox(title="Success", message="Staff member deleted successfully.", icon="check")
            self.view_staff()
        except mysql.connector.Error as e:
            CTkMessagebox(title="Database Error", message=f"An error occurred: {e}", icon="cancel")

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

    def run(self):
        self.app.mainloop()


