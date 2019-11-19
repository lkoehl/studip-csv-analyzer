import csv
import matplotlib.pyplot as plt

DELIMITER = ";"
FILE = "list.csv"

students = []


class Student:
    def __init__(self, group, name, surname, id, login, courses):
        self.group = group
        self.name = name
        self.surname = surname
        self.id = id
        self.login = login
        self.courses = courses

    def get_group(self):
        return self.group

    def get_name(self):
        return self.name

    def get_surname(self):
        return self.surname

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


def strip_group(group):
    elements = group.split(" ")
    if len(elements) == 5:
        return -1

    return elements[2]


def read_file():
    with open(FILE, mode='r', encoding='utf-8-sig')as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=DELIMITER)

        for row in csv_reader:
            group = strip_group(row["Gruppe"])
            name = row["Vorname"]
            surname = row["Nachname"]
            id = row["Nutzernamen"]
            login = row["Anmeldedatum"]
            courses = strip_courses(row["Studiengänge"])

            student = Student(group, name, surname, id, login, courses)
            students.append(student)


read_file()

data = {}
for student in students:
    semesters = student.get_semesters()
    for semester in semesters:
        if semester in data:
            data[semester] = data[semester] +  1
        else: 
            data[semester] = 1
print(data)
data = sorted(data.items(), key = lambda kv:(kv[1], kv[0]), reverse=True)
x, y = zip(*data)
plt.bar(x, y)
plt.xticks(rotation=90)
plt.savefig("graph.png")

