import csv
import matplotlib.pyplot as plt
import sqlite3
from sqlite3 import Error

DELIMITER = ";"
FILE = "list.csv"
ALL_STUDENTS_AUD = "all_students_aud.csv"
ALL_STUDENTS_CC = "all_students_cc.csv"
ALL_GROUPS_AUD = "all_groups_aud.csv"
ALL_GROUPS_CC = "all_groups_cc.csv"

students = []
all_students = {}

database = r"studip_students.db"


def connect_to(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print("Connection established. Using sqlite3 version:", sqlite3.version)
    except Error as e:
        print("No connection to database possible", e)

    return conn


def execute_sql(conn, sql):
    try:
        c = conn.cursor()
        c.execute(sql)
    except Error as e:
        print("Execution of sql not possible", e)


conn = connect_to(database)

if conn is not None:
    # create projects table
    execute_sql(conn, """ CREATE TABLE IF NOT EXISTS all_students (
                                student_id integer PRIMARY KEY,
                                user_name text NOT NULL,
                                mat_nr bigint,
                                first_name text NOT NULL,
                                last_name text NOT NULL,
                                gender text NOT NULL,
                                login_date text NOT NULL
                            ); """)

    # create tasks table
    execute_sql(conn, """ CREATE TABLE IF NOT EXISTS groups (
                                groups_id integer PRIMARY KEY,
                                user_name text NOT NULL,
                                group_nr integer NOT NULL,
                                codingclass_nr integer NOT NULL
                            ); """)

    # create courses table
    execute_sql(conn, """ CREATE TABLE IF NOT EXISTS courses (
                                courses_id integer PRIMARY KEY,
                                user_name text NOT NULL,
                                first_area text NOT NULL,
                                first_degree text NOT NULL,
                                first_semester text NOT NULL,
                                second_area text,
                                second_degree text,
                                second_semester text
                            ); """)
else:
    print("Error! cannot create the database connection.")


"""
class Student:
    def __init__(self, name, surname, gender, id, login, courses, group=-1, codingclass=-1):
        self.group = group
        self.name = name
        self.surname = surname
        self.gender = gender
        self.id = id
        self.login = login
        self.courses = courses
        self.codingclass = codingclass

    def get_group(self):
        return self.group

    def get_codingclass(self):
        return self.codingclass

    def get_name(self):
        return self.name

    def get_surname(self):
        return self.surname

    def get_gender(self):
        return self.gender

    def get_id(self):
        return self.id

    def get_login(self):
        return self.login

    def get_courses(self):
        return self.courses

    def get_areas(self):
        areas = []
        for course in self.courses:
            areas.append(course["area"])

        return areas

    def get_degree(self):
        degrees = []
        for course in self.courses:
            degrees.append(course["degree"])

        return degrees

    def get_semesters(self):
        semesters = []
        for course in self.courses:
            semesters.append(course["semester"])

        return semesters

    def add_to_group(self, group):
        if group == "keiner Funktion oder Gruppe zugeordnet":
            return -1
        elements = group.split(" ")
        if len(elements) == 2:
            return self.set_group(elements[1])
        else:
            return self.set_codingclass(elements[2])
        return -1

    def set_group(self, group):
        self.group = group

    def set_codingclass(self, codingclass):
        self.codingclass = codingclass


def strip_courses(course):
    courses = []
    multi_course = course.split(";")
    for single_course in multi_course:
        chopped_course = single_course.split(",")
        if len(chopped_course) == 3:
            area = chopped_course[0].strip()
            degree = chopped_course[1].strip()
            semester = chopped_course[2].strip()
            course_dic = {"area": area, "degree": degree, "semester": semester}
            courses.append(course_dic)

    return courses


def read_all_students(file):
    with open(file, mode='r', encoding='utf-8-sig') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=DELIMITER)
        for row in csv_reader:
            name = row["Vorname"]
            surname = row["Nachname"]
            if row["Anrede"] == "Herr":
                gender = "male"
            elif row["Anrede"] == "Frau":
                gender = "female"
            else:
                gender = -1
            id = row["Nutzernamen"]
            login = row["Anmeldedatum"]
            courses = strip_courses(row["Studiengänge"])
            if id not in all_students:
                all_students[id] = Student(
                    name, surname, gender, id, login, courses)


def read_all_groups(file):
    with open(file, mode='r', encoding='utf-8-sig') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=DELIMITER)
        for row in csv_reader:
            id = row["Nutzernamen"]
            if id in all_students:
                student = all_students[id]
                if 'Gruppe' in row:
                    student.add_to_group(row["Gruppe"])
            else:
                print(row["Vorname"])
                print(row["Nachname"])


gender_guesser = gender.Detector()
read_all_students(ALL_STUDENTS_AUD)
read_all_students(ALL_STUDENTS_CC)
read_all_groups(ALL_GROUPS_AUD)
read_all_groups(ALL_GROUPS_CC)

data = {}
dataM = {}
dataF = {}

ccmin = -1
ccmax = -1
testatmin = -1
testatmax = -1
user_input = -1

print_all_students = False
print_cc = False
print_testate = False

while user_input != 1 and user_input != 2 and user_input != 3:
    print("Deine Möglichkeiten:")
    print("1. Alle Studenten plotten")
    print("2. Bestimmte CC plotten")
    print("3. Bestimmte Testate plotten")
    user_input = int(input("Was möchtest du tun?: "))

if user_input == 1:
    print_all_students = True

if user_input == 2:
    print_cc = True
    while ccmin < 1:
        ccmin = int(input("Kleinste Coding Class( >= 1 ): "))
    while ccmax > 14 or ccmax < 1:
        ccmax = int(input("Größte Coding Class( <= 14 ): "))

if user_input == 3:
    print_testate = True
    while testatmin < 1:
        testatmin = int(input("Kleinstes Testat( >= 1 ): "))
    while testatmax > 300 or testatmax < 1:
        testatmax = int(input("Größtes Testat( >= 300 ): "))

zfb_doppelt = ""
while zfb_doppelt != "j" and zfb_doppelt != "n":
    zfb_doppelt = input(
        "Sollen 2FB pro Studiengang nur als 0.5 Personen zählen? (j/n): ")


for student in all_students.values():
    testat_in_range = testatmin <= int(student.get_group()) <= testatmax
    cc_in_range = ccmin <= int(student.get_codingclass()) <= ccmax
    if(print_all_students) or (print_testate and testat_in_range) or (print_cc and cc_in_range):
        courses = student.get_courses()
        student_gender = student.get_gender()
        for course in courses:
            full_course = course["area"]
            student_life_value = 1
            if course["degree"] == "2-Fächer-Bachelor":
                full_course += " 2FB"
                if zfb_doppelt == "j":
                    student_life_value = 0.5

            if full_course in data:
                data[full_course] = data[full_course] + student_life_value
            else:
                data[full_course] = student_life_value

            if student_gender == "female":
                if full_course in dataF:
                    dataF[full_course] = dataF[full_course] + \
                        student_life_value
                else:
                    dataF[full_course] = student_life_value
            elif student_gender == "male":
                if full_course in dataM:
                    dataM[full_course] = dataM[full_course] + \
                        student_life_value
                else:
                    dataM[full_course] = student_life_value


# for student in students:
#    semesters = student.get_semesters()
#    for semester in semesters:
#        if semester in data:
#            data[semester] = data[semester] +  1
#        else: 
#            data[semester] = 1


data = sorted(data.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
dataF = sorted(dataF.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
dataM = sorted(dataM.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)

print(data)
print(dataF)
print(dataM)

if data != []:
    x, y = zip(*data)
    p1 = plt.bar(x, y, color=(1.0, 0.64, 0.0, 0.6))

if dataF != []:
    x, y = zip(*dataF)
    p2 = plt.bar(x, y, color=(0.0, 0.0, 1.0, 0.6))


plt.xticks(rotation=90)

plt.savefig("graph.png")
plt.show()
"""
