import sys
import csv
from csv import DictWriter, DictReader
import os.path
import os
from functools import partial

from PyQt5 import uic, QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QFileDialog, QTableWidgetItem, QTableWidget, QComboBox, QLineEdit, QGroupBox, \
    QDialog, QInputDialog, QLabel, QVBoxLayout, QPushButton, QFormLayout
from PyQt5.uic import loadUiType

# GLOBAL VARIABLES
filename_studentCSV = "university_records.csv"
filename_courseCSV = "course_records.csv"
student_field_csv = ['IDNumber', 'Name', 'Year Level', 'Gender', 'Course Code']
course_field_csv = ['Course Code', 'Course Name']
MainForm, _ = loadUiType("GUIforSSIS.ui")
class StudentInformationEditor(QDialog, MainForm):
    def __init__(self, parent, studentIDnum):
        super().__init__(parent)

        self.setWindowTitle("Student Information Editor")
        self.setGeometry(100, 100, 300, 100)

        self.studentID = studentIDnum

        self.name_label = QLabel('New Name:')
        self.name_edit = QLineEdit()

        self.year_label = QLabel('New Year Level:')
        self.year_edit = QLineEdit()

        self.gender_label = QLabel('New Gender:')
        self.gender_edit = QLineEdit()

        self.course_label = QLabel('Course Code:')
        self.course_combo = QComboBox()
        # Code to populate the combobox, same function used in the Controller class.
        course_list = []
        # Open CSV File and store data to a variable
        with open('course_records.csv', 'r') as file:
            courselist = csv.reader(file)
            next(courselist)
            # For loop to read the values of the Course Name column
            for row in courselist:
                course_list.append(row[0])  # Populate the list of course_code
        self.course_combo.addItems(course_list)

        self.update_button = QPushButton('Update Info', self)
        self.update_button.clicked.connect(self.update_student)
        self.cancel_button = QPushButton('Cancel', self)
        self.cancel_button.clicked.connect(self.cancel)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.name_label)
        self.layout.addWidget(self.name_edit)
        self.layout.addWidget(self.year_label)
        self.layout.addWidget(self.year_edit)
        self.layout.addWidget(self.gender_label)
        self.layout.addWidget(self.gender_edit)
        self.layout.addWidget(self.course_label)
        self.layout.addWidget(self.course_combo)
        self.layout.addWidget(self.update_button)
        self.layout.addWidget(self.cancel_button)
        self.setLayout(self.layout)
    def update_student(self):
        try:
            student_id = self.studentID
            new_name = self.name_edit.text()
            new_yearlevel = self.year_edit.text()
            new_gender = self.gender_edit.text()
            new_course = self.course_combo.currentText()
            updated_values = {'IDNumber': student_id, 'Name': new_name, 'Year Level': new_yearlevel, 'Gender': new_gender, 'Course Code': new_course}
            # Read the CSV file and load its contents into a list of dictionaries
            rows = []
            with open(filename_studentCSV, 'r', newline='') as csvfile:
                studentcsv = csv.DictReader(csvfile)
                for row in studentcsv:
                    rows.append(row)
            # Find the specific row you want to edit based on the IDNumber
            for row in rows:
                if row['IDNumber'] == student_id:
                    # Modify the values in the dictionary for the desired fields
                    row.update(updated_values)
                    break  # Break the loop once the row is found and updated
            # Write the updated data back to the CSV file
            with open(filename_studentCSV, 'w', newline='') as csvfile:
                studentcsv_update = csv.DictWriter(csvfile, fieldnames=student_field_csv, extrasaction='ignore')
                # Write the Headers
                studentcsv_update.writeheader()
                # Write the updated rows
                studentcsv_update.writerows(rows)
            update_success = QMessageBox()
            update_success.setWindowTitle('Success!')
            update_success.setText('Student information updated successfully!')
            update_success.setIcon(QMessageBox.Information)
            update_success.exec_()
            self.close()
        except Exception as e:  # Catch any exceptions
            print(f"An error occurred: {e}")
            error_message = QMessageBox()
            error_message.setWindowTitle('Error')
            error_message.setText(f"An error occurred while updating: {e}")
            error_message.setIcon(QMessageBox.Critical)
            error_message.exec_()
    def cancel(self):
        self.close()

class Controller(QtWidgets.QMainWindow, MainForm):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Student Information System')
        self.show()
        # Creating the CSV files for student and course records
        self.createCSV.clicked.connect(self.createcsvfiles)
        # Populating the Tables for the SSIS Application
        self.loadstudentCSV("university_records.csv", self.studentInfoDisplay)
        self.loadcourseCSV('course_records.csv', self.courseListDisplay)
        # Populating the ComboBox for the Course Picker
        self.coursepickerbox = self.findChild(QComboBox, 'coursePicker')
        self.loadcoursecode()
        # Opening the Dialog

        # Adding the student info
        self.addStudent.clicked.connect(self.addstudent)
        # Deleting student info
        self.deleteStudent.clicked.connect(self.deletestudent)
        # Editing student info
        self.editStudent.clicked.connect(self.editstudent)
        # Adding course
        self.addCourse.clicked.connect(self.addcourse)
        # Deleting a course from the CSV file
        self.deleteCourse.clicked.connect(self.deletecourse)



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
                    tableWidget.insertRow(row - 2)
                    for column in range(len(headers)):
                        item = QTableWidgetItem(data[row][column])
                        tableWidget.setItem(row - 2, column, item)

                # Sets the width for the Course Code and Course Name columns
                tableWidget.setColumnWidth(0, 90)
                tableWidget.setColumnWidth(1, 190)

    def loadcoursecode(self):
        course_list = []
        # Open CSV File and store data to a variable
        with open('course_records.csv', 'r') as file:
            courserecord = csv.reader(file)
            next(courserecord)
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
            student_read = csv.DictReader(csvfile)
            for row_dict in student_read:
                row_position = self.studentInfoDisplay.rowCount()
                self.studentInfoDisplay.insertRow(row_position)
                # Appending the values into the table
                for col_num, key in enumerate(['IDNumber', 'Name', 'Year Level', 'Gender', 'Course Code']):
                    item = QTableWidgetItem(str(row_dict[key]))
                    self.studentInfoDisplay.setItem(row_position, col_num, item)
    def updatecoursetable(self):
        # Clear the existing data in the table
        self.courseListDisplay.clearContents()
        self.courseListDisplay.setRowCount(0)
        # Read data from the CSV file. Will work for either the student or course CSV file.
        with open(filename_courseCSV, mode='r') as csvfile:
            course_read = csv.DictReader(csvfile)
            for row_dict in course_read:
                if course_read.line_num == 2:
                    continue

                row_position = self.courseListDisplay.rowCount()
                self.courseListDisplay.insertRow(row_position)
                # Appending the values into the table
                for col_num, key in enumerate(['Course Code', 'Course Name']):
                    item = QTableWidgetItem(str(row_dict[key]))
                    self.courseListDisplay.setItem(row_position, col_num, item)

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
        # Call the function to update the table whenever the button is clicked
        self.updatestudenttable()
    def addcourse(self):
        # Get input from text fields
        course_code_input = self.courseCodeInput.text()
        course_name_input = self.courseNameInput.text()
        # Add values to the CSV file
        with open(filename_courseCSV, mode='a', newline='') as file:
            append = csv.DictWriter(file, fieldnames= course_field_csv, extrasaction='ignore')
            append.writerow({'Course Code': course_code_input, 'Course Name': course_name_input})
        # Call the function to update the table whenever the button is clicked
        self.updatecoursetable()


    def deletestudent(self):
        key = 'IDNumber'
        deleteDialog = QInputDialog()
        id_value, okPressed = deleteDialog.getText(self, "Delete Student Information", "Enter student ID number: ")
        if okPressed and id_value != '':
            rows = []
            with open(filename_studentCSV, 'r', newline='') as csvfile:
                reader = csv.DictReader(csvfile, fieldnames=student_field_csv)
                for row in reader:
                    rows.append(row)
            # Identify the row to delete
            index_to_delete = None
            for i, row in enumerate(rows):
                if row[key] == id_value:
                    index_to_delete = i
                    break
            # Remove the corresponding dictionary
            if index_to_delete is not None:
                del rows[index_to_delete]
                student_del = QMessageBox()
                student_del.setWindowTitle('Delete Student Info')
                student_del.setText('Student with ID Number: ' + id_value + ' has been deleted.')
                student_del.setIcon(QMessageBox.Information)
                student_del.exec_()
            else:
                student_not_exist = QMessageBox()
                student_not_exist.setWindowTitle('Delete Student Info')
                student_not_exist.setText('Student with ID Number: ' + id_value + ' does not exist!')
                student_not_exist.setIcon(QMessageBox.Critical)
                student_not_exist.setStandardButtons(QMessageBox.Close)
                student_not_exist.exec_()
            #  Write the updated list of dictionaries back to the CSV file
            with open(filename_studentCSV, 'w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=student_field_csv)
                writer.writerows(rows)
                # Popup notification if student info is deleted
        else:
            # Popup notification if the user presses ok without inputing ID number.
            student_not_exist = QMessageBox()
            student_not_exist.setWindowTitle('Student Delete')
            student_not_exist.setText('Please enter student ID number.')
            student_not_exist.setIcon(QMessageBox.Critical)
            student_not_exist.setStandardButtons(QMessageBox.Close)
            student_not_exist.exec_()

        self.updatestudenttable()

    def deletecourse(self):
        key_identifier = 'Course Code'
        deletecourseDialog = QInputDialog()
        course_codevalue, okPressed = deletecourseDialog.getText(self, "Delete Course", "Enter course code: ")
        if okPressed and course_codevalue != '':
            rows = []
            with open(filename_courseCSV, 'r', newline='') as csvfile:
                coursereader = csv.DictReader(csvfile, fieldnames=course_field_csv)
                for row in coursereader:
                    rows.append(row)
            # Identify the row to delete
            index_to_delete = None
            for i, row in enumerate(rows):
                if row[key_identifier] == course_codevalue:
                    index_to_delete = i
                    break
            # Remove the corresponding dictionary
            if index_to_delete is not None:
                del rows[index_to_delete]
                course_del = QMessageBox()
                course_del.setWindowTitle('Course Delete')
                course_del.setText('Course with code: ' + course_codevalue + ' has been deleted.')
                course_del.setIcon(QMessageBox.Information)
                course_del.exec_()
            else:
                course_not_found = QMessageBox()
                course_not_found.setWindowTitle('Course Delete')
                course_not_found.setText('Course with code: ' + course_codevalue + ' does not exist!')
                course_not_found.setIcon(QMessageBox.Critical)
                course_not_found.exec_()
            #  Write the updated list of dictionaries back to the CSV file
            with open(filename_courseCSV, 'w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=course_field_csv)
                writer.writerows(rows)
        else:
            # Popup notification if course code does not exist in the CSV file.
            course_not_exist = QMessageBox()
            course_not_exist.setWindowTitle('Delete Course')
            course_not_exist.setText('Please enter a valid course code to delete.')
            course_not_exist.setIcon(QMessageBox.Critical)
            course_not_exist.setStandardButtons(QMessageBox.Close)
            course_not_exist.exec_()

        self.updatecoursetable()

    def editstudent(self):
       # Code for the QInputDialog for the ID Number input
        key = 'IDNumber'
        enteridnum = QInputDialog()
        studentID_edit, ok = enteridnum.getText(self, "Edit Student", "Enter student ID number to edit info: ")
        studentID = str(studentID_edit)

        if ok and studentID_edit:
            try:
                self.update_dialog = StudentInformationEditor(self, studentID)  # Pass self and studentID
                self.update_dialog.show()
                self.update_dialog.exec_()
                self.updatestudenttable()
            except Exception as e:  # Add exception handling
                print(f"An error occurred: {e}")
                error_message = QMessageBox()
                error_message.setWindowTitle('Error')
                error_message.setText(f"An error occurred: {e}")
                error_message.setIcon(QMessageBox.Critical)
                error_message.exec_()
        else:
            not_updated = QMessageBox()
            not_updated.setWindowTitle('Update Student Info')
            not_updated.setText('Student ID Number does not exist!')
            not_updated.setIcon(QMessageBox.Warning)
            not_updated.setStandardButtons(QMessageBox.Close)
            not_updated.exec_()


app = QtWidgets.QApplication(sys.argv)
window = Controller()
sys.exit(app.exec_())
