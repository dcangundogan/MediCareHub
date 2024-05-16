import customtkinter as ctk
from customtkinter import *
from tkinter import *
from tkinter import ttk
import mysql.connector
from CTkMessagebox import CTkMessagebox
from PIL import Image

class PrescriptionsPage:
    def __init__(self, patient_id):
        self.patient_id = patient_id
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="bercan2003",
            database="MediCareHub",
        )

        self.app = CTk()
        self.app.geometry("900x600")
        self.app.title("Prescriptions Page")
        self.app.resizable(False, False)

        self.initialize_ui()

    def initialize_ui(self):
        main_frame = CTkFrame(master=self.app)
        main_frame.pack(fill=BOTH, expand=True)

        # Left Frame for Logo
        left_frame = CTkFrame(master=main_frame, width=200, height=600, fg_color="#2C3E50")
        left_frame.pack_propagate(0)
        left_frame.pack(side=LEFT, fill=Y)

        imgLogo = Image.open("images/logo.png")
        imgLogoicon = CTkImage(dark_image=imgLogo, light_image=imgLogo, size=(150, 150))
        logoLabel = CTkLabel(master=left_frame, text="", image=imgLogoicon)
        logoLabel.pack(pady=20)

        # Right Frame for Prescriptions
        right_frame = CTkFrame(master=main_frame, width=700, height=600, fg_color="#ECF0F1")
        right_frame.pack_propagate(0)
        right_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=20, pady=20)

        label = CTkLabel(master=right_frame, text="Prescriptions", font=("Arial Bold", 20),text_color="#000000")
        label.pack(pady=10)

        columns = ("Prescription_ID", "Medicine Name", "Date", "Dosage", "Doctor Name")
        self.tree = ttk.Treeview(right_frame, columns=columns, show='headings', style="mystyle.Treeview")

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, minwidth=0, width=130)

        self.tree.pack(expand=True, fill=BOTH, padx=10, pady=10)

        self.fetch_prescriptions()

        # Customize Treeview Style
        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Arial', 12))
        style.configure("mystyle.Treeview.Heading", font=('Arial Bold', 14))
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])

    def fetch_prescriptions(self):
        try:
            cursor = self.mydb.cursor()
            query = """
                SELECT 
                    p.Prescription_ID, 
                    m.M_Name, 
                    p.Date, 
                    p.Dosage, 
                    CONCAT(d.DoctorName, ' ', d.DoctorSurname) AS Doctor_Name
                FROM 
                    prescription p
                JOIN 
                    medicine m ON p.Medicine_ID = m.Medicine_ID
                JOIN 
                    doctor d ON p.Doctor_ID = d.Doctor_ID
                WHERE 
                    p.Patient_ID = %s
            """
            cursor.execute(query, (self.patient_id,))
            rows = cursor.fetchall()

            for row in rows:
                self.tree.insert('', 'end', values=row)

            cursor.close()
        except mysql.connector.Error as e:
            CTkMessagebox(title="Database Error", message=f"An error occurred: {e}", icon="cancel")
    def run(self):
        self.app.mainloop()


if __name__ == "__main__":
    patient_id = 1  # Replace with the actual patient ID
    prescriptions_page = PrescriptionsPage(patient_id)
    prescriptions_page.app.mainloop()
