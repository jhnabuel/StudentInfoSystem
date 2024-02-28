import sys
import csv
from csv import DictWriter, DictReader
import os.path
import os
from PyQt5 import uic, QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QFileDialog, QTableWidgetItem, QTableWidget, QComboBox, QLineEdit, QGroupBox

# GLOBAL VARIABLES
filename_studentCSV = "university_records.csv"
filename_courseCSV = "course_records.csv"
student_field_csv = ['IDNumber', 'Name', 'Year Level', 'Gender', 'Course Code']
course_field_csv = ['Course Code', 'Course Name']


class Controller(QtWidgets.QMainWindow):
    def __init__(self):
        super(Controller, self).__init__()
        self.ui = uic.loadUi('GUIforSSIS.ui', self)
        self.show()
        # Creating the CSV files for student and course records
        self.createCSV.clicked.connect(lambda:self.createcsvfiles())
        # Populating the Tables for the SSIS Application
        self.loadstudentCSV("university_records.csv", self.studentInfoDisplay)
        self.loadcourseCSV('course_records.csv', self.courseListDisplay)
        # Populating the ComboBox for the Course Picker
        self.coursepickerbox = self.findChild(QComboBox, 'coursePicker')
        self.loadcoursecode()
        # Adding the student info
        self.studentInfoEditor = self.findChild(QGroupBox, 'studentInfoEditor')
        self.addStudent.clicked.connect(lambda:self.addstudent())
        #self.deleteStudent.clicked.connect(lambda: self.pushButton_handler())


    def pushButton_handler(self):
        course = self.coursepickerbox.currentText()
        idnum = self.idNumberInput.text()
        name = self.nameInput.text()
        year = self.yearlvlInput.text()
        gender = self.genderInput.text()
        print(course, idnum, name, year, gender)




    def createcsvfiles(self) -> None:
        if os.path.exists('university_records.csv') and os.path.exists('course_records.csv'):
            dialog_exist_already = QMessageBox()
            dialog_exist_already.setText('CSV files already exist!')
            dialog_exist_already.setWindowTitle('CSV files already created')
            dialog_exist_already.setIcon(QMessageBox.Critical)
            dialog_exist_already.setStandardButtons(QMessageBox.Close)
            dialog_exist_already.exec_()
        else:
            with open(filename_studentCSV, 'w', newline='') as studentCSV:
                csvwriter_student = DictWriter(studentCSV, fieldnames=student_field_csv)
                csvwriter_student.writeheader()
            with open(filename_courseCSV, 'w', newline='') as courseCSV:
                csvwriter_course = DictWriter(courseCSV, fieldnames=course_field_csv)
                csvwriter_course.writeheader()
            dialog_exist = QMessageBox()
            dialog_exist.setWindowTitle('Files created')
            dialog_exist.setText('Student and Course CSV files created.')
            dialog_exist.setIcon(QMessageBox.Information)
            dialog_exist.exec_()

    def loadstudentCSV(self, filename, tableWidget):
        filepath = f"{filename}"
        if filepath:
            tableWidget.setRowCount(0)
            tableWidget.setColumnCount(0)
            # Read CSV file and populate QTableWidget
            with open(filepath, 'r') as file:
                reader = csv.reader(file)
                data = list(reader)
            if data:
                # Set column headers using the first row of the CSV file
                headers = data[0]
                tableWidget.setColumnCount(len(headers))
                tableWidget.setHorizontalHeaderLabels(headers)

                # Populate the table with data excluding the header row
                for row in range(1, len(data)):
                    tableWidget.insertRow(row - 1)
                    for column in range(len(headers)):
                        item = QTableWidgetItem(data[row][column])
                        tableWidget.setItem(row - 1, column, item)

                # Sets the column widths for the ID Number, Name, Year Level, Gender, and Course Code fields.
                tableWidget.setColumnWidth(0, 70)
                tableWidget.setColumnWidth(1, 180)
                tableWidget.setColumnWidth(2, 70)
                tableWidget.setColumnWidth(3, 75)
                tableWidget.setColumnWidth(4, 80)

    def loadcourseCSV(self, filename, tableWidget):
        filepath = f"{filename}"
        if filepath:
            tableWidget.setRowCount(0)
            tableWidget.setColumnCount(0)
            # Read CSV file and populate QTableWidget
            with open(filepath, 'r') as file:
                reader = csv.reader(file)
                data = list(reader)
            if data:
                # Set column headers using the first row of the CSV file
                headers = data[0]
                tableWidget.setColumnCount(len(headers))
                tableWidget.setHorizontalHeaderLabels(headers)

                # Populate the table with data excluding the header row
                for row in range(1, len(data)):
                    tableWidget.insertRow(row - 1)
                    for column in range(len(headers)):
                        item = QTableWidgetItem(data[row][column])
                        tableWidget.setItem(row - 1, column, item)

                # Sets the width for the Course Code and Course Name columns
                tableWidget.setColumnWidth(0, 90)
                tableWidget.setColumnWidth(1, 190)

    def loadcoursecode(self):
        course_list = []
        # Open CSV File and store data to a variable
        with open('course_records.csv', 'r') as file:
            courserecord = csv.reader(file)
            # For loop to read the values of the Course Name column
            for row in courserecord:
                course_list.append(row[0])  # Populate the list of course_code
        self.coursepickerbox.addItems(course_list)

    def updatestudenttable(self):
        # Clear the existing data in the table
        self.studentInfoDisplay.clearContents()
        self.studentInfoDisplay.setRowCount(0)
        # Read data from the CSV file. Will work for either the student or course CSV file.
        with open(filename_studentCSV, mode='r') as csvfile:
            csv_read = csv.DictReader(csvfile)
            for row_dict in csv_read:
                row_position = self.studentInfoDisplay.rowCount()
                self.studentInfoDisplay.insertRow(row_position)
                # Appending the values into the table
                for col_num, key in enumerate(['IDNumber', 'Name', 'Year Level', 'Gender', 'Course Code']):
                    item = QTableWidgetItem(str(row_dict[key]))
                    self.studentInfoDisplay.setItem(row_position, col_num, item)

    def addstudent(self):
        # Get input from text fields
        id_input = self.idNumberInput.text()
        name_input = self.nameInput.text()
        year_input = self.yearlvlInput.text()
        gender_input = self.genderInput.text()
        course_input = self.coursepickerbox.currentText()
        # Add values to the CSV file
        with open(filename_studentCSV, mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames= student_field_csv, extrasaction='ignore')
            writer.writerow({'IDNumber': id_input, 'Name': name_input, 'Year Level': year_input, 'Gender': gender_input, 'Course Code': course_input})
        # Call the function to update the table whenver the button is clicked
        self.updatestudenttable()





app = QtWidgets.QApplication(sys.argv)
window = Controller()
app.exec_()
