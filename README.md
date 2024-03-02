# Simple Student Information System by John Christian Nino T. Abuel
* A project for the subject, **CCC151 - Information Management**, create using Python and PyQt5.
## Usage
  * You must have PyQT(https://pypi.org/project/PyQt5/) installed.
  * Load the both university_records.csv file and course_records.csv.
  * Make sure that StudentInfoSystem.py and GUIforSSIS.ui are in the same directory.
    
  * This application will let you open CSV files that contain student information and a list of courses.
  * You can view, add, edit, and delete the data from those CSV files.
  * **Warning:** The console version, SSIS.py, will work. However, the edit student information function does not.

  ## If the system is empty, click the Create file button. This creates two CSV files named: university_records.csv and course_records.csv
  * If the files are created, you may now start using the system.

  ## Student CSV Editor Functions
  * Add student: Enter the student ID in the ID number field, then the name, year level, and gender. Choose the course of the student from the dropbox. Make sure to complete all fields before pressing the 'Add Student' button. Choose 'Course not found' option for Course Code if course of student is not in the course list.
  * Delete student: Enter valid student ID number in the list to delete.
  * Edit student: Enter valid student ID number to edit student information.
    
  ## Course List CSV Editor Functions
  * Add course: The same thing with adding student. Fill up the fields first before clicking 'Add Course' button.
  * Delete course: Enter valid course code in the list to delete course.

