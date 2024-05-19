import customtkinter as ctk
from tkinter import ttk, BOTH, LEFT, Y, X, END
import mysql.connector
from CTkMessagebox import CTkMessagebox
from PIL import Image

class WageSlipManagement:
    def __init__(self):
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="bercan2003",
            database="MediCareHub",
        )

        self.app = ctk.CTk()
        self.app.geometry("1400x900")
        self.app.title("Admin - Wage Slip Management")
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

        self.create_wage_slip_manager()

    def create_wage_slip_manager(self):
        label = ctk.CTkLabel(master=self.right_frame, text="Wage Slip Management", font=("Arial Bold", 24), text_color="#1C2833")
        label.pack(pady=10)

        form_frame = ctk.CTkFrame(master=self.right_frame, fg_color="#F2F3F4")
        form_frame.pack(fill=X, padx=10, pady=10)

        ctk.CTkLabel(master=form_frame, text="Account No:", font=("Arial", 12), text_color="#000000").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.account_no_entry = ctk.CTkEntry(master=form_frame, width=200, text_color="#000000", fg_color="#ffffff")
        self.account_no_entry.grid(row=0, column=1, padx=5, pady=5)

        ctk.CTkLabel(master=form_frame, text="Salary:", font=("Arial", 12), text_color="#000000").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.salary_entry = ctk.CTkEntry(master=form_frame, width=200, text_color="#000000", fg_color="#ffffff")
        self.salary_entry.grid(row=1, column=1, padx=5, pady=5)

        ctk.CTkLabel(master=form_frame, text="Bonus:", font=("Arial", 12), text_color="#000000").grid(row=2, column=0, padx=5, pady=5, sticky='w')
        self.bonus_entry = ctk.CTkEntry(master=form_frame, width=200, text_color="#000000", fg_color="#ffffff")
        self.bonus_entry.grid(row=2, column=1, padx=5, pady=5)

        ctk.CTkLabel(master=form_frame, text="Employee ID:", font=("Arial", 12), text_color="#000000").grid(row=3, column=0, padx=5, pady=5, sticky='w')
        self.emp_id_entry = ctk.CTkEntry(master=form_frame, width=200, text_color="#000000", fg_color="#ffffff")
        self.emp_id_entry.grid(row=3, column=1, padx=5, pady=5)

        ctk.CTkLabel(master=form_frame, text="IBAN:", font=("Arial", 12), text_color="#000000").grid(row=4, column=0, padx=5, pady=5, sticky='w')
        self.iban_entry = ctk.CTkEntry(master=form_frame, width=200, text_color="#000000", fg_color="#ffffff")
        self.iban_entry.grid(row=4, column=1, padx=5, pady=5)

        button_frame = ctk.CTkFrame(master=self.right_frame, fg_color="#F2F3F4")
        button_frame.pack(fill=X, padx=10, pady=10)

        add_button = ctk.CTkButton(master=button_frame, text="Add Wage Slip", command=self.add_wage_slip, fg_color="#4CAF50", hover_color="#388E3C", font=("Arial Bold", 14))
        add_button.pack(side=LEFT, padx=10)

        update_button = ctk.CTkButton(master=button_frame, text="Update Wage Slip", command=self.update_wage_slip, fg_color="#FF9800", hover_color="#F57C00", font=("Arial Bold", 14))
        update_button.pack(side=LEFT, padx=10)

        delete_button = ctk.CTkButton(master=button_frame, text="Delete Wage Slip", command=self.delete_wage_slip, fg_color="#F44336", hover_color="#D32F2F", font=("Arial Bold", 14))
        delete_button.pack(side=LEFT, padx=10)

        refresh_button = ctk.CTkButton(master=button_frame, text="Refresh Table", command=self.refresh_table, fg_color="#607D8B", hover_color="#455A64", font=("Arial Bold", 14))
        refresh_button.pack(side=LEFT, padx=10)

        self.wage_table = ttk.Treeview(self.right_frame, show='headings', style="mystyle.Treeview")
        self.wage_table.pack(expand=True, fill=BOTH, padx=10, pady=10)

        self.refresh_table()

    def refresh_table(self):
        for widget in self.wage_table.get_children():
            self.wage_table.delete(widget)

        headers = ["Account No", "Salary", "Bonus", "Employee ID", "IBAN"]
        self.wage_table["columns"] = headers
        for col in headers:
            self.wage_table.heading(col, text=col)
            self.wage_table.column(col, minwidth=0, width=150, stretch=False)

        try:
            cursor = self.mydb.cursor(dictionary=True)
            cursor.execute("SELECT * FROM wageslip")
            results = cursor.fetchall()
            for row in results:
                values = list(row.values())
                self.wage_table.insert("", "end", values=values)
        except mysql.connector.Error as error:
            CTkMessagebox(title="Database Error", message=f"Failed to read data from MySQL table: {error}", icon="cancel")
        finally:
            if cursor:
                cursor.close()

    def add_wage_slip(self):
        try:
            cursor = self.mydb.cursor()
            query = "INSERT INTO wageslip (Account_No, Salary, Bonus, Emp_ID, IBAN) VALUES (%s, %s, %s, %s, %s)"
            values = (
                self.account_no_entry.get(),
                self.salary_entry.get(),
                self.bonus_entry.get(),
                self.emp_id_entry.get(),
                self.iban_entry.get()
            )
            cursor.execute(query, values)
            self.mydb.commit()
            CTkMessagebox(title="Success", message="Wage slip added successfully", icon="check")
            self.refresh_table()
        except mysql.connector.Error as error:
            CTkMessagebox(title="Error", message=f"Failed to add wage slip: {error}", icon="cancel")
        finally:
            if cursor:
                cursor.close()

    def update_wage_slip(self):
        try:
            cursor = self.mydb.cursor()
            query = "UPDATE wageslip SET Salary = %s, Bonus = %s, Emp_ID = %s, IBAN = %s WHERE Account_No = %s"
            values = (
                self.salary_entry.get(),
                self.bonus_entry.get(),
                self.emp_id_entry.get(),
                self.iban_entry.get(),
                self.account_no_entry.get()
            )
            cursor.execute(query, values)
            self.mydb.commit()
            CTkMessagebox(title="Success", message="Wage slip updated successfully", icon="check")
            self.refresh_table()
        except mysql.connector.Error as error:
            CTkMessagebox(title="Error", message=f"Failed to update wage slip: {error}", icon="cancel")
        finally:
            if cursor:
                cursor.close()

    def delete_wage_slip(self):
        try:
            cursor = self.mydb.cursor()
            query = "DELETE FROM wageslip WHERE Account_No = %s"
            value = (self.account_no_entry.get(),)
            cursor.execute(query, value)
            self.mydb.commit()
            CTkMessagebox(title="Success", message="Wage slip deleted successfully", icon="check")
            self.refresh_table()
        except mysql.connector.Error as error:
            CTkMessagebox(title="Error", message=f"Failed to delete wage slip: {error}", icon="cancel")
        finally:
            if cursor:
                cursor.close()

    def run(self):
        self.app.mainloop()

