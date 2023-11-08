import sqlite3
import csv
import random

dbFilePath = "Student.db"
conn = sqlite3.connect(dbFilePath)
mycursor = conn.cursor()

# create Student database
mycursor.execute('''
CREATE TABLE IF NOT EXISTS Student (
StudentId INTEGER PRIMARY KEY,
FirstName TEXT,
LastName TEXT,
GPA REAL,
Major TEXT,
FacultyAdvisor TEXT,
Address TEXT,
City TEXT,
State TEXT,
ZipCode TEXT,
MobilePhoneNumber TEXT,
isDeleted INTEGER);
''')

advisors = ["Rene German", "Kendra Day", "Jon Humphreys", "Erik Linstead"]
state_names = ["Alaska", "Alabama", "Arkansas", "American Samoa", "Arizona", "California", "Colorado", "Connecticut", "District of Columbia", "Delaware", "Florida", "Georgia", "Guam", "Hawaii", "Iowa", "Idaho", "Illinois", "Indiana", "Kansas", "Kentucky", "Louisiana", "Massachusetts", "Maryland", "Maine", "Michigan", "Minnesota", "Missouri", "Mississippi", "Montana", "North Carolina", "North Dakota", "Nebraska", "New Hampshire", "New Jersey", "New Mexico", "Nevada", "New York", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Puerto Rico", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Virginia", "Virgin Islands", "Vermont", "Washington", "Wisconsin", "West Virginia", "Wyoming"]

# getValidState() ensures user inputs a valid state and returns the state
def getValidState():
    state = None
    isStateInvalid = True
    while isStateInvalid:
        state = input("Enter state:")
        if state in state_names:
            isStateInvalid = False
        else:
            print(state + "is not a valid state. Please use Title Case.")
    return state

# getValidGPA() ensures user inputs a valid gpa and returns the gpa
def getValidGPA():
    gpa = None
    # check if gpa entered is valid
    isGPAInvalid = True
    while isGPAInvalid:
        try:
            gpa = float(input("Enter GPA:"))
            if (gpa > 0.0) and (gpa <= 4.8):
                isGPAInvalid = False
            else:
                print(str(gpa) + " is not a valid GPA. GPA must be between 0.0 and 4.0.")
        except ValueError:
            print("Not a valid GPA. GPA must be between 0.0 and 4.0.")

    return gpa

# import_data() imports the contents of a csv file into the Student table
def import_data():
    with open('/Users/gilliancanicosa/Documents/CPSC_Courses/CPSC408/students.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            index = random.randint(0, 3)
            advisor = advisors[index]
            mycursor.execute(
                "INSERT INTO Student(FirstName, LastName, GPA, Major, FacultyAdvisor, Address, City, State, ZipCode, MobilePhoneNumber, isDeleted)"
                "VALUES (?,?,?,?,?,?,?,?,?,?,?);", (row['FirstName'], row['LastName'], row['GPA'], row['Major'],
                                                    advisor, row['Address'], row['City'], row['State'], row['ZipCode'],
                                                    row['MobilePhoneNumber'], False))
            conn.commit()
    print('data import complete')

# display_all_students() prints all the student records
def display_all_students():
    mycursor.execute(
        "SELECT * FROM Student WHERE isDeleted = False"
    )
    results = mycursor.fetchall()  # Fetch all the students + attributes
    for row in results:  # Display the results
        print(row)

# add_students adds new student records to the database
def add_students():
    # check if first name entered is valid
    isFirstNameInvalid = True
    while isFirstNameInvalid:
        firstName = input("Enter your first name:")
        if all(name.isalpha() or ("-" == name) or ("'" == name) or
               ("." == name) for name in firstName):
            isFirstNameInvalid = False
        else:
            print(firstName + " is not a valid name. Please only use letters, ', -, or .")

    # check if last name entered is valid
    isLastNameInvalid = True
    while isLastNameInvalid:
        lastName = input("Enter your last name:")
        if all(name.isalpha() or ("-" == name) or ("'" == name) or
               ("." == name) for name in lastName):
            isLastNameInvalid = False
        else:
            print(lastName + " is not a valid name. Please only use letters, ', -, or .")

    gpa = getValidGPA()

    # check if major is valid
    isMajorInvalid = True
    while isMajorInvalid:
        major = input("Enter your major:")
        if all(m.isalpha() or m.isspace() for m in major):
            isMajorInvalid = False
        else:
            print(major + " is not a valid major.")

    # check if faculty advisor is valid
    isFacAdvisorInvalid = True
    while isFacAdvisorInvalid:
        facultyAdvisor = input("Enter your faculty advisor:")
        if all(name.isalpha() or ("-" == name) or ("'" == name) or
               ("." == name) for name in facultyAdvisor):
            isFacAdvisorInvalid = False
        else:
            print(facultyAdvisor + " is not a current faculty advisor.")

    # check if address is valid
    isAddressInvalid = True
    while isAddressInvalid:
        address = input("Enter your address (street number, street, apt/suite:")
        if all(name.isalpha() or name.isdigit() or ("-" == name) or
               ("." == name) for name in address):
            isAddressInvalid = False
        else:
            print(address + " is not a valid address.")

    # check if city is valid
    isCityNotValid = True
    while isCityNotValid:
        city = input("Enter the city of your permanent address:")
        if all(c.isalpha() or c.isspace() or (c == "-") or (c == "'") for c in city):
            isCityNotValid = False
        else:
            print("You have entered an invalid city.")

    # check if state is valid
    state = getValidState()

    # check if zip code is valid
    isZipCodeInvalid = True
    while isZipCodeInvalid:
        zipCode = input("Enter your zip code:")
        if all(zip.isdigit() for zip in zipCode) and (len(zipCode) == 5):
            isZipCodeInvalid = False
        else:
            print(zipCode + "is not a valid zip code.")

    isPhoneNumberInvalid = True
    while isPhoneNumberInvalid:
        phoneNumber = input("Enter your mobile phone number:")
        if all(num.isdigit() or num == "-" or num == "(" or num == ")"
               or num == "x" for num in phoneNumber):
            isPhoneNumberInvalid = False
        else:
            print(phoneNumber + "is not a valid phone number,")

    # add all user information into Students
    mycursor.execute(
        "INSERT INTO Student(FirstName, LastName, GPA, Major, FacultyAdvisor, Address, City, State, ZipCode, MobilePhoneNumber, isDeleted)"
        "VALUES (?,?,?,?,?,?,?,?,?,?,?);", (firstName, lastName, gpa, major,
                                            facultyAdvisor, address, city, state, zipCode,
                                            phoneNumber, False))
    conn.commit()

# extract_letters() removes all non-letters from a string and returns a sting
def extract_letters(input_string):
    letters = ""
    for char in input_string:
        if char.isalpha():
            letters += char
    return letters

# getCorrectStudentID() verifies which student record a user wants to update or delete
def getCorrectStudentID():
    studentID = None

    isNotCorrectStudent = True
    while isNotCorrectStudent:
        try:
            studentID = int(input("Enter Student ID:"))
            mycursor.execute("SELECT firstName FROM Student WHERE StudentId = ?",
                         (studentID,))
            results = mycursor.fetchone()
            name = extract_letters(str(results))

            if (name != "None"):
                response = input("Are you trying to update " + name + "'s record?: [y] or [n]")
                if (response == "y"):
                    break
                else:
                    print("Unfortunate, let's try this again.")
            else:
                print("There is no student with that ID. Please enter a valid ID.")
        except ValueError:
            print("There is no student with that ID. Please enter a valid ID.")

    return studentID

#update_student() function updates individual student records
def update_student():
    studentID = getCorrectStudentID()

    # determining which part of the student record a user wants to update
    isStudRecordNotUpdated = True
    while isStudRecordNotUpdated:
        try:
            print("""
                Which would you like to update?
                1. Major
                2. Faculty Advisor
                3. Phone Number
                """)
            response = input("Please enter 1, 2, or 3:")
            if response == "1":
                major = input("Enter your updated major:")
                mycursor.execute(("UPDATE Student SET Major = ? WHERE StudentId = ?"),(major, studentID))
                isStudRecordNotUpdated = False
            elif response == "2":
                facAdvisor = input("Enter your new faculty advisor's name:")
                mycursor.execute(("UPDATE Student SET FacultyAdvisor = ? WHERE StudentId = ?"), (facAdvisor, studentID))
                isStudRecordNotUpdated = False
            elif response == "3":
                pNumber = input("Enter your new mobile phone number:")
                mycursor.execute(("UPDATE Student SET MobilePhoneNumber = ? WHERE StudentId = ?"), (pNumber, studentID))
                isStudRecordNotUpdated = False
            else:
                print("You have entered an option that is not available.")
        except ValueError:
            print("You have entered an option that is not available.")
    conn.commit()
    mycursor.close()

# delete_student() performs a soft delete so a student record is no longer viewable
def delete_student():
    studentID = getCorrectStudentID()
    mycursor.execute(("UPDATE Student SET isDeleted = 1 WHERE StudentId = ?"), (studentID,))
    print("Your student record has been deleted")
    conn.commit()
    mycursor.close()

#filter_students() shows all students according to a specified attribute
def filter_students():
    isStudRecordNotDisplayed = True
    while isStudRecordNotDisplayed:
        print("""
            Filter students by
            1. Major
            2. GPA
            3. City
            4. State
            5. Faculty Advisor
            """)
        response = input("Please enter 1, 2, 3, 4 or 5: ")
        if response == "1":
            major = input("Enter a major:")
            results = mycursor.execute("SELECT * FROM Student WHERE Major = ?", (major,))
        elif response == "2":
            gpa = getValidGPA()
            results = mycursor.execute("SELECT * FROM Student WHERE GPA = ?", (gpa,))
        elif response == "3":
            city = input("Enter a city:")
            results = mycursor.execute("SELECT * FROM Student WHERE City = ?", (city,))
        elif response == "4":
            state = getValidState()
            results = mycursor.execute("SELECT * FROM Student WHERE State = ?", (state,))
        elif response == "5":
            facAdvisor = input("Enter a faculty advisory:")
            results = mycursor.execute("SELECT * FROM Student WHERE FacultyAdvisor = ?", (facAdvisor,))
        else:
            print("Not a current menu option.")

        for student in results:
            print(student)
        isStudRecordNotDisplayed = False

    mycursor.close()

def main():
    isDone = True
    while isDone:
        print("""
                Which would you like to do?
                1. Display all students.
                2. Add a new student.
                3. Update a student record.
                4. Delete a student record.
                5. Filter search student records
                6. Exit
                """)
        response = input("Please enter 1,2,3,4,5 or 6: ")
        if response == "1":
            display_all_students()
        elif response == "2":
            add_students()
        elif response == "3":
            update_student()
        elif response == "4":
            delete_student()
        elif response == "5":
            filter_students()
        elif (response == "6"):
            print("Goodbye!")
            isDone = False
        else:
            print("\nNot a valid menu option.")
    conn.close()
main()