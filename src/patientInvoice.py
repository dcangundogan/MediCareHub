import customtkinter as ctk
from PIL import Image
import mysql.connector

class InvoicePage:
    def __init__(self, patient_id):
        self.patient_id = patient_id
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="bercan2003",
            database="MediCareHub",
        )

        self.app = ctk.CTk()
        self.app.geometry("800x600")
        self.app.title("Invoice Information")
        self.app.resizable(False, False)

        # Load images and convert them to CTkImage for customtkinter compatibility
        imgLogo = Image.open("images/logo.png").resize((300, 300))
        imgLogoicon = ctk.CTkImage(dark_image=imgLogo, light_image=imgLogo, size=(300, 300))
        userLogo = Image.open("images/user.png").resize((120, 120))
        imgUsericon = ctk.CTkImage(dark_image=userLogo, light_image=userLogo, size=(120, 120))

        # Logo at the top left
        logoLabel = ctk.CTkLabel(master=self.app, text="", image=imgLogoicon)
        logoLabel.image = imgLogoicon  # Keep a reference!
        logoLabel.pack(side="left", fill="y")

        # Main Frame for content
        frame = ctk.CTkFrame(master=self.app, width=500, height=600, fg_color="#ffffff")
        frame.pack_propagate(0)
        frame.pack(side="right", fill="both", expand=True)

        # User icon
        userLabel = ctk.CTkLabel(master=frame, text="", image=imgUsericon, bg_color="#ffffff")
        userLabel.image = imgUsericon  # Keep a reference!
        userLabel.place(x=180, y=10)  # Adjust placement

        # Display invoice information
        self.display_invoice_info(frame)

        # Back button
        back_button = ctk.CTkButton(master=frame, text="Back", command=self.go_back_to_main_page,hover_color="#08e590", font=("Arial Bold", 12), text_color="#FFFFFF")
        back_button.place(x=20, y=500)

        # Pay button
        pay_button = ctk.CTkButton(master=frame, text="Pay", command=self.pay_invoice,hover_color="#08e590", font=("Arial Bold", 12), text_color="#FFFFFF",bg_color="#E9EAEC")
        pay_button.place(x=300, y=500)

        self.app.mainloop()

    def display_invoice_info(self, frame):
        # Fetch and display invoice information
        try:
            cursor = self.mydb.cursor(dictionary=True)
            query = """
            SELECT Invoice_ID, Date, Room_Cost, Test_Cost, Other_Charges, Total, Patient_ID, Policy_Number, Medicine_Cost, Status
            FROM invoice
            WHERE Patient_ID = %s
            """
            cursor.execute(query, (self.patient_id,))
            result = cursor.fetchone()

            if result:
                self.invoice_id = result['Invoice_ID']  # Store the invoice ID for payment
                labels = [
                    'Invoice ID:', 'Date:', 'Room Cost:', 'Test Cost:', 'Other Charges:',
                    'Total:', 'Patient ID:', 'Policy Number:', 'Medicine Cost:', 'Status:'
                ]
                y_offset = 150
                for label in labels:
                    value = result.get(label[:-1].replace(" ", "_"))
                    info_label = ctk.CTkLabel(master=frame, text=f"{label} {value}", font=("Arial", 12), text_color="#000000")
                    info_label.place(x=20, y=y_offset)  # Adjust placement
                    y_offset += 30

        except mysql.connector.Error as error:
            print("Failed to read data from MySQL table:", error)
        finally:
            if cursor:
                cursor.close()

    def pay_invoice(self):
        # Mock payment process
        try:
            cursor = self.mydb.cursor()
            update_query = "UPDATE invoice SET Status = 'Paid' WHERE Invoice_ID = %s"
            cursor.execute(update_query, (self.invoice_id,))
            self.mydb.commit()

            # Display a success message
            success_message = ctk.CTkLabel(master=self.app, text="Payment Successful!", font=("Arial Bold", 14), text_color="#000000",bg_color="#FFFFFF")
            success_message.place(x=320, y=550)

        except mysql.connector.Error as error:
            print("Failed to update invoice status:", error)
        finally:
            if cursor:
                cursor.close()

    def go_back_to_main_page(self):
        self.app.destroy()
        from patientMain import PatientMainPage
        patient_main_page = PatientMainPage(self.patient_id)
        patient_main_page.run()

    def run(self):
        self.app.mainloop()
