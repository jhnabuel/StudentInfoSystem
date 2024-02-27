import csv
from csv import DictReader, DictWriter
import os.path
import sys


filename_studentCSV = "university_records.csv"
filename_courseCSV = "course_records.csv"
student_field_csv = ['IDNumber', 'Name', 'Year Level', 'Gender', 'Course Code']
course_field_csv = ['Course Code', 'Course Name']
class StudentInfoCSV:
    def __init__(self):
        self.studentID = {}

    def createstudent(self, student_id, name, yearlevel, gender, coursecode):
        self.studentID = {'IDNumber': student_id, 'Name': name, 'Year Level': yearlevel, 'Gender': gender, 'Course Code': coursecode}
        self.studentID[student_id] = self.studentID

    def createcsvfile(self,):
        with open(filename_studentCSV, 'w', newline='') as csvfile:
            csvwriter = DictWriter(csvfile, fieldnames=student_field_csv)
            csvwriter.writeheader()
            print("CSV File created")

    def addstudent(self):
        with open(filename_studentCSV, 'a+', newline='') as csvfile:
            infowriter = DictWriter(csvfile, fieldnames=student_field_csv, extrasaction='ignore')
            infowriter.writerow(self.studentID)

    def deletestudent(self, key, value):
        # Step 1: Read CSV file into a list of dictionaries
        rows = []
        with open(filename_studentCSV, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile, fieldnames=student_field_csv)
            for row in reader:
                rows.append(row)
        # Step 2: Identify the row to delete
        index_to_delete = None
        for i, row in enumerate(rows):
            if row[key] == value:
                index_to_delete = i
                break
        # Step 3: Remove the corresponding dictionary
        if index_to_delete is not None:
            del rows[index_to_delete]
            # Step 4: Write the updated list of dictionaries back to the CSV file
            with open(filename_studentCSV, 'w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=student_field_csv)
                writer.writerows(rows)
            print(f"Row with {key}={value} deleted successfully.")
        else:
            print(f"No row with {key}={value} found.")

    def editstudentinfo(self, key, value_to_find, new_values):
        rows = []
        with open(filename_studentCSV, 'r', newline='') as csvfile:
            info = csv.DictReader(filename_studentCSV, fieldnames=student_field_csv)
            for row in info:
                rows.append(row)

        index_to_edit = None
        for i, row in enumerate(rows):
            if row[key] == value_to_find:
                    index_to_edit = i
                    break

        if index_to_edit is not None:
            rows[index_to_edit].update(new_values)

            with open(filename_studentCSV, 'w', newline='') as csvfile:
                studenteditor = csv.DictWriter(csvfile, fieldnames=student_field_csv)
                studenteditor.writerows(rows)


class CourseInfoCSV:

    def __init__(self):
        self.course = {}

    def createcoursecsv(self):
        with open(filename_courseCSV, 'w', newline='') as courseCSV:
            csvwriter = DictWriter(courseCSV, fieldnames=course_field_csv)
            csvwriter.writeheader()
            print("CSV File created")

    def createcourse(self, courseCode, courseName):
        self.course = {'Course Code': courseCode, 'Course Name': courseName}
        self.course[courseCode] = self.course
    def addcourse(self):
        with open(filename_courseCSV, 'a+', newline='') as courseCSV:
            courselister = DictWriter(courseCSV, fieldnames=course_field_csv, extrasaction='ignore')
            courselister.writerow(self.course)

    def deletecourse(self, key, value):
        # Step 1: Read CSV file into a list of dictionaries
        rows = []
        with open(filename_courseCSV, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile, fieldnames=course_field_csv)
            for row in reader:
                rows.append(row)
        # Step 2: Identify the row to delete
        index_to_delete = None
        for i, row in enumerate(rows):
            if row[key] == value:
                index_to_delete = i
                break
        # Step 3: Remove the corresponding dictionary
        if index_to_delete is not None:
            del rows[index_to_delete]
            # Step 4: Write the updated list of dictionaries back to the CSV file
            with open(filename_courseCSV, 'w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=course_field_csv)
                writer.writerows(rows)
            print(f"Row with {key}={value} deleted successfully.")
        else:
            print(f"No row with {key}={value} found.")


def main():
    student_info = StudentInfoCSV()
    course_info = CourseInfoCSV()
    while True:
        print('\nStudent Information System')
        print("1. Create Student CSV File")
        print("2. Add student")
        print("3. Delete student information")
        print("4. Edit student information")
        print("5. Create Course CSV File")
        print("6. Add course")
        print("7. Delete course")
        print("8. Exit")

        choice = int(input("Enter your choice: "))

        match choice:
            case 1:
                if os.path.exists(filename_studentCSV):
                    print("CSV File Already Exists")
                else:
                    student_info.createcsvfile()
                    print("CSV File Created Successfully")

            case 2:
                student_id = input('Enter the ID Number of the student: ')
                student_name = input('Enter the name of the student: ')
                student_year = input('Enter student year: ')
                student_gender = input('Enter the gender of the student: ')
                student_course = input('Enter course code: ')

                student_info.createstudent(student_id, student_name, student_year, student_gender, student_course)
                student_info.addstudent()
                print('CSV File Updated')
            case 3:
                student_id = input('Enter the ID Number of the student: ')
                student_info.deletestudent('IDNumber', student_id)
                print("Student info deleted successfully.")
            case 4:
                student_id = input('Enter student ID number to edit student info: ')
                key_header = 'IDNumber'
                findvalue = student_id
                new_studentname = input('Enter student name: ')
                new_studentyear = input('Enter student year: ')
                new_studentcourse = input('Enter new course code:')
                new_values = {'Name': new_studentname, 'Year Level': new_studentyear, 'Course Code': new_studentcourse}
                student_info.editstudentinfo(key_header, findvalue, new_values)

            case 5:
                if os.path.exists(filename_courseCSV):
                    print("CSV File Already Exists")
                else:
                    course_info.createcoursecsv()
                    print("CSV File Created Successfully")
            case 6:
                course_id = input('Enter course code: ')
                course_name = input('Enter course name: ')
                course_info.createcourse(course_id, course_name)
                course_info.addcourse()
                print("Course added successfully.")
            case 7:
                course_id = input('Enter the ID Number of the student: ')
                course_info.deletecourse( 'Course Code', course_id)
                print("Student info deleted successfully.")
            case 8:
                sys.exit()


main()
