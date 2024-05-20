

# MediCareHubV2

MediCareHubV2 is a comprehensive hospital management system designed to streamline administrative and clinical operations. The system includes modules for managing patient records, lab results, invoices, staff details, and wage slips, all integrated with a MySQL database and a user-friendly interface built with customtkinter.

## Features

1. **Patient Management**
   - Add, edit, and delete patient records.
   - View detailed patient information.

2. **Lab Management**
   - Display and manage lab test results.
   - Generate random blood test results.

3. **Invoice Management**
   - Create and manage invoices.
   - Process payments through a dedicated payment button.

4. **Staff Management**
   - Manage staff records with functionalities to add, edit, and delete details.
   - View detailed staff information.

5. **Wage Slip Management**
   - Create and manage wage slips for staff.
   - Edit, add, and delete wage details.

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/dcangundogan/MediCareHubV2.git
   cd MediCareHubV2


2. **Install the required packages:**

   Ensure you have Python installed. Then, install the necessary Python packages using pip:

   ```bash
   pip install customtkinter mysql-connector-python
   ```

3. **Set up the MySQL database:**

   - Install MySQL and create a database.
   - Import the provided SQL file to set up the necessary tables.

   ```bash
   mysql -u yourusername -p yourpassword < db/hospital_management_system.sql
   ```

4. **Configure database connection:**

   Update the database connection details in your Python scripts:

   ```python
   db_config = {
       'user': 'yourusername',
       'password': 'yourpassword',
       'host': 'localhost',
       'database': 'hospital_management_system'
   }
   ```

## Usage

Run the main script to start the application:

```bash
python src/main.py
```

## File Structure

- `src/main.py` - The main entry point of the application.
- `src/lab_page.py` - Handles the lab test results display.
- `src/invoice_page.py` - Manages the invoice details and payment processing.
- `src/staff_management.py` - Manages staff details.
- `src/wage_management.py` - Handles the wage slip management.
- `db/hospital_management_system.sql` - SQL script to set up the database.
- `images/` - Contains images used in the application.
- `README.md` - This readme file.

## Contributing

Contributions are welcome! Please fork this repository and submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any questions or feedback, please contact:

- **Name:** Duygu Can Gündoğan
- **Community:** Bilim ve Teknoloji
```

Feel free to customize this `README.md` further to better fit your project's specifics and needs.
