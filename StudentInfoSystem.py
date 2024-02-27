import sys
import csv
from csv import DictWriter, DictReader
import os.path
import pandas as pd
import os
from PyQt5 import uic, QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QFileDialog, QTableWidgetItem, QTableWidget

filename_studentCSV = "university_records.csv"
filename_courseCSV = "course_records.csv"
student_field_csv = ['IDNumber', 'Name', 'Year Level', 'Gender', 'Course Code']
course_field_csv = ['Course Code', 'Course Name']


class Controller(QtWidgets.QMainWindow):
    def __init__(self):
        super(Controller, self).__init__()
        uic.loadUi('GUIforSSIS.ui', self)
        self.show()
        self.createCSV.clicked.connect(lambda:self.createcsvfiles())
        self.studentTableWidget = self.findChild(QTableWidget, 'studentInfoDisplay')
        self.courseTableWidget = self.findChild(QTableWidget, 'courseListDisplay')
        self.loadstudentCSV("university_records.csv", self.studentTableWidget)
        self.loadcourseCSV('course_records.csv', self.courseTableWidget)
        self.addStudent.clicked.connect(self.pushButton_handler)


    def pushButton_handler(self):
        print('BruH')

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

    def addstudent(self):
        idnumber = self.idNumberInput.text()    # Get ID number value from user
        name = self.nameInput.text()            # Get name value fromm user
        year_level = self.yearlvlInput.text()   # Get year level value from user
        gender = self.gender

        # Add values to the Student Table Widget
        row_pos = self.studentTableWidget.rowCount()
        self.studentTableWidget.insertRow(row_pos)
        self.studentTableWidget.setItem(row_pos, 0, QTableWidgetItem(idnumber))
        self.studentTableWidget.setItem(row_pos, 1, QTableWidgetItem(name))
        self.studentTableWidget.setItem(row_pos, 2, QTableWidgetItem(year_level))
        self.studentTableWidget.setItem(row_pos, 3, QTableWidgetItem(gender))

        # Add values to the CSV file
        with open(filename_studentCSV, mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=student_field_csv)
            writer.writerows({"IDNumber": idnumber, "Name": name, "Year Level": year_level, "Gender": gender})


    def loadcoursecode(self):
        



app = QtWidgets.QApplication(sys.argv)
window = Controller()
app.exec_()
