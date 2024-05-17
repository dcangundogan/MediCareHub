import customtkinter as ctk
from tkinter import ttk, BOTH, LEFT, Y, X, END
import mysql.connector
from CTkMessagebox import CTkMessagebox
from PIL import Image

class SQLEditorPage:
    def __init__(self):
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="bercan2003",
            database="MediCareHub",
        )

        self.app = ctk.CTk()
        self.app.geometry("1400x900")
        self.app.title("Admin - SQL Editor Page")
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

        self.create_sql_editor()

    def create_sql_editor(self):
        label = ctk.CTkLabel(master=self.right_frame, text="SQL Editor", font=("Arial Bold", 24), text_color="#1C2833")
        label.pack(pady=10)

        self.query_text = ctk.CTkTextbox(master=self.right_frame, height=10, font=("Arial", 14), fg_color="#ffffff", text_color="#000000")
        self.query_text.pack(fill=X, padx=10, pady=10)

        button_frame = ctk.CTkFrame(master=self.right_frame, fg_color="#F2F3F4")
        button_frame.pack(fill=X, padx=10, pady=10)

        execute_button = ctk.CTkButton(master=button_frame, text="Execute", command=self.execute_query, fg_color="#4CAF50", hover_color="#388E3C", font=("Arial Bold", 14))
        execute_button.pack(side=LEFT, padx=10)

        clear_button = ctk.CTkButton(master=button_frame, text="Clear", command=self.clear_query, fg_color="#F44336", hover_color="#D32F2F", font=("Arial Bold", 14))
        clear_button.pack(side=LEFT, padx=10)

        back_button = ctk.CTkButton(master=button_frame, text="Back", command=self.go_back, fg_color="#607D8B", hover_color="#455A64", font=("Arial Bold", 14))
        back_button.pack(side=LEFT, padx=10)

        self.result_tree = ttk.Treeview(self.right_frame, show='headings', style="mystyle.Treeview")
        self.result_tree.pack(expand=True, fill=BOTH, padx=10, pady=10)

    def clear_right_frame(self):
        for widget in self.right_frame.winfo_children():
            widget.destroy()

    def execute_query(self):
        query = self.query_text.get("1.0", END).strip()

        if not query:
            CTkMessagebox(title="Input Error", message="Please enter a SQL query.", icon="cancel")
            return

        try:
            cursor = self.mydb.cursor(dictionary=True)
            cursor.execute(query)
            if query.lower().startswith("select"):
                rows = cursor.fetchall()
                self.display_results(rows)
            else:
                self.mydb.commit()
                CTkMessagebox(title="Success", message="Query executed successfully.", icon="check")
            cursor.close()
        except mysql.connector.Error as e:
            CTkMessagebox(title="Database Error", message=f"An error occurred: {e}", icon="cancel")

    def display_results(self, rows):
        if not rows:
            CTkMessagebox(title="No Results", message="The query did not return any results.", icon="info")
            return

        columns = list(rows[0].keys())
        self.result_tree["columns"] = columns
        for col in columns:
            self.result_tree.heading(col, text=col)
            self.result_tree.column(col, minwidth=0, width=150)

        for row in rows:
            self.result_tree.insert('', 'end', values=list(row.values()))

    def clear_query(self):
        self.query_text.delete("1.0", END)
        for item in self.result_tree.get_children():
            self.result_tree.delete(item)
        self.result_tree["columns"] = []

    def go_back(self):
        # Implement the logic to navigate back to the previous page or main menu
        pass

    def run(self):
        self.app.mainloop()


