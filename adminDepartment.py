import customtkinter as ctk
from tkinter import ttk, BOTH, LEFT, X, Y
import mysql.connector
from CTkMessagebox import CTkMessagebox
from PIL import Image

class AdminDepartmentPage:
    def __init__(self):
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="bercan2003",
            database="MediCareHub",
        )

        self.app = ctk.CTk()
        self.app.geometry("1400x900")
        self.app.title("Admin - Department Management Page")
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

        self.view_departments()

    def clear_right_frame(self):
        for widget in self.right_frame.winfo_children():
            widget.destroy()

    def view_departments(self):
        self.clear_right_frame()
        label = ctk.CTkLabel(master=self.right_frame, text="Departments", font=("Arial Bold", 24), text_color="#1C2833")
        label.pack(pady=10)

        columns = ("Dept_ID", "Department Head", "Department Name", "Employee Count")
        self.tree = ttk.Treeview(self.right_frame, columns=columns, show='headings', style="mystyle.Treeview")

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, minwidth=0, width=200)

        self.tree.pack(expand=True, fill=BOTH, padx=10, pady=10)
        self.fetch_departments()

        self.create_department_buttons()

    def fetch_departments(self):
        try:
            cursor = self.mydb.cursor()
            query = """
                SELECT 
                    Dept_ID, 
                    Dept_Head, 
                    Dept_Name, 
                    Emp_Count 
                FROM 
                    department
            """
            cursor.execute(query)
            rows = cursor.fetchall()

            for row in rows:
                self.tree.insert('', 'end', values=row)

            cursor.close()
        except mysql.connector.Error as e:
            CTkMessagebox(title="Database Error", message=f"An error occurred: {e}", icon="cancel")

    def create_department_buttons(self):
        button_frame = ctk.CTkFrame(self.right_frame, fg_color="#F2F3F4")
        button_frame.pack(fill=X, padx=10, pady=10)

        add_button = ctk.CTkButton(master=button_frame, text="Add Department", command=self.add_department_form, fg_color="#4CAF50", hover_color="#388E3C", font=("Arial Bold", 14))
        add_button.pack(side=LEFT, padx=10)

        edit_button = ctk.CTkButton(master=button_frame, text="Edit Department", command=self.edit_department_form, fg_color="#FFC107", hover_color="#FFA000", font=("Arial Bold", 14))
        edit_button.pack(side=LEFT, padx=10)

        delete_button = ctk.CTkButton(master=button_frame, text="Delete Department", command=self.delete_department, fg_color="#F44336", hover_color="#D32F2F", font=("Arial Bold", 14))
        delete_button.pack(side=LEFT, padx=10)

    def add_department_form(self):
        self.clear_right_frame()

        form_frame = ctk.CTkFrame(master=self.right_frame, fg_color="#F2F3F4")
        form_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)

        label = ctk.CTkLabel(master=form_frame, text="Add Department", font=("Arial Bold", 24), text_color="#1C2833")
        label.pack(pady=10)

        form_labels = ["Department Head", "Department Name", "Employee Count"]
        self.form_entries = {}

        for label_text in form_labels:
            row_frame = ctk.CTkFrame(master=form_frame, fg_color="#F2F3F4")
            row_frame.pack(fill=X, pady=5)

            label = ctk.CTkLabel(master=row_frame, text=label_text, font=("Arial", 14), text_color="#1C2833")
            label.pack(side=LEFT, padx=5)

            entry = ctk.CTkEntry(master=row_frame, width=300)
            entry.pack(side=LEFT, padx=5)
            self.form_entries[label_text] = entry

        submit_button = ctk.CTkButton(master=form_frame, text="Submit", command=self.submit_new_department, fg_color="#4CAF50", hover_color="#388E3C", font=("Arial Bold", 14))
        submit_button.pack(pady=10)

        back_button = ctk.CTkButton(master=form_frame, text="Back", command=self.view_departments, fg_color="#607D8B", hover_color="#455A64", font=("Arial Bold", 14))
        back_button.pack(pady=10)

    def submit_new_department(self):
        dept_head = self.form_entries["Department Head"].get()
        dept_name = self.form_entries["Department Name"].get()
        emp_count = self.form_entries["Employee Count"].get()

        dept_id = self.generate_unique_dept_id()

        query = """
            INSERT INTO department (Dept_ID, Dept_Head, Dept_Name, Emp_Count)
            VALUES (%s, %s, %s, %s)
        """
        try:
            cursor = self.mydb.cursor()
            cursor.execute(query, (dept_id, dept_head, dept_name, emp_count))
            self.mydb.commit()
            cursor.close()
            CTkMessagebox(title="Success", message="New department added successfully.", icon="check")
            self.view_departments()
        except mysql.connector.Error as e:
            CTkMessagebox(title="Database Error", message=f"An error occurred: {e}", icon="cancel")

    def edit_department_form(self):
        selected_item = self.tree.selection()
        if not selected_item:
            CTkMessagebox(title="Selection Error", message="Please select a department to edit.", icon="cancel")
            return

        dept_values = self.tree.item(selected_item, 'values')
        self.clear_right_frame()

        form_frame = ctk.CTkFrame(master=self.right_frame, fg_color="#F2F3F4")
        form_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)

        label = ctk.CTkLabel(master=form_frame, text="Edit Department", font=("Arial Bold", 24), text_color="#1C2833")
        label.pack(pady=10)

        form_labels = ["Department Head", "Department Name", "Employee Count"]
        self.form_entries = {}

        for i, label_text in enumerate(form_labels):
            row_frame = ctk.CTkFrame(master=form_frame, fg_color="#F2F3F4")
            row_frame.pack(fill=X, pady=5)

            label = ctk.CTkLabel(master=row_frame, text=label_text, font=("Arial", 14), text_color="#1C2833")
            label.pack(side=LEFT, padx=5)

            entry = ctk.CTkEntry(master=row_frame, width=300)
            entry.insert(0, dept_values[i+1])
            entry.pack(side=LEFT, padx=5)
            self.form_entries[label_text] = entry

        submit_button = ctk.CTkButton(master=form_frame, text="Submit", command=lambda: self.submit_edit_department(dept_values[0]), fg_color="#FFC107", hover_color="#FFA000", font=("Arial Bold", 14))
        submit_button.pack(pady=10)

        back_button = ctk.CTkButton(master=form_frame, text="Back", command=self.view_departments, fg_color="#607D8B", hover_color="#455A64", font=("Arial Bold", 14))
        back_button.pack(pady=10)

    def submit_edit_department(self, dept_id):
        dept_head = self.form_entries["Department Head"].get()
        dept_name = self.form_entries["Department Name"].get()
        emp_count = self.form_entries["Employee Count"].get()

        query = """
            UPDATE department
            SET Dept_Head = %s, Dept_Name = %s, Emp_Count = %s
            WHERE Dept_ID = %s
        """
        try:
            cursor = self.mydb.cursor()
            cursor.execute(query, (dept_head, dept_name, emp_count, dept_id))
            self.mydb.commit()
            cursor.close()
            CTkMessagebox(title="Success", message="Department updated successfully.", icon="check")
            self.view_departments()
        except mysql.connector.Error as e:
            CTkMessagebox(title="Database Error", message=f"An error occurred: {e}", icon="cancel")

    def delete_department(self):
        selected_item = self.tree.selection()
        if not selected_item:
            CTkMessagebox(title="Selection Error", message="Please select a department to delete.", icon="cancel")
            return

        dept_id = self.tree.item(selected_item, 'values')[0]
        cursor = self.mydb.cursor()

        query = "DELETE FROM department WHERE Dept_ID = %s"
        try:
            cursor.execute(query, (dept_id,))
            self.mydb.commit()
            cursor.close()
            CTkMessagebox(title="Success", message="Department deleted successfully.", icon="check")
            self.view_departments()
        except mysql.connector.Error as e:
            CTkMessagebox(title="Database Error", message=f"An error occurred: {e}", icon="cancel")

    def generate_unique_dept_id(self):
        import random
        while True:
            new_id = random.randint(1000, 9999)
            cursor = self.mydb.cursor()
            cursor.execute("SELECT COUNT(*) FROM department WHERE Dept_ID = %s", (new_id,))
            if cursor.fetchone()[0] == 0:
                cursor.close()
                return new_id
            cursor.close()

    def run(self):
        self.app.mainloop()


