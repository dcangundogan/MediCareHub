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

        # Navigation Buttons
        nav_buttons = [
            ("View Departments", self.view_departments),
            ("Edit Department", self.open_edit_department_form),
            ("Add New Department", self.open_new_department_form),
            ("Delete Department", self.delete_department),
        ]

        for text, command in nav_buttons:
            button = ctk.CTkButton(master=left_frame, text=text, command=command, fg_color="#EEEEEE", hover_color="#08e590", font=("Arial Bold", 18), text_color="#601E88", width=200, height=50)
            button.pack(pady=10)

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

    def open_edit_department_form(self):
        selected_item = self.tree.selection()
        if not selected_item:
            CTkMessagebox(title="Selection Error", message="Please select a department to edit.", icon="cancel")
            return

        dept_id = self.tree.item(selected_item, 'values')[0]

        form_window = ctk.CTkToplevel(self.app)
        form_window.geometry("700x700")
        form_window.title("Edit Department Form")

        label = ctk.CTkLabel(form_window, text="Edit Department", font=("Arial Bold", 20), text_color="#1C2833")
        label.pack(pady=10)

        # Fetching existing department details
        cursor = self.mydb.cursor(dictionary=True)
        cursor.execute("SELECT * FROM department WHERE Dept_ID = %s", (dept_id,))
        department = cursor.fetchone()
        cursor.close()

        # Department Head
        head_label = ctk.CTkLabel(form_window, text="Department Head:", font=("Arial Bold", 16), text_color="#1C2833")
        head_label.pack(pady=10)
        self.head_entry = ctk.CTkEntry(form_window, width=300)
        self.head_entry.insert(0, department['Dept_Head'])
        self.head_entry.pack(pady=5)

        # Department Name
        name_label = ctk.CTkLabel(form_window, text="Department Name:", font=("Arial Bold", 16), text_color="#1C2833")
        name_label.pack(pady=10)
        self.name_entry = ctk.CTkEntry(form_window, width=300)
        self.name_entry.insert(0, department['Dept_Name'])
        self.name_entry.pack(pady=5)

        # Employee Count
        emp_count_label = ctk.CTkLabel(form_window, text="Employee Count:", font=("Arial Bold", 16), text_color="#1C2833")
        emp_count_label.pack(pady=10)
        self.emp_count_entry = ctk.CTkEntry(form_window, width=300)
        self.emp_count_entry.insert(0, department['Emp_Count'])
        self.emp_count_entry.pack(pady=5)

        # Save Button
        save_button = ctk.CTkButton(form_window, text="Save Changes", command=lambda: self.save_department_changes(dept_id, form_window), fg_color="#1C2833", text_color="#F2F3F4", hover_color="#1A5276")
        save_button.pack(pady=20)

    def open_new_department_form(self):
        form_window = ctk.CTkToplevel(self.app)
        form_window.geometry("650x650")
        form_window.title("New Department Form")

        label = ctk.CTkLabel(form_window, text="New Department", font=("Arial Bold", 20), text_color="#1C2833")
        label.pack(pady=10)

        # Department Head
        head_label = ctk.CTkLabel(form_window, text="Department Head:", font=("Arial Bold", 16), text_color="#1C2833")
        head_label.pack(pady=10)
        self.head_entry = ctk.CTkEntry(form_window, width=300)
        self.head_entry.pack(pady=5)

        # Department Name
        name_label = ctk.CTkLabel(form_window, text="Department Name:", font=("Arial Bold", 16), text_color="#1C2833")
        name_label.pack(pady=10)
        self.name_entry = ctk.CTkEntry(form_window, width=300)
        self.name_entry.pack(pady=5)

        # Employee Count
        emp_count_label = ctk.CTkLabel(form_window, text="Employee Count:", font=("Arial Bold", 16), text_color="#1C2833")
        emp_count_label.pack(pady=10)
        self.emp_count_entry = ctk.CTkEntry(form_window, width=300)
        self.emp_count_entry.pack(pady=5)

        # Save Button
        save_button = ctk.CTkButton(form_window, text="Add Department", command=lambda: self.add_new_department(form_window), fg_color="#1C2833", text_color="#F2F3F4", hover_color="#1A5276")
        save_button.pack(pady=20)

    def save_department_changes(self, dept_id, form_window):
        dept_head = self.head_entry.get()
        dept_name = self.name_entry.get()
        emp_count = self.emp_count_entry.get()

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
            form_window.destroy()
            self.view_departments()
        except mysql.connector.Error as e:
            CTkMessagebox(title="Database Error", message=f"An error occurred: {e}", icon="cancel")

    def add_new_department(self, form_window):
        dept_head = self.head_entry.get()
        dept_name = self.name_entry.get()
        emp_count = self.emp_count_entry.get()

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
            form_window.destroy()
            self.view_departments()
        except mysql.connector.Error as e:
            CTkMessagebox(title="Database Error", message=f"An error occurred: {e}", icon="cancel")

    def delete_department(self):
        selected_item = self.tree.selection()
        if not selected_item:
            CTkMessagebox(title="Selection Error", message="Please select a department to delete.", icon="cancel")
            return

        dept_id = self.tree.item(selected_item, 'values')[0]

        query = "DELETE FROM department WHERE Dept_ID = %s"
        try:
            cursor = self.mydb.cursor()
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


# Usage example
if __name__ == "__main__":
    app = AdminDepartmentPage()
    app.run()
