import csv
import os
import sys
from csv import writer
from prettytable import from_csv, PrettyTable
from csv import DictReader, DictWriter
from tempfile import NamedTemporaryFile
import shutil
import pandas as pd


def countPersonnel():
    count = pd.read_csv('./personnel.csv')
    print("No. of Employee:", len(count))


def total():
    with open("./personnel.csv", "r") as file:
        total_salary = 0
        next(file)
        for row in csv.reader(file):
            total_salary += int(row[3])
        return total_salary


def addPersonnel():
    emp_name = input('Employee Name: ')
    gender = input('Gender: ')
    designation = input('Designation: ')
    salary = (input('Salary : '))

    if not (emp_name and not emp_name.isspace()) or not (gender and not gender.isspace()) or \
            not (designation and not designation.isspace()) or not (salary and not salary.isspace()):
        print('PLEASE FILL ALL THE REQUIRED DATA.')
        addPersonnel()
    else:
        # checks if the employee already exists in the csv file
        csv_file = csv.reader(open('./personnel.csv', "r"), delimiter=",")
        for row in csv_file:
            if emp_name == row[0]:
                print('EMPLOYEE ALREADY EXISTS.\n')
                addPersonnel()
        # append the data to the personnel csv
        with open('./personnel.csv', 'a') as file:
            csv_writer = writer(file, lineterminator='\n')

            personnel_data = (emp_name, gender, designation, int(salary))
            csv_writer.writerow(personnel_data)
            file.close()
            print("PERSONNEL ADDED SUCCESSFULLY\n")


def searchPersonnel():
    search_input = input('Enter name to search: ')
    csv_file = csv.reader(open('./personnel.csv', "r"), delimiter=",")

    table = PrettyTable()
    count = 0
    for row in csv_file:
        if search_input.lower() == row[0].lower():
            count += 1
            table.add_row(row)

    if count != 0:
        table.field_names = ['EMPLOYEE NAME', 'GENDER', 'DESIGNATION', 'SALARY']
        print('FOUND: ', count)
        print(table)
    else:
        print('NO RECORDS FOUND.')


def updatePersonnel():
    name = input('Enter name to update: ')
    print('What do you want to update?')
    print('ENTER [1] TO UPDATE EMPLOYEE NAME')
    print('ENTER [2] TO UPDATE EMPLOYEE GENDER')
    print('ENTER [3] TO UPDATE EMPLOYEE DESIGNATION')
    print('ENTER [4] TO UPDATE EMPLOYEE SALARY')
    opt = int(input('ENTER CHOICE TO UPDATE: '))

    with open('./personnel.csv') as file:
        csv_reader = DictReader(file)
        data = list(csv_reader)

    with open('./personnel.csv', 'w') as up_file:
        header = ('EMPLOYEE NAME', 'GENDER', 'DESIGNATION', 'SALARY')
        csv_writer = DictWriter(
            up_file,
            fieldnames=header,
            lineterminator='\n'
        )
        csv_writer.writeheader()
        for row in data:
            if row['EMPLOYEE NAME'] == name:
                if opt == 1:
                    up_name = input('ENTER VALUE TO UPDATE EMPLOYEE NAME: ')
                    row['EMPLOYEE NAME'] = up_name
                if opt == 2:
                    up_gender = input('ENTER VALUE TO UPDATE GENDER: ')
                    row['GENDER'] = up_gender
                if opt == 3:
                    up_designation = input('ENTER VALUE TO UPDATE DESIGNATION: ')
                    row['DESIGNATION'] = up_designation
                if opt == 4:
                    up_salary = input('ENTER VALUE TO UPDATE SALARY: ')
                    row['SALARY'] = int(up_salary)
                if (opt < 1) or (opt > 4):
                    print('ERROR! PLEASE CHECK YOUR INPUT.')
            else:
                print("INPUT DON'T MATCH WITH THE RECORDS. PLEASE TRY AGAIN")
            csv_writer.writerow(row)
        print('EMPLOYEE RECORD UPDATED SUCCESSFULLY')


def deletePersonnel():
    name = input('\nEnter name to delete: ')
    delete = input("Are you sure you want to delete (YES/NO)? ")

    if delete == 'YES':
        with open('./personnel.csv') as file:
            csv_reader = DictReader(file)
            data = list(csv_reader)

        with NamedTemporaryFile(mode='w', delete=False) as temp_file:
            header = ('EMPLOYEE NAME', 'GENDER', 'DESIGNATION', 'SALARY')
            csv_writer = DictWriter(
                temp_file,
                fieldnames=header,
                lineterminator='\n'
            )
            csv_writer.writeheader()

            for row in data:
                if row['EMPLOYEE NAME'] == name:
                    continue
                csv_writer.writerow(row)
            print('PERSONNEL RECORD DELETED SUCCESSFULLY')
            temp_file.close()
            shutil.move(temp_file.name, './personnel.csv')

    else:
        print('Canceled!')


def viewRecord():
    with open("./personnel.csv", "r") as file:
        table = from_csv(file)
        file.close()
        countPersonnel()
        print('Total salary of employees: ', total())
        print(table)


def createEmployeeCSV():
    with open('./personnel.csv', 'w') as file:
        csv_writer = writer(file, lineterminator='\n')
        header = ('EMPLOYEE NAME', 'GENDER', 'DESIGNATION', 'SALARY')
        csv_writer.writerow(header)
        file.close()


def isEmployeeCSVCreated():
    if os.path.isfile('./personnel.csv'):
        return
    else:
        # calling the function to create the CSV file
        createEmployeeCSV()


def main():
    while True:
        isEmployeeCSVCreated()
        print('Personnel Management System in a Construction Firm')
        print('ENTER [1] TO ADD PERSONNEL')
        print('ENTER [2] TO SEARCH PERSONNEL')
        print('ENTER [3] TO UPDATE PERSONNEL RECORD')
        print('ENTER [4] TO DELETE PERSONNEL RECORD')
        print('ENTER [5] TO VIEW ALL RECORD')
        print('ENTER [6] TO QUIT')
        inp = int(input('PLEASE ENTER YOUR CHOICE: '))

        if inp == 1:
            addPersonnel()
        elif inp == 2:
            searchPersonnel()
        elif inp == 3:
            updatePersonnel()
        elif inp == 4:
            deletePersonnel()
        elif inp == 5:
            viewRecord()
        elif inp == 6:
            print('You have exited.')
            sys.exit(0)
        else:
            print('ERROR! PLEASE TRY AGAIN')


if __name__ == '__main__':
    main()
