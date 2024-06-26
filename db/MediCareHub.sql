-- Create Patient table

CREATE TABLE Patient (
    Patient_ID INT PRIMARY KEY,
    Patient_Fname VARCHAR(50) NOT NULL ,
    Patient_Lname VARCHAR(50) NOT NULL,
    Phone VARCHAR(20) UNIQUE NOT NULL  ,
    Blood_Type VARCHAR(5) ,
    Email VARCHAR(100) NOT NULL unique,
    Gender VARCHAR(10) NOT NULL,
    Condition_ VARCHAR(100),
    Admisson_Date DATE ,
    Discharge_Date DATE,
    Address VARCHAR(255) NOT NULL
);

-- Create Room table
CREATE TABLE Room (
    Room_ID INT PRIMARY KEY,
    Room_Type VARCHAR(50),
    Patient_ID INT,
    Room_Cost DECIMAL(10, 2),
    FOREIGN KEY (Patient_ID) REFERENCES Patient(Patient_ID)
);

-- Create Lab table
CREATE TABLE Lab (
    Lab_ID INT PRIMARY KEY,
    Patient_ID INT,
    Lab_Techinican_ID INT,
    Doctor_ID INT,
    Test_Cost DECIMAL(10, 2),
    Date DATE,
    FOREIGN KEY (Patient_ID) REFERENCES Patient(Patient_ID),
    FOREIGN KEY (Lab_Techinican_ID) REFERENCES Staff(Emp_ID),
    FOREIGN KEY (Doctor_ID) REFERENCES Doctor(Doctor_ID)
);

-- Create Invoice table
CREATE TABLE Invoice (
    Invoice_ID INT PRIMARY KEY,
    Date DATE,
    Room_Cost DECIMAL(10, 2),
    Test_Cost DECIMAL(10, 2),
    Other_Charges DECIMAL(10, 2),
    Total DECIMAL(10, 2),
    Patient_ID INT,
    Policy_Number INT UNIQUE,
    Medicine_Cost DECIMAL(10, 2),
    FOREIGN KEY (Patient_ID) REFERENCES Patient(Patient_ID),
    FOREIGN KEY (Policy_Number) REFERENCES Insurance(Policy_Number)
);

-- Create Insurance table
CREATE TABLE Insurance (
    Policy_Number INT PRIMARY KEY,
    Patient_ID INT,
    Ins_Code VARCHAR(20) UNIQUE NOT NULL,
    End_Date DATE,
    Provider VARCHAR(100),
    Plan VARCHAR(100),
    Coop_Pay DECIMAL(5, 2),
    Coverage VARCHAR(255),
    Dental BOOLEAN,
    Optical BOOLEAN,
    FOREIGN KEY (Patient_ID) REFERENCES Patient(Patient_ID)
);

-- Create Medicine table
CREATE TABLE Medicine (
    Medicine_ID INT PRIMARY KEY,
    M_Name VARCHAR(100) UNIQUE NOT NULL,
    M_Quantity INT,
    Medicine_Cost DECIMAL(10, 2)
);

-- Create Prescription table
CREATE TABLE Prescription (
    Prescription_ID INT PRIMARY KEY,
    Patient_ID INT,
    Medicine_ID INT,
    Date TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    Dosage VARCHAR(100),
    Doctor_ID INT,
    FOREIGN KEY (Patient_ID) REFERENCES Patient(Patient_ID),
    FOREIGN KEY (Medicine_ID) REFERENCES Medicine(Medicine_ID),
    FOREIGN KEY (Doctor_ID) REFERENCES Doctor(Doctor_ID)
);

-- Create LoginPageDoctor table
CREATE TABLE LoginPageDoctor (
    User_id INT PRIMARY KEY,
    Doctor_ID INT,
    Username VARCHAR(50),
    Password VARCHAR(50),
    FOREIGN KEY (Doctor_ID) REFERENCES Doctor(Doctor_ID)
);

-- Create LoginPagePatient table
CREATE TABLE LoginPagePatient (
    User_id INT PRIMARY KEY,
    Patient_ID INT,
    Username VARCHAR(50),
    Password VARCHAR(50),
    FOREIGN KEY (Patient_ID) REFERENCES Patient(Patient_ID)
);

-- Create Medical_History table
CREATE TABLE Medical_History (
    Record_ID INT PRIMARY KEY,
    Patient_ID INT,
    Pre_Conditions VARCHAR(255),
    FOREIGN KEY (Patient_ID) REFERENCES Patient(Patient_ID)
);

-- Create Appointment table
CREATE TABLE Appointment (
    Appointment_ID INT PRIMARY KEY,
    Scheduled_On DATE,
    Date DATE,
    Time TIME,
    Doctor_ID INT,
    Patient_ID INT,
    FOREIGN KEY (Doctor_ID) REFERENCES Doctor(Doctor_ID),
    FOREIGN KEY (Patient_ID) REFERENCES Patient(Patient_ID)
);

-- Create Nurse table
CREATE TABLE Nurse (
    Nurse_ID INT PRIMARY KEY,
    Dept_ID INT,
    Patient_ID INT,
    Emp_ID INT,
    FOREIGN KEY (Dept_ID) REFERENCES Department(Dept_ID),
    FOREIGN KEY (Patient_ID) REFERENCES Patient(Patient_ID),
    FOREIGN KEY (Emp_ID) REFERENCES Staff(Emp_ID)
);

-- Create Staff table
CREATE TABLE Staff (
    Emp_ID INT PRIMARY KEY,
    Emp_FName VARCHAR(50) NOT NULL,
    Emp_LName VARCHAR(50) NOT NULL,
    Date_Joining DATE,
    Date_Separation DATE,
    Emp_Type VARCHAR(50),
    Email VARCHAR(100),
    Address VARCHAR(255),
    Dept_ID INT,
    SSN VARCHAR(20) NOT NULL,
    FOREIGN KEY (Dept_ID) REFERENCES Department(Dept_ID)
);

-- Create Doctor table
CREATE TABLE Doctor (
    Doctor_ID INT PRIMARY KEY,
    DoctorName VARCHAR(50) NOT NULL,
    DoctorSurname VARCHAR(50) NOT NULL,
    Emp_ID INT,
    Specialization VARCHAR(100),
    Dept_ID INT,
    FOREIGN KEY (Emp_ID) REFERENCES Staff(Emp_ID),
    FOREIGN KEY (Dept_ID) REFERENCES Department(Dept_ID)
);

-- Create Department table
CREATE TABLE Department (
    Dept_ID INT PRIMARY KEY,
    Dept_Head VARCHAR(100),
    Dept_Name VARCHAR(100),
    Emp_Count INT
);

-- Create WageSlip table
CREATE TABLE WageSlip (
    Account_No INT PRIMARY KEY,
    Salary DECIMAL(10, 2) NOT NULL ,
    Bonus DECIMAL(10, 2),
    Emp_ID INT,
    IBAN VARCHAR(50) check (IBAN like ('TR%')),
    FOREIGN KEY (Emp_ID) REFERENCES Staff(Emp_ID)
);


CREATE TABLE admin(
admin_id SERIAL PRIMARY KEY ,
username VARCHAR(50) NOT NULL UNIQUE,
password VARCHAR(18) NOT NULL UNIQUE
)
INSERT INTO admin(username,password)
VALUES
("can",123456),
('melisa',12345),
('alp',1234),
('yelda',123)


INSERT INTO `patient` (
  `Patient_ID`, 
  `Patient_Fname`, 
  `Patient_Lname`, 
  `Phone`, 
  `Blood_Type`, 
  `Email`, 
  `Gender`, 
  `Condition_`, 
  `Admisson_Date`, 
  `Discharge_Date`, 
  `Address`
) VALUES
(1, 'Alice', 'Johnson', '123-456-7890', 'A+', 'alice.johnson@example.com', 'Female', 'Hypertension', '2024-05-01', '2024-05-05', '123 Elm Street'),
(2, 'Bob', 'Smith', '234-567-8901', 'B-', 'bob.smith@example.com', 'Male', 'Diabetes', '2024-05-03', '2024-05-10', '456 Oak Avenue'),
(3, 'Charlie', 'Brown', '345-678-9012', 'O+', 'charlie.brown@example.com', 'Male', 'Flu', '2024-05-02', '2024-05-08', '789 Pine Road'),
(4, 'Diana', 'Evans', '456-789-0123', 'AB-', 'diana.evans@example.com', 'Female', 'Asthma', '2024-05-05', '2024-05-12', '101 Maple Street'),
(5, 'Ethan', 'Green', '567-890-1234', 'A-', 'ethan.green@example.com', 'Male', 'Fracture', '2024-05-04', '2024-05-09', '202 Birch Lane'),
(6, 'Fiona', 'Miller', '678-901-2345', 'B+', 'fiona.miller@example.com', 'Female', 'Migraine', '2024-05-06', '2024-05-11', '303 Cedar Circle'),
(7, 'George', 'Nelson', '789-012-3456', 'O-', 'george.nelson@example.com', 'Male', 'Covid-19', '2024-05-07', '2024-05-14', '404 Spruce Boulevard');

INSERT INTO `department` (
  `Dept_ID`, 
  `Dept_Head`, 
  `Dept_Name`, 
  `Emp_Count`
) VALUES
(1, 'Dr. Susan Johnson', 'Cardiology', 35),
(2, 'Dr. David Lee', 'Neurology', 28),
(3, 'Dr. Emily Harris', 'Orthopedics', 40),
(4, 'Dr. Robert Clark', 'Radiology', 22),
(5, 'Dr. Olivia Martinez', 'Pediatrics', 30),
(6, 'Dr. Andrew Brown', 'Emergency', 50),
(7, 'Dr. Jessica White', 'Oncology', 25);

INSERT INTO `staff` (
  `Emp_ID`, 
  `Emp_FName`, 
  `Emp_LName`, 
  `Date_Joining`, 
  `Date_Separation`, 
  `Emp_Type`, 
  `Email`, 
  `Address`, 
  `Dept_ID`, 
  `SSN`
) VALUES
(1, 'John', 'Doe', '2021-01-10', NULL, 'Nurse', 'john.doe@example.com', '123 Elm Street', 1, '123-45-6789'),
(2, 'Jane', 'Smith', '2020-11-05', NULL, 'Doctor', 'jane.smith@example.com', '456 Oak Avenue', 2, '987-65-4321'),
(3, 'Peter', 'Brown', '2022-02-20', NULL, 'Technician', 'peter.brown@example.com', '789 Pine Road', 3, '456-78-9012'),
(4, 'Linda', 'Green', '2019-05-15', NULL, 'Surgeon', 'linda.green@example.com', '101 Maple Street', 4, '321-54-9876'),
(5, 'Emma', 'Wilson', '2018-09-25', '2023-01-15', 'Nurse', 'emma.wilson@example.com', '202 Birch Lane', 5, '852-41-9630'),
(6, 'James', 'Taylor', '2023-03-01', NULL, 'Pharmacist', 'james.taylor@example.com', '303 Cedar Circle', 6, '159-73-0486'),
(7, 'Sophia', 'Anderson', '2021-06-14', NULL, 'Lab Technician', 'sophia.anderson@example.com', '404 Spruce Boulevard', 7, '357-19-2468');


INSERT INTO `doctor` (
  `Doctor_ID`, 
  `DoctorName`, 
  `DoctorSurname`, 
  `Emp_ID`, 
  `Specialization`, 
  `Dept_ID`
) VALUES
(1, 'Alice', 'Williams', 2, 'Neurology', 2),
(2, 'Michael', 'Johnson', 4, 'Orthopedics', 3),
(3, 'Robert', 'Davis', 5, 'Pediatrics', 5),
(4, 'Jennifer', 'Wilson', 6, 'Emergency Medicine', 6),
(5, 'David', 'Martinez', 7, 'Oncology', 7),
(6, 'Charles', 'Harris', 1, 'Cardiology', 1),
(7, 'Emma', 'Clark', 3, 'Radiology', 4);


INSERT INTO `nurse` (
  `Nurse_ID`, 
  `Dept_ID`, 
  `Patient_ID`, 
  `Emp_ID`
) VALUES
(1, 1, 1, 1),
(2, 5, 3, 2),
(3, 3, 2, 3),
(4, 4, 4, 4),
(5, 6, 6, 5),
(6, 2, 7, 6),
(7, 7, 5, 7);

INSERT INTO `wageslip` (
  `Account_No`, 
  `Salary`, 
  `Bonus`, 
  `Emp_ID`, 
  `IBAN`
) VALUES
(10001, 4500.00, 500.00, 1, 'TR123456789012345678901234'),
(10002, 3800.00, NULL, 2, 'TR987654321098765432109876'),
(10003, 5200.00, 300.00, 3, 'TR567890123456789012345678'),
(10004, 6000.00, 800.00, 4, 'TR234567890123456789012345'),
(10005, 4400.00, NULL, 5, 'TR876543210987654321098765'),
(10006, 4900.00, 200.00, 6, 'TR345678901234567890123456'),
(10007, 5500.00, 700.00, 7, 'TR456789012345678901234567');


INSERT INTO `lab` (
  `Lab_ID`, 
  `Patient_ID`, 
  `Lab_Techinican_ID`, 
  `Doctor_ID`, 
  `Test_Cost`, 
  `Date`
) VALUES
(1, 1, 3, 1, 200.00, '2024-05-01'),
(2, 2, 4, 2, 350.00, '2024-05-02'),
(3, 3, 3, 3, 150.00, '2024-05-03'),
(4, 4, 4, 4, 500.00, '2024-05-04'),
(5, 5, 3, 5, 400.00, '2024-05-05'),
(6, 6, 4, 6, 250.00, '2024-05-06'),
(7, 7, 3, 7, 300.00, '2024-05-07');


INSERT INTO `insurance` (
  `Policy_Number`, 
  `Patient_ID`, 
  `Ins_Code`, 
  `End_Date`, 
  `Provider`, 
  `Plan`, 
  `Coop_Pay`, 
  `Coverage`, 
  `Dental`, 
  `Optical`
) VALUES
(1001, 1, 'INS123456', '2025-01-15', 'HealthFirst', 'Gold Plan', 20.00, 'Full coverage for inpatient and outpatient care', 1, 1),
(1002, 2, 'INS234567', '2024-12-20', 'CarePlus', 'Silver Plan', 15.00, 'Coverage for major illnesses and conditions', 0, 1),
(1003, 3, 'INS345678', '2025-03-30', 'WellCare', 'Bronze Plan', 25.00, 'Partial coverage with co-pay for specialist visits', 0, 0),
(1004, 4, 'INS456789', '2025-06-10', 'MediShield', 'Platinum Plan', 30.00, 'Comprehensive coverage with additional dental benefits', 1, 1),
(1005, 5, 'INS567890', '2024-09-25', 'HealthyLife', 'Basic Plan', 10.00, 'Limited coverage for routine and preventive care', 0, 0);


INSERT INTO `medicine` (
  `Medicine_ID`, 
  `M_Name`, 
  `M_Quantity`, 
  `Medicine_Cost`
) VALUES
(1, 'Acetaminophen', 100, 5.99),
(2, 'Ibuprofen', 200, 8.49),
(3, 'Amoxicillin', 150, 15.50),
(4, 'Simvastatin', 120, 12.99),
(5, 'Metformin', 180, 9.75),
(6, 'Amlodipine', 90, 14.99),
(7, 'Omeprazole', 80, 10.50),
(8, 'Atorvastatin', 140, 11.20),
(9, 'Lisinopril', 110, 10.00),
(10, 'Losartan', 70, 13.50);




INSERT INTO `prescription` (
  `Prescription_ID`, 
  `Patient_ID`, 
  `Medicine_ID`, 
  `Date`, 
  `Dosage`, 
  `Doctor_ID`
) VALUES
(1, 1, 1, '2024-05-01 10:30:00', '500 mg twice a day', 1),
(2, 2, 2, '2024-05-02 14:45:00', '200 mg three times a day', 2),
(3, 3, 3, '2024-05-03 09:00:00', '250 mg twice a day', 3),
(4, 4, 4, '2024-05-04 16:15:00', '10 mg once a day', 4),
(5, 5, 5, '2024-05-05 11:00:00', '500 mg after each meal', 5),
(6, 6, 6, '2024-05-06 12:30:00', '40 mg once daily', 6),
(7, 7, 7, '2024-05-07 08:45:00', '50 mg twice a day', 7);




INSERT INTO `medical_history` (
  `Record_ID`, 
  `Patient_ID`, 
  `Pre_Conditions`
) VALUES
(1, 1, 'Hypertension, Diabetes'),
(2, 2, 'Asthma, Allergy to Penicillin'),
(3, 3, 'Heart Disease, High Cholesterol'),
(4, 4, 'Arthritis, Migraine'),
(5, 5, 'Chronic Kidney Disease, Anemia'),
(6, 6, 'Depression, Anxiety'),
(7, 7, 'COPD, Chronic Back Pain');




INSERT INTO `appointment` (
  `Appointment_ID`, 
  `Scheduled_On`, 
  `Date`, 
  `Time`, 
  `Doctor_ID`, 
  `Patient_ID`
) VALUES
(1, '2024-04-28', '2024-05-01', '10:00:00', 1, 1),
(2, '2024-04-29', '2024-05-02', '14:30:00', 2, 2),
(3, '2024-04-30', '2024-05-03', '09:00:00', 3, 3),
(4, '2024-05-01', '2024-05-04', '16:15:00', 4, 4),
(5, '2024-05-02', '2024-05-05', '11:45:00', 5, 5),
(6, '2024-05-03', '2024-05-06', '13:30:00', 6, 6),
(7, '2024-05-04', '2024-05-07', '08:15:00', 7, 7);








INSERT INTO `room` (
  `Room_ID`, 
  `Room_Type`, 
  `Patient_ID`, 
  `Room_Cost`
) VALUES
(1, 'Single', 1, 200.00),
(2, 'Double', 2, 150.00),
(3, 'ICU', 3, 500.00),
(4, 'Single', 4, 180.00),
(5, 'Suite', 5, 300.00),
(6, 'Double', 6, 160.00),
(7, 'ICU', 7, 550.00);





INSERT INTO `invoice` (
  `Invoice_ID`, 
  `Date`, 
  `Room_Cost`, 
  `Test_Cost`, 
  `Other_Charges`, 
  `Total`, 
  `Patient_ID`, 
  `Policy_Number`, 
  `Medicine_Cost`
) VALUES
(1, '2024-05-01', 200.00, 150.00, 50.00, 400.00, 1, 1001, 50.00),
(2, '2024-05-02', 180.00, 100.00, 30.00, 350.00, 2, 1002, 40.00),
(3, '2024-05-03', 500.00, 200.00, 75.00, 800.00, 3, 1003, 25.00),
(4, '2024-05-04', 300.00, 250.00, 45.00, 625.00, 4, 1004, 30.00),
(5, '2024-05-05', 160.00, 180.00, 60.00, 400.00, 5, 1005, 45.00);

SELECT * FROM PATIENT
INSERT INTO `loginpagepatient` (
  `User_id`, 
  `Patient_ID`, 
  `Username`, 
  `Password`
) VALUES
(1, 1, 'alice123', 'password123'),
(2, 2, 'bob456', 'securepassword'),
(3, 3, 'charlie789', 'mypassword'),
(4, 4, 'diana111', 'mypassword111'),
(5, 5, 'ethan222', 'password222'),
(6, 6, 'fiona333', 'pass333'),
(7, 7, 'george444', 'georgepass444');





INSERT INTO `loginpagedoctor` (
  `User_id`, 
  `Doctor_ID`, 
  `Username`, 
  `Password`
) VALUES
(1, 1, 'alice_williams', 'docpass123'),
(2, 2, 'michael_johnson', 'johnson456'),
(3, 3, 'robert_davis', 'davismed789'),
(4, 4, 'jennifer_wilson', 'wilsonmed111'),
(5, 5, 'david_martinez', 'martinez222'),
(6, 6, 'charles_harris', 'harris333'),
(7, 7, 'emma_clark', 'clarkdoc444');


CREATE VIEW Patient_Appointments AS
SELECT
    Patient.Patient_ID,
    Patient.Patient_Fname,
    Patient.Patient_Lname,
    Appointment.Appointment_ID,
    Appointment.Date AS Appointment_Date,
    Appointment.Time AS Appointment_Time,
    Doctor.DoctorName,
    Doctor.DoctorSurname
FROM
    Patient
JOIN Appointment ON Patient.Patient_ID = Appointment.Patient_ID
JOIN Doctor ON Appointment.Doctor_ID = Doctor.Doctor_ID;


CREATE VIEW Doctor_Lab_Tests AS
SELECT
    Doctor.Doctor_ID,
    Doctor.DoctorName,
    Doctor.DoctorSurname,
    Lab.Lab_ID,
    Lab.Patient_ID,
    Lab.Test_Cost,
    Lab.Date
FROM
    Doctor
JOIN Lab ON Doctor.Doctor_ID = Lab.Doctor_ID;

CREATE VIEW Billing_Summary AS
SELECT
    Patient.Patient_ID,
    Patient.Patient_Fname,
    Patient.Patient_Lname,
    SUM(Invoice.Room_Cost + Invoice.Test_Cost + Invoice.Other_Charges + Invoice.Medicine_Cost) AS Total_Amount
FROM
    Patient
JOIN Invoice ON Patient.Patient_ID = Invoice.Patient_ID
GROUP BY Patient.Patient_ID, Patient.Patient_Fname, Patient.Patient_Lname;



SELECT * FROM Billing_Summary
SELECT * FROM Doctor_Lab_Tests
SELECT * FROM Patient_Appointments


DELIMITER //

CREATE TRIGGER track_room_changes
AFTER UPDATE ON Room
FOR EACH ROW
BEGIN
    INSERT INTO room_changes (room_id, operation, patient_id_before, patient_id_after)
    VALUES (OLD.Room_ID, 'Update', OLD.Patient_ID, NEW.Patient_ID);
END //

DELIMITER ;


DELIMITER //

CREATE TRIGGER audit_patient_changes
AFTER UPDATE ON Patient
FOR EACH ROW
BEGIN
    INSERT INTO audit_patient (patient_id, operation, details)
    VALUES (
        OLD.Patient_ID,
        'Update',
        CONCAT(
            'From: ', OLD.Patient_Fname, ' ', OLD.Patient_Lname,
            ', To: ', NEW.Patient_Fname, ' ', NEW.Patient_Lname,
            ', Phone: ', OLD.Phone, ' -> ', NEW.Phone
        )
    );
END //

DELIMITER ;



DELIMITER //

CREATE TRIGGER update_billing_summary
AFTER INSERT ON Invoice
FOR EACH ROW
BEGIN
    UPDATE Billing_Summary
    SET Total_Amount = (
        SELECT SUM(Room_Cost + Test_Cost + Other_Charges + Medicine_Cost)
        FROM Invoice
        WHERE Patient_ID = NEW.Patient_ID
    )
    WHERE Patient_ID = NEW.Patient_ID;
END //

DELIMITER ;

SELECT * FROM admin
SELECT * FROM patient
SELECT * FROM loginpagepatient
SELECT * FROM loginpagedoctor
SELECT * FROM medical_history
select * from doctor
select * from appointment
select * from medical_history
select * from prescription
select * from insurance;

DROP TRIGGER IF EXISTS audit_patient_changes;


OPTIMIZE TABLE Prescription;invoice
ALTER TABLE `invoice` ADD COLUMN `Status` VARCHAR(10) DEFAULT 'Unpaid';


