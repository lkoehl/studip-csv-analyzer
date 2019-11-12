import csv

DELIMITER = ";"
FILE = "list.csv"


studiengaenge = []
students = []


class Student:
    def __init__(self, name, surname, id, login):
        self.name = name
        self.surname = surname
        self.id = id
        self.login = login

    def get_name(self):
        return self.name


def init_studiengaenge():
    result = {}
    for studiengang in studiengaenge:
        splitted_studiengang = studiengang.split(DELIMITER)
        for single_studiengang in splitted_studiengang:
            stripped_studiengang = single_studiengang.split(",")[0].strip()
            if(stripped_studiengang in result):
                result[stripped_studiengang] = result[stripped_studiengang] + 1
            else:
                result[stripped_studiengang] = 1

    print(sorted(result.items(), key=lambda kv: (kv[1], kv[0]), reverse=True))


def iterate_file():
    with open(FILE, mode='r')as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=DELIMITER)
        for row in csv_reader:
            studiengaenge.append(row["Studiengänge"])

            name = row["Vorname"]
            surname = row["Nachname"]
            id = row["Nutzernamen"]
            login = row["Anmeldedatum"]
            student = Student(name, surname, id, login)
            students.append(student)


iterate_file()
