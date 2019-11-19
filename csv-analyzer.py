import csv
import matplotlib.pyplot as plt
import gender_guesser.detector as gender

DELIMITER = ";"
FILE = "list.csv"
ALL_STUDENTS_AUD = "all_students_aud.csv"
ALL_STUDENTS_CC = "all_students_cc.csv"
ALL_GROUPS_AUD = "all_groups_aud.csv"
ALL_GROUPS_CC = "all_groups_cc.csv"

students = []
all_students = {}

class Student:
    def __init__(self, name, surname, gender, id, login, courses, group, codingclass):
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


def is_CC(group):
    if group == "keiner Funktion oder Gruppe zugeordnet":
        return False
    elements = group.split(" ")
    if elements[0] == "Coding":
        return True
    return False

def strip_group(group):
    if group == "keiner Funktion oder Gruppe zugeordnet":
        return -1
    elements = group.split(" ")
    if len(elements) == 2:
        return elements[1]
    else:
        return elements[2]
    return -1

def read_all_students(file):
    with open(ALL_STUDENTS_AUD, mode='r', encoding='utf-8-sig')as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=DELIMITER)
        for row in csv_reader:
            name = row["Vorname"]
            surname = row["Nachname"]
            if row["Anrede"] == "Herr":
                    gender = "male"
            if row["Anrede"] == "Frau":
                gender = "female"
            id = row["Nutzernamen"]
            login = row["Anmeldedatum"]
            courses = strip_courses(row["Studiengänge"])
            if id not in all_students:
                all_students[id] = Student(name, surname, gender, id, login, courses, 0, 0)


def read_all_groups(file):
    with open(file, mode='r', encoding='utf-8-sig') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=DELIMITER)
        for row in csv_reader:
            id = row["Nutzernamen"]
            if id in all_students:
                student = all_students[id]
                if 'Gruppe' in row:
                    group = strip_group(row["Gruppe"])
                    if group != -1:
                        if is_CC(row["Gruppe"]):
                            student.set_codingclass(group)
                        else:
                            student.set_group(group)
            else:
                name = row["Vorname"]
                surname = row["Nachname"]
                login = row["Anmeldedatum"]
                courses = strip_courses(row["Studiengänge"])
                tmp_gender = gender_guesser.get_gender(name)
                if tmp_gender == "male" or tmp_gender == "mostly_male":
                    gender = "male"
                elif tmp_gender == "female" or tmp_gender == "mostly_female":
                    gender = "female"
                elif tmp_gender == "andy" or tmp_gender == "unknown":
                    gender = "unknown"
                    print(name)
                    print(surname)
                if 'Gruppe' in row:
                    group = strip_group(row["Gruppe"])
                    if group != -1:
                        if is_CC(row["Gruppe"]):
                            all_students[id] = Student(name, surname, gender, id, login, courses, 0, group)
                        else:
                            all_students[id] = Student(name, surname, gender, id, login, courses, group, 0)  
                else:
                    all_students[id] = Student(name, surname, gender, id, login, courses, 0, 0)


gender_guesser = gender.Detector()
read_all_students(ALL_STUDENTS_AUD)
read_all_students(ALL_STUDENTS_CC)
read_all_groups(ALL_GROUPS_AUD)
read_all_groups(ALL_GROUPS_CC)

data = {}
dataM = {}
dataF = {}
dataA = {}

ccmin = 0
ccmax = 0
testatmin = 0
testatmax = 0
print("Deine Möglichkeiten:")
print("1. Alle Studenten plotten")
print("2. Bestimmte CC plotten")
print("3. Bestimmte Testate plotten")
user_input = int(input("Was möchtest du tun?: "))
while user_input != 1 and user_input != 2 and user_input != 3:
    print("Deine Möglichkeiten:")
    print("1. Alle Studenten plotten")
    print("2. Bestimmte CC plotten")
    print("3. Bestimmte Testate plotten")
    user_input = int(input("Was möchtest du tun?: "))

if user_input == 2:
    ccmin = int(input("Kleinste Coding Class: "))
    while ccmin < 1:
        ccmin = int(input("Kleinste Coding Class: "))
    ccmax = int(input("Größte Coding Class: "))
    while ccmax > 14:
        ccmax = int(input("Größte Coding Class: "))

if user_input == 3:
    testatmin = int(input("Kleinstes Testat: "))
    while testatmin < 1:
        testatmin = int(input("Kleinstes Testat: "))
    testatmax = int(input("Größtes Testat: "))
    while testatmax > 300:
        testatmax = int(input("Größtes Testat: "))

zfb_doppelt = input("Sollen 2FB pro Studiengang nur als 0.5 Personen zählen? (j/n): ")
while zfb_doppelt != "j" and zfb_doppelt != "n":
    zfb_doppelt = input("Sollen 2FB pro Studiengang nur als 0.5 Personen zählen? (j/n): ")
    

for student in all_students.values():
    if(testatmin == 0 and ccmin == 0) or (testatmin != 0 and (testatmin <= int(student.get_group()) <= testatmax)) or (ccmin != 0 and (ccmin <= int(student.get_codingclass()) <= ccmax)):
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
                data[full_course] = data[full_course] +  student_life_value
            else: 
                data[full_course] = student_life_value
            
            if full_course in dataF and student_gender == "female":
                dataF[full_course] = dataF[full_course] + student_life_value
            elif full_course not in dataF and student_gender == "female":
                dataF[full_course] = student_life_value
            elif full_course in dataM and student_gender == "male":
                dataM[full_course] = dataM[full_course] + student_life_value
            elif full_course not in dataM and student_gender == "male":
                dataM[full_course] = student_life_value
            elif full_course in dataA and student_gender == "unknown":
                dataA[full_course] = dataA[full_course] + student_life_value
            elif full_course not in dataA and student_gender == "unknown":
                dataA[full_course] = student_life_value 
    


"""for student in students:
    semesters = student.get_semesters()
    for semester in semesters:
        if semester in data:
            data[semester] = data[semester] +  1
        else: 
            data[semester] = 1"""



data = sorted(data.items(), key = lambda kv:(kv[1], kv[0]), reverse=True)
dataF = sorted(dataF.items(), key = lambda kv:(kv[1], kv[0]), reverse=True)
dataM = sorted(dataM.items(), key = lambda kv:(kv[1], kv[0]), reverse=True)
dataA = sorted(dataA.items(), key = lambda kv:(kv[1], kv[0]), reverse=True)

print(data)
print(dataF)
print(dataM)
print(dataA)

if data != []:
    x, y = zip(*data)
    p1 = plt.bar(x, y, color=(1.0, 0.64, 0.0, 0.6))

if dataF != []:
    x, y = zip(*dataF)
    p2 = plt.bar(x, y, color=(0.0, 0.0, 1.0, 0.6))


plt.xticks(rotation=90)

plt.savefig("graph.png")
plt.show()
