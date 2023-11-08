import sqlite3
import csv
import random

dbFilePath = "Students.db"
conn = sqlite3.connect(dbFilePath)
mycursor = conn.cursor()

# create Students database
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

# import csv into Student table (import_data())
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


def display_students():
    mycursor.execute(
        "SELECT * FROM Students WHERE isDeleted = False"
    )
    results = mycursor.fetchall()  # Fetch all the students + attributes
    for row in results:  # Display the results
        print(row)

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

    # check if gpa entered is valid
    isGPAInvalid = True
    while isGPAInvalid:
        try:
            gpa = float(input("Enter your GPA:"))
            if (gpa > 0.0) and (gpa <= 4.8):
                isGPAInvalid = False
            else:
                 print(str(gpa) + " is not a valid GPA. GPA must be between 0.0 and 4.0.")
        except ValueError:
            print("Not a valid GPA. GPA must be between 0.0 and 4.0.")

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
    isStateInvalid = True
    while isStateInvalid:
        state = input("Enter your state:")
        if state in state_names:
            isStateInvalid = False
        else:
            print(state + "is not a valid state. Please use Title Case.")

    # check if zip code is valid
    isZipCodeInvalid = True
    while isZipCodeInvalid:
        zipCode = input("Enter your zip code:")
        if all(zip.isdigit() for zip in zipCode) and (len(zipCode) == 5):
            isZipCodeInvalid = False
        else:
            print(zipCode + "is not a valid zip code.")

    #FIXME: phone number validation
    isPhoneNumberInvalid = True
    while isPhoneNumberInvalid:
        phoneNumber = input("Enter your mobile phone number:")
        cleanedPhoneNumber = phoneNumber


    # add all user information into Students
    mycursor.execute(
        "INSERT INTO Students(FirstName, LastName, GPA, Major, FacultyAdvisor, Address, City, State, ZipCode, MobilePhoneNumber, isDeleted)"
        "VALUES (?,?,?,?,?,?,?,?,?,?,?);", (firstName, lastName, gpa, major,
                                            facultyAdvisor, address, city, state, zipCode,
                                            phoneNumber, False))
    conn.commit()

# add_students()


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
            mycursor.execute("SELECT firstName FROM Students WHERE StudentId = ?",
                         (studentID,))
            results = mycursor.fetchone()
            justName = extract_letters(str(results))

            if (results != []):
                response = input("Are you trying to update " + justName + "'s record?: [y] or [n]")
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
        print("""
            Which would you like to update?
            1. Major
            2. Faculty Advisor
            3. Phone Number
            """)
        response = input("Please enter 1, 2, or 3:")
        if response == "1":
            major = input("Enter your updated major:")
            mycursor.execute(("UPDATE Students SET Major = ? WHERE StudentId = ?"),(major, studentID))
            isStudRecordNotUpdated = False
        elif response == "2":
            facAdvisor = input("Enter your new faculty advisor's name:")
            mycursor.execute(("UPDATE Students SET FacultyAdvisor = ? WHERE StudentId = ?"), (facAdvisor, studentID))
            isStudRecordNotUpdated = False
        elif response == "3":
            pNumber = input("Enter your new mobile phone number:")
            mycursor.execute(("UPDATE Students SET MobilePhoneNumber = ? WHERE StudentId = ?"), (pNumber, studentID))
            isStudRecordNotUpdated = False
        else:
            print("You have entered an option that is not available.")
    conn.commit()
    mycursor.close()

# delete_student() performs a soft delete so a student record is no longer viewable
def delete_student():
    studentID = getCorrectStudentID()
    mycursor.execute(("UPDATE Students SET isDeleted = 1 WHERE StudentId = ?"), (studentID,))
    print("Your student record has been deleted")
    conn.commit()
    mycursor.close()

def display_students():
    print("""
            Filter students by
            1. Major
            2. GPA
            3. City
            4. State
            5. Faculty Advisor
            """)
    response = input("Please enter 1, 2, 3, 4 or 5")


def main():

    conn.close()