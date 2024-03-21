import sys
import csv
from csv import DictWriter, DictReader
import os.path
import os
from functools import partial

from PyQt5 import uic, QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QFileDialog, QTableWidgetItem, QTableWidget, QComboBox, QLineEdit, QGroupBox, \
    QDialog, QInputDialog, QLabel, QVBoxLayout, QPushButton, QFormLayout, QHeaderView
from PyQt5.uic import loadUiType

# GLOBAL VARIABLES
filename_studentCSV = "university_records.csv"
filename_courseCSV = "course_records.csv"
student_field_csv = ['IDNumber', 'Name', 'Year Level', 'Gender', 'Course Code', 'Enrollment Status']
course_field_csv = ['Course Code', 'Course Name']
MainForm, _ = loadUiType("GUIforSSIS.ui")

class CourseCodeEditor(QDialog, MainForm):
    def __init__(self, parent, courseCode):
        super().__init__(parent)

        self.setWindowTitle("Course Editor")

        self.setGeometry(100, 100, 300, 100)

        self.courseCodetoEdit = courseCode

        self.code_label = QLabel('New Course Code:')
        self.code_edit = QLineEdit()

        self.course_name_label = QLabel('New Course Name:')
        self.course_name_edit = QLineEdit()

        self.update_button = QPushButton('Update Info', self)
        self.update_button.clicked.connect(self.update_course)

        self.cancel_button = QPushButton('Cancel', self)
        self.cancel_button.clicked.connect(self.cancel)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.code_label)
        self.layout.addWidget(self.code_edit)
        self.layout.addWidget(self.course_name_label)
        self.layout.addWidget(self.course_name_edit)
        self.layout.addWidget(self.update_button)
        self.layout.addWidget(self.cancel_button)
        self.setLayout(self.layout)
        
    def update_course(self):
        try:
            new_code = self.code_edit.text()
            new_course_name = self.course_name_edit.text()

            updated_values = {'Course Code': new_code, 'Course Name': new_course_name}
            # Read the CSV file and load its contents into a list of dictionaries
            rows = []
            with open(filename_courseCSV, 'r', newline='') as csvfile:
                coursecsv = csv.DictReader(csvfile)
                for row in coursecsv:
                    rows.append(row)
            # Find the specific row you want to edit based on the IDNumber
            for row in rows:
                if row['Course Code'] == self.courseCodetoEdit:
                    # Modify the values in the dictionary for the desired fields
                    row.update(updated_values)
                    break  # Break the loop once the row is found and updated
            # Write the updated data back to the CSV file
            with open(filename_courseCSV, 'w', newline='') as csvfile:
                coursecsv_update = csv.DictWriter(csvfile, fieldnames=course_field_csv, extrasaction='ignore')
                # Write the Headers
                coursecsv_update.writeheader()
                # Write the updated rows
                coursecsv_update.writerows(rows)
            update_success = QMessageBox()
            update_success.setWindowTitle('Success!')
            update_success.setText('Course information updated successfully!')
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
        





class StudentInformationEditor(QDialog, MainForm):
    def __init__(self, parent, studentIDnum):
        super().__init__(parent)

        self.setWindowTitle("Student Information Editor")
        self.setGeometry(100, 100, 300, 100)

        edit_gender = ['Male', 'Female', 'Nonbinary', 'Decline to state']
        edit_year_level = ['1','2','3','4']

        self.studentID = studentIDnum

        self.name_label = QLabel('New Name:')
        self.name_edit = QLineEdit()

        self.year_label = QLabel('New Year Level:')
        self.year_combo = QComboBox()

        self.gender_label = QLabel('New Gender:')
        self.gender_combo = QComboBox()

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

        self.year_combo.addItems(edit_year_level)
        self.gender_combo.addItems(edit_gender)
        
        self.update_button = QPushButton('Update Info', self)
        self.update_button.clicked.connect(self.update_student)
        self.cancel_button = QPushButton('Cancel', self)
        self.cancel_button.clicked.connect(self.cancel)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.name_label)
        self.layout.addWidget(self.name_edit)
        self.layout.addWidget(self.year_label)
        self.layout.addWidget(self.year_combo)
        self.layout.addWidget(self.gender_label)
        self.layout.addWidget(self.gender_combo)
        self.layout.addWidget(self.course_label)
        self.layout.addWidget(self.course_combo)
        self.layout.addWidget(self.update_button)
        self.layout.addWidget(self.cancel_button)
        self.setLayout(self.layout)

    def update_student(self):
        try:
            student_id = self.studentID
            new_name = self.name_edit.text()
            new_yearlevel = self.year_combo.currentText()
            new_gender = self.gender_combo.currentText()
            new_course = self.course_combo.currentText()
             # Determine enrollment status based on the edited course
            if new_course == "Course not available":
                new_status = "Not enrolled"
            else:
                new_status = "Enrolled"
            updated_values = {'IDNumber': student_id, 'Name': new_name, 'Year Level': new_yearlevel, 'Gender': new_gender, 'Course Code': new_course, 'Enrollment Status': new_status}
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
        gender = ['Male', 'Female', 'Nonbinary', 'Decline to state']
        year_level = ['1','2','3','4']
        self.yearLevelPicker.addItems(year_level)
        self.genderPicker.addItems(gender)
        self.searchFilter.addItems(["IDNumber", "Name", "Year Level", "Course Code"])

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
        # Editing a course info
        self.editCourse.clicked.connect(self.editcourse)
        # Searching for a student
        self.searchStudent.textChanged.connect(self.filter_student_table)
        # Searching for a course
        self.searchCourse.textChanged.connect(self.filter_course_table)

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

    def loadstudentCSV(self, filename, tableWidget, search_text=None):
        filepath = f"{filename}"
        if filepath:
            tableWidget.clearContents() 
            tableWidget.setRowCount(0)
            tableWidget.setColumnCount(0)
            # Read CSV file and populate QTableWidget
            with open(filepath, 'r') as file:
                reader = csv.reader(file)
                data = list(reader)
            if data:
                # Set column headers using the first row of the CSV file
                header = tableWidget.horizontalHeader()
                header.setStyleSheet("QHeaderView::section { background-color: #101010; color: white; }")

                headers = data[0]

                tableWidget.setColumnCount(len(headers))
                tableWidget.setHorizontalHeaderLabels(headers)
              

                # Hide vertical header (row numbers)
                tableWidget.verticalHeader().setVisible(False)

                # Populate the table with data excluding the header row
                for row in range(1, len(data)):
                    tableWidget.insertRow(row - 1)
                    for column in range(len(headers)):
                        if column == len(headers) - 1:  # Check if it's the last column
                            # Determine enrollment status based on course availability
                            course_code = data[row][4]  # Assuming "Course Code" is at index 4
                            if course_code == "Course not found":
                                item = QTableWidgetItem("Not enrolled")
                            else:
                                item = QTableWidgetItem("Enrolled")
                        else:
                            item = QTableWidgetItem(data[row][column])
                        tableWidget.setItem(row - 1, column, item)

                # Sets the column widths for the ID Number, Name, Year Level, Gender, and Course Code fields.
                tableWidget.setColumnWidth(0, 70)
                tableWidget.setColumnWidth(1, 184)
                tableWidget.setColumnWidth(2, 70)
                tableWidget.setColumnWidth(3, 75)
                tableWidget.setColumnWidth(4, 80)
                tableWidget.setColumnWidth(5, 120)

                # Filter rows based on search_text
                if search_text:
                    search_text = search_text.lower() # Convert search_text to lowercase for case-sensitive comparison
                    search_category = self.searchFilter.currentText()
                    column_index = -1 

                    if search_category == "IDNumber":
                        column_index = 0
                    elif search_category == "Name":
                        column_index = 1
                    elif search_category == "Year Level":
                        column_index = 2
                    elif search_category == "Course Code":
                        column_index = 4

                    if column_index != -1:  
                        for row in range(tableWidget.rowCount()):
                                row_hidden = True
                                item = tableWidget.item(row, column_index)
                                if item and search_text in item.text().lower():  # Compare case sensitively
                                        row_hidden = False
                                tableWidget.setRowHidden(row, row_hidden)
                    else: 
                        # If search_text is empty, show all rows
                        for row in range(tableWidget.rowCount()):
                            tableWidget.setRowHidden(row, False)

    def loadcourseCSV(self, filename, tableWidget, search_text=None):
        filepath = f"{filename}"
        if filepath:
            tableWidget.clearContents() 
            tableWidget.setRowCount(0)
            tableWidget.setColumnCount(0)
            # Read CSV file and populate QTableWidget
            with open(filepath, 'r') as file:
                reader = csv.reader(file)
                data = list(reader)
            if data:
                # Set column headers using the first row of the CSV file
                headers = data[0]
                header = tableWidget.horizontalHeader()
                header.setStyleSheet("QHeaderView::section { background-color: #101010; color: white; }")
                tableWidget.setColumnCount(len(headers))
                tableWidget.setHorizontalHeaderLabels(headers)
                
                # Hide vertical header (row numbers)
                tableWidget.verticalHeader().setVisible(False)

                # Populate the table with data excluding the header row
                for row in range(1, len(data)):
                    tableWidget.insertRow(row - 2)
                    for column in range(len(headers)):
                        item = QTableWidgetItem(data[row][column])
                        tableWidget.setItem(row - 2, column, item)

                # Sets the width for the Course Code and Course Name columns
                tableWidget.setColumnWidth(0, 90)
                tableWidget.setColumnWidth(1, 190)

                # Determine which courses to hide based on search_text
                if search_text:
                    search_text = search_text.lower()
                    for row in range(tableWidget.rowCount()):
                        row_hidden = True
                        for column in range(tableWidget.columnCount()):
                            # Check whether current column is Course Code or Course Name
                            if column == 0 or column == 1:
                                item = tableWidget.item(row, column)
                                if item and search_text in item.text().lower():
                                    row_hidden = False
                                    break
                        tableWidget.setRowHidden(row, row_hidden)
                else:
                # If search_text is empty, show all rows
                    for row in range(tableWidget.rowCount()):
                        tableWidget.setRowHidden(row, False)


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
                for col_num, key in enumerate(['IDNumber', 'Name', 'Year Level', 'Gender', 'Course Code', 'Enrollment Status']):
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
        # Check whether name field is empty or not
        if self.nameInput.text() != "":
            name_input = self.nameInput.text()
        else:
            empty_name = QMessageBox()
            empty_name.setWindowTitle('Create Student')
            empty_name.setText('Name field must not be empty')
            empty_name.setIcon(QMessageBox.Critical)
            empty_name.setStandardButtons(QMessageBox.Close)
            empty_name.exec_()
            return

        id_input_year = self.idNumberInput.text()
        id_input_number = self.idNumberInput_2.text()

        if id_input_year.isdigit() and id_input_number.isdigit() and len(id_input_year) == 4 and len(id_input_number) == 4:
            id_input = "-".join([id_input_year, id_input_number])
        else:
            invalid_id = QMessageBox()
            invalid_id.setWindowTitle('Create Student')
            invalid_id.setText('Please enter valid student ID number')
            invalid_id.setIcon(QMessageBox.Critical)
            invalid_id.setStandardButtons(QMessageBox.Close)
            invalid_id.exec_()
            return
        
            # Check if the entered ID number already exist
        if self.is_valid_student_id(id_input) == True:
            id_exists = QMessageBox()
            id_exists.setWindowTitle('Create Student')
            id_exists.setText('ID number already exists. Please enter a different ID number.')
            id_exists.setIcon(QMessageBox.Critical)
            id_exists.setStandardButtons(QMessageBox.Close)
            id_exists.exec_()
            return  # Exit the function if ID number already exists

        year_input = self.yearLevelPicker.currentText()
        gender_input = self.genderPicker.currentText()
        course_input = self.coursepickerbox.currentText()

         # Determine enrollment status based on course availability
        if course_input == "Course not available":
            enrollment_status = "Not enrolled"
        else:
            enrollment_status = "Enrolled"

        # Add values to the CSV file
        with open(filename_studentCSV, mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames= student_field_csv, extrasaction='ignore')
            writer.writerow({'IDNumber': id_input, 'Name': name_input, 'Year Level': year_input, 
                             'Gender': gender_input, 'Course Code': course_input, 'Enrollment Status': enrollment_status})
        # Call the function to update the table whenever the button is clicked
        self.updatestudenttable()

    def addcourse(self):
        # Get input from text fields
        course_code_input = self.courseCodeInput.text().strip()
        course_name_input = self.courseNameInput.text().strip()
          
        # Check if both course code and course name are not empty
        if not course_code_input:
            empty_code = QMessageBox()
            empty_code.setWindowTitle('Add Course')
            empty_code.setText('Course Code must not be empty')
            empty_code.setIcon(QMessageBox.Critical)
            empty_code.setStandardButtons(QMessageBox.Close)
            empty_code.exec_()
            return  # Exit the function if course code is empty

        if not course_name_input:
            empty_name = QMessageBox()
            empty_name.setWindowTitle('Add Course')
            empty_name.setText('Course Name must not be empty')
            empty_name.setIcon(QMessageBox.Critical)
            empty_name.setStandardButtons(QMessageBox.Close)
            empty_name.exec_()
            return  # Exit the function if course name is empty
        
        # Check if both Course Code and Course Name already exists
        if self.is_valid_course_code == True:
            course_code_exists = QMessageBox()
            course_code_exists.setWindowTitle('Add Course')
            course_code_exists.setText('Course code already exists. Please enter a different course code.')
            course_code_exists.setIcon(QMessageBox.Critical)
            course_code_exists.setStandardButtons(QMessageBox.Close)
            course_code_exists.exec_()
            return  # Exit the function if ID number already exists
        
            # Check if the entered course name already exists
        with open(filename_courseCSV, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['Course Name'] == course_name_input:
                    name_exists = QMessageBox()
                    name_exists.setWindowTitle('Add Course')
                    name_exists.setText('Course name already exists. Please enter a different course name.')
                    name_exists.setIcon(QMessageBox.Critical)
                    name_exists.setStandardButtons(QMessageBox.Close)
                    name_exists.exec_()
                    return  # Exit the function if course name already exists


        # Add values to the CSV file
        with open(filename_courseCSV, mode='a', newline='') as file:
            append = csv.DictWriter(file, fieldnames= course_field_csv, extrasaction='ignore')
            append.writerow({'Course Code': course_code_input, 'Course Name': course_name_input})
        # Call the function to update the table whenever the button is clicked
        self.updatecoursetable()
        self.coursepickerbox.clear()
        self.loadcoursecode()



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
                # Check if any students are enrolled in the deleted course
            students_to_update = []
            with open(filename_studentCSV, 'r', newline='') as csvfile:
                student_reader = csv.DictReader(csvfile)
                for student in student_reader:
                    if student['Course Code'] == course_codevalue:
                        students_to_update.append(student)
    
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
            # Update the course and enrollment status for affected students
            for student in students_to_update:
                student['Course Code'] = 'Course not found'
                student['Enrollment Status'] = 'Not enrolled'

            updated_students = []
            with open(filename_studentCSV, 'r', newline='') as csvfile:
                student_reader = csv.DictReader(csvfile)
                for student in student_reader:
                    if student['Course Code'] == course_codevalue:
                        student['Course Code'] = 'Course not found'
                        student['Enrollment Status'] = 'Not enrolled'
                    updated_students.append(student)

            # Rewrite the updated list of dictionaries back to the student CSV file
            with open(filename_studentCSV, 'w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=student_field_csv)
                writer.writeheader()
                writer.writerows(updated_students)

        else:
            # Popup notification if course code does not exist in the CSV file.
            course_not_exist = QMessageBox()
            course_not_exist.setWindowTitle('Delete Course')
            course_not_exist.setText('Please enter a valid course code to delete.')
            course_not_exist.setIcon(QMessageBox.Critical)
            course_not_exist.setStandardButtons(QMessageBox.Close)
            course_not_exist.exec_()

        self.updatecoursetable()
        self.updatestudenttable()
        self.coursepickerbox.clear()
        self.loadcoursecode()


    def editstudent(self):
       # Code for the QInputDialog for the ID Number input
        key = 'IDNumber'
        enteridnum = QInputDialog()
        studentID_edit, ok = enteridnum.getText(self, "Edit Student", "Enter student ID number to edit info: ")
        studentID = str(studentID_edit)

        if ok and studentID_edit:
            if self.is_valid_student_id(studentID):
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
                not_updated.setText('Invalid student ID Number!')
                not_updated.setIcon(QMessageBox.Warning)
                not_updated.setStandardButtons(QMessageBox.Close)
                not_updated.exec_()
        else:
            not_updated = QMessageBox()
            not_updated.setWindowTitle('Update Student Info')
            not_updated.setText('Student ID Number does not exist!')
            not_updated.setIcon(QMessageBox.Warning)
            not_updated.setStandardButtons(QMessageBox.Close)
            not_updated.exec_()
    
    def editcourse(self):
         # Code for the QInputDialog for the ID Number input
        key = 'Course Code'
        enter_course_code = QInputDialog()
        course_edit, ok = enter_course_code.getText(self, "Edit Course Info", "Enter course code to edit course: ")
        course_code_edit = str(course_edit)
        if ok and course_code_edit:
            if self.is_valid_course_code(course_code_edit):
                try:
                    self.update_dialog = CourseCodeEditor(self, course_code_edit)  # Pass self and studentID
                    self.update_dialog.show()
                    self.update_dialog.exec_()
                    self.updatecoursetable()
                    self.updatestudenttable()
                    # Update enrollment status for students enrolled in the edited course
                    updated_students = []
                    with open(filename_studentCSV, 'r', newline='') as csvfile:
                        student_reader = csv.DictReader(csvfile)
                        for student in student_reader:
                            if student['Course Code'] == course_code_edit:
                                student_id = student['IDNumber']  # Extract student IDNumber
                                student['Course Code'] = 'Course not available'
                                student['Enrollment Status'] = 'Not enrolled'
                                self.update_student_display(student['IDNumber'], 'Course not available', 'Not enrolled')
                            updated_students.append(student)
                # Rewrite the updated list of dictionaries back to the student CSV file
                    with open(filename_studentCSV, 'w', newline='') as csvfile:
                        writer = csv.DictWriter(csvfile, fieldnames=student_field_csv)
                        writer.writeheader()
                        writer.writerows(updated_students)
                    # Reload the course picker after editing the course.
                    self.coursepickerbox.clear()
                    self.loadcoursecode()
                except Exception as e:  # Add exception handling
                    print(f"An error occurred: {e}")
                    error_message = QMessageBox()
                    error_message.setWindowTitle('Error')
                    error_message.setText(f"An error occurred: {e}")
                    error_message.setIcon(QMessageBox.Critical)
                    error_message.exec_()
            else:
                not_updated = QMessageBox()
                not_updated.setWindowTitle('Update Course Code')
                not_updated.setText('Invalid course code!')
                not_updated.setIcon(QMessageBox.Warning)
                not_updated.setStandardButtons(QMessageBox.Close)
                not_updated.exec_()
        else:
            not_updated = QMessageBox()
            not_updated.setWindowTitle('Update Course Info')
            not_updated.setText('Course code does not exist!')
            not_updated.setIcon(QMessageBox.Warning)
            not_updated.setStandardButtons(QMessageBox.Close)
            not_updated.exec_()

    # This function is used for refreshing the student info table after editing a course.
    def update_student_display(self, student_id, course_code, enrollment_status):
        # Iterate through each row in the Student Info Display
        for row in range(self.studentInfoDisplay.rowCount()):
            # Check if the IDNumber matches the student ID
            if self.studentInfoDisplay.item(row, 0).text() == student_id:
                # Update the Course Code and Enrollment Status in the Student Info Display
                self.studentInfoDisplay.item(row, 4).setText(course_code)
                self.studentInfoDisplay.item(row, 5).setText(enrollment_status)
                break  # Stop iterating once the student is found and updated

    def is_valid_student_id(self, student_id):
        # Read student records and check if the entered student ID exists
        with open(filename_studentCSV, 'r', newline='') as csvfile:
            student_reader = csv.DictReader(csvfile)
            for student in student_reader:
                if student['IDNumber'] == student_id:
                    return True
        return False
    
    def is_valid_course_code(self, course_code):
        # Read student records and check if the entered student ID exists
        with open(filename_courseCSV, 'r', newline='') as csvfile:
            course_reader = csv.DictReader(csvfile)
            for course in course_reader:
                if course['Course Code'] == course_code:
                    return True
        return False

    def filter_student_table(self):
        search_text = self.searchStudent.text().strip().lower()
        self.loadstudentCSV(filename_studentCSV, self.studentInfoDisplay, search_text)

    def filter_course_table(self):
        search_text = self.searchCourse.text().strip().lower()
        self.loadcourseCSV(filename_courseCSV, self.courseListDisplay, search_text)
        

app = QtWidgets.QApplication(sys.argv)
window = Controller()
sys.exit(app.exec_())
